# Ruff rule RET504: unnecessary-assign

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/unnecessary-assign/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [unnecessary-assign (RET504)](#unnecessary-assign-ret504)

Added in [v0.0.154](https://github.com/astral-sh/ruff/releases/tag/v0.0.154) ·
Category: [pedantic](../?category=pedantic) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27unnecessary-assign%27%20OR%20RET504)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fflake8_return%2Frules%2Ffunction.rs#L182)

Derived from the **[flake8-return](../#flake8-return-ret)** linter.

Fix is always available.

## [What it does](#what-it-does)

Checks for variable assignments that immediately precede a `return` of the
assigned variable.

## [Why is this bad?](#why-is-this-bad)

The variable assignment is not necessary, as the value can be returned directly.

## [Example](#example)

Use instead:
