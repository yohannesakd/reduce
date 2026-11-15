# Scope existing code

Collect the facts about the target: its limits, its sources, its features, and the tool results. Later steps judge it.

1. **1.1** Record the goal that the user gave, the requested paths, languages, and exclusions. The driver recorded the revision and the hash of the uncommitted edits.
2. **1.2** Save the uncommitted edits outside the target: `git diff --binary --no-ext-diff --no-textconv HEAD > "$records/existing-edits.patch"`. List untracked inputs, or record that none exist.
3. **1.3** Record the limits: authorized sources and accounts, live access, delegation, isolation, and host placement for any execution.
4. **1.4** Separate owned, generated, and vendored code. Reduce generated or platform code through its source, and exclude it from savings.
5. **1.5** List the sources in `## Sources`: the user's request, the ticket, the PR body, commit messages, decision records, product and repository documentation, agent instructions, and plans. Give each row one authority, and quote the problem or goal that the source states. Do not interpret it.
   - `user`: the user's request or answer.
   - `external`: a ticket, decision record, accepted plan, existing contract, or consumer outside the target. A PR body, ticket, issue, or commit message is `external` for the goals that it states.
   - `target`: a document, test, or comment that the target itself adds or owns. It describes the target.
6. **1.6** Read each file. Group the files into features. A feature is one capability that a user, caller, or operator can observe, or one internal responsibility.
7. **1.7** List the areas that you could not inspect, and why.
8. **1.8** Run the analyzers that are installed, within the limits of 1.3. Read [tools and evidence](../../evidence/tools-and-evidence.md) for the tools and their limits. Record each tool's version and scope, or that it is unavailable. When Desloppify is available, inspect its help and reports, and run `desloppify scan --path <project>` as a scratch run outside the target. Save the outputs under the records directory. Do not install tools, autofix, or upload code. Execute project code only with isolation that excludes credentials and unrelated data.
9. **1.9** List each tool result in `## Tool results` with the feature that it belongs to. Copy what the tool reports. A score, an empty scan, or a report from another revision is a result to check, never evidence of safety or completion. List the suspected defects that a tool reports, such as a security problem or a wrong result, apart from the reductions.

List the features in `## Features`. Each feature gets one map record and its checks later.
In the paths column, list the files, folders, or globs of the feature, separated by `;`.
In the entry points column, cite each public interface, command, route, job, persistent store, or operational path of the feature, as `path:line`, separated by `;`.
Every file must be in a feature or in `## Excluded` with its reason, such as generated or vendored code.

This step collects. Do not judge the target here: state no purpose of your own, propose no reduction, and trace no cause. The design step does that work with the map records.
