# Ruff rule SIM118: in-dict-keys

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/in-dict-keys/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [in-dict-keys (SIM118)](#in-dict-keys-sim118)

Added in [v0.0.176](https://github.com/astral-sh/ruff/releases/tag/v0.0.176) ·
Category: [complexity](../?category=complexity) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27in-dict-keys%27%20OR%20SIM118)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fflake8_simplify%2Frules%2Fkey_in_dict.rs#L41)

Derived from the **[flake8-simplify](../#flake8-simplify-sim)** linter.

Fix is always available.

## [What it does](#what-it-does)

Checks for key-existence checks against `dict.keys()` calls.

## [Why is this bad?](#why-is-this-bad)

When checking for the existence of a key in a given dictionary, using
`key in dict` is more readable and efficient than `key in dict.keys()`,
while having the same semantics.

## [Example](#example)

Use instead:

## [Fix safety](#fix-safety)

Given `key in obj.keys()`, `obj` *could* be a dictionary, or it could be
another type that defines a `.keys()` method. In the latter case, removing
the `.keys()` attribute could lead to a runtime error. The fix is marked
as safe when the type of `obj` is known to be a dictionary; otherwise, it
is marked as unsafe.
