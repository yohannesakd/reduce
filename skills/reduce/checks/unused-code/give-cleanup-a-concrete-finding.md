# Give cleanup a concrete finding instead of a general request

**Source:** Engr Mejba Ahmed, 4 June 2026. **Evidence:** firsthand tool report and public analyzer; application code is private.

**Look for.** A cleanup with no named symbol, duplicate range, or dependency, or tool findings that mix new problems with inherited ones.

**Observed.** Three copies of audio extraction logic, an unused `extractAllAudio` export, and a testing dependency in production dependencies.
Deterministic analysis located them. Branch comparison separated new findings from inherited ones.

**Inferred practice.** Give each cleanup a specific symbol, duplicate range, or dependency. Verify its callers and purpose before changing it.

**Applies when.** Include public contracts, generated callers, platform entry points, and tests.

**Limits.** Static analysis supplies candidates, not decisions. The report promotes a tool and provides no public diff.

**Reduce fit.** Mechanical evidence from the tool results of the scope step. A tool finding is a candidate until its users are traced.

[Firsthand report](https://www.mejba.me/blog/fallow-ai-code-quality-tool). [Analyzer source](https://github.com/fallow-rs/fallow). [Companion skill source](https://github.com/fallow-rs/fallow-skills).
