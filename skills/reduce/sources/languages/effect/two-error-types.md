# Two Types of Errors

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Effect team, effect.website
- Date: 2026-05-30
- License: MIT, as the site states
- Original location: https://effect.website/docs/v4/error-management/two-error-types/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# Two Types of Errors

Effect distinguishes between errors that are part of a program’s domain and unexpected problems that indicate a bug or broken invariant.

## 

Expected errors, also called **failures**, **typed errors**, or **recoverable errors**, are part of normal program execution. Examples include invalid input, a missing record, or a rejected request.

They are tracked in the error channel of `Effect`:

The type makes the possible failure visible to callers, who can recover from it with operators such as `Effect.catch` or `Effect.catchTag`.

## 

Unexpected errors, also called **defects**, are not part of the intended control flow. Examples include failed assertions, impossible states, and bugs in third-party code.

Defects are not tracked in the `Effect` error channel. They are still retained by the runtime in the effect’s `Cause`, together with typed failures and fiber interruptions.

Defects usually should not be recovered from inside domain logic. At application boundaries, `Effect.exit`, `Effect.catchDefect`, or `Effect.catchCause` can be used to inspect or report them.
