# Remove an unnecessary scheduling step instead of building an ordering subsystem

This is the strongest directly inspectable case. Both PRs fix the same bug, and both diffs are public.

**Source:** Hatchet co-founder Alexander Belanger, X, 19 October 2026, linking two August PRs. **Attribution:** explicit AI-versus-human comparison with both diffs available.

**Look for.** An async step, thread handoff, timer, or queue, or the ordering, retry, lock, or sequence state around one, added to fix a race or an order problem.

**Required behavior.** Preserve callback ordering in Hatchet's Python SDK so durable execution can replay branches consistently.

**Observed, AI approach.** Claude's PR 4734 adds a `satisfied_order` protocol field, propagates it through the dispatcher, and introduces per-invocation release sequences.
The listener holds completions, waits for gaps, drains them in order, and cleans up sequence state. The patch also adds diagnostics and tests.
It includes the local fix below, surrounded by the larger ordering design.

**Observed, human implementation.** Matt Kaye's PR 4733 removes the thread handoff during result extraction:

```diff
- return await asyncio.to_thread(self._extract_result, res)
+ return self._extract_result(res)
```

**Why the human code is better.** It removes an unnecessary scheduling point that can reorder branch continuation. It adds no protocol field, completion buffer, or release lifecycle.
The AI patch describes extraction as local, GIL-bound Pydantic validation. Its own explanation says the thread pool supplies no concurrency benefit here.

**Measured scope.** Claude's PR changes nine files, with +627/−291 lines. Matt's changes two files, with +3/−2 lines, including the changelog.
The production change in Matt's PR is one replaced line. Claude's totals include generated protocol bindings and tests, so they overstate handwritten size.

**Outcome.** Matt's PR merged on 19 August. Claude's closed without merging on 27 August.

**Other forms.** A `setTimeout(fn, 0)`, `requestAnimationFrame`, `queueMicrotask`, or `asyncio.to_thread` added to fix an order problem. A debounce, lock, or sequence number that hides a race. First ask whether the extra step causes the disorder.

**Inferred lesson.** Remove an unnecessary source of disorder before building machinery to restore order.
Check whether the operation needs concurrency before adding queues, tokens, and sequencing state.

**Applies when.** The work can safely stay synchronous: it is short, local, and does not block on I/O.

**Limits.** Blocking I/O or expensive computation can still require offloading and explicit coordination.
Matt initially expressed uncertainty about the diagnosis. The October report endorses the smaller fix, but no reproduction or test suite was independently run.
The two PRs use different base revisions.

**Reduce fit.** Treat the thread handoff as a candidate cause. The larger PR already includes its removal.
Check whether that fix keeps every inventory entry without the sequencing subsystem. If it does, the subsystem is a candidate `prevent` group.
Public protocol fields and emitted diagnostics are behavior. When the reduction cannot keep them, the affected units are `unresolved`.
Report them for the user's decision. Do not plan their removal.

[Original X comparison](https://x.com/abelanger5/status/2112250085044068801). [Reply linking both PRs](https://x.com/abelanger5/status/2112522897671508236).
[Human PR 4733](https://github.com/hatchet-dev/hatchet/pull/4733). [AI PR 4734](https://github.com/hatchet-dev/hatchet/pull/4734). [Pinned human diff](https://github.com/hatchet-dev/hatchet/commit/832536464a349982a373f3019f1ef6d291e4f153).
Human head `832536464a349982a373f3019f1ef6d291e4f153`, merge `9b2c6ad9377b1f78267e4ce815970e02af2edb6c`. Unmerged AI head `208bbd19597aac50e4f1987a11ed6025629fd67d`.
