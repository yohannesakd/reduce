# Basic Concurrency

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Effect team, effect.website
- Date: 2026-05-30
- License: MIT, as the site states
- Original location: https://effect.website/docs/v4/concurrency/basic-concurrency/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# Basic Concurrency

## 

Effect provides options to manage how effects are executed, particularly focusing on controlling how many effects run concurrently.

The `concurrency` option is used to determine the level of concurrency, with the following values:

Let’s explore each configuration in detail.

### 

By default, if you don’t specify any concurrency option, effects will run sequentially, one after the other. This means each effect starts only after the previous one completes.

**Example** (Sequential Execution)

### 

You can control how many effects run concurrently by setting a `number` for `concurrency`. For example, `concurrency: 2` allows up to two effects to run at the same time.

**Example** (Limiting to 2 Concurrent Tasks)

### 

When `concurrency: "unbounded"` is used, there’s no limit to the number of effects running concurrently.

**Example** (Unbounded Concurrency)

## 

All effects in Effect are executed by [fibers](/docs/v4/concurrency/fibers/). If you didn’t create the fiber yourself, it was created by an operation you’re using (if it’s concurrent) or by the Effect [runtime](/docs/v4/runtime/) system.

A fiber is created any time an effect is run. When running effects concurrently, a fiber is created for each concurrent effect.

To summarize:

- An `Effect` is a higher-level concept that describes an effectful computation. It is lazy and immutable, meaning it represents a computation that may produce a value or fail but does not immediately execute.
- A fiber, on the other hand, represents the running execution of an `Effect`. It can be interrupted or awaited to retrieve its result. Think of it as a way to control and interact with the ongoing computation.

Fibers can be interrupted in various ways. Let’s explore some of these scenarios and see examples of how to interrupt fibers in Effect.

### 

A fiber can be interrupted using the `Effect.interrupt` effect on that particular fiber.

This effect models the explicit interruption of the fiber in which it runs.
When executed, it causes the fiber to stop its operation immediately, capturing the interruption details such as the fiber’s ID and its start time.
The resulting interruption can be observed in the [Exit](/docs/v4/data-types/exit/) type if the effect is run with functions like [runPromiseExit](/docs/v4/getting-started/running-effects/#runpromiseexit).

**Example** (Without Interruption)

In this case, the program runs without any interruption, logging the start and completion of the task.

**Example** (With Interruption)

Here, the fiber is interrupted after the log `"start"` but before the `"done"` log. The `Effect.interrupt` stops the fiber, and it never reaches the final log.

### 

Registers a cleanup effect to run when an effect is interrupted.

This function allows you to specify an effect to run when the fiber is interrupted. This effect will be executed when the fiber is interrupted, allowing you to perform cleanup or other actions.

**Example** (Running a Cleanup Action on Interruption)

In this example, we set up a handler that logs “Cleanup completed” whenever the fiber is interrupted. We then show three cases: a successful effect, a failing effect, and an interrupted effect, demonstrating how the handler is triggered depending on how the effect ends.

### 

When running multiple effects concurrently, such as with `Effect.forEach`, if one of the effects is interrupted, it causes all concurrent effects to be interrupted as well.

The resulting [cause](/docs/v4/data-types/cause/) includes information about which fibers were interrupted.

**Example** (Interrupting Concurrent Effects)

## 

### 

This function takes two effects and runs them concurrently. The first effect that successfully completes will determine the result of the race, and the other effect will be interrupted.

If neither effect succeeds, the function will fail with a [cause](/docs/v4/data-types/cause/) containing all the errors.

This is useful when you want to run two effects concurrently, but only care about the first one to succeed. It is commonly used in cases like timeouts, retries, or when you want to optimize for the faster response without worrying about the other effect.

**Example** (Both Tasks Succeed)

**Example** (One Task Fails, One Succeeds)

**Example** (Both Tasks Fail)

If you want to handle the result of whichever task completes first, whether it succeeds or fails, you can use the `Effect.result` function. This function wraps the result in a [Result](/docs/v4/data-types/result/) type, allowing you to see if the result was a success (`Success`) or a failure (`Failure`):

**Example** (Handling Success or Failure with Result)

### 

This function runs multiple effects concurrently and returns the result of the first one to succeed. If one effect succeeds, the others will be interrupted.

If none of the effects succeed, the function will fail with the last error encountered.

This is useful when you want to race multiple effects, but only care about the first one to succeed. It is commonly used in cases like timeouts, retries, or when you want to optimize for the faster response without worrying about the other effects.

**Example** (All Tasks Succeed)

**Example** (One Task Fails, Two Tasks Succeed)

**Example** (All Tasks Fail)

### 

This function takes two effects and runs them concurrently, returning the result of the first one that completes, regardless of whether it succeeds or fails.

This function is useful when you want to race two operations, and you want to proceed with whichever one finishes first, regardless of whether it succeeds or fails.

**Example** (Both Tasks Succeed)

**Example** (One Task Fails, One Succeeds)

#### 

The optional `onWinner` callback receives the winning fiber and its index (`0` for the first effect, `1` for the second). The callback is observational: the result of `raceFirst` is still determined by the first effect to complete.

**Example** (Observing Which Task Completes First)
