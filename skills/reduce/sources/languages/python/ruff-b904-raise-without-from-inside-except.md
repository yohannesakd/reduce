# Ruff rule B904: raise-without-from-inside-except

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/raise-without-from-inside-except/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [raise-without-from-inside-except (B904)](#raise-without-from-inside-except-b904)

Added in [v0.0.138](https://github.com/astral-sh/ruff/releases/tag/v0.0.138) ·
Category: [pedantic](../?category=pedantic) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27raise-without-from-inside-except%27%20OR%20B904)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fflake8_bugbear%2Frules%2Fraise_without_from_inside_except.rs#L52)

Derived from the **[flake8-bugbear](../#flake8-bugbear-b)** linter.

## [What it does](#what-it-does)

Checks for `raise` statements in exception handlers that lack a `from`
clause.

## [Why is this bad?](#why-is-this-bad)

In Python, `raise` can be used with or without an exception from which the
current exception is derived. This is known as exception chaining. When
printing the stack trace, chained exceptions are displayed in such a way
so as make it easier to trace the exception back to its root cause.

When raising a new exception from within an `except` clause, it's recommended to
include a `from` clause to explicitly set the exception's cause. Without it,
Python will implicitly chain from the current exception (setting `__context__`),
but the `__cause__` attribute won't be set, which may make debugging slightly
more difficult.

## [Example](#example)

Use instead:
