# Code-change phases

Apply this section when a code-change review produces a plan with phases.
Order phases so each leaves the code working and verifiable.
Put inseparable units in one phase. Otherwise, order phases by `remove`, each `prevent` fix and affected units, `reuse`, then `simplify`.
Perform remaining restructuring in the final `simplify` phase.
Plan directly toward a replacement design. Skip a phase with no units.

- Keep a structural target even when its behavior matches the base. Dropping the whole target needs the user's decision.
- List commits that the default branch already contains separately from code that the target duplicates.
- When the plan drops commits with a rebase, name the new base, and verify the result against the recorded target state.
- Each phase's `Verify` names the preserved inventory entries and links their checks.
- For an example-derived change, link its local case and the review record explaining applicability, limits, and preserved behavior.
- Make a test change that replaces another test in the same phase as the removal, or earlier.
- List `unresolved` units under Risks with the evidence that decides them.

Write any requested plan to the specified path, or outside the repository. Apply the [plan review guidance](workflow.md#plan-review).
For authorized implementation, follow the [implementation handoff](workflow.md#implementation-handoff).

