# Express an upstream guarantee in the input type

**Source:** Peter Steinberger, OpenClaw PR 161659, 30 September 2026. **Attribution:** human-directed cleanup; original generation history is not established.

**Look for.** A function checks or rejects input states that every caller already excludes, so a narrower input type can carry the guarantee.

**Required behavior.** Convert a finished worker receipt into a process result. Preserve output, errors, cancellation, and termination fields.

**Observed, expanded approach.** Accept a receipt type that includes unfinished states. Check four terminal states before returning the result. Throw otherwise.

**Observed, human-directed implementation.** Accept the narrower terminal receipt type and return the same result mapping directly. Normalized:

```ts
// Before: the mapper repeats a guarantee provided by its caller.
function mapReceipt(receipt: AnyReceipt): ProcessResult {
  if (isTerminal(receipt)) return projectResult(receipt);
  throw new Error('Receipt is unfinished');
}

// After: the input contract expresses the guarantee.
function mapReceipt(receipt: FinishedReceipt): ProcessResult {
  return projectResult(receipt);
}
```

**Why it works.** The PR records one production caller. Its launcher validates receipts and returns only terminal results, including during cancellation.

**Inferred lesson.** Represent what the caller actually guarantees, not every state the larger system can express. Validate at the boundary, then operate on validated values.

**Applies when.** Every entry point that reaches the function passes only values that meet the narrower type.

**Limits.** The author reports 78 passing tests across the two-file cleanup. The PR closed without merging and documented a separate CI blocker.
Keep runtime validation where untrusted or unfinished values can enter.

**Reduce fit.** `prevent` with a type. The removed throw is unreachable only when the guarantee holds across all entry points.

[PR and verification](https://github.com/openclaw/openclaw/pull/161659). [Pinned mapper change](https://github.com/openclaw/openclaw/compare/0a0a2e0489026b2e73d139383e7b60515fcaf7f3...7745effd839d26863d8480c1888715841523c808).
