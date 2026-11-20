# Automating dead code cleanup

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Will Shackleton; Andy Pincombe; Katriel Cohn-Gordon
- Date: 2023-10-24
- Original location: https://engineering.fb.com/2023/10/24/data-infrastructure/automating-dead-code-cleanup/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
- Meta’s Systematic Code and Asset Removal Framework (SCARF) has a subsystem for identifying and removing dead code.
- SCARF combines static and dynamic analysis of programs to detect dead code from both a business and programming language perspective.
- SCARF automatically creates change requests that delete the dead code identified from the program analysis, minimizing developer costs.

In our last blog post on [automatic product deprecation](https://engineering.fb.com/2023/10/17/data-infrastructure/automating-product-deprecation-meta/), we talked about the complexities of product deprecations, and a solution Meta has built called the Systematic Code and Asset Removal Framework (SCARF). As an example, we looked at [Moments](https://about.fb.com/news/2015/06/introducing-moments/), the photo sharing app Meta launched in 2015 and eventually shut down in 2019, and how SCARF can help with the deprecation process through its workflow management capabilities. We discussed how SCARF saves engineering time by identifying the correct order of tasks for cleaning up a product and how it can be blocked from automating the cleanup when there are intersystem dependencies. This naturally leads to the question: How do we automatically unblock SCARF when there is code that references an asset?

## Dead code removal in SCARF

SCARF contains a subsystem that automatically identifies dead code through a combination of static, runtime, and application analysis. It leverages this analysis to submit change requests to remove this code from our systems. This automated dead code removal improves the quality of our systems and also unblocks unused data removal in SCARF when the dead code includes references to data assets that prevent automated data cleanup.

## Code analysis

SCARF’s code analysis subsystem gathers information from a variety of sources. First, a code dependency graph for each language is extracted from our compilers via [Glean](https://glean.software/). This is then augmented with further information, like the usage of API endpoints from operational logs that determine whether an endpoint is used at runtime. Additional examples of domain-specific usage encoded include:

- Script invocations for internal developer tools and system management commands.
- Template hooks for dynamically rendering pages in the [Instagram Django backend and URI handler and routing](https://instagram-engineering.com/web-service-efficiency-at-instagram-with-python-4976d078e366).
- Async’s dynamically referenced dispatch methods ([Meta’s deferred job execution service](https://engineering.fb.com/2020/08/17/production-engineering/async/)).

SCARF must be capable of introspecting any and all types of dynamic usage in addition to the static dependency graph to make accurate determinations of whether a piece of code is truly safe to remove. These are combined and form an augmented dependency graph.

SCARF supports multiple programming languages. This is very important, as products at Meta may have client code written in Java, Objective-C, and JavaScript, with server code written in [Hack](https://hacklang.org/), and some backend infrastructure written in [Python](https://engineering.fb.com/2023/10/05/developer-tools/python-312-meta-new-features/). All of these pieces of code should be deleted as they all combine to form the same dependency graph since they are associated via APIs and other known forms of dynamic and language-spanning references.

SCARF operates at a symbol level as opposed to a file level, which allows for more granular analysis and cleanup. For example, an individual variable that is unused in a function will have its own fully qualified symbol, which allows for more granular cleanup than is possible at the file level.

## Garbage collection

SCARF analyzes the augmented dependency graph to identify unreachable nodes and subgraphs that can be deleted and will automatically generate code change requests to delete the corresponding code on a daily basis. A key benefit of analyzing the complete graph is that we can detect and delete cycles, where different parts of the codebase depend on each other. Deleting entire subgraphs accelerates the deletion of dead code and provides a better experience for the engineers leveraging this automation in their deprecations.

It’s important that the graph contains the augmented information, as static analysis alone may not reveal links between components created through dynamic references or runtime language features. There is a trade-off, though, in that augmenting the graph with dynamic usage information requires the full processing of the indexed code and the subsequent data analysis pipelines that provide the metrics. This increases the end to end duration of the entire process which can make prototyping new features or capabilities more difficult.

Earlier versions of SCARF avoided this upfront cost by taking a different approach. It analyzed each discoverable symbol individually and at runtime would run classifiers that queried for static and dynamic references in order to find dead root nodes — pieces of code with no inbound dependencies. This did not require the upfront construction of the complete dependency graph and simplified the process of running the system over small subsets of the codebase. As a result, it was trivial to prototype new classifiers that identified potential dynamic references without requiring time-consuming indexing or data analysis.

However, this longer end-to-end development cycle led to a dramatic improvement in coverage. The transition from analyzing individual symbols to the entire graph led to a nearly 50% increase in dead code removed from one of Meta’s largest codebases. The new approach improves visibility into the state of our codebases: how much is alive, how much is dead, and how much of that we are removing in any given pass of SCARF.

## Fine-tuning the dependency graph

Many of the dependencies that we index using Glean are for patterns of code invocation which do not necessarily block the deletion of that code. For example, let’s say we had a class PhotoRenderer, and the only dependency on it was in code like this:

```
if isinstance(renderer, PhotoRenderer):
    return renderer.render_photo()
else:
    return renderer.render_generic()
```
In this case, the references to PhotoRenderer and render\_photo() can be removed, and the code changed to this:

`return renderer.render_generic()`
In this example, the class, PhotoRenderer, was **inlined** based on a rule derived from the semantics of Python: if there are no places where the PhotoRenderer class is instantiated, we can be confident that this code cannot take the first branch and it is therefore dead.

In some cases, we derive these rules based on our application semantics as opposed to language semantics. Imagine this code:

```
uri_dispatch = {
  '/home/': HomeController,
  '/photos/': PhotosController,
  ...
}
```
If we only analyzed a language-level dependency graph, it would be impossible to determine whether or not PhotosController is ever referenced as it can be invoked via this URI dispatch mechanism. However, if we know from our application analysis that the ‘/photos/’ endpoint never receives any requests in production, then we could remove the corresponding entry from this dictionary.

There’s no inherent way to infer this given Python’s language semantics, but our domain-specific logging and graph augmentation allow us to inform SCARF that this operation is safe.

## Automating code changes

At Meta, we heavily automate changes to code. We built an internal service, called CodemodService, which empowers engineers to deploy configurations to automate code changes at scale. SCARF was the first instance of company-wide, fully automated code changes at Meta, and was built hand-in-hand alongside CodemodService. Today, CodemodService also powers hundreds of other types of automated code changes at Meta, from automating the formatting of code, automatically removing completed experiments, empowering large-scale API migrations, to improving coverage of strong types in partially-typed languages like Python and Hack.

## Dead code removal at scale

SCARF uses CodemodService to create code change requests for engineers to review. These change requests incorporate human-readable descriptions informing engineers about the analysis that determined the targeted code is provably dead.

SCARF has grown to analyze hundreds of millions of lines of code; and five years on, it has automatically deleted more than 100 million lines of code in over 370,000 change requests. False-positives caught by engineers during code review are triaged and used to improve the analysis that SCARF performs and typically reflect new sources of dynamic usage that our augmented graphs must account for. Sometimes these misunderstood dynamic references can lead to incorrect deletion of code, and these deletions can make it to production. Meta has [other mechanisms in place to catch these problems](https://engineering.fb.com/2017/08/31/web/rapid-release-at-massive-scale/) and we take such incidents very seriously.

In some languages, we have such high confidence in our analysis that we can automatically accept and merge the change requests without human intervention to make better use of engineers’ valuable time.

## Is dead code removal sufficient?

SCARF’s automated dead code removal accelerates the process of shutting down and removing the code and data for deprecated products, but it does not solve it fully. Beyond the problems caused by interconnectivity, we are constantly improving our ability to integrate across all languages, systems, and frameworks at Meta. It is difficult to accurately cover every type of usage of code and data that enables our systems to determine what is truly dead.

Our systems also err on the side of caution, by searching for textual references to code and data through our [BigGrep system](https://www.facebook.com/watch/?v=1911812842425144) and not solely relying on the curated graphs produced through Glean and our dynamic usage augmentations. This is a fallback safety mechanism that helps avoid accidentally deleting MySQL tables that are referenced by name in other languages and preventing deletions of dynamically invoked code in languages like Hack, Python, and JavaScript that can call code through string references or use *eval*. This approach can cause false negatives, but avoids false positives. When automating the removal of dead code, those are a more serious problem.

As mentioned in [our first post](https://engineering.fb.com/2023/10/17/data-infrastructure/automating-product-deprecation-meta/) of this series, SCARF provides workflow management features that work together with the dead code subsystem to provide a cohesive experience for fully deprecating products and features. Crucially, our engineers can iterate on code changes faster than our automation! If an engineer understands that a change has rendered a branch of code (and therefore an entire subgraph) unreachable, they can easily incorporate that deletion into their changes without waiting for our infrastructure to index the new code, analyze it, and eventually get around to submitting its automated changes. Engineers sometimes find it more productive to manually delete things rather than waiting to see if the automated systems will clean it up for them later.

In the next and final blog post in this series, which covers [automating data removal](https://engineering.fb.com/2023/10/31/data-infrastructure/automating-data-removal/), we will look at SCARF’s unused data type subsystem that Meta has built that, in conjunction with the dead code subsystem, amplifies Meta’s data minimization capabilities by automating the removal of dead and unused assets.
