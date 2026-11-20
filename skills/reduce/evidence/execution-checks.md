# Execution checks

Read this file completely when execution is needed to decide a claim.

### Baseline and gates

For scratch reductions, apply these gates before and after each phase:

1. Record affected tests, inventory outputs, typecheck/lint diagnostics, and any claimed branch/dependency counts.
2. Fix clocks/seeds. Normalize generated IDs/timestamps; mark other varying outputs untested.
3. Record every baseline failure/diagnostic. Do not fix it in the reduction or use failing checks as proof.
4. Require passing tests to remain passing, controlled outputs to match, and no new diagnostics.
5. Rerun red checks and compare each failure. New failures fail the gate; missing checks remain gaps.
6. For consequential remove/prevent/reuse/group claims, link inventory entries to a disproof check.
   Omit the equivalence card when one source trace settles the claim:

```text
Claim:           inline QUERY_TIMEOUT, a constant with one user (constants.py:12, query.py:8)
Entries kept:    B3 default timeout 30 s, B4 timeout error text
Old path:        run_query(sql) -> timeout=QUERY_TIMEOUT (30)
New path:        run_query(sql) -> timeout=30
Inputs compared: 12 recorded queries, one runs longer than 30 s
Result:          outputs and error text identical (hashes match)
Disproved by:    any importer of QUERY_TIMEOUT (git grep finds none)
Status:          confirmed
```

Derive expected values independently of changed code. Snapshot-only comparisons retain baseline defects; label that evidence and its limits.
For consequential running-system claims, plan randomized old/new comparison on identical real inputs. Do not execute against production during review.
Compare concepts, branches, layers, dependencies, locality, reader burden, and additions' costs. Moving/reformatting alone proves no improvement.
Record contradictions in Proof; do not propose contradicted changes again.

Sources: [isomorphic simplify listing](../sources/x/doodlestein-2047808489838329993.md), [Debloating post](../sources/web/dev-to-maximsaplin-debloating-the-ai-grown-codebase-2om.md), [Scientist.NET](../sources/web/docsearch-algolia-com-mcp-docs-repo-scientistproject-scientist-net.md), [Tesbo](../sources/web/tesbo-io-insights-roadmap-reviewing-ai-written-tests.md).

### Run checks

Choose the narrowest real check covering affected entries. Trace uncovered behavior or add scratch comparisons.
For keep claims requiring execution, shrink/remove the unit and confirm assertions observe its required effects.
Refute keep only when source and checks establish unnecessary behavior; otherwise add proof or leave unresolved.
Plant focused broken behavior to test protection. Count failures caused by that defect, not unrelated setup failures.
Reverting a production change tests protection only when it breaks the named behavior.
Where practical, compare old/new results on identical inputs; use generated inputs for pure logic.
For example-derived changes, check all entries and apply [Shorter code can change behavior](shorter-code-can-change-behavior.md).

### Strongest check

| Claim | Check when execution is required |
|---|---|
| Application behavior | Project checks at the affected boundary |
| Visible/interactive behavior | Baseline/candidate builds and interactions |
| Concurrent/event-ordered unreachability | Reconcile existing formal checks; use suitable scratch formal checks when ordinary checks cannot decide |
| Cache/batch/query/loop/concurrency cost | Compare complete operations on representative workloads; record measurement limits |

