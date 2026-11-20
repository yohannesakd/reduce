# Ruff rule RET506: superfluous-else-raise

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/superfluous-else-raise/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [superfluous-else-raise (RET506)](#superfluous-else-raise-ret506)

Added in [v0.0.154](https://github.com/astral-sh/ruff/releases/tag/v0.0.154) ·
Category: [pedantic](../?category=pedantic) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27superfluous-else-raise%27%20OR%20RET506)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fflake8_return%2Frules%2Ffunction.rs#L270)

Derived from the **[flake8-return](../#flake8-return-ret)** linter.

Fix is sometimes available.

## [What it does](#what-it-does)

Checks for `else` statements with a `raise` statement in the preceding `if`
block.

## [Why is this bad?](#why-is-this-bad)

The `else` statement is not needed as the `raise` statement will always
break out of the current scope. Removing the `else` will reduce nesting
and make the code more readable.

## [Example](#example)

Use instead:
