# AI and GNOME Shell Extensions

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Javad Rahmatzadeh
- Date: 2025-12-06
- Original location: https://blogs.gnome.org/jrahmatzadeh/2025/12/06/ai-and-gnome-shell-extensions/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
Since I joined the extensions team, I’ve only had one goal in mind. Making the extension developers’ job easier by providing them documentation and help.

I started with the port guide and then I became involved in the reviews by providing developers code samples, mentioning best practices, even fixing the issue myself and sending them merge requests. Andy Holmes and I spent a lot of time writing all the necessary documentation for the extension developers. We even made the review guidelines very strict and easy to understand with code samples.

Today, extension developers have all the documentation to start with extensions, a port guide to port their extensions, and a very friendly place on the GNOME Extensions Matrix channel to ask questions and get fast answers. Now, we have a very strong community for GNOME Shell extensions that can easily overcome all the difficulties of learning and changes.

The number of submitted packages to [EGO](https://extensions.gnome.org/) is growing every month and we see more and more people joining the extensions community to create their own extensions. Some days, I spend more than 6 hours a day reviewing over 15,000 lines of extension code and answering the community.

In the past two months, we have received many new extensions on EGO. This is a good thing since it can make the extensions community grow even more, but there is one issue with some packages. Some devs are using AI without understanding the code.

This has led to receiving packages with many unnecessary lines and bad practices. And once a bad practice is introduced in one package, it can create a domino effect, appearing on other extensions. That alone has increased the waiting time for all packages to be reviewed.

At the start, I was really curious about the increase in unnecessary try-catch block usage in many new extensions submitted on EGO. So I asked, and they answered that it is coming from AI.

Just to give you a gist of how these unnecessary code might look:

```
destroy() {
    try {
        if (typeof super.destroy === 'function') {
            super.destroy();
        }
    } catch (e) {
        console.warn(`${e.message}`);
    }
}
```
Instead of simply calling \`super.destroy()\`, which you clearly know exists in the parent:

```
destroy() {
    super.destroy();
}
```
At this point, we have to add a [new rule](https://gjs.guide/extensions/review-guidelines/review-guidelines.html#extensions-must-not-be-ai-generated) to the EGO review guidelines. So the packages with unnecessary code that indicate they are AI-generated will be rejected.

This doesn’t mean you cannot use AI for learning or fixing some issues. AI is a fantastic tool for learning and helping find and fix issues. Use it for that, not for generating the entire extension. For sure, in the future, AI can generate very high quality code without any unnecessary lines but until then, if you want to start writing extensions, you can always ask us in the [GNOME Extensions Matrix channel](https://matrix.to/#/#extensions:gnome.org).

## Leave a Reply Cancel reply
