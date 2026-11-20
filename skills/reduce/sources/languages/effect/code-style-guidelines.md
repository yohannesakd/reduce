# Guidelines

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Effect team, effect.website
- Date: 2026-05-30
- License: MIT, as the site states
- Original location: https://effect.website/docs/v4/code-style/guidelines/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# Guidelines

## 

In Effect, `runMain` is the primary entry point for executing an Effect application on Node.js.

**Example** (Running an Effect Application with Graceful Teardown)

The `runMain` function handles finding and interrupting all fibers. Internally, it observes the fiber and listens for `sigint` signals, ensuring a graceful shutdown of the application when interrupted (e.g., using CTRL+C).

### 

Effect provides versions of `runMain` tailored for different platforms:

| Platform | Runtime Version | Import Path | 
|---|---|---|
| Node.js | `NodeRuntime.runMain` | `@effect/platform-node` | 
| Bun | `BunRuntime.runMain` | `@effect/platform-bun` | 
| Browser | `BrowserRuntime.runMain` | `@effect/platform-browser` | 

## 

Avoid using tacit (point-free) function calls, such as `Effect.map(fn)`, or using `flow` from the `effect/Function` module.

In Effect, it’s generally safer to write functions explicitly:

rather than in a point-free style:

While tacit functions may be appealing for their brevity, they can introduce a number of problems:

- Using tacit functions, particularly when dealing with optional parameters, can be unsafe. For example, if a function has overloads, writing it in a tacit style may erase all generics, resulting in bugs. Check out this X thread for more details: [link to thread](https://twitter.com/MichaelArnaldi/status/1670715270845935616).
- Tacit usage can also compromise TypeScript’s ability to infer types, potentially causing unexpected errors. This isn’t just a matter of style but a way to avoid subtle mistakes that can arise from type inference issues.
- Additionally, stack traces might not be as clear when tacit usage is employed.

Avoiding tacit usage is a simple precaution that makes your code more reliable.
