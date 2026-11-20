# Expected Errors

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Effect team, effect.website
- Date: 2026-05-30
- License: MIT, as the site states
- Original location: https://effect.website/docs/v4/error-management/expected-errors/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# Expected Errors

Expected errors are represented in the error channel of [`Effect`](/docs/v4/getting-started/the-effect-type/):

Because the error type is explicit, callers can see which failures are possible and decide which ones to recover from.

## 

`Effect.fail(error)` creates an Effect that fails with `error`. Use `Effect.failSync` when constructing the error should be deferred until the Effect runs.

**Example** (Creating a Typed Failure)

Errors built with `Data.Error` or `Data.TaggedError` are also yieldable directly inside `Effect.gen`. See [Yieldable Errors](/docs/v4/error-management/yieldable-errors/).

## 

When effects with different error types are composed, Effect tracks their union.

Sequential composition short-circuits on the first failure. Operations after the failure are not evaluated.

## 

Sometimes the caller needs to inspect both outcomes without recovering into another Effect.

### 

`Effect.result` moves the typed error into a [`Result`](/docs/v4/data-types/result/) in the success channel:

**Example** (Inspecting a Result)

`Effect.result` handles typed failures only. Defects and interruptions remain failures of the fiber.

### 

`Effect.option` discards the error value, returning `Option.some(value)` on success and `Option.none()` on a typed failure.

Use `result` when the error value matters and `option` only when every typed failure means absence.

## 

`Effect.catch` handles every typed error with a recovery Effect. It does not catch defects or interruptions.

**Example** (Recovering from Every Typed Error)

When the handler cannot fail, `Effect.catchEager` is an eager optimization for recovery Effects that can be evaluated immediately.

Use [`Effect.catchCause`](/docs/v4/error-management/unexpected-errors/#catchcause) when the handler needs the complete failure cause.

## 

Selective catch operators preserve all unmatched errors in the error channel.

### 

`Effect.catchTag` handles one member of a tagged error union and removes that member from the resulting error type.

**Example** (Catching One Tagged Error)

`catchTag` also accepts a non-empty array of tags when several tagged errors share one handler.

### 

`Effect.catchTags` handles several tagged errors with a table of tag-specific handlers.

**Example** (Catching Several Tagged Errors)

### 

`Effect.catchIf` selects errors with a predicate or type guard.

### 

`Effect.catchFilter` uses the `Filter` module for reusable or composable selection logic. A narrowing filter also removes the handled subtype from the error channel.

**Example** (Catching with a Filter)

## 

Some tagged errors contain another tagged error in a readonly `reason` field. `Effect.catchReason` handles one nested reason while keeping the parent error type for unmatched reasons; `Effect.catchReasons` handles several.

**Example** (Catching a Nested Reason)

Use `Effect.unwrapReason(errorTag)` when the nested reasons should replace the parent error in the error channel instead of being handled immediately.
