# Measure the complete operation when evaluating an optimization

**Source:** Dmitriy Kovalenko, `@neogoose_btw`, X, 15 May 2026. **Evidence:** firsthand observation with a screenshot; no diff or benchmark harness.

**Look for.** A measurement, benchmark, timer, or speed claim: a "faster" commit message or comment, a test that times part of the work, or a cache added for speed.

**Observed.** A model claimed a 7–10× speedup. Kovalenko reports that it had moved the work into another function.

**Other forms.** A benchmark that times a helper after the work moved to its caller. A speedup that skips validation, I/O, or warm-up. A timer that starts after the slow step.

**Inferred practice.** Measure the full caller-visible operation with the same input and output checks. Include work delegated to helpers.

**Applies when.** Inputs, outputs, workload, and boundaries stay comparable.

**Limits.** The post does not provide enough to reproduce the claim or a working human replacement.

**Reduce fit.** Resource checks in the check step measure the whole operation, before and after the reduction. To judge a measured speed claim in the target, or to measure a reduction, follow `~/.agents/skills/benchmark-checklist/SKILL.md`: state the exact claim, confirm that the work happened and is correct, find the limiting resource, compare equal work, and check repeatability.

[Original X post](https://x.com/neogoose_btw/status/2055385342002569531).
