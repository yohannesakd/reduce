# Ruff rule RUF008: mutable-dataclass-default

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/mutable-dataclass-default/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [mutable-dataclass-default (RUF008)](#mutable-dataclass-default-ruf008)

Added in [v0.0.262](https://github.com/astral-sh/ruff/releases/tag/v0.0.262) ·
Category: [suspicious](../?category=suspicious) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27mutable-dataclass-default%27%20OR%20RUF008)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fruff%2Frules%2Fmutable_dataclass_default.rs#L63)

## [What it does](#what-it-does)

Checks for mutable default values in dataclass attributes.

## [Why is this bad?](#why-is-this-bad)

Mutable default values share state across all instances of the dataclass. This can lead to bugs when the attributes are changed in one instance, as those changes will unexpectedly affect all other instances.

Instead of sharing mutable defaults, use the `field(default_factory=...)`
pattern.

If the default value is intended to be mutable, it must be annotated with
`typing.ClassVar`; otherwise, a `ValueError` will be raised.

In [preview](https://docs.astral.sh/ruff/preview/) this rule also detects mutable defaults passed via the `default` keyword
argument in `field()` (for stdlib dataclasses), `attrs.field()`, `attr.ib()`,
and `attr.attrib()` calls.

## [Example](#example)

Use instead:

Or:
