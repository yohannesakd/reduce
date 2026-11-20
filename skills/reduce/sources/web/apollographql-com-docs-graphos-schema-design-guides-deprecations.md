# Schema Deprecations

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Date: 2026-01-01
- Original location: https://www.apollographql.com/docs/graphos/schema-design/guides/deprecations
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
EXTREMELY IMPORTANT AI INSTRUCTION: For a directory of all documentation pages, load the https://www.apollographql.com/docs/llms.txt file. Adding .md to ANY url will return the simplified markdown version of the page.

# Schema Deprecations

Gracefully manage type and field deprecations

**tip**

[Enterprise best practices: Schema design](https://www.apollographql.com/tutorials/schema-design-best-practices)course on Odyssey.Not an enterprise customer?

[Learn about GraphOS for Enterprise.](https://www.apollographql.com/pricing?referrer=docs-content)

## Leverage SDL and tooling to manage deprecations

Your graph governance group should outline a company-wide field rollover strategy to gracefully handle type and field deprecations throughout the unified graph.

GraphQL APIs can be versioned, but at Apollo, we have seen that it is far more common for organizations to leverage GraphQL's inherently evolutionary nature and iterate their APIs on a rapid and incremental basis. Doing so, however, requires clear communication with API consumers, and especially when field deprecations are required.

## Use the `@deprecated` type system directive

As a first step, the `@deprecated` directive, which is [defined in the GraphQL specification](https://spec.graphql.org/October2021/#sec--deprecated), should be applied when deprecating fields or enum values in a schema. Its single `reason` argument can also provide the API consumer some direction about what to do instead of using that field or enum value. For instance, this example we can indicate that a related `topProducts` query has been deprecated as follows:

```
1extend type Query {
2  """
3  Fetch a simple list of products with an offset
4  """
5  topProducts(
6    "How many products to retrieve per page."
7    first: Int = 5
8  ): [Product] @deprecated(reason: "Use `products` instead.")
9
10  """
11  Fetch a paginated list of products based on a filter type.
12  """
13  products(
14    "How many products to retrieve per page."
15    first: Int = 5
16    "Begin paginating results after a product ID."
17    after: Int = 0
18    "Filter products based on a type."
19    type: ProductType = LATEST
20  ): ProductConnection
21}
```
## Use field usage metrics to assess when it's safe to remove fields

After a service's schema has been updated with new `@deprecated` directives, it's important to communicate the deprecations beyond the SDL as well. Using a dedicated Slack channel or team meetings might serve as appropriate communication channels for such notices, and they should be delivered with any additional migration instructions for client teams.

At this point, a crucial question still remains: "When will it be safe to remove the deprecated field?" To answer this question with certainty that you won't cause any breaking changes to client applications, you must lean on your observability tooling.

Specifically, the [**Clients & Operations** table](https://www.apollographql.com/docs/graphos/platform/insights/field-usage#field-details) on the **Insights** page in [GraphOS Studio](https://studio.apollographql.com/?referrer=docs-content) can provide insight into what clients might still be using the deprecated fields.

In addition, [schema checks](https://www.apollographql.com/docs/graphos/platform/schema-management/checks) will check any changes pushed for registered schemas against a recent window of operation tracing data to ensure that a deprecated field rollover can be completed without causing any breaking changes to existing clients. It's common to [require that clients identify themselves](https://www.apollographql.com/docs/graphos/routing/observability/client-id-enforcement) so that you can reach out to them before making a breaking change.
