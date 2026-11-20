# Unexpected Errors

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Effect team, effect.website
- Date: 2026-05-30
- License: MIT, as the site states
- Original location: https://effect.website/docs/v4/error-management/unexpected-errors/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
Unexpected errors, or defects, indicate bugs, violated invariants, or failures outside the program’s expected domain. They are retained in the runtime Cause, but do not appear in the typed error channel.

Defects normally should be reported and allowed to terminate the affected fiber. Recover from them only at boundaries where continuing is explicitly safe.

Creating a Defect

Effect.die(defect) creates an Effect that terminates with the supplied defect. Its typed error channel is never.

Example (Terminating on an Impossible Input)

Pass a string or, preferably, an Error with a useful message to Effect.die.

Exceptions thrown while evaluating Effect callbacks such as Effect.sync are also represented as defects.

Converting Typed Errors to Defects

Effect.orDie converts every typed failure into a defect and removes the typed error channel.

Example (Treating a Failure as Unrecoverable)

To customize the defect, transform the typed error first with Effect.mapError and then apply Effect.orDie.

Inspecting the Complete Exit

Effect.exit moves the complete outcome into the success channel:

Unlike Effect.result, an Exit preserves the complete Cause, including defects and interruptions.

Example (Inspecting a Defect with Exit)

This is useful at application boundaries, in tests, and when integrating with APIs that need an explicit value for every outcome.

catchDefect

Effect.catchDefect handles defects only. Typed failures and interruptions are left unchanged.

Example (Recovering from a Defect)

catchCause

Effect.catchCause handles the complete Cause, including typed failures, defects, interruptions, and multiple reasons.

Example (Recovering Based on the Cause)

Prefer typed recovery operators such as Effect.catch and Effect.catchTag for domain errors. Use catchDefect or catchCause only where recovering from unexpected failures is intentional and safe.
