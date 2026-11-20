# Close

Act on the report when implementation is requested, then clean up.

1. **6.1** When implementation is requested, read [implementation handoff](../guides/workflow.md#implementation-handoff). Apply the `autonomous` findings. Apply `user` findings only after the user decides. Make each change of code in the order of the five steps of the [refactoring check](../checks/every-feature/refactoring.md): "1. Inline every function that is only used once and tighten former call sites. 2. Eliminate defensive checks. Replace complex error handling with plain asserts. 3. Reduce deeply nested code by merging and inverting conditionals. 4. Co-optimize multi-consumer functions with their callers. 5. Apply syntax and style guide as a final pass." Keep its objective: "Preserve existing determinism." Then apply the language checks that `## Rules for the code` lists. Then run the project's formatter. Otherwise, record that implementation was not requested.
2. **6.2** Remove the worktrees, scratch checkouts, containers, and other resources that this run created. Record what you removed, or that you created none.

Do not change `review.md` or a submitted record. Record a needed correction in this step's record instead.
In the final reply, summarize the verdict, the main findings, the decisions for the user, the material limits, and the path of `review.md`.
