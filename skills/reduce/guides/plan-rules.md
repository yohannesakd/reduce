# Plan rules

Rules for the plan playbook. The plan steps link to the section that each one needs.

## Requirement kinds

In this playbook, a section is a feature, and a unit is a plan unit. The baseline is the source revision that the plan changes.

## Requirements

Identify accepted product scope, requirements, acceptance criteria, and decisions using [plan sources](workflow.md#plan-sources).
When the plan links no such document, use its requirement, scope, or acceptance section as the only accepted source.

- A test or QA section is a set of units, even when the plan calls it required. A QA item's expected result is accepted only when an accepted source states the same result.
- Workspace guidance is an accepted source for the results that its rules require, such as a "must" or "never" statement.
  Guidance that describes the current design, such as an architecture overview, is evidence about the baseline.
- A statement in an accepted source can still be design. Classify each statement with the kinds below.

The requirement inventory has three kinds of entries. The reduced plan delivers every entry except a delivery gap.

- `accepted`: an accepted source states or requires an observable result of a reachable input for a user, caller, or operator. Record the source.
  Examples are a named public API, an audit log, a staged rollout, and a compatibility promise.
  An accepted structural goal or implementation constraint is also `accepted`, with a completion check. The reduced plan meets it, even when the baseline already matches.
  A delivery mechanism is design unless a source gives another reason, or an external document requires it.
- `kept`: baseline behavior that passes through code that the plan changes or leaves unused, and that no other entry changes.
  This includes public interfaces, errors, logs, metrics, ordering, and resource use. Record one entry per entry point and starting state.
  When a `prevent` or `reuse` result changes code outside the plan, add `kept` entries for that code's other users.
  Each `kept` entry has a class in [Fixed behavior](fixed-behavior.md#fixed-behavior). Removing an `incidental` `kept` entry is a contingent reduction.
- `added by plan`: the plan changes an observable result at an entry point that the baseline or an accepted source gives. No accepted source requires that change.
  An example is a lock that makes a concurrent request fail. Record the source anchor, input, result, and any baseline result that it alters or removes.
  Keep baseline results as `kept` entries for the inputs and states that the entry does not change.
  Keep the entry in every sketch and in the reduced plan until the planning owner decides. Report it as a product question. Its delivery is design.

Everything else in the plan is design, and goes through the ladder: files, functions, types, fields, endpoints, messages, layers, phases, flags, migrations, recovery mechanisms, tests, and process records.

- A result that the plan adds is design when only an operator, the implementer, or a consumer inside the plan observes it. Examples are an unnamed endpoint, a log, a metric, and a rollback step.
  It is `accepted` when an accepted source or workspace guidance requires it, or a source names an existing consumer outside the plan. A future consumer is not evidence.
- An accepted requirement takes precedence over both rules and must be delivered.
- Otherwise, when both the `added by plan` rule and the design rule apply, classify the added result as design.
  An altered or removed baseline result is never design.
- Prove unreachability at the baseline, the planned target state, and each intermediate phase, including states that the plan introduces. Check it again for the reduced approach.
- When these rules cannot classify a statement, its units are `unresolved`. Record the question for the planning owner.
- Record product behavior that the sources leave open as a question.

Apply these requirement kinds when [the check step](../steps/4-check.md) compares differences.
Every inventory entry has a resource use field: the current cost of its path and the change that the plan makes.
The cost includes queries, calls, processes, computation, memory, and data volume. Write `unchanged` with the evidence when the plan does not change it.
For a path that the plan adds, record its traced cost as a limit in the entry for the result that it delivers.
Trace the cost of each approach at the application's real scale. When the trace cannot decide and the difference could matter, the unit is `unresolved`.
Put the deciding measurement in the reduced plan's verification.

## Plan units

A feature is one behavior that a user or caller can observe, or one structural need. Group units by feature across documents, repositories, layers, and phases.
A unit is one claim or choice that a reviewer could keep or remove independently. One unit can serve several features. Record its role in each.
Give each unit a stable ID using [plan units](workflow.md#plan-units). Keep the IDs of an earlier `review.md`.
Keep the unit table only in `review.md`, also when a linked reference asks for a `plan-map.md`.

Units include these proposals:

- Code: modules, functions, types, fields, endpoints, messages, error cases, abstractions, and layers.
- Machinery: caches, queues, jobs, state machines, dependencies, flags, and migrations.
- Operations: rollout steps, recovery steps, logs, and metrics.
- Checks and records: tests, QA items, and documentation changes.
- Plan structure: phases and ordering constraints.
Record each unit's source anchor, and the concepts, branches, and layers it adds.
Add the baseline code that the plan replaces or leaves unused as units marked "not in the plan". When `remove` holds, the reduced plan removes that code in the phase that leaves it unused.
Record a literal excerpt for each stated requirement, and for each unit that is `unresolved` or reaches `remove`, `prevent`, or `reuse`.

A delivery gap is a requirement that no unit delivers. Record it, and leave its delivery to the planning owner. A delivered requirement without a proof is not a gap; the check step plans its proof.
A question is a statement that the rules cannot classify, or a choice that the sources leave open. A gap that also needs a product answer is recorded once, as a gap.

## Plan ladder questions

Challenge the assumptions behind `keep` and `simplify` results across related units and owners.
Trace affected requirements and baseline behavior before changing an assumption.

- `remove`: which requirement or demonstrated structural benefit fails without the unit? Examples to cut are a phase that only prepares a later abstraction, recovery for an unreachable failure, and a compatibility path for callers that a search does not find.
- `prevent`: can one change at an owner, producer, schema, or type remove units in several features?
- `reuse`: does the baseline, a framework, or a dependency already have the endpoint, component, query, helper, job, or validation? Does the plan add a path next to an existing one?
  When the planned path runs in a different runtime environment than the baseline path, decide the claim with the environment rule in [Fixed behavior](fixed-behavior.md#fixed-behavior).
- `simplify`: does the plan add a layer with one user or a flag with one value? Can an existing field carry a new field's data? Can two phases become one verifiable phase?
- Keep a migration, backfill, rollout step, rollback, or recovery mechanism when a requirement entry fails without it, a source or workspace guidance requires it, or a reachable side effect would cause consequential harm. Record which.
- A QA item that only repeats an implementation step proves nothing.

## Design comparison

- Sketch from the baseline, problem, cause, and requirement inventory. Give an independent author the same inputs, without the plan. Record in `Coverage` when no independent sketch ran.
- Compare the original plan, its reduced design, and fresh sketches, including supported additions that improve structure.
- Each approach delivers every entry except the delivery gaps. Carry each gap into every sketch and the reduced plan, linked to `Questions`.
- When a plan unit delivers a result that the inventory lacks, classify the result. Add an entry when it is not design, and compare again.
- A reduction that depends on the planning owner's answer, such as removing an `added by plan` entry, is a contingent reduction.
  Record the question, the enabling answer, the units it removes, and the result. Keep it only in the review until the planning owner gives that answer.
- The reduced plan is the plan with every unit, feature, and group result applied, except contingent reductions.

## Proof

Evidence comes from source, history, documentation, existing tests, and scratch checks at the baseline.
Use run checks only on code that exists at the baseline or in a scratch spike. Implement neither plan to get comparison evidence.

- Confirm that an existing implementation gives the required result for the inventory inputs.
- Confirm that a `prevent` change keeps the behavior of the other users of that level with their existing checks.
- When only a working spike can decide a consequential claim, build the smallest spike in the scratch worktree.
- For behavior that does not exist yet, put the check in the reduced plan's verification, and record the evidence limit.

Give the reviewers the baseline, the requirement inventory, the original plan, and the reduced plan. Also ask them for a requirement entry that the reduced plan misses.
Derive each finding in [the check step](../steps/4-check.md) using the accepted requirements and kept baseline behavior.

## Reduced plan

Write to the path that the user or workspace guidance names. Otherwise, create a directory outside every repository.

Write `review.md` as [the report step](../steps/5-report.md) describes, with these plan-specific fields:

- `Coverage`: plan documents with revisions or hashes, baseline revisions, patch path, planning state, and whether an independent sketch and review ran.
- `Problem`: each feature's problem, cause with evidence, and recommended change site.
- `Requirements`: each entry's kind, source, and resource use.
- `Features`: each feature with its rung, or its count of units per rung when they differ. Then one row per unit: plan anchor, rung, rejected higher rungs with reasons, evidence, and change.
- `Proof`: the check in the reduced plan for each entry, or no lasting test with the reason. Mark a delivery gap as blocked on the planning owner.
- `Questions`: product questions, `added by plan` entries, `unresolved` units, contradictions, delivery gaps, and false plan claims. Link each to the contingent reductions its answer enables.
- `Contingent reductions`: question, enabling answer, units removed, and expected result.
- `Expected result`: structural benefits and tradeoffs; concepts, branches, layers, files, dependencies, migrations, flags, phases, tests, and QA items removed or added.

Link detailed queues, design comparisons, and case applications when they support a recommendation or decision.

Write a reduced copy of each changed plan document, named `reduced-<file name>`:

- After any front matter, start with `Status: proposal, not accepted`, the original path and revision or content hash, the baseline revisions, and the path of `review.md`.
- Keep the original format, headings, and requirement and QA IDs, so the copy reads as a normal plan.
  When a result removes a whole section, keep its heading with one line that names the removed units and links their rows in `review.md`.
- Apply every result except contingent reductions. Change an `unresolved` unit only after its question is answered, and link its row in `Questions`.
- Point links between changed documents to their reduced copies. Rewrite other relative links to reach the same targets.
- Order phases so each leaves a working, verifiable result. Put units that must change together in one phase.
  Without phases, add an order only when units must change in sequence.
- When a section applies an example, link its local case and the review record explaining applicability, limits, and preserved behavior.
- Apply the [plan review guidance](workflow.md#plan-review). Record any applicable checker result in `Coverage`.

Check every link in the output directory. Review the documents for accuracy, clarity, and completeness.
In the report, also name the contingent reductions, the false plan claims, and the questions for the planning owner. State that the planning owner must accept the reduced plan before implementation.
