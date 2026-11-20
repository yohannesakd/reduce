# Review one feature

You review one feature of a code change, codebase, or plan. Find what it can remove, prevent, reuse, or simplify while it keeps its required behavior.
This packet holds the feature's code, its map record, the design document, and the other features. A second file holds the checks. The packet names it.
Read the code in the target checkout. Do not change the target.

Write the reply yourself, from what you read. Do not write scripts or programs that create the reply, its lines, or its findings.

## How to apply the checks

A check is a signal check, a rule list, or a case:
- A **signal check** has a **Signal**, a **Decide with**, and a **Keeps it when**.
- A **rule list** gives the questions or rules for one kind of code, often for each rung.
- A **case** is a sourced real case. It has a **Look for** situation, an **Applies when** condition, and **Limits**.

1. **4.1** Read the feature's code, its map record, and the design document. The map record states what the feature is for, and holds the user's answers about it. The design document states the purpose of the target and its capabilities: do not search for them again. Find the capabilities that the feature carries, and the design findings, decisions, directions, and plan phases that name this feature. Class each map entry with [fixed behavior](../guides/fixed-behavior.md#fixed-behavior), from its consumers and its capability. Before you write a `reuse` or `simplify` finding, check whether another feature in the list already owns the same work.
2. **4.2** Read the checks file. It gives the checks that always apply in full: the refactoring check, and each language check that the feature's files match. Apply the language checks as [language rules](../checks/every-feature/refactoring.md#language-rules) says. For each other check, it gives the file and the pattern: decide whether the pattern appears in the feature, and read the check's file only when it does. When no pattern of a topic appears, give the topic one `absent` line in place of its checks. Take the checks in the order that the file lists them. For each check that you read in full, find every place in the feature where its **Signal**, rules, or **Look for** situation appears.
3. **4.3** At each place, apply the check's **Decide with** and **Keeps it when**, or for a case, its **Applies when** and **Limits**. Ask: what is the required behavior, which assumption led to the larger design, which responsibility or guarantee makes the smaller design possible, and which observation would disprove the reduction?
4. **4.4** At each place that the check flags, go down [the ladder](../guides/fixed-behavior.md#the-ladder) from `remove`. Stop at the first rung that the evidence supports, and write a finding for it. A place gets `keep` only when every rung fails with evidence.
5. **4.5** Then do an open review. The checks are not the limit of the review. Ask what you would remove, replace, or redesign if this feature were yours, and what no check covered: a part that no capability needs, a simpler approach to the same result, a wrong owner or data shape, or existing code that already does the work. Write a finding for each idea that the evidence supports: a finding does not need to match a check. Give `open-review` the last line of `## Checks`.
6. **4.6** For each finding, search for a consumer that the map did not find, and for an input or event order that would give a different result. Read [shorter code can change behavior](../evidence/shorter-code-can-change-behavior.md) before your first finding.
7. **4.7** When a design finding with the decision `autonomous` replaces a part of the feature, name that finding in the part's check lines, and do not write a second finding for it. Review the rest of the feature as the design finding would leave it. When the design finding has the decision `user`, review the part as it is now. Name the design finding in each finding that depends on it.
8. **4.8** When a finding needs a run to decide, read [execution checks](../evidence/execution-checks.md). Run checks only outside the target: copy the code that you run to a scratch folder first, because a run or an import inside the target writes files there. Otherwise, name the deciding check that you could not run.
9. **4.9** Give each finding an effect and a decision:
   - `parity`: it keeps every reachable `required` and `incidental` result.
   - `intent`: it removes or changes a result on purpose, including a contingent reduction. Name the entry IDs.
   - `autonomous`: it keeps every required and incidental result, stays within one owner, is easy to undo, and has source or scratch proof. An `intent` finding that applies a decision of the design document is also `autonomous`: a design finding with the decision `autonomous`, or the user's answer in its `## Decisions`. Cite the design finding. The same holds for the user's answer in the map record's `## Questions`: cite the question.
   - `user`: it has the effect `intent`, changes an interface, contract, stored data, security, operations, or a visible result, spans owners, or is costly or hard to undo when wrong.

## Reply

Write the reply in the record file that the packet names. Keep its three headings.

`## Checks` has one line for each check of the checks file, in its order, then one line for `open-review`. Name a check as the checks file names it, such as `guards-and-errors/guard-that-cannot-fail`. A topic without a pattern in the feature has one line for all its checks, such as `guards-and-errors`. Start every line at the margin: do not nest a check under its topic.

```text
- <topic> | absent | <path:line where you looked> | <what you looked at and why no pattern of the topic appears>
- <check> | absent | <path:line where you looked> | <what you looked at and why the pattern is absent>
- <check> | <finding IDs, such as X101, X102> | <path:line> | <what you looked at>
```

`## Findings` has one line for each finding, or `- none | <reason>`:

```text
- X<n> | <rung> | <effect> | <decision> | <entry IDs> | <path:line> | <finding and proposed change>
```

- Number the findings from the ID that the packet gives. One finding can be in the lines of several checks.
- The rung is `remove`, `prevent`, `reuse`, `simplify`, `keep`, or `unresolved`. The effect is `parity` or `intent`. The decision is `autonomous` or `user`.
- Entry IDs come from the map record. Separate several with `;`. Locations are `path:line` or `path:start-end` in the target.
- An `absent` line still names the place where you looked. A skipped check and a clean check must look different.

`## Leads` has one line for each lead, numbered from the ID that the packet gives. Leave it empty when you have no lead:

```text
- N<n> | <feature ID> | <lead> | <path:line>
```

## Rules for every check

- A signal or a case suggests a candidate, a place to examine. It is never evidence. Only the target's own trace, run, source, or search result decides the rung.
- A **Keeps it when** case rejects one rung, such as `remove` or `reuse`. Continue down the ladder: `simplify` can still apply.
- A count of callers, mocks, or uses alone does not decide a rung. One call site is the signal of step 1 of the refactoring check; its **Keeps it when** still applies.
- Code in a check is illustrative and normalized. It shows the shape of the pattern, not a verified implementation.
- In a case, **Observed** is what the source shows, and **Inferred practice** or **Inferred lesson** is a deduction. Line counts, costs, and model settings come from one report. They are not general rules or targets.
- A case's **Reduce fit** states how the case maps to [fixed behavior](../guides/fixed-behavior.md#fixed-behavior). Some cases changed behavior. The reduce skill keeps that behavior and reports it.
- A finding that would change an observable result is an `intent` finding. Removal of an `incidental` result is a contingent reduction.
- Most slop-detector rules find bugs or security problems, such as a mutable default argument or disabled TLS verification. They are not reductions.
- Record a suspected defect that is not a reduction in `## Leads`, as the packet says, and not as a finding. A line that breaks a language rule tagged `lead` is such a lead: name the rule ID. The report lists it apart from the reductions.
- A language rule is a rule, not a signal: each line that breaks it gets a finding or a lead, unless its **Unless** line or [the precedence](../checks/every-feature/refactoring.md#precedence) overrides it.
- Do not turn a signal into a ban. A catch that salvages data, a lazy import for start-up time, and a flag that serves as a kill switch each have a legitimate reason. Their value depends on the actual call path.
- Judge abstraction by concepts and reader effort, not by the number of files. Do not fragment what belongs together.
- For each finding, name what disappears: a branch, state variable, owner, dependency, interface, or optional feature. Explain why the required behavior survives.
- Reject reductions that only hide complexity, move it to another file, suppress failures, or remove necessary behavior.
