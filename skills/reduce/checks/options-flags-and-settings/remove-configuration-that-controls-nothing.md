# Remove configuration that does not control anything

**Source:** Strata's configuration cleanup in PR 76, 21 October 2026. **Attribution:** reported excess generated code; field provenance is not individually traced.

**Look for.** A setting that no execution reads: an option field, environment variable, command-line flag, component property, default, or builder method that code declares or sets but never uses.

**Required behavior.** Configure synchronization with values that the running implementation actually reads.

**Observed.** `SyncConfig` included retry-count and backoff settings, default functions, and builder methods that no execution read.
The cleanup removed those fields, defaults, builders, and assertions about their values. It kept read configuration such as batch size.

```text
Before
  Settings: workspace, batch size, retry count, backoff
  Execution reads: workspace, batch size

After
  Settings: workspace, batch size
  Execution reads: workspace, batch size
```

**Other forms.**

```ts
interface ClientOptions { timeoutMs?: number; retries?: number }   // only timeoutMs is read
const LOG_FORMAT = process.env.LOG_FORMAT ?? "json";             // nothing reads LOG_FORMAT
```

**Why it works.** An unread value cannot influence the execution path. The removal does not remove an implemented retry policy.

**Inferred lesson.** Every configurable choice should match behavior that the system actually selects. Trace an option from declaration to execution.
An assertion about a default value does not prove that the option controls anything.

**Applies when.** No execution path reads the option, and no external consumer sets it.

**Limits.** Serialized fields and exported builders can still have external consumers. Workspace searches and passing tests do not prove those consumers are absent.

**Reduce fit.** `remove`. An externally settable field is an accepted input. When its consumers are unknown, the unit is `unresolved`.

[Configuration diff at the cleanup commit](../../sources/github/phfarath-strata-commit-72045cc07e.md). [Previous schema](../../sources/github/phfarath-strata-crates-strata-core-src-schemas-rs.md).
