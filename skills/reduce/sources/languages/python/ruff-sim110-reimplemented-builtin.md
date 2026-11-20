# Ruff rule SIM110: reimplemented-builtin

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/reimplemented-builtin/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [reimplemented-builtin (SIM110)](#reimplemented-builtin-sim110)

Added in [v0.0.211](https://github.com/astral-sh/ruff/releases/tag/v0.0.211) ·
Category: [complexity](../?category=complexity) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27reimplemented-builtin%27%20OR%20SIM110)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fflake8_simplify%2Frules%2Freimplemented_builtin.rs#L53)

Derived from the **[flake8-simplify](../#flake8-simplify-sim)** linter.

Fix is sometimes available.

## [What it does](#what-it-does)

Checks for `for` loops that can be replaced with a builtin function, like
`any` or `all`.

## [Why is this bad?](#why-is-this-bad)

Using a builtin function is more concise and readable.

## [Example](#example)

Use instead:

## [Fix safety](#fix-safety)

This fix is always marked as unsafe because it might remove comments.

## [Options](#options)

The rule will avoid flagging cases where using the builtin function would exceed the configured line length, as determined by these options:
