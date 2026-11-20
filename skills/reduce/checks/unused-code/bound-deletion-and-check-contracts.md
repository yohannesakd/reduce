# Bound deletion and check contracts beyond local callers

**Source:** GitHub Agentic Workflows, report dated 7 September 2026, and merged PR 58996. **Evidence:** public workflow, diff, and review record.

**Look for.** A deletion of code that a tool reports as unused, including exported wrappers, platform entry points, or tests of a helper that stays.

**Observed.** An automated cleanup removed five functions that Go's `deadcode` analyzer found. The workflow limits batches and checks references and platform-specific entry points.
Review comments challenged deletion of an exported compatibility wrapper and of tests that applied to a surviving helper. They also found stale comments.

**Inferred practice.** Keep deletion batches reviewable, and allow a no-change outcome when evidence is insufficient.
Move applicable tests to the surviving behavior instead of deleting them.

**Applies when.** Include public contracts, generated callers, platform entry points, and tests.

**Limits.** The PR reports build and vet checks, plus a formatting failure. Its merge does not prove that the compatibility objections were resolved.

**Reduce fit.** Exported wrappers are public interfaces. Apply the test ladder to tests of surviving behavior.
Keep the necessary coverage when tests move to the surviving helper. Remove a redundant test only when kept checks detect every material regression that it detects.

[Dated report](../../sources/web/github-github-com-gh-aw-blog-2026-09-07-agent-of-the-day.md). [PR and objections](../../sources/github/github-gh-aw-pull-58996.md). [Workflow at the merge revision](../../sources/github/github-gh-aw-github-workflows-dead-code-remover-md.md).
