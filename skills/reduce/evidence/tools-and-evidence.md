# Evidence sources

Treat tool output as candidates, never proof. Keep unknown consumers unresolved.

### Existing implementations

Search beyond the diff by name, behavior, and body. Check language/platform/framework/dependency capabilities before additions.
Without documentation, inspect pinned source and record the limit.

### Static dead-code tools

Use suitable deterministic tools first. Check versions, help, scope, and write locations. Do not install missing tools.

| Tool | Finds | Cannot see | Use the result as |
| --- | --- | --- | --- |
| Knip (JS, TS) | Unused files, exports, dependencies, class members | Dynamic loading such as `React.lazy`. Treats package entry points as public, so it reports none of their exports by default. | A candidate list. Trace dynamic users and entry points. |
| ts-prune | Unused exports | Dynamic imports. It is in maintenance mode. | A weaker candidate list. Prefer Knip. |
| Vulture (Python) | Unused functions, classes, imports, variables, unreachable code, with a confidence of 60 to 100 | Its README says it is "likely to miss some dead code". Framework hooks and reflection. | A candidate list. Run with the default threshold. A higher `--min-confidence` hides the findings at confidence 60: unused functions, classes, methods, and variables. |
| Debride (Ruby) | Unused methods | Metaprogramming | A candidate list, best with runtime data. |
| Go `deadcode` | Unreachable functions | Platform-specific entry points | See [Bound deletion and check contracts beyond local callers](../checks/unused-code/bound-deletion-and-check-contracts.md). |
| Ruff `BLE001`, `PLC0415`, `B904` | Blind `except`, imports inside functions, `raise` without a cause | Whether the pattern is justified | A prompt for [A guard that cannot fail, or the same guard repeated](../checks/guards-and-errors/guard-that-cannot-fail.md), [An import or cast that hides a real constraint](../checks/dependencies-and-imports/import-inside-a-function.md), [A suppression directive that hides a cause](../checks/guards-and-errors/suppression-that-hides-a-cause.md). |
| import-linter | A forbidden dependency between modules | Dependencies it has no contract for | Evidence for a layer violation. |
| jscpd or a similar scanner | Textual clones | Clones with different text | Types I to III in [A clone, by degree of similarity](../checks/duplicates-and-existing-code/clone-by-similarity.md). |

```bash
knip --reporter compact
vulture src/
ruff check --select BLE001,PLC0415,B904 src/
```

Prove unreachability before removing untested code; otherwise record the protection gap.

### Runtime evidence

Record first/last activity and the observation window, including the longest rare/failover/admin cycle.
Zero hits cannot prove unreachability. Without sufficient cycle evidence, leave the unit unresolved.
Combine static/runtime evidence conservatively; string references and `eval` hide users.

### Consumer evidence

Search authorized public, preview, prerelease, and dependent-branch consumers and release/deployment records.
Record search limits. Include undocumented ordering, timing, and messages in contracts.

| Interface | Evidence that supports `incidental` | Blind spot, so `unknown` |
| --- | --- | --- |
| GraphQL field | Client usage reports and schema checks against recent operation traces. `@deprecated` marks the field first. | Clients that do not identify themselves, and old operations outside the trace window. |
| REST or RPC field | Access logs by client identifier, the OpenAPI document, and the client repositories that you can search | Unregistered clients, scripts, and partners |
| Consumer-driven contracts (Pact) | No consumer pact references the field | Only consumers that published pacts. A field that no pact references is not covered by any contract, and that is all it shows. |
| Event or queue payload | Subscriber code and schemas in every repository that you can search | Consumers that you cannot list |
| CLI output or exit code | Scripts and documentation in the repository | User scripts that parse the output |
| Log line or metric | Dashboards, alert rules, and runbooks | Ad hoc queries and incident tools |
| Database column | Queries, ETL jobs, and reports | Direct reads by other teams |

Worked classification:

| Entry | Search | Class |
| --- | --- | --- |
| `GET /orders/{id}` returns `internal_note` | Searched the API repository, both client repositories, the OpenAPI document, and the access-log client list. No reader found. The API is public. | `unknown`: outside clients cannot be listed. |
| `GET /orders/{id}` returns `internal_note` | Same search. The API is internal. Every client is in the two repositories. No reader found. No source requires it. | `incidental`: a contingent reduction. |

### Flag state

Use the flag system of record and [A feature flag that every user already has](../checks/options-flags-and-settings/flag-every-user-has.md), with [Split flag cleanup between mechanical rewrites and judgment](../checks/options-flags-and-settings/split-flag-cleanup-between-rewrites-and-judgment.md).

### History

Read adding/fixing commits and decisions before removal. Treat guards as failure evidence; disprove reason-bearing comments before removal.
Record failed searches. Without history, obtain other deciding evidence or remain unresolved.

```bash
git log -S'symbol' --oneline -- path/     # commits that added or removed the symbol
git log -G'pattern' --oneline -- path/    # commits that changed lines matching a pattern
git blame -L 40,60 path/file.py           # who last changed these lines, and in which commit
```

### Complexity, duplication, and test strength

When the project or host has them, use Crapper, Dryer, and Mutator. Check language support, versions, and write effects first. Do not install them in a read-only run.
- Crapper combines decision complexity with coverage in the CRAP score. Use the project's threshold, or CRAP 10 as an advisory signal. A score alone does not decide a rung. Do not move branches into wrappers only to lower a score. Distinguish unavailable coverage from measured zero coverage.
- Dryer reports similar code pairs. Use the project's threshold, or similarity 0.8 as an advisory signal. Decide each pair with [A clone, by degree of similarity](../checks/duplicates-and-existing-code/clone-by-similarity.md). A successful exit means that the analysis completed, not that no duplication exists.
- Mutator changes code on purpose to test whether tests detect it. Use it for [A test that cannot fail for the right reason](../checks/tests/test-that-cannot-fail.md). Timeouts and uncompiled mutations can count as killed; they do not prove that assertions detect a defect.

### Recurrence

Consider lint/CI prevention only for repeated findings. Record it as a follow-up, not a reduction.
Do not add a rule for one occurrence.

### Sources

- Tools and their limits: [Knip, ts-prune, and unimported](https://repowise.dev/blog/comparisons/knip-vs-ts-prune-vs-unimported), [dead-code tool comparison](https://repowise.dev/blog/comparisons/best-dead-code-detection-tools), [Anaconda](https://www.anaconda.com/blog/deslopping-ai-code) (Ruff rules, import-linter).
- Runtime evidence: [thoughtbot on Ruby dead code](https://thoughtbot.com/blog/how-to-remove-dead-code-ruby), [Coverband](https://www.ruby-toolbox.com/projects/coverband), [Meta's dead-code system](https://engineering.fb.com/2023/10/24/data-infrastructure/automating-dead-code-cleanup/).
- Consumer evidence: [Apollo schema deprecations](https://www.apollographql.com/docs/graphos/schema-design/guides/deprecations), [SmartBear contract-testing glossary](https://support.smartbear.com/swagger/contract-testing/docs/en/user-guide/troubleshooting/glossary.html).
- Reuse by agents: [More Code, Less Reuse](https://arxiv.org/abs/2601.21276v1).
- Flags: [Uber AutoClean](https://x.com/UberEng/status/2112604623454470476), [Piranha](https://eng.uber.com/piranha/).
- Complexity, duplication, and test strength: the pstack [code-quality checks](https://github.com/cursor/plugins/blob/main/pstack/skills/poteto-mode/references/code-quality.md), adapted from [ub-mode](https://github.com/unclebob/ub-mode/blob/master/SKILL.md), [Crapper](https://github.com/unclebob/crapper), [Dryer](https://github.com/unclebob/dryer), [Mutator](https://github.com/unclebob/mutator).
- History: [Atomic Object on Chesterton's Fence](https://spin.atomicobject.com/chestertons-fence-code-comments/), [Rach Smith](https://rachsmith.com/dont-remove-a-fence/).
