# Review and handoff guidance

## Plan sources

Start with the requested scope and follow its requirements, decisions, acceptance criteria, and relevant technical and QA plans.
Record each source's path, revision or hash, status, scope, and evidence of authority.
Separate intended behavior from current-state claims. A newer decision supersedes an older requirement only when evidence establishes that.
Record unresolved conflicts and their impact; do not silently select a convenient source.
Read applicable repository guidance. Treat earlier reviews as leads and check their claims against current source.

## Plan units

Assign stable IDs to independently reviewable requirements, constraints, choices, rollout steps, and verification obligations.
Retain existing requirement and QA IDs as aliases. Keep IDs stable across revisions and link split or merged units to their predecessors.
Record each unit's source anchor, excerpt, authority, dependencies, and assessment or unresolved status.
Group units by shared behavior and acceptance context, including unchanged callers and contracts.

## Plan review

Create an implementation plan only when requested or required by the selected task. A review can conclude with no changes or blocked findings.
When a plan exists, check its scope, requirements, affected files, dependencies, verification, open decisions, and recovery needs.
Use its established format. Do not require phases or run a phase checker when the plan has no executable phases.
Run an existing format-specific checker only when the plan uses that format and contains phases. Report checker failures without inventing phases.
For each proposed phase, name the affected files, outcome, dependencies, checks, and expected results.
For high-risk changes, identify failures, recovery, rollback, and safe intermediate states.
Keep the plan usable without this conversation. Name source revisions and the failures or source changes that require replanning.
Check links and review the document for accuracy, clarity, and completeness. Do not include secret values.

## Implementation handoff

Implement only when requested. Establish the relevant behavior baseline before changing structure.
Migrate callers and remove replaced code unless a concrete compatibility contract requires it.
Apply and verify one coherent group at a time. Check affected behavior at its strongest practical boundary.
Compare failures with the baseline, recheck affected findings, and report gaps. Preserve unrelated changes.
When formal checks already cover changed code, reconcile them with the implementation. Report unresolved invariants.
When the reduction moves requirements between plan units, compare the units before and after.
Derive each ownership change from that comparison. A list written by hand is a summary, not the source.
