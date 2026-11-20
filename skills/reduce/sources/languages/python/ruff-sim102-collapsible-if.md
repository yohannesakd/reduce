# Ruff rule SIM102: collapsible-if

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/collapsible-if/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [collapsible-if (SIM102)](#collapsible-if-sim102)

Added in [v0.0.211](https://github.com/astral-sh/ruff/releases/tag/v0.0.211) ·
Category: [complexity](../?category=complexity) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27collapsible-if%27%20OR%20SIM102)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fflake8_simplify%2Frules%2Fcollapsible_if.rs#L66)

Derived from the **[flake8-simplify](../#flake8-simplify-sim)** linter.

Fix is sometimes available.

## [What it does](#what-it-does)

Checks for nested `if` statements that can be collapsed into a single `if`
statement.

## [Why is this bad?](#why-is-this-bad)

Nesting `if` statements leads to deeper indentation and makes code harder to
read. Instead, combine the conditions into a single `if` statement with an
`and` operator.

## [Example](#example)

Use instead:

## [Preview and Fix Safety](#preview-and-fix-safety)

When [preview](https://docs.astral.sh/ruff/preview/) is enabled, the fix for this rule is considered
as safe. When [preview](https://docs.astral.sh/ruff/preview/) is not enabled, the fix is always
considered unsafe.

## [Options](#options)

The rule will consult these two settings when deciding if a fix can be provided:

Lines that would exceed the configured line length will not be fixed automatically.
