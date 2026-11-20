# Ruff rule UP008: super-call-with-parameters

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/super-call-with-parameters/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [super-call-with-parameters (UP008)](#super-call-with-parameters-up008)

Added in [v0.0.155](https://github.com/astral-sh/ruff/releases/tag/v0.0.155) ·
Category: [style](../?category=style) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27super-call-with-parameters%27%20OR%20UP008)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fpyupgrade%2Frules%2Fsuper_call_with_parameters.rs#L55)

Derived from the **[pyupgrade](../#pyupgrade-up)** linter.

Fix is sometimes available.

## [What it does](#what-it-does)

Checks for `super` calls that pass redundant arguments.

## [Why is this bad?](#why-is-this-bad)

In Python 3, `super` can be invoked without any arguments when: (1) the
first argument is `__class__`, and (2) the second argument is equivalent to
the first argument of the enclosing method.

When possible, omit the arguments to `super` to make the code more concise
and maintainable.

## [Example](#example)

Use instead:

## [Fix safety](#fix-safety)

This rule's fix is marked as unsafe because removing the arguments from a call may delete comments that are attached to the arguments.
