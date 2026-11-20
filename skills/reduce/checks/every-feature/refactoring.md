# The refactoring algorithm and the general style

**Signal.** Every feature that has code, or a plan that describes code. The driver gives this check to every feature, and gives the [language checks](../README.md#languages) that the feature's files match. The design and close steps apply it to every design and every change of code.

**Decide with.** The PufferLib guide below. Its text is copied 1:1 from [`SKILL_ISSUES.md`](https://github.com/PufferAI/PufferLib/blob/5.0/SKILL_ISSUES.md). Each **Reduce:** line under a PufferLib line extends that line for a reduce run. The [C](../languages/c.md) and [CUDA](../languages/cuda.md) sections of the guide are in the language checks.

> This is a hand-written guide of how I style and refactor PufferLib
> It is equally useful for human and AI brogrammers. And for other projects.
> If your name is not John Carmack, you should probably read it before blindly
> shoveling it into whatever language model is currently replacing you.

## Objective

Reduce source code length without golfing while preserving behavior and performance. Preserve existing determinism. Discard biases against long files or functions.

- **Reduce:** Behavior and performance are the [fixed behavior](../../guides/fixed-behavior.md#fixed-behavior). A long file or a long function is not a finding by itself. Golfing is a shorter form that is harder to read: dense one-line expressions, cryptic names, or removed meaning.

## Joseph's Stupid Refactoring Algorithm

- **Reduce:** Apply the five steps in order to each function and file of the feature. At each place, stop at the first rung that the evidence supports, as [the ladder](ladder.md) says.

1. Inline every function that is only used once and tighten former call sites
   - **Reduce:** The rung is `simplify`. A function with one call site is the signal. The map step records these functions.
   - **Reduce:** Keep the function only when [a constant or helper with one user](../functions-helpers-and-layers/helper-with-one-user.md) keeps it, such as a name that the caller needs to read its own logic.
   - **Reduce:** After the inline, tighten the former call site. Remove the temporary names, parameters, and conversions that only the call needed.
2. Eliminate defensive checks. Replace complex error handling with plain asserts.
   - **Reduce:** A check that cannot fail goes, because a type or an upstream guarantee excludes the state. The rung is `remove`, and the effect is `parity`. See [a guard that cannot fail](../guards-and-errors/guard-that-cannot-fail.md) and [express an upstream guarantee in the type](../guards-and-errors/express-an-upstream-guarantee-in-the-type.md).
   - **Reduce:** Complex handling of a state that only a bug produces becomes one plain assert, in the assert form of the language check. The rung is `simplify`, and the effect is `parity`.
   - **Reduce:** Handling of a failure that a reachable input causes stays. An assert in its place changes the result: write it as an `intent` finding with the decision `user`.
   - **Reduce:** Validate external data once, at the entry point where it enters the target: user input, files, the network, the environment, and other programs. Trust the validated type after that point. Remove the second and later checks of the same data.
3. Reduce deeply nested code by merging and inverting conditionals
   - **Reduce:** The rung is `simplify`. Merge conditions that lead to the same body. Invert a condition that wraps the rest of a block, and return, continue, or break early.
4. Co-optimize multi-consumer functions with their callers
   - **Reduce:** The rung is `remove` or `simplify`. Remove each parameter, branch, and result that no caller needs. Move work that only one caller needs into that caller. The map step records these functions and their callers.
   - **Reduce:** See [a shared function whose parameters and branches keep growing](../functions-helpers-and-layers/shared-function-that-keeps-growing.md).
5. Apply syntax and style guide as a final pass
   - **Reduce:** Apply the general style below and each language check that the feature's files match. Then run the project's formatter.

## Syntax & Style (General)

- **G1** Do not split up code into more files
  - **Reduce:** `simplify`. Merge a file that holds only code for one other file into that file.
- **G2** Soft 80-col / hard 100-col limit
  - **Reduce:** `lead`.
- **G3** Do not one-line loops or conditionals
  - **Reduce:** `lead`. The body of a loop or a conditional goes on its own line.
- **G4** 4-space indents. Do NOT match opening parens
  - **Reduce:** `lead`.
- **G5** Next line continuations indent 4 extra spaces instead of matching parens
  - **Reduce:** `lead`.
- **G6** Apply semantic vertical spacing between blocks of code sparingly
  - **Reduce:** `lead`. A blank line separates two blocks of different meaning only.
- **G7** Tests are important but their length and code quality is not counted
  - **Reduce:** Do not write a finding only to shorten a test or to improve its style.
- **G8** Do not add source complexity or shims for ease of testing
  - **Reduce:** `remove`. Remove a parameter, an interface, a hook, or a branch that only a test uses.
- **G9** Do not block off comments with --- or ### etc.
  - **Reduce:** `remove`. Remove the lines of `---`, `###`, `===`, or similar characters. Keep the comment text.

- **Reduce:** Apply G1 to G9 like the language rules below. A layout rule, G2 to G6, never gives a finding: record one lead for each file.

## Precedence

When two rules disagree, the first source in this list decides:

1. [Fixed behavior](../../guides/fixed-behavior.md#fixed-behavior): required results, contracts, performance, and determinism.
2. The project's configured formatter owns the layout: indentation, line length, wrapping, and blank lines. Examples are gofmt, Prettier, Black, Ruff, and clang-format. G2 to G6 apply only to files that no formatter formats.
3. A written project rule that requires the opposite of a language rule. Cite it in the check line. A looser linter setting is not such a rule.
4. The language checks.
5. G1, G8, G9, and the five steps of this check.

## Language rules

Each language check is a rule list. A rule is not a signal: a line that breaks it gets a record, unless the rule's **Keep when** holds or the precedence above overrides it.

- For the `code` playbook, apply the rules to the lines that the change adds or changes. For the `codebase` and `plan` playbooks, apply them to every line of the feature.
- A rule tagged `remove`, `reuse`, or `simplify` gives a finding at that rung. Name the rule ID, such as `languages/go` GO7.
- A rule tagged `lead` removes nothing. Record each line that breaks it in `## Leads`, with the rule ID. A quick review has no `## Leads`: list these lines in `## Report`, with the suspected defects.
- Give one finding or one lead to each rule, with every location that breaks it. Do not write one finding for each line.
- A rule that names a version applies only when the project's declared version meets it. Find the version in the manifest, such as `package.json`, `go.mod`, or `pyproject.toml`.
- In `## Checks`, give each language check one line: its finding and lead IDs, or `absent` with the place that you examined.

**Keeps it when.** The step's own condition keeps the part: a name that the caller needs, a reachable failure, or validation at an entry point. The precedence above gives the layout to a formatter, or a written project rule requires the opposite.

**Sources.** [PufferLib `SKILL_ISSUES.md`](https://github.com/PufferAI/PufferLib/blob/5.0/SKILL_ISSUES.md), MIT. The quoted text and the PufferLib lines are copied 1:1. The **Reduce:** lines, the precedence, and the language rules are additions of reduce. See [rule sources](../../guides/rule-sources.md).
