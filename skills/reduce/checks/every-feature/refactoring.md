# The refactoring algorithm and the general style

**Signal.** Every feature that has code, or a plan that describes code. The driver gives this check to every feature, with the [language checks](../README.md#languages) that the feature's files match. The design and close steps apply it to every design and every change of code.

**Decide with.** Read the guide first. It is the PufferLib guide, copied 1:1. Then apply it as [how reduce applies the guide](#how-reduce-applies-the-guide) says. When the two disagree, the table decides.

## The guide

> This is a hand-written guide of how I style and refactor PufferLib
> It is equally useful for human and AI brogrammers. And for other projects.
> If your name is not John Carmack, you should probably read it before blindly
> shoveling it into whatever language model is currently replacing you.

### Objective
Reduce source code length without golfing while preserving behavior and performance. Preserve existing determinism. Discard biases against long files or functions.

### Joseph's Stupid Refactoring Algorithm
1. Inline every function that is only used once and tighten former call sites
2. Eliminate defensive checks. Replace complex error handling with plain asserts.
3. Reduce deeply nested code by merging and inverting conditionals
4. Co-optimize multi-consumer functions with their callers
5. Apply syntax and style guide as a final pass

### Syntax & Style (General)
- Do not split up code into more files
- Soft 80-col / hard 100-col limit
- Do not one-line loops or conditionals
- 4-space indents. Do NOT match opening parens
- Next line continuations indent 4 extra spaces instead of matching parens
- Apply semantic vertical spacing between blocks of code sparingly
- Tests are important but their length and code quality is not counted
- Do not add source complexity or shims for ease of testing
- Do not block off comments with --- or ### etc.

## How reduce applies the guide

Apply the five steps in order to each function and file of the feature. At each place, stop at the first rung that the evidence supports, as [the ladder](ladder.md) says. The objective's "behavior and performance" is the [fixed behavior](../../guides/fixed-behavior.md#fixed-behavior). A long file or function is never a finding by itself.

| Step | Record | Do this | Keep the code when |
|---|---|---|---|
| 1 | `simplify`, `parity` | Inline the function into its one call site. Then remove the names, parameters, and conversions that only the call needed. | [A constant or helper with one user](../functions-helpers-and-layers/helper-with-one-user.md) keeps it. |
| 2 | `remove`, `parity` | Remove a check that cannot fail, because a type or an upstream guarantee excludes the state. See [a guard that cannot fail](../guards-and-errors/guard-that-cannot-fail.md). | |
| 2 | `simplify`, `parity` | Replace handling of a state that only a bug produces with one assert, in the language check's assert form. | |
| 2 | `intent`, decision `user` | Handling of a failure that a reachable input causes stays. Replacing it with an assert changes behavior, so the user decides. | Always, until the user decides. |
| 2 | `remove`, `parity` | Validate external data once, where it enters the target. Remove the second and later checks of the same data. | |
| 3 | `simplify`, `parity` | Merge conditions that lead to the same body. Invert a condition that wraps the rest of a block, and exit early. | |
| 4 | `remove` or `simplify` | Remove each parameter, branch, and result that no caller needs. Move work that only one caller needs into that caller. See [a shared function that keeps growing](../functions-helpers-and-layers/shared-function-that-keeps-growing.md). | |
| 5 | | Apply the style rules below and each language check. Then run the project's formatter. | |

The style rules are the lines of Syntax & Style (General), in order:

| ID | Rule, shortened | Tag | Note |
|---|---|---|---|
| G1 | Do not split up code into more files | `simplify` | Merge a file that only one other file uses into that file. |
| G2 | Soft 80-col / hard 100-col limit | `lead` | |
| G3 | Do not one-line loops or conditionals | `lead` | |
| G4 | 4-space indents. Do NOT match opening parens | `lead` | |
| G5 | Next line continuations indent 4 extra spaces | `lead` | |
| G6 | Apply semantic vertical spacing sparingly | `lead` | |
| G7 | Tests are important but not counted | none | Never write a finding only to shorten a test. |
| G8 | Do not add source complexity or shims for ease of testing | `remove` | Remove a parameter, interface, hook, or branch that only a test uses. |
| G9 | Do not block off comments with --- or ### etc. | `remove` | Keep the comment text. |

G2 to G6 are layout. They never give a finding: record one lead for each file.

## Precedence

When two rules disagree, the first source in this list decides:

1. [Fixed behavior](../../guides/fixed-behavior.md#fixed-behavior): required results, contracts, performance, and determinism.
2. The project's configured formatter owns the layout: indentation, line length, wrapping, and blank lines. Examples are gofmt, Prettier, Black, and Ruff. G2 to G6 apply only to files that no formatter formats.
3. A written project rule that requires the opposite of a language rule. Cite it in the check line. A looser linter setting is not such a rule.
4. The language checks.
5. G1, G8, G9, and the five steps.

## Language rules

Each language check is a list of rules. A rule is not a signal: each line that breaks it gets a record. The exceptions are the rule's **Unless** line and the precedence above.

- For the `code` playbook, apply the rules to the lines that the change adds or changes. For the `codebase` and `plan` playbooks, apply them to every line of the feature.
- A rule tagged `remove`, `reuse`, or `simplify` gives a finding at that rung. Name the rule ID, such as `languages/go` GO7.
- A rule tagged `lead` removes nothing. Record each line that breaks it in `## Leads`, with the rule ID. A quick review has no `## Leads`: list these lines in `## Report`, with the suspected defects.
- Give one finding or one lead to each rule, with every location that breaks it. Do not write one finding for each line.
- A rule that names a version applies only when the project's declared version meets it. Find the version in the manifest, such as `package.json`, `go.mod`, or `pyproject.toml`.
- In `## Checks`, give each language check one line: its finding and lead IDs, or `absent` with the place that you examined.

**Keeps it when.** The table's **Keep the code when** column holds, or the precedence gives the layout to a formatter or a written project rule.

**Sources.** [PufferLib `SKILL_ISSUES.md`](https://github.com/PufferAI/PufferLib/blob/5.0/SKILL_ISSUES.md), MIT. [The guide](#the-guide) is copied 1:1, without its C and CUDA sections. The rest of this file is an addition of reduce. See [rule sources](../../guides/rule-sources.md).
