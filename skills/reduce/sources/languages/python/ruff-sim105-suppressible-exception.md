# Ruff rule SIM105: suppressible-exception

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/suppressible-exception/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [suppressible-exception (SIM105)](#suppressible-exception-sim105)

Added in [v0.0.211](https://github.com/astral-sh/ruff/releases/tag/v0.0.211) ·
Category: [pedantic](../?category=pedantic) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27suppressible-exception%27%20OR%20SIM105)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fflake8_simplify%2Frules%2Fsuppressible_exception.rs#L46)

Derived from the **[flake8-simplify](../#flake8-simplify-sim)** linter.

Fix is sometimes available.

## [What it does](#what-it-does)

Checks for `try`-`except`-`pass` blocks that can be replaced with the
`contextlib.suppress` context manager.

## [Why is this bad?](#why-is-this-bad)

Using `contextlib.suppress` is more concise and directly communicates the
intent of the code: to suppress a given exception.

Note that `contextlib.suppress` is slower than using `try`-`except`-`pass`
directly. For performance-critical code, consider retaining the
`try`-`except`-`pass` pattern.

## [Example](#example)

Use instead:
