# The refactoring algorithm and the general style

**Signal.** Every feature that has code, or a plan that describes code. The driver gives this check to every feature, and gives the [language checks](../README.md#languages) that the feature's files match. The design and close steps apply it to every design and every change of code.

**Decide with.** The objective: make the source shorter without golfing. Keep the behavior, the performance, and the existing determinism. A long file or a long function is not a problem by itself.

Apply the five steps in order to each function and file of the feature. Stop at the first rung that the evidence supports, as [the ladder](ladder.md) says.

1. Inline every function that has one call site, and tighten the former call site. The rung is `simplify`. Keep the function only when [a constant or helper with one user](../functions-helpers-and-layers/helper-with-one-user.md) keeps it.
2. Remove defensive checks. Replace complex handling of internal failures with plain asserts.
   - A check that cannot fail, because a type or an upstream guarantee excludes the state, goes. The rung is `remove`, and the effect is `parity`. See [a guard that cannot fail](../guards-and-errors/guard-that-cannot-fail.md) and [express an upstream guarantee in the type](../guards-and-errors/express-an-upstream-guarantee-in-the-type.md).
   - Handling for a state that only a bug produces becomes one assert, in the assert form of the language check. The rung is `simplify`, and the effect is `parity`.
   - Handling for a failure that a reachable input causes stays. An assert in its place changes the result: write it as an `intent` finding with the decision `user`.
   - Validate external data once, at the entry point where it enters the target: user input, files, the network, the environment, and other programs. Trust the validated type after that point. Remove the second and later checks of the same data.
3. Reduce deep nesting. Merge conditionals, invert them, and return early. The rung is `simplify`.
4. Co-optimize each function that has several callers with its callers. Remove each parameter, branch, and result that no caller needs. Move work that only one caller needs into that caller. The rung is `remove` or `simplify`. See [a shared function whose parameters and branches keep growing](../functions-helpers-and-layers/shared-function-that-keeps-growing.md).
5. Apply the general style below and each language check as a final pass.

## General style

- G1. Do not split code into more files.
- G2. Keep lines to 80 columns where possible. Never exceed 100 columns.
- G3. Do not put a loop body or a conditional body on the line of its loop or condition.
- G4. Indent with 4 spaces. Do not align a continuation line with an opening parenthesis.
- G5. Indent a continuation line 4 more spaces than the line that it continues.
- G6. Use blank lines between blocks only to separate meaning, and only a few.
- G7. Do not add source complexity or a shim to make code easier to test.
- G8. Do not block off comments with lines of `---`, `###`, `===`, or similar characters.

Tests are important, but their length and their code quality do not count. Do not write a finding only to shorten a test.

## Precedence

When two rules disagree, the first source in this list decides:

1. [Fixed behavior](../../guides/fixed-behavior.md#fixed-behavior): required results, contracts, performance, and determinism.
2. The project's configured formatter owns the layout: indentation, line length, wrapping, and blank lines. Examples are gofmt, Prettier, Black, Ruff, and clang-format. G2 to G6 apply only to files that no formatter formats.
3. A written project rule that requires the opposite of a language rule. Cite it in the check line. A looser linter setting is not such a rule.
4. The language checks.
5. G1, G7, G8, and the five steps of this check.

## Language rules

Each language check is a rule list. A rule is not a signal: a line that breaks it gets a record, unless the rule's **Keep when** holds or the precedence above overrides it.

- For the `code` playbook, apply the rules to the lines that the change adds or changes. For the `codebase` and `plan` playbooks, apply them to every line of the feature.
- A rule tagged `remove`, `reuse`, or `simplify` gives a finding at that rung. Name the rule ID, such as `languages/go` G7.
- A rule tagged `lead` removes nothing. Record each line that breaks it in `## Leads`, with the rule ID.
- Give one finding or one lead to each rule, with every location that breaks it. Do not write one finding for each line.
- A rule that names a version applies only when the project's declared version meets it. Find the version in the manifest, such as `package.json`, `go.mod`, or `pyproject.toml`.
- In `## Checks`, give each language check one line: its finding and lead IDs, or `absent` with the place that you examined.

**Keeps it when.** The step's own condition keeps the part: a name that the caller needs, a reachable failure, or validation at an entry point. The precedence above gives the layout to a formatter, or a written project rule requires the opposite.

**Sources.** Adapted from the PufferLib refactoring guide, [`SKILL_ISSUES.md`](https://github.com/PufferAI/PufferLib/blob/5.0/SKILL_ISSUES.md), MIT. The changes: steps 2 and 4 name the rung, the effect, and the reachable-failure limit; the precedence and the language rules are new. See [rule sources](../../guides/rule-sources.md).
