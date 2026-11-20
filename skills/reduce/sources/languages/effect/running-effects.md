# Running Effects

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Effect team, effect.website
- Date: 2026-05-30
- License: MIT, as the site states
- Original location: https://effect.website/docs/v4/getting-started/running-effects/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# Running Effects

To execute an effect, you can use one of the many `run` functions provided by the `Effect` module.

## 

Executes an effect synchronously, running it immediately and returning the result.

**Example** (Synchronous Logging)

Use `Effect.runSync` to run an effect that does not fail and does not include any asynchronous operations. If the effect fails, `Effect.runSync` throws the error. If the effect involves asynchronous work, `Effect.runSync` throws an `AsyncFiberError` instead of waiting for the result. The effect is not interrupted. It keeps running in the background, and its finalizers still run. To stop it, call `Fiber.interrupt` on the `fiber` field of the error.

**Example** (Incorrect Usage with Failing or Async Effects)

## 

Runs an effect synchronously and returns the result as an [Exit](/docs/v4/data-types/exit/) type, which represents the outcome (success or failure) of the effect.

Use `Effect.runSyncExit` to find out whether an effect succeeded or failed,
including any defects, without dealing with asynchronous operations.

The `Exit` type represents the result of the effect:

- If the effect succeeds, the result is wrapped in a `Success`.
- If it fails, the failure information is provided as a `Failure` containing
a [Cause](/docs/v4/data-types/cause/) type.

**Example** (Handling Results as Exit)

If the effect contains asynchronous operations, `Effect.runSyncExit` will
return an `Failure` with a `Die` cause, indicating that the effect cannot be
resolved synchronously. The effect is not interrupted. It keeps running in the background.

**Example** (Asynchronous Operation Resulting in Die)

## 

Executes an effect and returns the result as a `Promise`.

Use `Effect.runPromise` when you need to execute an effect and work with the
result using `Promise` syntax, typically for compatibility with other
promise-based code.

**Example** (Running a Successful Effect as a Promise)

If the effect succeeds, the promise will resolve with the result. If the effect fails, the promise will reject with an error.

**Example** (Handling a Failing Effect as a Rejected Promise)

## 

Runs an effect and returns a `Promise` that resolves to an [Exit](/docs/v4/data-types/exit/), which
represents the outcome (success or failure) of the effect.

Use `Effect.runPromiseExit` when you need to determine if an effect succeeded
or failed, including any defects, and you want to work with a `Promise`.

The `Exit` type represents the result of the effect:

- If the effect succeeds, the result is wrapped in a `Success`.
- If it fails, the failure information is provided as a `Failure` containing
a [Cause](/docs/v4/data-types/cause/) type.

**Example** (Handling Results as Exit)

## 

The foundational function for running effects, returning a “fiber” that can be observed or interrupted.

`Effect.runFork` is used to run an effect in the background by creating a fiber. It is the base function
for all other run functions. It starts a fiber that can be observed or interrupted.

**Example** (Running an Effect in the Background)

In this example, the `program` continuously logs “running…” with each repetition spaced 200 milliseconds apart. You can learn more in [Using Schedules](/docs/v4/scheduling/using-schedules/).

To stop the execution of the program, we use `Fiber.interrupt` on the fiber returned by `Effect.runFork`. This allows you to control the execution flow and terminate it when necessary.

For a deeper understanding of how fibers work and how to handle interruptions, check out our guides on [Fibers](/docs/v4/concurrency/fibers/) and [Interruptions](/docs/v4/concurrency/basic-concurrency/#interruptions).

## 

There is no built-in way to determine in advance whether an effect will execute synchronously or asynchronously. Tracking this distinction would introduce several problems:

1. **Complexity:** Introducing this feature to track sync/async behavior in the type system would make Effect more complex to use and limit its composability.
2. **Safety Concerns:** Tracking asynchronous effects would not significantly improve safety. A callback-based API can invoke its callback immediately or defer it, and the type system cannot distinguish those behaviors reliably.

### 

In most cases, effects are run at the outermost parts of your application. Typically, an application built around Effect will involve a single call to the main effect. Here’s how you should approach effect execution:

- Use `runPromise` or `runFork`: For most cases, asynchronous execution should be the default. These methods provide the best way to handle Effect-based workflows.
- Use `runSync` only when necessary: Synchronous execution should be considered an edge case, used only in scenarios where asynchronous execution is not feasible. For example, when you are sure the effect is purely synchronous and need immediate results.

## 

The table provides a summary of the available `run*` functions, along with their input and output types, allowing you to choose the appropriate function based on your needs.

| API | Given | Result | 
|---|---|---|
| `runSync` | `Effect<A, E>` | `A` | 
| `runSyncExit` | `Effect<A, E>` | `Exit<A, E>` | 
| `runPromise` | `Effect<A, E>` | `Promise<A>` | 
| `runPromiseExit` | `Effect<A, E>` | `Promise<Exit<A, E>>` | 
| `runFork` | `Effect<A, E>` | `Fiber<A, E>` | 

You can find the complete list of `run*` functions [here](/docs/v4/api/effect/Effect#category-running).
