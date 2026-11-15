# Recovery, compatibility, or a flag for a state that no reachable input produces

**Signal.** Code or a plan has a recovery branch, a flag, a rollback path, or a compatibility shim.

```text
Phase 4: Add `legacy_mode` flag (default off). Remove it in Phase 9.
Phase 5: Keep a compatibility shim for callers of the old endpoint.
```

**Decide with.** Classify the old endpoint's consumers with the [consumer evidence](../../evidence/tools-and-evidence.md#consumer-evidence) rules, not with a search of the baseline alone.

- Every caller is in repositories that you searched, and the endpoint is internal. Trace each caller at the baseline, at each phase, and in the reduced target. If the plan moves every caller to the new endpoint before the shim would run, no entry needs the shim, and Phase 5 is `remove`.
  If a caller still reaches the old endpoint in any state, the shim serves a requirement entry. Phase 5 stays, or the plan moves that caller first.
- Outside clients, partner scripts, or released versions can call the endpoint: the behavior entry is `unknown`. Phase 5 is `unresolved`, and the evidence that decides it is a client list or a release record.

A flag whose value never changes in production has one value. Remove it. Keep a rollout step, rollback, or recovery mechanism only when a requirement entry fails without it, a source requires it, or a reachable side effect would cause consequential harm.

**Keeps it when.** An accepted source names the consumer of the old endpoint, or the migration touches persisted data that cannot be rebuilt.

**Sources.** [Google review guidance](https://www.freecodecamp.org/news/what-google-taught-me-about-code-reviews/).
