# Keep a local expression at its decision point

**Source:** the desktop error change in OpenClaw PR 161659, 30 September 2026. **Attribution:** human-directed cleanup.

**Look for.** A small helper with one caller separates a decision from its result, so the reader must go to another place to see what happens.

**Required behavior.** If launch fails, trim the supplied error message and use the existing fallback when it is empty.

**Observed.** A separate helper constructed the error, and the failure branch threw its return value. The cleanup moved the same construction into that branch. Normalized:

```js
// Before.
function makeLaunchError(result) {
  const text = result.error?.message?.trim();
  return new Error(text || fallbackMessage);
}
if (!result.ok) throw makeLaunchError(result);

// After.
if (!result.ok) {
  const text = result.error?.message?.trim();
  throw new Error(text || fallbackMessage);
}
```

**Other forms.** A `buildErrorMessage()` that one `throw` uses. A `shouldShowBanner()` that one `if` uses. A `getDefaultOptions()` that one constructor uses.

**Why it works.** The expression, fallback, and throw condition stay the same. This relocates logic; it does not remove error handling.

**Inferred lesson.** An abstraction earns its place by hiding meaningful complexity, naming a useful concept, or owning a policy. Keep a small decision and its consequence together.

**Applies when.** The helper adds navigation only, with no name, policy, or boundary that helps the reader.

**Limits.** A single caller does not automatically make a helper unnecessary. Keep helpers that name substantial logic, enforce a boundary, or improve understanding.

**Reduce fit.** `simplify`. One caller is a reason to inspect a helper, not proof that it is unnecessary.

[Pinned desktop carrier diff](https://github.com/openclaw/openclaw/commit/b231790955).
