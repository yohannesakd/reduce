# Ruff rule RUF006: asyncio-dangling-task

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Astral Software
- Date: 2023-02-11
- License: MIT
- Original location: https://docs.astral.sh/ruff/rules/asyncio-dangling-task/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# [asyncio-dangling-task (RUF006)](#asyncio-dangling-task-ruf006)

Added in [v0.0.247](https://github.com/astral-sh/ruff/releases/tag/v0.0.247) ·
Category: [pedantic](../?category=pedantic) ·
[Related issues](<https://github.com/astral-sh/ruff/issues?q=sort%3Aupdated-desc%20is%3Aissue%20is%3Aopen%20(%27asyncio-dangling-task%27%20OR%20RUF006)>) ·
[View source](https://github.com/astral-sh/ruff/blob/main/crates%2Fruff_linter%2Fsrc%2Frules%2Fruff%2Frules%2Fasyncio_dangling_task.rs#L70)

## [What it does](#what-it-does)

Checks for `asyncio.create_task` and `asyncio.ensure_future` calls
that do not store a reference to the returned result.

## [Why is this bad?](#why-is-this-bad)

Per the `asyncio` documentation, the event loop only retains a weak
reference to tasks. If the task returned by `asyncio.create_task` and
`asyncio.ensure_future` is not stored in a variable, or a collection,
or otherwise referenced, it may be garbage collected at any time. This
can lead to unexpected and inconsistent behavior, as your tasks may or
may not run to completion.

## [Example](#example)

Use instead:

Or, for Python 3.11 and later, use structured concurrency with
`asyncio.TaskGroup` when the tasks should be awaited as part of the current
operation:
