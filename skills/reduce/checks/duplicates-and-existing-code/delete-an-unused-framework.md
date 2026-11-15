# Delete an unused framework instead of maintaining two designs

**Source:** phfarath, Strata PR 76, 21 October 2026. **Attribution:** the author identifies excess generated code; cleanup also uses agent tools.

**Look for.** A general mechanism next to the path that runs: a registry, plugin system, gateway, event bus, policy layer, or manager that the running code does not call.

**Required behavior.** Dispatch tools through the application's active server path.

**Observed.** An additional `ToolGateway` trait and `DefaultToolGateway` provided registration, permissions, rate limiting, and event logging. The author identified it as unused.
The cleanup kept the active dispatcher and deleted the gateway, its exports, and its tests.

```text
Before
  Active server -> existing tool dispatch -> tool execution
  Unused ToolGateway -> separate policies, registry, limiter, event logging

After
  Active server -> existing tool dispatch -> tool execution
```

**Why it works.** The real dispatch path already bypassed the deleted abstraction. `gateway.rs` alone loses 403 lines.

**Other forms.** A plugin registry with one plugin that the application also imports directly. An event bus with publishers and no subscribers. A strategy interface whose one strategy the callers build by hand.

**Inferred lesson.** Architectural completeness is not evidence of necessity. Start from the executing path and find the component that already owns each responsibility.

**Applies when.** No supported external consumer or entry point uses the parallel design.

**Limits.** The author reports 354 passing tests; four gateway tests were removed. That does not prove external API compatibility. The PR remained open when checked.

**Reduce fit.** `remove` for the group. Exported types are public interfaces. Check their consumers first.

[PR rationale](https://github.com/phfarath/Strata/pull/76). [Pinned gateway deletion](https://github.com/phfarath/Strata/commit/72045cc07e8459ff97d861c46cffcac57b30d7ce).
