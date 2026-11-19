# Quick review

Review a small target in one pass: its results, its intent, a design from scratch, and the checks. Do the work yourself, without subagents. The record is the report for the user.

Start skeptical: the target probably does not need a capability until a source or a consumer outside the target shows the need.

Take every reference into account, but not in depth: look over each one, and decide whether it applies to this target. Study a reference only when it applies. Look over these design references before 2.7:

| Design reference | Use |
|---|---|
| [design-red-flags](../design/design-red-flags.md) | Red flags across features |
| [codebase-design](../design/codebase-design.md) | Module, interface, seam, depth, and the deletion test |
| [redesign-from-first-principles](../design/redesign-from-first-principles.md) | A requirement added to an existing design |
| [exhaust-the-design-space](../design/exhaust-the-design-space.md) | Several plausible designs |
| [attack-the-premise](../design/attack-the-premise.md) | Repeated fixes at one boundary |
| [refactoring](../checks/every-feature/refactoring.md) | The refactoring algorithm, the general style, and the precedence between rules |

1. **2.1** Read the intent sources: the user's request, the ticket, the PR body, commit messages, and the documents that the target adds or changes. Give each source one authority:
   - `user`: the user's request or answer.
   - `external`: a ticket, decision record, accepted plan, existing contract, or consumer outside the target. A PR body, ticket, issue, or commit message is `external` for the goals that it states, and `target` for the implementation details that it only describes.
   - `target`: a document, test, or comment that the target itself adds or owns. It describes the target. It does not show that the target is needed.
   - `inferred`: a deduction from the code. Label it as an inference.
2. **2.2** In `## Intent`, state the core intent in one paragraph: the problem that the target solves, for whom, and the observable result that shows that it works. Start from the goals that the scope record quotes. Then name each source with its authority.
3. **2.3** Trace each feature below from its entry points, including unchanged callers. You read the code in the scope step: read again only what the trace needs. In `## Inventory`, give each result one entry: what a caller, user, operator, test, or other program can observe. A branch, guard, default, fallback, or retry gets no entry of its own; name it in the entry of the result that it produces. Name each consumer of the result and what it does with it: shows, sends, stores, or decides something, or discards it. Give each entry a class from [fixed behavior](../guides/fixed-behavior.md#fixed-behavior). Before you choose `incidental` or `unknown`, search tests, callers, configuration, and documentation, and cite the search.
4. **2.4** In `## Capabilities`, list what a user, caller, operator, or other program can do or observe because of the target. Name what it gives, not the code that gives it. List the entries that serve it. An entry that serves no capability is an orphan result. Give each capability one need:
   - `core`: the core intent fails without it.
   - `supporting`: a `user` or `external` source needs it.
   - `questioned`: only `target` or `inferred` sources support it, or no user, caller, or operator would notice its removal.
5. **2.5** For each `questioned` capability, and each capability that a smaller one could replace, write an `intent` finding. Its decision is `autonomous` when the capability is clearly useless: no `user` or `external` source names it, no consumer outside the target uses its results, and its removal breaks no contract. Otherwise, its decision is `user`. Recommend removal or the smaller capability, unless a `user` or `external` source, or a consumer outside the target, shows the need.
6. **2.6** Do an open review before you read the checks file. Ask what you would remove, replace, or redesign, now that you know the results and their consumers. Write a finding for each idea that the evidence supports. No check limits this review: a finding does not need to match a check. Give `open-review` one line in `## Checks`.
7. **2.7** In `## From scratch`, answer: "Knowing the current implementation, how would you build this from scratch?" Use only the `core` and `supporting` capabilities. Name the owners and data shapes before the files. Apply each design reference that fits the target. Build the design so that it follows the five steps of the [refactoring check](../checks/every-feature/refactoring.md). Look for the red flags across features: split ownership, two ways to do one task, a hand-synced list, leaked information, and a pass-through layer. Compare the result with the current design: owners, interfaces, data shapes, layers, state, and duplicated rules. The current design keeps a part only when evidence shows that the part is better. Write a finding for each difference.
8. **2.8** Read the checks file that the packet names. Look over every topic in its list. For each check of a topic, read its pattern, and decide whether the pattern appears in the target. Read a check's file only when its pattern appears.
9. **2.9** Apply the checks that the checks file gives in full, and each check whose pattern appears. Find each place where its **Signal**, rules, or **Look for** situation appears. At each place, apply its **Decide with** and **Keeps it when**, or for a case, its **Applies when** and **Limits**. Go down [the ladder](../guides/fixed-behavior.md#the-ladder) from `remove`, and stop at the first rung that the evidence supports. In `## Checks`, give one line to each check that the checks file gives in full, and one line to each topic. Close each tool result of the scope record in the `every-feature/tool-results` line or in a finding. Apply each language check to every line, as [language rules](../checks/every-feature/refactoring.md#language-rules) says, and give it one line.
10. **2.10** For each finding, search for a consumer that the inventory did not find, and for an input or event order that would give a different result. Read [shorter code can change behavior](../evidence/shorter-code-can-change-behavior.md) before your first finding.
11. **2.11** Give each finding an effect and a decision:
    - `parity`: it keeps every reachable `required` and `incidental` result.
    - `intent`: it removes or changes a result on purpose. Name the entry IDs.
    - `autonomous`: it keeps every required and incidental result, stays within one owner, is easy to undo, and has source or scratch proof. A finding of 2.5 can also be `autonomous`.
    - `user`: it has the effect `intent`, changes an interface, contract, stored data, security, operations, or a visible result, spans owners, or is costly or hard to undo when wrong.
12. **2.12** In `## Report`, write the verdict: complete, partial, or blocked, with the material coverage gaps. List the parity findings that matter most, then the intent findings, by their IDs. List the contingent reductions with the decision or evidence that blocks each. List suspected defects that are not reductions. End with the decisions for the user: for each `user` finding, one question, the options, and your recommendation.

## Record lines

```text
## Capabilities
- C<n> | <core, supporting, or questioned> | <capability> | <entry IDs> | <source: path:line, or the user's request>
## Inventory
- B<n> | <feature ID> | <required, incidental, or unknown> | <result, its consumers, and what each does with it> | <path:line>
## Checks
- open-review | <finding IDs, or absent> | <path:line> | <what you asked and looked at>
- <check or topic> | absent | <path:line where you looked> | <what you looked at and why no pattern appears>
- <check or topic> | <finding IDs, such as X1, X2> | <path:line> | <the checks that applied and what you looked at>
## Findings
- X<n> | <rung> | <effect> | <decision> | <entry and capability IDs> | <path:line> | <finding and proposed change>
```

Number the findings from X1. Separate several IDs or paths in one cell with `;`. An `absent` line still names the place where you looked: a skipped check and a clean check must look different. For each finding, name what disappears and why the required behavior survives. Reject reductions that only hide complexity, move it to another file, or suppress failures.

Write the record yourself, from what you read. Do not write scripts or programs that create its lines or findings.
