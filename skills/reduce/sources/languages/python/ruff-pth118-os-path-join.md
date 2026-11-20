# Ruff rule PTH118: os-path-join

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- Date: 2018-12-01
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/os-path-join/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [os-path-join (PTH118)](#os-path-join-pth118)

Added in [v0.0.231](https://github.com/astral-sh/ruff/releases/tag/v0.0.231) ·
Category: [pedantic](../?category=pedantic) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27os-path-join%27%20OR%20PTH118)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fflake8_use_pathlib%2Fviolations.rs#L41)

Derived from the **[flake8-use-pathlib](../#flake8-use-pathlib-pth)** linter.

## [What it does](#what-it-does)

Checks for uses of `os.path.join`.

## [Why is this bad?](#why-is-this-bad)

`pathlib` offers a high-level API for path manipulation, as compared to
the lower-level API offered by `os.path`. When possible, using `Path` object
methods such as `Path.joinpath()` or the `/` operator can improve
readability over the `os.path` module's counterparts (e.g., `os.path.join()`).

## [Examples](#examples)

Use instead:

## [Known issues](#known-issues)

While using `pathlib` can improve the readability and type safety of your code,
it can be less performant than the lower-level alternatives that work directly with strings,
especially on older versions of Python.
