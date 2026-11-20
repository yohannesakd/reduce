# A hunk that does not serve the problem

**Signal.** Several unrelated fixes in one commit. A refactor inside a bug fix. An edit to code that was already correct. A removed comment or guard that the author did not understand.

Trace each hunk to the problem:

| Hunk | Inventory entry | Result |
| --- | --- | --- |
| `billing/tax.py`: round half-up | B1 | Serves the problem. |
| `billing/tax.py`: rename `calc` to `compute` | none | Report. Not part of the problem. |
| `ui/Header.tsx`: remove a `// keep: legacy layout` comment | none | Restore. The comment was a constraint ([Chesterton check](../../evidence/tools-and-evidence.md#history)). |

**Decide with.** A hunk with no entry is an unrelated change. Its removal is a contingent reduction. Record it with the contingent reductions of the report.
An agent that edits code it does not understand also deletes guards. Run the history check on each removed line before you accept it.

**Keeps it when.** The hunk traces to an inventory entry, or the history check shows that a removed line was a constraint. Then restore or keep it.

**Sources.** [Karpathy](../../sources/x/karpathy-2015883857489522876.md), [Anaconda](../../sources/web/anaconda-com-blog-deslopping-ai-code.md), [Agentic Refactoring](../../sources/papers/arxiv-2511.04824.md), [Coding Agents Don't Know When to Act](../../sources/papers/arxiv-2605.07769.md).
