# Inspect readability separately from line count

**Source:** Armin Ronacher, 7 September 2026. **Evidence:** firsthand report with generated code excerpts; no successful replacement.

**Look for.** Code that hides its meaning: positional access such as `row[3]`, numbers without names, nested conditional expressions, dense one-line expressions, boolean arguments, or names that do not say what the value is.

**Observed.** Compressed tests, deeply nested shell scripts, and production behavior reached through numeric list positions:

```python
if _task_accelerator is not None:
    _task_accelerator[6](task)
```

**Other forms.**

```ts
const s = r[2] && !(f ? a : b[1]) ? 1 : x > 86400 ? 2 : 0;
send(user, true, false);
```

**Inferred practice.** Review names, responsibilities, and control flow after functional checks. Compare with nearby code that serves the same role.

**Applies when.** Meaning and required performance stay the same.

**Limits.** The report supplies no validated rewrite. Do not present a named replacement as observed human code.

**Reduce fit.** A `simplify` result must not compress meaning. Judge by concepts and reader effort; line count is secondary.

[Report with original excerpts](../../sources/web/lucumr-pocoo-org-2026-9-7-astra-why.md).
