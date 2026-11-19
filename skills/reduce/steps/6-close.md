# Close

Act on the report when implementation is requested, then clean up.

1. **6.1** When implementation is requested, read [implementation handoff](../guides/workflow.md#implementation-handoff). Apply the `autonomous` findings. Apply `user` findings only after the user decides. Make each change of code in the order of the five steps of the [refactoring check](../checks/every-feature/refactoring.md). Then apply the language checks that `## Rules for the code` lists. Then run the project's formatter. Otherwise, record that implementation was not requested.
2. **6.2** Remove the worktrees, scratch checkouts, containers, and other resources that this run created. Record what you removed, or that you created none.

Do not change `review.md` or a submitted record. Record a needed correction in this step's record instead.
In the final reply, summarize the verdict, the main findings, the decisions for the user, the material limits, and the path of `review.md`.
