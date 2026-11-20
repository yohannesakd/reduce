# pstack poteto-mode: references/code-quality.md

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Cursor, pstack plugin
- Original location: https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/references/code-quality.md
- Copied: 2026-11-20, from the installed pstack skill on this machine; the file is no longer on the main branch of cursor/plugins

## Text
# Code-quality checks

Use this reference when changing executable logic or planning its verification.
Apply complexity, duplication, and test-strength checks within the task's affected behavior.
Keep project policy, scope, runtime permissions, and host scheduling rules.

## Select the checks

Trace changed functions and their callers before choosing tools.
Use project-configured checks first.
Where compatible, use Crapper, Dryer, and Mutator for the checks below.
Verify language, framework, coverage format, and command support before relying on a tool.
Their documented language sets do not establish support for C# or Vue single-file components.
Use a compatible project tool when these tools cannot analyze the affected code.
Report unavailable checks explicitly.

Start with changed functions and related code that could share the same responsibility.
Include committed task changes, staged edits, unstaged edits, and new files in the selected scope.
Do not assume `--changed` includes the full task branch.
Exclude generated, vendored, and unrelated code.
For a trivial change, use focused verification when additional analysis would add no material evidence.
For documentation or presentation-only changes, mark these checks as not applicable.
Configuration changes that affect executable behavior still need verification at that boundary.
State the reason for each omitted applicable check.

Before implementation, use a failing behavior test when practical.
For existing correct behavior, establish passing checks before refactoring.
After the behavior works, improve structure and test strength without expanding the requested change.
Remove obsolete task code and rerun affected behavior checks after refactoring.

## Complexity and coverage

Crapper combines decision complexity with coverage in the CRAP score.
CRAP means Change Risk Anti-Patterns.
Higher scores identify complex code with insufficient test coverage.

Use the project's threshold when one exists.
Otherwise, use CRAP 10 as an advisory review signal from ub-mode.
Reduce unnecessary decisions or add tests for material uncovered behavior.
Split a function only when distinct responsibilities justify the split.
Do not move branches into wrappers merely to lower a score.
Record justified exceptions, including clear case dispatch that benefits from remaining together.

Confirm coverage matches the tested revision, selected files, and configuration.
Distinguish unavailable coverage from measured zero coverage.
Crapper can report zero coverage after a failed coverage command or missing dependency.
Inspect command results before treating that value as a test gap.
A complexity-only run does not establish CRAP or coverage success.

## Duplication

Use Dryer to inspect candidate pairs around changed code.
Use the project's threshold when one exists.
Otherwise, use similarity 0.8 as an advisory review signal from ub-mode.
Inspect both implementations, callers, domain meaning, and reasons they might change.
Consolidate duplicated responsibility when one shared implementation improves clarity and ownership.
Keep similar structures separate when their contracts or reasons for change differ.
Record retained candidates and their concrete reasons.
A successful Dryer exit means analysis completed; it does not mean no duplication exists.

## Test strength

Use focused mutation testing for material logic whose tests must detect incorrect results.
A mutation is a deliberate code change that can expose a missing assertion.
Begin with passing baseline tests and an explicit file set.
Use Mutator or the project's compatible mutation tool.
Bound workers, runtime, and test scope to the task and available resources.
Keep all child test computation inside the scheduled job when host policy requires scheduling.

Inspect uncovered sites and surviving mutations.
Add behavior tests for reachable, material gaps.
Remove dead code only after checking callers and reachable behavior.
For equivalent mutations, record why observable behavior cannot differ.
Investigate timeouts, compilation failures, and runner errors separately from assertion failures.
Mutator can count timeouts and uncompilable mutations as killed.
Those results alone do not prove that assertions detect incorrect behavior.
Report incomplete runs and untested sites without claiming full mutation coverage.

Validate cached results against test changes as well as source changes.
Mutator's differential mode can retain killed results when function text is unchanged.
When tests or relevant configuration change, rerun the selected mutations instead of trusting those cached results.
After improving tests or structure, rerun affected behavior checks and the applicable quality checks.

## Execution

Inspect installed tool versions, help, setup steps, test commands, and external effects before execution.
The three upstream launchers can create environments and install dependencies on first use.
Crapper can regenerate coverage, install coverage helpers, and replace previous reports.
Mutator requires a sibling Crapper checkout and runs project tests before creating mutation workers.
Its worker overlays link other project files; they are not a credential or filesystem sandbox.
Use an isolated disposable checkout when tool writes or test effects could affect unrelated work.
Run untrusted tool code only within the isolation required by the host's security policy.
Do not install tools automatically during read-only work.
For implementation, use the project's dependency process and the host's computation scheduler.

Prefer explicit task paths and verified existing coverage when available.
These examples assume inspected tools already exist on PATH and the coverage matches the current source:

```sh
crapper --use-existing-coverage src/changed-module.py
dryer --threshold 0.8 src/changed-module.py src/related-module.py
mutator --use-existing-coverage --mutate-all --max-workers 1 src/changed-module.py
```

Adapt commands to the actual project and installed versions.
Keep source files, tests, dependency files, and unrelated reports intact after the run.

## Evidence and completion

Reuse the task's decision log or verification record.
Record tool versions, selected paths, tested revision, relevant dirty files, commands, and report locations.
For each applicable check, record its result, fixes, retained exceptions, or explicit verification gap.
Keep the before-and-after evidence needed to assess improvements.
Complete the unit when behavior checks pass and applicable findings have supported dispositions.
If a required check is unavailable, report the blocker rather than accepting the unit as verified.
Advisory exceptions require a reason; they do not require unrelated cleanup.
Summarize consequential decisions and remaining limits in the final reply.
Commit verified units locally under the existing publication rules.

## Sources

Adapted from [ub-mode](https://github.com/unclebob/ub-mode/blob/master/SKILL.md).
Tool behavior was checked against the [Crapper](https://github.com/unclebob/crapper), [Dryer](https://github.com/unclebob/dryer), and [Mutator](https://github.com/unclebob/mutator) documentation on 2026-10-25.
These sources inform quality checks. They do not change account, cleanup, publication, or merge authorization.
