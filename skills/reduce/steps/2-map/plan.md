# Map a planned feature

Describe what the planned feature must deliver, and check the plan's claims against the baseline. This step describes. It does not judge whether the plan needs a requirement: the design step does that with every map record.

Apply the requirement kinds and precedence in [plan rules](../../guides/plan-rules.md#requirement-kinds).

1. **2.1** Find the statements about the feature in the accepted sources of the scope record. Record each statement's source anchor, a literal excerpt, and its authority: `user`, `external`, or `target`.
2. **2.2** Make the requirement entries. For each entry, name each consumer and what it does with the result, and record the entry point, actor, input, starting state, configuration, observable result, and resource use. Record a completion check for each structural goal. When you find no consumer, write `no consumer found` and cite the search.
3. **2.3** Divide the feature into plan units with [plan rules](../../guides/plan-rules.md#plan-units). Add baseline code that the plan replaces or leaves unused as units marked "not in the plan".
4. **2.4** Confirm each existing file, function, owner, contract, and path that the plan names at the baseline. Check each proposed addition for name conflicts and wrong assumptions. Record each false claim and its dependent units.
5. **2.5** Trace producers, callers, and existing implementations for each unit. Record each function, file, and layer that the plan adds, with its planned call sites. Step 1 of the [refactoring check](../../checks/every-feature/refactoring.md) uses the functions with one planned call site: "Inline every function that is only used once and tighten former call sites". Step 4 uses the functions with several callers: "Co-optimize multi-consumer functions with their callers". Inspect already-implemented parts as evidence, labeled separately, and recommend a code run for them.
6. **2.6** When the feature has state that changes over events, write a table of every state, event, and reader, including operator, timeout, and recovery events. Otherwise, record why the feature has no such state.
7. **2.7** Record delivery gaps and questions. A gap that also needs a product answer is recorded once, as a gap.

List the entries in `## Requirements`, with the IDs `R1`, `R2`, and so on. Use `kept` entries for baseline behavior that the plan passes through or leaves unused.
