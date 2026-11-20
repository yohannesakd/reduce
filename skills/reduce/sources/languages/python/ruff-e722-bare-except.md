# Ruff rule E722: bare-except

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/bare-except/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [bare-except (E722)](#bare-except-e722)

Added in [v0.0.36](https://github.com/astral-sh/ruff/releases/tag/v0.0.36) ·
Category: [suspicious](../?category=suspicious) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27bare-except%27%20OR%20E722)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fpycodestyle%2Frules%2Fbare_except.rs#L48)

Derived from the **[pycodestyle](../#pycodestyle-e-w)** linter.

## [What it does](#what-it-does)

Checks for bare `except` catches in `try`-`except` statements.

## [Why is this bad?](#why-is-this-bad)

A bare `except` catches `BaseException` which includes
`KeyboardInterrupt`, `SystemExit`, `Exception`, and others. Catching
`BaseException` can make it hard to interrupt the program (e.g., with
Ctrl-C) and can disguise other problems.

## [Example](#example)

Use instead:

If you actually need to catch an unknown error, use `Exception` which will
catch regular program errors but not important system exceptions.
