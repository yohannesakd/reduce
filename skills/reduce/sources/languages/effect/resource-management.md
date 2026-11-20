# Introduction to Resource Management

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Effect team, effect.website
- Date: 2026-05-30
- License: MIT, as the site states
- Original location: https://effect.website/docs/v4/resource-management/introduction/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# Introduction

In long-running applications, managing resources efficiently is essential, particularly when building large-scale systems. If resources like socket connections, database connections, or file descriptors are not properly managed, it can lead to resource leaks, which degrade application performance and reliability. Effect provides constructs that help ensure resources are properly managed and released, even in cases where exceptions occur.

By ensuring that every time a resource is acquired, there is a corresponding mechanism to release it, Effect simplifies the process of resource management in your application.

## 

In many programming languages, the `try` / `finally` construct ensures that cleanup code runs regardless of whether an operation succeeds or fails. Effect provides similar functionality through `Effect.ensuring`, `Effect.onExit`, and `Effect.onError`.

### 

The `Effect.ensuring` function guarantees that a finalizer effect runs whether the main effect succeeds, fails, or is interrupted.

This is useful for performing cleanup actions such as closing file handles, logging messages, or releasing locks.

If you need access to the effect’s result, consider using [onExit](#onexit).

**Example** (Running a Finalizer in All Outcomes)

### 

`Effect.onExit` allows you to run a cleanup effect after the main effect completes, receiving an [Exit](/docs/v4/data-types/exit/) value that describes the outcome.

- If the effect succeeds, the `Exit` holds the success value.
- If it fails, the `Exit` includes the error or failure cause.
- If it is interrupted, the `Exit` reflects that interruption.

The cleanup step itself is uninterruptible, which can help manage resources in complex or high-concurrency cases.

**Example** (Running a Cleanup Function with the Effect’s Result)

### 

This function lets you attach a cleanup effect that runs whenever the calling effect fails, passing the cause of the failure to the cleanup effect.

You can use it to perform actions such as logging, releasing resources, or applying additional recovery steps.

The cleanup effect will also run if the failure is caused by interruption, and it is uninterruptible, so it always finishes once it starts.

**Example** (Running Cleanup Only on Failure)

## 

Many real-world operations involve working with resources that must be released when no longer needed, such as:

- Database connections
- File handles
- Network requests

Effect provides `Effect.acquireUseRelease`, which ensures that a resource is:

1. **Acquired** properly.
2. **Used** for its intended purpose.
3. **Released** even if an error occurs.

**Syntax**

**Example** (Automatically Managing Resource Lifetime)
