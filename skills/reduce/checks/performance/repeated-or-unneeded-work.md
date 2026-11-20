# Repeated or unneeded work on the feature's paths

**Signal.** The feature reads, transfers, parses, or computes data, holds a cache, or runs steps one after another.

```ts
const rows = await db.select("*").from("orders");     // reads every column; callers use two
const total = rows.map(r => JSON.parse(r.meta)).length;
const names = rows.map(r => JSON.parse(r.meta).name);  // parses the same field again
```

**Decide with.** Trace every consumer before you reduce a data read or transfer.
Look for parsing, preparation, or computation that runs more than once where one operation can serve every user.
Compare data shapes and access patterns that remove transformations, lookups, or state.
Where steps run in series or apply partial updates without need, compare parallel or atomic orchestration. Keep ordering, failures, and resource limits.
Before you remove a cache, trace its freshness, invalidation, failures, and every user.
Compare complete representative operations, including time and internal work.

**Keeps it when.** A consumer reads the data, the order is required, or no measurement shows that a replacement is better. Keep a necessary cache or data structure without replacement evidence.
Keep performance-only findings separate. Do not expand into a codebase-wide performance audit.

**Sources.** These questions adapt [Dylan Garcia](../../sources/x/_dylanga-2117400205314421058.md) and [Jarred Sumner](../../sources/x/jarredsumner-2117037940031496252.md).
