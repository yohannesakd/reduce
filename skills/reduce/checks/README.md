# Checks

Each folder is one topic. Each file in a topic is one check, and each check belongs to one topic only. A case is a check that a sourced real case demonstrates.

The check step lists every check of every topic in the feature's checks file, in the order of this index: its file and its pattern, from the check's **Signal** or **Look for** line. The reviewer reads a check's file only when its pattern appears, gives a topic without a pattern one `absent` line, and does an open review after the checks.
The driver adds the folders that always apply: `every-feature` for every playbook, `unrelated-changes` for the `code` playbook, and `plans` for the `plan` playbook. It also adds each check of `languages` whose files appear in the feature.

For the provenance and limits of the cases, see [case sources](../guides/case-sources.md).

## Index

### `every-feature`

Always applies. The driver adds these checks.

- [A fresh design needs less](every-feature/fresh-design.md)
- [The feature and its parts go down the ladder](every-feature/ladder.md)
- [A behavior that nothing needs](every-feature/behavior-nothing-needs.md)
- [The refactoring algorithm and the general style](every-feature/refactoring.md)
- [A tool result](every-feature/tool-results.md)

### `languages`

The driver adds each check whose files appear in the feature: by extension, by a Python shebang, or by an import of React or Effect. The [refactoring check](every-feature/refactoring.md#language-rules) says how to apply them, and [rule sources](../guides/rule-sources.md) gives their licenses.

- [C rules](languages/c.md): `.c`, `.h`, `.cu`, `.cuh`
- [CUDA rules](languages/cuda.md): `.cu`, `.cuh`
- [JavaScript and TypeScript rules](languages/typescript.md): `.js`, `.mjs`, `.cjs`, `.jsx`, `.ts`, `.mts`, `.cts`, `.tsx`, `.vue`
- [React rules](languages/react.md): `.jsx`, `.tsx`, and files that import `react`
- [Vue rules](languages/vue.md): `.vue`
- [Effect rules](languages/effect.md): files that import `effect` or `@effect/`
- [Go rules](languages/go.md): `.go`
- [Python rules](languages/python.md): `.py`, `.pyi`, and Python shebang scripts

### `comments-and-docs`

The feature contains: comment, docstring, or documentation passage.

- [A comment or document that repeats the code, tells history, or hedges](comments-and-docs/comment-repeats-code.md)

### `guards-and-errors`

The feature contains: `try`/`catch`, guard, null check, error result, suppression directive, or cast.

- [A guard that cannot fail, or the same guard repeated](guards-and-errors/guard-that-cannot-fail.md)
- [One failure result stands for two different states](guards-and-errors/one-failure-for-two-states.md)
- [A suppression directive that hides a cause](guards-and-errors/suppression-that-hides-a-cause.md)
- [Call a guaranteed method directly](guards-and-errors/call-a-guaranteed-method-directly.md) (case)
- [Express an upstream guarantee in the input type](guards-and-errors/express-an-upstream-guarantee-in-the-type.md) (case)

### `functions-helpers-and-layers`

The feature contains: helper, wrapper, constant, pass-through layer, large or growing function, or code that hides its meaning.

- [A constant or helper with one user](functions-helpers-and-layers/helper-with-one-user.md)
- [A layer that only passes calls or values through](functions-helpers-and-layers/pass-through-layer.md)
- [A function that grew by accretion](functions-helpers-and-layers/function-grown-by-accretion.md)
- [A shared function whose parameters and branches keep growing](functions-helpers-and-layers/shared-function-that-keeps-growing.md)
- [Keep a local expression at its decision point](functions-helpers-and-layers/keep-a-local-expression-at-its-decision-point.md) (case)
- [Inspect readability separately from line count](functions-helpers-and-layers/inspect-readability-separately-from-line-count.md) (case)

### `unused-code`

The feature contains: function that does nothing, unused export, parameter, field, or branch, debug or harness code, or static-analysis results.

- [A function that does nothing, a result that is fixed, or an empty handler](unused-code/function-that-does-nothing.md)
- [An unused export, parameter, field, or branch](unused-code/unused-export-parameter-or-branch.md)
- [Debug or harness code in shipping source](unused-code/debug-code-in-shipping-source.md)
- [Bound deletion and check contracts beyond local callers](unused-code/bound-deletion-and-check-contracts.md) (case)
- [Give cleanup a concrete finding instead of a general request](unused-code/give-cleanup-a-concrete-finding.md) (case)

### `options-flags-and-settings`

The feature contains: option, parameter default, configuration, setting, environment variable, or feature flag.

- [An option that no caller uses](options-flags-and-settings/option-no-caller-uses.md)
- [A feature flag that every user already has](options-flags-and-settings/flag-every-user-has.md)
- [Remove configuration that does not control anything](options-flags-and-settings/remove-configuration-that-controls-nothing.md) (case)
- [Split flag cleanup between mechanical rewrites and judgment](options-flags-and-settings/split-flag-cleanup-between-rewrites-and-judgment.md) (case)

### `duplicates-and-existing-code`

The feature contains: second copy of code, similar code, a parallel design, or new code for work that the platform, a dependency, or the repository already does.

- [A second copy next to the first](duplicates-and-existing-code/second-copy.md)
- [A clone, by degree of similarity](duplicates-and-existing-code/clone-by-similarity.md)
- [An implementation that already exists](duplicates-and-existing-code/implementation-that-already-exists.md)
- [Delete an unused framework instead of maintaining two designs](duplicates-and-existing-code/delete-an-unused-framework.md) (case)
- [Reuse a protocol implementation instead of rebuilding it](duplicates-and-existing-code/reuse-a-protocol-implementation.md) (case)

### `dependencies-and-imports`

The feature contains: dependency or import.

- [A dependency that the code does not need](dependencies-and-imports/dependency-the-code-does-not-need.md)
- [An import inside a function](dependencies-and-imports/import-inside-a-function.md)

### `owners-and-producers`

The feature contains: the same fix at several call sites, or state that copies a value that another owner holds.

- [A fix at the call sites instead of the source](owners-and-producers/fix-at-the-call-sites.md)
- [State that mirrors other state](owners-and-producers/state-that-mirrors-other-state.md)

### `tests`

The feature contains: test, fixture, mock, or test helper, or a test expectation that changed.

- [Tests](tests/test-rules.md)
- [A test that cannot fail for the right reason](tests/test-that-cannot-fail.md)
- [A fix and its tests share one wrong assumption](tests/fix-and-tests-share-an-assumption.md)

### `async-ordering-and-recovery`

The feature contains: async step, timer, queue, ordering, retry, or recovery machinery, or compatibility for a state that may be unreachable.

- [Recovery, compatibility, or a flag for a state that no reachable input produces](async-ordering-and-recovery/recovery-for-an-unreachable-state.md)
- [Fix event coordination instead of adding recovery state](async-ordering-and-recovery/fix-event-coordination-instead-of-recovery-state.md) (case)
- [Remove an unnecessary scheduling step instead of building an ordering subsystem](async-ordering-and-recovery/remove-an-unnecessary-scheduling-step.md) (case)

### `performance`

The feature contains: data reads, parsing, computation, cache, batch, query, loop, measurement, or a performance claim.

- [Repeated or unneeded work on the feature's paths](performance/repeated-or-unneeded-work.md)
- [Measure the complete operation when evaluating an optimization](performance/measure-the-complete-operation.md) (case)
- [Choose the measurement before building an analytics system](performance/choose-the-measurement-before-building-analytics.md) (case)

### `extra-scope`

The feature contains: variant, feature, demonstration, or restriction that the request did not ask for.

- [Deliver the requested component instead of several expanded variants](extra-scope/deliver-the-requested-component.md) (case)
- [Separate required behavior from an unsolicited demonstration](extra-scope/separate-required-behavior-from-a-demonstration.md) (case)
- [Remove an unnecessary browser restriction, then verify the real inputs](extra-scope/remove-an-unnecessary-browser-restriction.md) (case)

### `mechanical-migrations`

The feature contains: one syntax change repeated across many files.

- [Use a mechanical edit for a mechanical migration](mechanical-migrations/use-a-mechanical-edit-for-a-mechanical-migration.md) (case)

### `agent-instructions`

The feature contains: agent instructions or skills.

- [Compare instructions with a controlled baseline](agent-instructions/compare-instructions-with-a-controlled-baseline.md) (case)
- [Set task boundaries before selecting tools and effort](agent-instructions/set-task-boundaries-before-tools-and-effort.md) (case)
- [Test whether each standing instruction changes behavior](agent-instructions/test-whether-each-instruction-changes-behavior.md) (case)

### `unrelated-changes`

The feature contains: hunk that does not serve the stated problem.

- [A hunk that does not serve the problem](unrelated-changes/hunk-that-does-not-serve-the-problem.md)

### `plans`

The feature contains: phase, abstraction, or plan unit for a later or unrequired need.

- [A phase or abstraction that serves a later phase only](plans/phase-that-serves-a-later-phase.md)
- [A plan unit that no requirement needs](plans/plan-unit-no-requirement-needs.md)
