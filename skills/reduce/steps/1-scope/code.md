# Scope a code change

Collect the facts about the change under review: its limits, its sources, its features, and the tool results. Later steps judge it.

1. **1.1** Identify the target. Default to the current branch against its merge base on the default branch, plus uncommitted changes. Accept a named PR, commit range, or paths. Record the base and head revisions in `## Revisions`.
2. **1.2** Save the uncommitted edits outside the target: `git diff --binary --no-ext-diff --no-textconv HEAD > "$records/existing-edits.patch"`. List untracked inputs, or record that none exist.
3. **1.3** Record the limits: authorized sources and accounts, live access, delegation, isolation, and host placement for any execution.
4. **1.4** Check whether the default branch already contains the target's commits, or changed the same code after the merge base. Record which branches contain the commits.
5. **1.5** List the sources in `## Sources`: the user's request, the ticket, the PR body, commit messages, decision records, product and repository documentation, agent instructions, and plans. Give each row one authority, and quote the problem or goal that the source states. Do not interpret it.
   - `user`: the user's request or answer.
   - `external`: a ticket, decision record, accepted plan, existing contract, or consumer outside the target. A PR body, ticket, issue, or commit message is `external` for the goals that it states.
   - `target`: a document, test, or comment that the target itself adds or owns. It describes the target.
6. **1.6** Read each changed file. Group the hunks into features. A feature is one behavior that the change adds or alters, or one existing behavior that passes through changed code.
7. **1.7** Run the analyzers that are installed, within the limits of 1.3. Read [tools and evidence](../../evidence/tools-and-evidence.md) for the tools and their limits. Record each tool's version and scope, or that it is unavailable. When Desloppify is available, inspect its help and reports, and run `desloppify scan --path <project>` as a scratch run outside the target. Save the outputs under the records directory. Do not install tools, autofix, or upload code. Execute project code only with isolation that excludes credentials and unrelated data.
8. **1.8** List each tool result in `## Tool results` with the feature that it belongs to. Copy what the tool reports. A score, an empty scan, or a report from another revision is a result to check, never evidence of safety or completion. List the suspected defects that a tool reports, such as a security problem or a wrong result, apart from the reductions.

List the features in `## Features`. Each feature gets one map record and its checks later.
In the paths column, list the changed files of the feature, separated by `;`. The driver selects the [language checks](../../checks/README.md#languages) from these files, so list real file paths. Every changed, added, deleted, and untracked file must be in a feature or in `## Excluded` with its reason.
In the entry points column, cite each public interface, command, route, job, persistent store, or operational path that reaches the feature, as `path:line`, separated by `;`.

This step collects. Do not judge the target here: state no purpose of your own, propose no reduction, and trace no cause. The design step does that work with the map records.
