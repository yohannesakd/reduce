# Fix event coordination instead of adding recovery state

**Source:** AustinMroz's review and ComfyUI PR 18781, 25 September 2026. **Attribution:** explicit human intervention; original AI generation is not established.

**Look for.** Recovery state, such as pending promises, settle waits, or retries, added because two operations that depend on each other start separately.

**Required behavior.** Reload model folders after capability changes select a different data source. Previously loaded folders stay usable.

**Observed, expanded approach.** Separate watchers triggered immediate reloads. Later patches tracked pending promises, recorded the committed source, waited for reload settlement, and retried folder rebuilding.

**Observed, human intervention.** The reviewer identified existing debounced reload behavior and recommended one capability watcher that reused it:

```ts
watch([() => flags.assetsEnabled, () => flags.supportsModelTypeTags], () =>
  scheduleModelReload()
)
```

**Why it helps.** Both flags arrive together. The existing delayed reload can include folders whose eager loading has already begun.

**Measured scope.** The simplifying commit changes production code by +20/−70 lines. Its +28/−264 total includes test deletions.

**Inferred lesson.** Before adding recovery state, examine how the competing operations start. Coordinating their triggers through one existing owner can remove later reconciliation.

**Applies when.** One existing lifecycle owner can express the required ordering.

**Limits.** The final PR documents a residual race when the library first opens during an active reload. This is not proof of complete behavioral equivalence.
Keep coordination state when independent operations genuinely require it.

**Reduce fit.** A `reuse` group that replaces the recovery units together. Prove ordering claims with the formal verification reference when ordinary checks cannot decide them.

[Human review](https://github.com/Comfy-Org/ComfyUI_frontend/pull/18781#discussion_r4107026627). [Exact simplifying commit](https://github.com/Comfy-Org/ComfyUI_frontend/commit/073237b79c7547f5e1550d9cf4b1b74884bffbfe). [Final behavior limits](https://github.com/Comfy-Org/ComfyUI_frontend/pull/18781).
