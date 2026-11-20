# Ruff rule RET501: unnecessary-return-none

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/unnecessary-return-none/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [unnecessary-return-none (RET501)](#unnecessary-return-none-ret501)

Added in [v0.0.154](https://github.com/astral-sh/ruff/releases/tag/v0.0.154) ·
Category: [style](../?category=style) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27unnecessary-return-none%27%20OR%20RET501)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fflake8_return%2Frules%2Ffunction.rs#L65)

Derived from the **[flake8-return](../#flake8-return-ret)** linter.

Fix is always available.

## [What it does](#what-it-does)

Checks for the presence of a `return None` statement when `None` is the only
possible return value.

## [Why is this bad?](#why-is-this-bad)

Python implicitly assumes `return None` if an explicit `return` value is
omitted. Therefore, explicitly returning `None` is redundant and should be
avoided when it is the only possible `return` value across all code paths
in a given function.

## [Example](#example)

Use instead:

## [Fix safety](#fix-safety)

This rule's fix is marked as unsafe for cases in which comments would be
dropped from the `return` statement.

## [Options](#options)

This rule ignores functions marked as properties.
