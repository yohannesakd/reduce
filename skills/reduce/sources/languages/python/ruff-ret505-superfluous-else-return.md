# Ruff rule RET505: superfluous-else-return

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/superfluous-else-return/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [superfluous-else-return (RET505)](#superfluous-else-return-ret505)

Added in [v0.0.154](https://github.com/astral-sh/ruff/releases/tag/v0.0.154) ·
Category: [pedantic](../?category=pedantic) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27superfluous-else-return%27%20OR%20RET505)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fflake8_return%2Frules%2Ffunction.rs#L225)

Derived from the **[flake8-return](../#flake8-return-ret)** linter.

Fix is sometimes available.

## [What it does](#what-it-does)

Checks for `else` statements with a `return` statement in the preceding
`if` block.

## [Why is this bad?](#why-is-this-bad)

The `else` statement is not needed as the `return` statement will always
break out of the enclosing function. Removing the `else` will reduce
nesting and make the code more readable.

## [Example](#example)

Use instead:
