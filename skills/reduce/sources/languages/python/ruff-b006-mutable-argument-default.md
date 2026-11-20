# Ruff rule B006: mutable-argument-default

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/mutable-argument-default/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [mutable-argument-default (B006)](#mutable-argument-default-b006)

Added in [v0.0.92](https://github.com/astral-sh/ruff/releases/tag/v0.0.92) ·
Category: [suspicious](../?category=suspicious) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27mutable-argument-default%27%20OR%20B006)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fflake8_bugbear%2Frules%2Fmutable_argument_default.rs#L82)

Derived from the **[flake8-bugbear](../#flake8-bugbear-b)** linter.

Fix is sometimes available.

## [What it does](#what-it-does)

Checks for uses of mutable objects as function argument defaults.

## [Why is this bad?](#why-is-this-bad)

Function defaults are evaluated once, when the function is defined.

The same mutable object is then shared across all calls to the function. If the object is modified, those modifications will persist across calls, which can lead to unexpected behavior.

Instead, prefer to use immutable data structures, or take `None` as a
default, and initialize a new mutable object inside the function body
for each call.

Arguments with immutable type annotations will be ignored by this rule.
Types outside of the standard library can be marked as immutable with the
[`lint.flake8-bugbear.extend-immutable-calls`](../../settings/#lint_flake8-bugbear_extend-immutable-calls) configuration option.

## [Known problems](#known-problems)

Mutable argument defaults can be used intentionally to cache computation
results. Replacing the default with `None` or an immutable data structure
does not work for such usages. Instead, prefer the `@functools.lru_cache`
decorator from the standard library.

## [Example](#example)

Use instead:

## [Options](#options)

## [Fix safety](#fix-safety)

This fix is marked as unsafe because it replaces the mutable default with `None`
and initializes it in the function body, which may not be what the user intended,
as described above.
