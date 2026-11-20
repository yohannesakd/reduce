# Retrying

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Effect team, effect.website
- Date: 2026-05-30
- License: MIT, as the site states
- Original location: https://effect.website/docs/v4/error-management/retrying/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
Retrying is appropriate for transient failures such as temporary network or service unavailability. It is not a substitute for handling permanent errors, and defects or interruptions are never retried.

retry

Effect.retry reruns an Effect after a typed failure. The source Effect is always evaluated once before the retry policy is applied.

Example (Retrying a Fixed Number of Times)

times is the number of retries after the initial attempt. Therefore { times: 5 } allows at most six executions of the source Effect.

Retrying Selected Errors

The options object can combine:

while: retry while the predicate is true;

until: stop retrying when the predicate is true;

times: limit the number of retries;

schedule: control timing and additional stopping conditions.

Predicates may return either a boolean or an Effect.

Example (Retrying Only Transient Errors)

Using a Schedule

A Schedule can define delays, backoff, jitter, and retry limits. Schedule.recurs(3), for example, permits three retries after the initial attempt.

Use Effect.repeat instead when repetition depends on successful values rather than errors.

retryOrElse

Effect.retryOrElse uses a Schedule and runs a fallback Effect when the schedule is exhausted. The fallback receives the final error and the schedule’s output.
