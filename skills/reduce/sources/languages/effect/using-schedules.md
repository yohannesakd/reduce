# Introduction to Schedules

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Effect team, effect.website
- Date: 2026-05-30
- License: MIT, as the site states
- Original location: https://effect.website/docs/v4/scheduling/using-schedules/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# Using schedules

A `Schedule` controls when an Effect may run again and when repetition stops.
Choose the function that matches what triggers the next run:

- Use `Effect.repeat` after a successful run.
- Use `Effect.schedule` when the first run must also wait for the schedule.
- Use `Effect.retry` after a failure.

These functions schedule work only while the current Effect runtime is running. They do not persist jobs or recover runs missed during downtime.

The function determines what triggers another run. The schedule determines when
that run may start and when repetition stops. See
[Choosing and combining schedules](/docs/v4/scheduling/choosing-and-combining-schedules)
to select those rules.

## 

`Effect.repeat` schedules another run only after the action succeeds. A failure
or interruption stops repetition and is propagated by the resulting Effect.
The action runs once before the schedule starts, so the schedule controls only
the additional runs.

**Example** (Polling a Background Job)

An application checks the status of a background job every 100 milliseconds.

`Effect.repeat` runs `checkJobStatus` immediately. After each successful run,
`pollingInterval` waits 100 milliseconds before allowing the next one.
`Schedule.spaced` does not stop on its own, so the effect continues until it
fails or is interrupted.

### 

You can stop repetition based on the action’s result with `until` or `while`,
and limit the number of repetitions with `times`. Pass these options directly
to `Effect.repeat`. This example stops when the job completes, with a limit of
ten checks.

**Example** (Waiting for the Job to Complete)

`times: 9` allows nine checks after the first one, for at most ten checks. If the
job has not completed by then, `Effect.repeat` returns the latest status.

## 

`Effect.repeat` runs the action immediately. Use `Effect.schedule` instead when
the first run must wait for the first scheduled time.

**Example** (Removing Expired Local Cache Files)

An application removes expired files from its local cache once per hour. It waits for the first hour to pass instead of doing disk work during startup.

`cacheCleanup` waits one hour before its first run, then waits another hour after
each successful cleanup before running again.

## 

Use `Effect.retry` when another run should happen after a failure instead of a
successful result. The first attempt runs immediately, and the schedule controls
the retries that follow.

**Example** (Retrying a Temporary Failure)

`Schedule.recurs(2)` permits two retries after the initial attempt, for at most
three attempts in total.

See [Retrying](/docs/v4/error-management/retrying) for retry conditions and
fallbacks. [Schedule cookbook](/docs/v4/scheduling/cookbook) shows how to
follow `Retry-After`, reconnect in stages, and record scheduled retries.

## 

`Effect.repeat` and `Effect.schedule` stop at the first failure. If an expected
failure should not stop later runs, handle it inside the repeated action. Do not
hide permanent errors only to keep the loop running.

Use `Effect.repeatOrElse` when the loop should stop but a fallback needs the
failure and the latest schedule metadata, when available. See the
[`Effect` API reference](/docs/v4/api/effect/Effect) for its full signature and
the other repetition options.

Next, choose a starting rule and add only the limits or changes it needs in
[Choosing and combining schedules](/docs/v4/scheduling/choosing-and-combining-schedules).
