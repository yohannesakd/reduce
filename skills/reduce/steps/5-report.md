# Report

Combine the check outputs into one review for the person who decides what to change.

Write the report in `review.md`, below the driver's tables. This step's record holds only the status of each item below, `## Whole-target findings`, `## Leads`, and, for the plan playbook, `## Dispositions`.

The driver writes two tables in `review.md`: one row for each feature and check, with its findings or `none`, and one row for each finding of the design and check steps. It writes them again when you submit, so do not edit them or copy their rows.

1. **5.1** Below the table, write the verdict: complete, partial, or blocked. Name the material coverage gaps near the verdict.
2. **5.2** Link the design document, `design.md`, near the verdict. Compare each design finding with the check results. Record where the checks confirm, change, or contradict it. Then apply [the ladder](../guides/fixed-behavior.md#the-ladder) to the whole target for what only the check results show: a shared owner, producer, schema, configuration, or duplicated concept whose change removes the need for parts or findings in several features. Record each such finding in `## Whole-target findings` in the record, numbered from W1, with entry IDs written as `F<n>:<entry ID>` or as the IDs of the findings that it replaces. Otherwise, write `- none | <reason>`.
3. **5.3** Read the `## Leads` rows of `design.md` and of each check record. Each lead is a possible reduction that a subagent saw outside its task, or a suspected defect. Trace each lead in the code, unless a finding already covers it. In `## Leads`, give each lead one row that starts with its ID. Its result is the ID of a new whole-target finding, the ID of a finding that already covers it, or `rejected` with the reason. A suspected defect that is not a reduction gets `rejected`, and a line in the suspected defects of 5.7. A lead of a rule tagged `lead` gets `rejected` with the reason `rule lead`, and a line in the rule leads of 5.7.
4. **5.4** Merge findings that name the same place or the same cause. Merge the findings of one language rule across features into one finding with every location. Record the merged IDs. When a change to a shared owner affects another feature, recheck that feature's findings and record the result.
5. **5.5** List the parity findings that matter most, ordered by structural benefit, confidence, risk, and dependencies. For each: location, problem and cause, proposed change, benefit, preserved entry IDs, deciding evidence, and tradeoffs.
6. **5.6** List the intent findings separately, ordered by benefit and risk. For each: the entry IDs that it removes or changes, the capabilities of `design.md` that they serve, the searches that support it, and what fails if the judgment is wrong.
7. **5.7** Add these sections when they apply: the rule leads, which are the lines that break a rule tagged `lead`, grouped by rule ID, with their locations; contingent reductions with their blocking decision or evidence; `unresolved` findings with their missing evidence and deciding check; suspected defects from the scope step's tool results and from the leads, with their baseline attribution.
8. **5.8** Record the coverage: unmapped files, uninspected areas, the checks that ran, their results, and the claims that only source supports.
9. **5.9** End with `## Decisions for you` when a finding has the decision `user`, the design document has an `unanswered` decision, or a map record has an `unanswered` question that no decision covers. For each: its ID, one question, the options and their effects, your recommendation, and the check that would settle it.

Name each whole-target finding. Refer to other findings by their IDs, and link detailed records instead of repeating them.
Create a plan only when requested or required. For code-change phases, read [code phases](../guides/code-phases.md). For existing plans, use [plan review](../guides/workflow.md#plan-review).

For the plan playbook, also write the reduced plan copies that [plan rules](../guides/plan-rules.md#reduced-plan) describe, and give each finding its row in `## Dispositions`.
