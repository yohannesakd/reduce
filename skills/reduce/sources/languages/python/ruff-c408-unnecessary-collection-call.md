# Ruff rule C408: unnecessary-collection-call

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/unnecessary-collection-call/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [unnecessary-collection-call (C408)](#unnecessary-collection-call-c408)

Added in [v0.0.61](https://github.com/astral-sh/ruff/releases/tag/v0.0.61) ·
Category: [complexity](../?category=complexity) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27unnecessary-collection-call%27%20OR%20C408)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fflake8_comprehensions%2Frules%2Funnecessary_collection_call.rs#L43)

Derived from the **[flake8-comprehensions](../#flake8-comprehensions-c4)** linter.

Fix is always available.

## [What it does](#what-it-does)

Checks for unnecessary `dict()`, `list()` or `tuple()` calls that can be
rewritten as empty literals.

## [Why is this bad?](#why-is-this-bad)

It's unnecessary to call, e.g., `dict()` as opposed to using an empty
literal (`{}`). The former is slower because the name `dict` must be
looked up in the global scope in case it has been rebound.

## [Example](#example)

Use instead:

## [Fix safety](#fix-safety)

This rule's fix is marked as unsafe, as it may occasionally drop comments when rewriting the call. In most cases, though, comments will be preserved.
