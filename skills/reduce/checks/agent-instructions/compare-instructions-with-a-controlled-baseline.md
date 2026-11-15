# Compare instructions with a controlled baseline

**Source:** Igor Warzocha, `@Howaboua`, X, 24 August 2026, and instruction-calibration guidance revised 24 September.

**Look for.** Agent instructions or skills that a change adds or removes without a run that compares them with a baseline.

**Observed.** Warzocha first rewrote skills without isolated tests, then inspected default model behavior before deciding which instructions added value.
The published practice compares fresh sessions with the same model, effort, tools, task, folder, and files, and changes only the candidate instruction.
It separates initial output from coached corrections and checks which instruction files were actually read.
The guidance then verifies the candidate in the normal working environment.

**Inferred practice.** Use a real failure, a nearby ambiguous case, and an unrelated task. Keep guidance that changes the intended decision without expanding unrelated work.

**Applies when.** Judge the intended behavior and check unrelated tasks.

**Limits.** The repository shows the procedure, but not complete paired runs that prove code-quality gains. The current guidance postdates the X report.

**Reduce fit.** Proof in the check step when the target is agent instructions.

[Original X report](https://x.com/Howaboua/status/2091789833794376005). [Pinned calibration procedure](https://github.com/IgorWarzocha/howaboua-pi-stuff/blob/a06eae4d141fae421a8d0108a4a560013d6508a8/packages/pi-skill-harness-and-agent-engineering/skills/instruction-calibration/SKILL.md).
