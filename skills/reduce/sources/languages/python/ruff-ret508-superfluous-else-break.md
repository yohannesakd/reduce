# Ruff rule RET508: superfluous-else-break

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/superfluous-else-break/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [superfluous-else-break (RET508)](#superfluous-else-break-ret508)

Added in [v0.0.154](https://github.com/astral-sh/ruff/releases/tag/v0.0.154) ·
Category: [pedantic](../?category=pedantic) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27superfluous-else-break%27%20OR%20RET508)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fflake8_return%2Frules%2Ffunction.rs#L364)

Derived from the **[flake8-return](../#flake8-return-ret)** linter.

Fix is sometimes available.

## [What it does](#what-it-does)

Checks for `else` statements with a `break` statement in the preceding `if`
block.

## [Why is this bad?](#why-is-this-bad)

The `else` statement is not needed, as the `break` statement will always
break out of the loop. Removing the `else` will reduce nesting and make the
code more readable.

## [Example](#example)

Use instead:
