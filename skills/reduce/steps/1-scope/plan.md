# Scope a plan

Collect the facts about the plan: its documents, its sources, its baseline, its limits, its features, and the tool results. Later steps judge it.

Read [plan rules](../../guides/plan-rules.md) completely before this step.

1. **1.1** Identify the plan: the one that the user names, then the one in the conversation or workspace. Record each plan document's path, revision or content hash, and status.
2. **1.2** Find the accepted sources with [plan sources](../../guides/workflow.md#plan-sources): requirements, decisions, acceptance criteria, and technical and QA plans. List them in `## Sources`. Give each row one authority, `user`, `external`, or `target`, and quote the problem or goal that the source states. Do not interpret it. A document that the plan itself adds is `target`.
3. **1.3** In `## Revisions`, record the baseline revision of each repository that the plan changes, with the role `baseline`. Without one, use the current head and record that choice. Give each other revision that the plan or its sources cite the role `reference`, such as an installed release or an old build, and say what it is. Save named uncommitted changes as a patch outside the repository, or record that none exist.
4. **1.4** Record the limits: authorized sources and accounts, live access, delegation, isolation, and host placement for any execution.
5. **1.5** Record the planning state: approval evidence, open questions, and contradictions between documents. When planning is incomplete, name what is missing.
6. **1.6** Read each plan document. Group its units into features with [plan units](../../guides/workflow.md#plan-units). A feature is one observable behavior or one structural need, across documents, repositories, layers, and phases.
7. **1.7** Run the analyzers that are installed, within the limits of 1.4. Read [tools and evidence](../../evidence/tools-and-evidence.md) for the tools and their limits. Record each tool's version and scope, or that it is unavailable. When Desloppify is available, inspect its help and reports, and run `desloppify scan --path <project>` as a scratch run outside the target. Save the outputs under the records directory. Do not install tools, autofix, or upload code. Execute project code only with isolation that excludes credentials and unrelated data. Scan only the baseline code that the plan touches. A planned unit is not a tool result.
8. **1.8** List each tool result in `## Tool results` with the feature that it belongs to. Copy what the tool reports. A score, an empty scan, or a report from another revision is a result to check, never evidence of safety or completion. List the suspected defects that a tool reports, such as a security problem or a wrong result, apart from the reductions.

List the features in `## Features`. Each feature gets one map record and its checks later.

This step collects. Do not judge the target here: state no purpose of your own, propose no reduction, and trace no cause. The design step does that work with the map records.
