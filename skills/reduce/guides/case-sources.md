# Case sources

The provenance and limits of the cases: concrete cases where a smaller design met the same need as a larger one.
The check step prints the rules for applying a case.

Compiled on 23 October 2026 from the public sources cited in each case. Dates identify the report, PR, or experiment.
[Split flag cleanup between mechanical rewrites and judgment](../checks/options-flags-and-settings/split-flag-cleanup-between-rewrites-and-judgment.md) and [Treat a simplification as a proof obligation](../evidence/treat-a-simplification-as-a-proof-obligation.md) were added on 31 October 2026 from the sources that they cite.

## Cases by kind of code

The [check index](../checks/README.md#index) lists each case under its kind of code. Each case states what to look for in its **Look for** field.

## Evidence labels

**Human implementation** means a human proposal, review intervention, or directed cleanup. It does not mean that a person typed every line.

- **Reported AI output:** the source identifies generated code, but does not supply its complete generation history.
- **Human-directed cleanup:** the diff proves the simplification. Original AI authorship is not established for every line.
- **Controlled comparison:** the same model receives different instructions. This measures guidance, not handwritten human code.

An automated review does not prove AI authorship. Verification results attributed to authors were not independently rerun.
Architecture and workflow comparisons are explanatory deductions. They do not claim that an author implemented or validated every alternative.


## Architecture comparisons

These comparisons extrapolate the design choices behind the reports. They illustrate practices; they are not additional observed implementations.

| Reports | Expanded approach | Smaller choice | Condition for the lesson |
| --- | --- | --- | --- |
| [A fresh design needs less](../checks/every-feature/fresh-design.md) | Improve helpers inside an elaborate design. | Reconsider the design, then build only the required responsibilities. | Both meet the same acceptance criteria. |
| [Test whether each standing instruction changes behavior](../checks/agent-instructions/test-whether-each-instruction-changes-behavior.md), [Compare instructions with a controlled baseline](../checks/agent-instructions/compare-instructions-with-a-controlled-baseline.md) | Add standing instructions after each disappointing output. | Change one instruction and compare otherwise identical runs. | Judge the intended behavior and check unrelated tasks. |
| [Set task boundaries before selecting tools and effort](../checks/agent-instructions/set-task-boundaries-before-tools-and-effort.md), [Separate required behavior from an unsolicited demonstration](../checks/extra-scope/separate-required-behavior-from-a-demonstration.md) | Treat plausible extras as part of the product. | Tie each component to a current requirement. | Keep behavior needed for correctness, including implied behavior. |
| [Inspect readability separately from line count](../checks/functions-helpers-and-layers/inspect-readability-separately-from-line-count.md) | Hide operations behind compressed syntax and positions. | Use explicit names and the codebase's structure. | Meaning and required performance stay the same. |
| [Give cleanup a concrete finding instead of a general request](../checks/unused-code/give-cleanup-a-concrete-finding.md), [Bound deletion and check contracts beyond local callers](../checks/unused-code/bound-deletion-and-check-contracts.md) | Ask for a broad cleanup and accept what disappears. | Select concrete findings, trace consumers, change in bounded batches. | Include public contracts, generated callers, platform entry points, and tests. |
| [Choose the measurement before building an analytics system](../checks/performance/choose-the-measurement-before-building-analytics.md) | Analytics APIs, event pipeline, general reporting. | One defined counter, with `New` until data is sufficient. | Request counts are adequate for the indicator. |
| [Use a mechanical edit for a mechanical migration](../checks/mechanical-migrations/use-a-mechanical-edit-for-a-mechanical-migration.md) | A model edits each instance of a repeated migration. | One transformation, applied mechanically, then a diff and type check. | The rule covers the real syntax and nothing else. |
| [Measure the complete operation when evaluating an optimization](../checks/performance/measure-the-complete-operation.md) | Time a helper after moving its work elsewhere. | Time the complete caller-visible operation. | Inputs, outputs, workload, and boundaries stay comparable. |
| [Split flag cleanup between mechanical rewrites and judgment](../checks/options-flags-and-settings/split-flag-cleanup-between-rewrites-and-judgment.md) | Leave a rolled-out flag, its branch, and its tests. | Remove them together, driven by the flag system of record. | No kill switch, override, or season depends on the flag. |
| [Treat a simplification as a proof obligation](../evidence/treat-a-simplification-as-a-proof-obligation.md) | Accept a cleanup because it looks cleaner. | Accept it after a baseline, a written equivalence reason, and a mechanical gate. | The inventory inputs cover the behavior that the claim touches. |

For each reduction, name what disappears: a branch, state variable, owner, dependency, interface, or optional feature. Explain why the required behavior survives.
Reject reductions that only hide complexity, move it to another file, suppress failures, or remove necessary behavior.
Do not turn these cases into blanket bans on helpers, retries, configuration, tests, or defensive checks. Their value depends on the actual call path.

## Evidence record

- Public PR metadata, file patches, commit sequences, and relevant review comments were inspected. Immutable revisions are used where available.
- No repository builds, test suites, or end-to-end runs were performed for these cases.
- [Remove an unnecessary scheduling step instead of building an ordering subsystem](../checks/async-ordering-and-recovery/remove-an-unnecessary-scheduling-step.md)'s X post dates from October; both compared PRs date from August. The Hatchet PR bodies, metadata, and patches were inspected; no Hatchet code was run.
- [Remove an unnecessary browser restriction, then verify the real inputs](../checks/extra-scope/remove-an-unnecessary-browser-restriction.md)'s generated HTML contains the cited assignment. No corrected browser run was performed.
- [Use a mechanical edit for a mechanical migration](../checks/mechanical-migrations/use-a-mechanical-edit-for-a-mechanical-migration.md) and [Measure the complete operation when evaluating an optimization](../checks/performance/measure-the-complete-operation.md) screenshots could not be downloaded, so they were not independently inspected.
- X mirror timestamps conflicted. [Test whether each standing instruction changes behavior](../checks/agent-instructions/test-whether-each-instruction-changes-behavior.md) and [Set task boundaries before selecting tools and effort](../checks/agent-instructions/set-task-boundaries-before-tools-and-effort.md) omit post dates; [A fresh design needs less](../checks/every-feature/fresh-design.md) uses the dated archived copy.
- Reports and posts without code or outcome evidence were excluded from the engineering examples, the cases that cite code or a PR.
- [Split flag cleanup between mechanical rewrites and judgment](../checks/options-flags-and-settings/split-flag-cleanup-between-rewrites-and-judgment.md) and [Treat a simplification as a proof obligation](../evidence/treat-a-simplification-as-a-proof-obligation.md) are practice reports. Neither has a public diff. [Split flag cleanup between mechanical rewrites and judgment](../checks/options-flags-and-settings/split-flag-cleanup-between-rewrites-and-judgment.md)'s article was read through its background section. [Treat a simplification as a proof obligation](../evidence/treat-a-simplification-as-a-proof-obligation.md)'s skill files were not inspected.
