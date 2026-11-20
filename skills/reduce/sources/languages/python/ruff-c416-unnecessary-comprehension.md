# Ruff rule C416: unnecessary-comprehension

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/unnecessary-comprehension/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [unnecessary-comprehension (C416)](#unnecessary-comprehension-c416)

Added in [v0.0.73](https://github.com/astral-sh/ruff/releases/tag/v0.0.73) ·
Category: [pedantic](../?category=pedantic) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27unnecessary-comprehension%27%20OR%20C416)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fflake8_comprehensions%2Frules%2Funnecessary_comprehension.rs#L62)

Derived from the **[flake8-comprehensions](../#flake8-comprehensions-c4)** linter.

Fix is always available.

## [What it does](#what-it-does)

Checks for unnecessary dict, list, and set comprehension.

## [Why is this bad?](#why-is-this-bad)

It's unnecessary to use a dict/list/set comprehension to build a data structure if the
elements are unchanged. Wrap the iterable with `dict()`, `list()`, or `set()` instead.

## [Example](#example)

Use instead:

## [Known problems](#known-problems)

This rule may produce false positives for dictionary comprehensions that iterate over a mapping.
The dict constructor behaves differently depending on if it receives a sequence (e.g., a
list) or a mapping (e.g., a dict). When a comprehension iterates over the keys of a mapping,
replacing it with a `dict()` constructor call will give a different result.

For example:

When the comprehension iterates over a sequence, Ruff's suggested fix is correct. However, Ruff cannot consistently infer if the iterable type is a sequence or a mapping and cannot suggest the correct fix for mappings.

Additionally, rewriting comprehensions inside an object's `__len__` method may cause a
`RecursionError`, as collection constructors can call back into `__len__`.

## [Fix safety](#fix-safety)

This rule's fix is always marked as unsafe because of the known problems described above and because comments may be dropped when rewriting the comprehension.
