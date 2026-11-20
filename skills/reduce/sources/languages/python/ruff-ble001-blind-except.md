# Ruff rule BLE001: blind-except

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/blind-except/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [blind-except (BLE001)](#blind-except-ble001)

Added in [v0.0.127](https://github.com/astral-sh/ruff/releases/tag/v0.0.127) ·
Category: [suspicious](../?category=suspicious) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27blind-except%27%20OR%20BLE001)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fflake8_blind_except%2Frules%2Fblind_except.rs#L70)

Derived from the **[flake8-blind-except](../#flake8-blind-except-ble)** linter.

## [What it does](#what-it-does)

Checks for `except` clauses that catch all exceptions. This includes
`except BaseException` and `except Exception`.

## [Why is this bad?](#why-is-this-bad)

Overly broad `except` clauses can lead to unexpected behavior, such as
catching `KeyboardInterrupt` or `SystemExit` exceptions that prevent the
user from exiting the program.

Instead of catching all exceptions, catch only those that are expected to
be raised in the `try` block.

## [Example](#example)

Use instead:

Exceptions that are re-raised will *not* be flagged, as they're expected to
be caught elsewhere:

Exceptions that are logged with `exc_info` enabled will
*not* be flagged, as this is a common pattern for propagating exception
traces:
