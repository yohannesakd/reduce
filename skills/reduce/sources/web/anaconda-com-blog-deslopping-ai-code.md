# Deslopping AI, Part 1: Code

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Andrew Huang
- Date: 2026-10-15
- Original location: https://www.anaconda.com/blog/deslopping-ai-code
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
In part one of this short blog series, I’ll walk through telltale signs of AI-generated code and how to improve it. It started with a question a colleague, Julian, asked: how do we keep AI slop out of our repos? It matters because you pay for every line an agent reads, in tokens, money, and time. Slop fills the agent’s context window before it starts on your change, and a large enough file won’t fit at all. And the slop snowballs, because the agent copies it into the next change.

As an exercise, try to spot as many signs of AI slop as you can in this snippet, which runs an async function with a timeout:

```
import asyncio
class QueryRunner:
    ...
# Seconds to wait before giving up on a query.
QUERY_TIMEOUT = 60
async def run_with_timeout(coro, timeout: float = QUERY_TIMEOUT):
    """Run a coroutine with a timeout."""
    try:
        return await asyncio.wait_for(coro, timeout)
    except TimeoutError:
        return None
def missing_table(error: Exception) -> str | None:
    """Return the name of the missing table from an error."""
    import re
    try:
        match = re.search(r"Table with name\s(\S+)", str(error))
        return match.group(1) if match else None
    except Exception:
        return None
```
How many did you find?

1. The comment and both docstrings repeat what the code already says.
2. `QUERY_TIMEOUT` is a constant used only once.
3. `QueryRunner` sits above the constant and both functions, and `import re` is inside a function.
4. The `try/except Exception` wraps code that can’t fail, and `return None` hides the timeout.

Those are the ones you can see. With the rest of the repo, there are two more:

1. The repo’s `utils.py` already has `with_timeout`.
2. The repo’s `sources/duckdb.py` already parses that error message with the same regex.

People make every one of these mistakes too, but an agent makes them faster than anyone can review line by line. Figure 1 marks each one, and the pitfalls below cover them in more detail.

## Common pitfalls

1. Comments that say what instead of why. In the snippet, the comment repeats the constant’s name and both docstrings repeat the function names. The code already says what it does, so **a comment should explain why**, like a constraint, a workaround, or the reason behind a number.
2. Constants and helpers with only one use. In the snippet, `QUERY_TIMEOUT` is a module-level constant used exactly once, as a default argument. Another module does the same with `EMPTY_COMPLETION`, a string used once. If something is only used once, **keep it inline**, like `timeout_seconds: float = 60`. Pull it out when a second caller needs it, or when the name explains something the value can’t.
3. Code in the wrong place. In the snippet, `QueryRunner` sits above the constant and both functions, and `import re` is inside a function for no reason. The fix is to **order each file as imports, constants, functions, then classes** so the agent finds existing imports and definitions before adding duplicates. An import inside a function to avoid a circular import can be fine, with a `# noqa` that names the cycle, but it can also mean the function belongs in another module.
4. Guards that can’t fail, and failures they hide. In the snippet, the `try/except Exception` wraps code that can’t fail, and `run_with_timeout` returns `None` on a timeout, so the caller can’t tell a timeout from an empty result. Elsewhere in the repo, `import numpy` sits inside a `try/except ImportError` even though numpy is required. For each guard, **ask how it could fail and what the caller sees when it does**.
5. Reinventing a helper that already exists. In the snippet, that’s `run_with_timeout`. The repo’s `with_timeout(coro, timeout_seconds=10, default_value=None)` already does the same job, and it has the same flaw, since it also returns `None` on a timeout by default. Pass `timeout_seconds=60` to keep the snippet’s limit, and **fix the one helper instead of keeping two**.
6. The same knowledge in two places. In the snippet, that’s the regex, which sources/duckdb.py already has. Two copies **leave the next agent without a single source of truth**, and they drift apart over time. Reuse that parser instead.
7. Fixing an error where it shows up instead of where it starts. When a traceback points at a caller, an agent tends to patch the caller, like adding `.strip()` wherever a helper’s output gets used instead of fixing the helper once. The worst version is **editing a test’s expected value so it matches the wrong output**.
8. Files too long to search. For example, a repo’s `utils.py` could be 2,209 lines with 65 top-level functions, and its large language model (LLM) module is 3,659 lines. An agent reads a file that size in pieces, so **a helper on line 1,551 of `utils.py`, where `with_timeout` sits, is easy to miss**, and a vague or inconsistent name makes it easier still. Split long modules by what they do, and reuse the names nearby code already uses (`font_size`, not `fontsize`).

## Why models code like this

A model working on a change sees the task, the files it opened, and the failing test, not the whole repo, and writing something new is cheaper than finding the existing one. One likely reason: during training, people rate the model’s answers, and code that looks careful gets rated higher. So the model learns to add the look of care, like try/except blocks, named constants, and docstrings, even where they do nothing. It also tends to write its own tests, which check that the code does what the model assumed rather than what you need.

## How to deslop code

Julian, the colleague who started the conversation, linked to [PostHog’s AGENTS.md](https://github.com/PostHog/posthog/blob/master/AGENTS.md), which pairs agent instructions with lint and continuous integration (CI) rules, proof the change works, and a human who owns the merge. Another colleague, Marius, argued that a company-wide standard would go stale within a few model releases, and that what lasts is project-specific checks like lints and architecture tests, with AGENTS.md kept to a short map of the repo. Marius had already seen agents ignore a new AGENTS.md, and an agent can skip an instruction but can’t merge past a failing programmatic check.

## Before you generate

Keep AGENTS.md short and make it a router, with a section that sends each kind of task to the file with the details, so the agent reads only what applies. The [contributing-to-holoviz skill](https://holoviz-dev.github.io/holoviz-skills/contributing-to-holoviz/) works this way. A router loads on every task, and agents may stop reading partway through a long file. It still goes stale when files move, so add a check that every path it lists exists, and update it in the same change that moves the code. [Matt Pocock’s guide to AGENTS.md](https://www.aihero.dev/a-complete-guide-to-agents-md) is a good place to start.

A starter might look like this. Rules that a lint already enforces shrink to one line, and the rest carry a reason, because, in my experience, models follow reasoning better than bare rules:

```
# AGENTS.md
## Where things live
- Shared helpers live in `src/pkg/utils/`, one module per topic (`timeouts.py`, `retries.py`, `errors.py`). Search there before writing a new one.
- Code that parses database error messages belongs in `src/pkg/sources/`, next to the code that talks to each database.
## Rules
- Run `ruff check` and `pre-commit run` before finishing. They enforce import placement, blind excepts, and, with a small script, file order. Fix what they flag, and if a flag is wrong, add a `# noqa` that says why.
- Keep modules focused and name functions for the job they do, since agents find code by searching for it.
## Tasks
- Reviewing a change: read `docs/agents/review.md`.
- Writing tests: read `docs/agents/testing.md`.
```
Give the agent a way to search by meaning, like the codebase index in [Kilo by Anaconda](https://kilo.ai/docs/customize/context/codebase-indexing) or [Cursor](https://cursor.com/blog/secure-codebase-indexing), so it can look for “a helper that runs a coroutine with a timeout” instead of guessing the name to grep for.

Ask for the root cause rather than a passing test. Keep each pull request (PR) to one change that a reviewer can hold in their head and roll back on its own. One change I reviewed bundled eight separate fixes into one commit, so there was no clean way to revert one without the others.

## Checks and proof

If the rule names below mean nothing to you, ask your agent to turn these checks on and fix what they flag.

Start with the lints you already have. That repo’s Ruff config ignores `PLC0415`, the rule that flags imports inside functions, and doesn’t enable `BLE001`, which flags `except Exception`. So two of the problems in the opening snippet have a rule that’s turned off. Turning them on takes one line, plus removing `PLC0415` from `ignore` if it’s there:

```
[tool.ruff.lint]
extend-select = ["BLE001", "PLC0415"]  # blind except, import inside a function
```
Ruff has no rule for constants defined after the first function or class. The cleanup skill below checks file order, or a short script can check it from pre-commit.

Treat every `# noqa` as a review question too. One PR silenced `B904`, the rule that asks for `raise ... from err`, with a comment explaining that the retry helper would otherwise follow the chain back to the raw database error and show that to the model. That’s a fair why-comment, but the workaround it describes is the real problem, a retry helper that reads the wrong error. Even as a stopgap, `raise ... from None` satisfies the rule and cuts the chain without a # noqa.

A rule like “`utils` must not import the UI modules” can be an [import-linter](https://import-linter.readthedocs.io/) contract, which flags those imports whether or not they’re deferred into a function:

```
[tool.importlinter]
root_package = "pkg"
[[tool.importlinter.contracts]]
name = "utils doesn't import the UI modules"
type = "forbidden"
source_modules = ["pkg.utils"]
forbidden_modules = ["pkg.editors", "pkg.controls"]
```
A new test should fail on the main branch before the fix, and proof that a change works has to show the changed code ran. Ask for a runnable “how to test” snippet that ends with what you should see before and after the fix. For anything visible, ask for before-and-after screenshots, as the [HoloViz PR description guide](https://holoviz-dev.github.io/holoviz-skills/contributing-to-holoviz/pr-description/) does, because they’re hard to produce without running the change.

## After you generate

Delete first: dead guards, single-use constants whose name adds nothing, and wrappers that only reword an error.

Then review against the whole repo. A prompt like this one works:

```
Review this change against the whole repo, not just the diff.
- For each new function, search the repo for one that already does the same job.
- For each comment, check that what it claims is true.
- For each try/except, say how the code inside could fail. If it can't, remove the except.
- List the constants and helpers that are used only once.
- For each fix, say whether it's where the problem starts or where it showed up.
```
The [cleanup skill in holoviz-skills](https://holoviz-dev.github.io/holoviz-skills/contributing-to-holoviz/cleanup/) covers several of these checks, like file order, comments that restate the code, and fixes that belong somewhere else. Install it by running `pip install holoviz-skills`, then holoviz-skills install, which detects Kilo, Claude Code, Cursor, and other tools. Then ask your agent to review the branch with the contributing-to-holoviz skill, which routes review requests to the cleanup checklist. The checklist works on any Python repo, not only HoloViz.

Disclosing which tool and model wrote a change tells the reviewer where to look harder, but a person still owns the merge.

When the same finding keeps coming up, turn it into a rule, a lint, or a skill entry. Then check with evals that each rule still earns its place after the next model release.

## What not to do

Don’t overcorrect. A mistake that only happened once doesn’t need a rule, and a growing list of bans makes AGENTS.md longer, which makes the agent more likely to stop reading partway. The same goes for lints: enable a rule once its finding recurs.

And if a PR is slop from top to bottom, split it or start over rather than cleaning it up, same as with prose. A rough test is whether fixing the review comments would touch most of the diff. If so, a smaller, clearer request is faster than a cleanup pass.

## Takeaways

- Clean up the slop before it spreads. You pay for every line the agent reads, and the agent copies what it finds into the next change.
- Review against the whole repo, not just the diff. The duplicate helper and the duplicate regex in the snippet don’t show up in the diff.
- Put your rules in checks where you can, not in written instructions. An agent might skip an instruction but cannot bypass a failing programmatic check.
- Make the repo easy to search, with small files, clear names, and an AGENTS.md that says where things live, so the agent finds existing helpers instead of rewriting them.
- Keep each change small, with proof that it ran.

Got any other ideas? [Post them on the forum](https://forum.anaconda.com/).

Want some tips for deslopping your AI prose and pull requests? [Check out part 2 of this blog series](https://www.anaconda.com/blog/deslopping-ai-prose).
