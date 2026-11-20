# Ruff rule UP032: f-string

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/f-string/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [f-string (UP032)](#f-string-up032)

Added in [v0.0.224](https://github.com/astral-sh/ruff/releases/tag/v0.0.224) ·
Category: [complexity](../?category=complexity) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27f-string%27%20OR%20UP032)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fpyupgrade%2Frules%2Ff_strings.rs#L44)

Derived from the **[pyupgrade](../#pyupgrade-up)** linter.

Fix is sometimes available.

## [What it does](#what-it-does)

Checks for `str.format` calls that can be replaced with f-strings.

## [Why is this bad?](#why-is-this-bad)

f-strings are more readable and generally preferred over `str.format`
calls.

## [Example](#example)

Use instead:
