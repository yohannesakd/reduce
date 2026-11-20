# hatchet-dev/hatchet pull request #4733: fix(python): callback ordering bug

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: mrkaye97
- Date: 2026-08-18
- Original location: https://github.com/hatchet-dev/hatchet/pull/4733
- Copied: 2026-11-20, from the pull request, its comments, its reviews, and its diff, from the GitHub API

## Text
# Description

It appears that `asyncio.to_thread` (the threading portion of it) is causing event loop weirdness which results in callbacks being returned in inconsistent orders. I'm only 90% sure this is a real fix, but wanted to try shipping it before doing the much more complicated thing

## Type of change

<!-- Please delete options that are not relevant. -->

- [x] Bug fix (non-breaking change which fixes an issue)


## What's Changed

- [ ] Add a list of tasks or features here...

## Checklist

<!-- Check all that apply. -->

Changes have been:

- [x] Tested (unit, integration, or manually with steps specified)
- [x] Linted and formatted
- [x] Documented (where applicable)
- [x] Added to CHANGELOG (where applicable) -- see [Keep a Changelog](https://keepachangelog.com/en/1.0.0/)

<!-- Optional: How are the proposed changes tested? -->
<!-- ## Testing

-->


<!-- Optional: Include additional material to supplement your changes (e.g screenshots for frontend changes) -->
<!-- ## Related

-->

---

<details id="ai-disclosure">
<summary><b>🤖 AI Disclosure</b></summary>

<!-- In accordance with Hatchet's AI_POLICY.md, LLM usage must be explicitly disclosed. -->

- [x] _I acknowledge that an LLM was used in the creation of this Pull Request, in accordance with Hatchet's [AI_POLICY.md](./AI_POLICY.md)._

<!-- Please specify the tooling/model and the extent to which it was used. -->

- **Details**: Used Claude Code to initially attempt to diagnose the problem, which led me to this, and then I removed everything Claude wrote

</details>


## Change

3 commits, 2 files, +3 -2. Merged: 2026-08-19T00:44:17Z.

## Comment by vercel[bot], 2026-08-18

[vc]: #bdzZo3ju97uRiUkhYXUcFfR6inek41+5qHHPpaR/AL0=:eyJpc01vbm9yZXBvIjp0cnVlLCJ0eXBlIjoiZ2l0aHViIiwicHJvamVjdHMiOlt7Im5hbWUiOiJoYXRjaGV0LWRvY3MiLCJwcm9qZWN0SWQiOiJwcmpfZU52dEJQZjdiZGJMNW44c3FUZlVhd2VHQTB5NCIsInYwIjpmYWxzZSwibGl2ZUZlZWRiYWNrIjp7InJlc29sdmVkIjowLCJ1bnJlc29sdmVkIjowLCJ0b3RhbCI6MCwibGluayI6ImhhdGNoZXQtZG9jcy1naXQtbWstZml4LWNhbGxiYWNrLW9yZGVyaW5nLWJ1Zy1oYXRjaGV0LWI2YzA2NTJjLnZlcmNlbC5hcHAifSwiaW5zcGVjdG9yVXJsIjoiaHR0cHM6Ly92ZXJjZWwuY29tL2hhdGNoZXQtYjZjMDY1MmMvaGF0Y2hldC1kb2NzLzdjOTFNbnI3dkpxWk1XZ3hycE5mTHVqc1RtdUUiLCJwcmV2aWV3VXJsIjoiaGF0Y2hldC1kb2NzLWdpdC1tay1maXgtY2FsbGJhY2stb3JkZXJpbmctYnVnLWhhdGNoZXQtYjZjMDY1MmMudmVyY2VsLmFwcCIsIm5leHRDb21taXRTdGF0dXMiOiJERVBMT1lFRCIsInJvb3REaXJlY3RvcnkiOiJmcm9udGVuZC9kb2NzIn1dLCJyZXF1ZXN0UmV2aWV3VXJsIjoiaHR0cHM6Ly92ZXJjZWwuY29tL3ZlcmNlbC1hZ2VudC9yZXF1ZXN0LXJldmlldz9vd25lcj1oYXRjaGV0LWRldiZyZXBvPWhhdGNoZXQmcHI9NDczMyJ9
The latest updates on your projects. Learn more about [Vercel for GitHub](https://vercel.link/github-learn-more).

| Project | Deployment | Actions | Updated (UTC) |
| :--- | :----- | :------ | :------ |
| <a href="https://vercel.com/hatchet-b6c0652c/hatchet-docs"><sup><img src="https://vercel.com/api/www/avatar?projectId=prj_eNvtBPf7bdbL5n8sqTfUaweGA0y4&teamId=team_dk7kTBZz550S8zPkMtKPdF2u&s=32" width="16" height="16" align="middle" alt="" /></sup></a> [hatchet-docs](https://vercel.com/hatchet-b6c0652c/hatchet-docs) | ![Ready](https://vercel.com/static/status/ready.svg) [Ready](https://vercel.com/hatchet-b6c0652c/hatchet-docs/7c91Mnr7vJqZMWgxrpNfLujsTmuE) | [Preview](https://hatchet-docs-git-mk-fix-callback-ordering-bug-hatchet-b6c0652c.vercel.app) | Aug 19, 2026 12:46am |

<a href="https://vercel.com/vercel-agent/request-review?owner=hatchet-dev&repo=hatchet&pr=4733" rel="noreferrer"><picture><source media="(prefers-color-scheme: dark)" srcset="https://agents-vade-review.vercel.sh/request-review-dark.svg"><source media="(prefers-color-scheme: light)" srcset="https://agents-vade-review.vercel.sh/request-review-light.svg"><img src="https://agents-vade-review.vercel.sh/request-review-light.svg" alt="Request Review"></picture></a>



## Comment by greptile-apps[bot], 2026-08-18

<h3>Greptile Summary</h3>

The PR changes asynchronous standalone workflow result extraction to run directly on the event-loop thread, avoiding callback reordering caused by `asyncio.to_thread`.
- Calls `_extract_result` directly after an asynchronous workflow run.
- Records the callback-ordering fix in the Python SDK changelog and updates the 1.37.3 release date.

<h3>Confidence Score: 5/5</h3>

The PR appears safe to merge.

No blocking failure remains.

<!-- greptile_other_comments_section -->

<sub>Reviews (3): Last reviewed commit: ["Merge branch &#39;mk/fix-rest-client-ssl-cer..."](https://github.com/hatchet-dev/hatchet/commit/832536464a349982a373f3019f1ef6d291e4f153) | [Re-trigger Greptile](https://app.greptile.com/api/retrigger?id=54533562)</sub>

## Diff

````diff
diff --git a/sdks/python/CHANGELOG.md b/sdks/python/CHANGELOG.md
index c914287dcf..eb462b92ef 100644
--- a/sdks/python/CHANGELOG.md
+++ b/sdks/python/CHANGELOG.md
@@ -5,12 +5,13 @@ All notable changes to Hatchet's Python SDK will be documented in this changelog
 The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
 and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).
 
-## [1.37.3] - 2026-08-17
+## [1.37.3] - 2026-08-19
 
 ### Fixed
 
 - Correctly passes TLS config through to the API client
 - Passes the configured TLS server name (SNI) through to the REST client
+- Removes a call to `asyncio.to_thread` that was causing durable callback ordering to end up out-of-ordering, causing non-determinism errors.
 
 ## [1.37.2] - 2026-08-12
 
diff --git a/sdks/python/hatchet_sdk/runnables/workflow.py b/sdks/python/hatchet_sdk/runnables/workflow.py
index 83a3446f36..2b4de9bab7 100644
--- a/sdks/python/hatchet_sdk/runnables/workflow.py
+++ b/sdks/python/hatchet_sdk/runnables/workflow.py
@@ -2178,7 +2178,7 @@ async def aio_run(
             desired_worker_id=desired_worker_id,
             desired_worker_labels=desired_worker_labels,
         )
-        return await asyncio.to_thread(self._extract_result, res)
+        return self._extract_result(res)
 
     def run_no_wait(
         self,

````
