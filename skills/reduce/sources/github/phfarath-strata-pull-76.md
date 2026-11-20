# phfarath/Strata pull request #76: refactor(workspace): remove dead code, unused deps and AI-slop (-1932 lines)

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: phfarath
- Date: 2026-10-21
- Original location: https://github.com/phfarath/Strata/pull/76
- Copied: 2026-11-20, from the pull request, its comments, its reviews, and its diff, from the GitHub API

## Text
## Contexto

Limpeza sistemática de código gerado a mais, usando as disciplinas clean-ai-slop + dead-code + ponytail: um passe por categoria de smell, testes rodados após **cada** passe.

## Resultado

- **60 arquivos, +257 / -2189 linhas** (líquido −1932)
- **354/354 testes verdes** (baseline 358; −4 tests do subsistema gateway removidos junto com ele)
- `cargo fmt --check` limpo; clippy só com hints de design (too-many-args, complex-type)

## Passes

| # | Categoria | Removido |
|---|---|---|
| 0 | Mecânico | ~70 warnings clippy auto-fix + rustfmt |
| 1 | Triviais | branches idênticos, strip_prefix, struct-literal, vec![], param morto em recursão, doc overindent |
| 2 | Deps | `futures`, `tower-http` (workspace), `thiserror` ×4 crates, `anyhow` (tools), `hex` (core) — todas verificadas com grep antes |
| 3 | Dead code | ~120 símbolos zero-ref em todo o workspace (47 memory, 31 core/tools, 37 cli/reasoning/evals): fns SQL nunca chamadas, builders, consts MCP duplicados, twin morto de scenario, `parse_json_dag`, `from_env` ×4 |
| 4 | Abstrações | **subsistema ToolGateway inteiro** (trait + DefaultToolGateway + gateway.rs + tests — órfão: MCP server despacha à mão), `EventStore::append_batch`, aliases `load_from_path`/`save_to_path`, campos de config nunca lidos (`SyncConfig.max_retries`, `learning_rate_guidance`, `allowed_working_dirs`), guarda paranóica em store.rs, endpoint hardcoded → const |
| 5 | Comentários | emoji em logs tracing, docs triviais de getter, docs que repetem assinatura, comentários numerados redundantes, banner duplicado |

## Mantido deliberadamente

- APIs usadas apenas pelos próprios `#[cfg(test)]` (travam comportamento testado: cold storage, self_editing, a2a)
- Emoji em output visível de CLI/lib (house style; mudar = mudança de comportamento)
- `run_all_scenarios` (entry point do crate evals)

## Report-only (refactor de design, fora do escopo desta limpeza)

- Traits `ReasoningEngine` duplicados (traits.rs vs engine.rs; 5 adapters implementam ambos)
- Variantes de erro duplicadas em errors.rs (`Validation` vs `ValidationError` etc.)
- 8× too-many-args (retrieval.rs) + 3× complex-type
- ~310 símbolos `pub` candidatos a `pub(crate)`


## Change

2 commits, 57 files, +254 -2129. Merged: 2026-10-24T16:50:17Z.

## Comment by coderabbitai[bot], 2026-10-21

<!-- coderabbit-ai-generated:v1 -->

<!-- This is an auto-generated comment: summarize by coderabbit.ai -->
<!-- This is an auto-generated comment: skip review by coderabbit.ai -->

> [!IMPORTANT]
> - [ ] <!-- {"checkboxId":"e9bb8d72-00e8-4f67-9cb2-caf3b22574fe"} --> 🔍 Trigger review
> 
> This repository does not receive automatic reviews because it has fewer than 10 stars.
> 
> <details>
> <summary><strong><picture><source media="(prefers-color-scheme: dark)" srcset="https://storage.googleapis.com/coderabbit_public_assets/review-comment-icons-v1/cog-dark.svg"><img src="https://storage.googleapis.com/coderabbit_public_assets/review-comment-icons-v1/cog.svg" width="16" height="16" align="absmiddle" alt=""></picture> Run configuration</strong></summary>
> <dl>
> <dd>
> 
> - **Source mode**: Auto
> - **Repository**: Unavailable
> - **Branch**: Unavailable
> - **File**: No configuration file from this repository applied
> - **Commit**: Unavailable
> - **Layers**: defaults
> - **Review profile**: CHILL
> - **Plan**: Advanced
> - **Run ID**: `996b25fa-a32b-4063-925d-f7e68b9a7831`
> 
> </dd>
> </dl>
> </details>

<!-- end of auto-generated comment: skip review by coderabbit.ai -->

<!-- autopilot:start -->
- [ ] <!-- {"checkboxId":"2708ad07-9f24-4260-9c11-7dc76a49f2e3"} --> <strong title="Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts">Autofix</strong> · Keep fixing CodeRabbit findings and required CI, and resolving merge conflicts
<!-- autopilot:end -->
<!-- tips_start -->



Thanks for using [CodeRabbit](https://coderabbit.ai?utm_source=oss&utm_medium=github&utm_campaign=phfarath/Strata&utm_content=76)! It's free for OSS, and your support helps us grow. If you like it, consider giving us a shout-out.

<details>
<summary><strong>❤️ Share</strong></summary>
<dl>
<dd>

- [X](https://twitter.com/intent/tweet?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A&url=https%3A//coderabbit.ai)
- [Mastodon](https://mastodon.social/share?text=I%20just%20used%20%40coderabbitai%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20the%20proprietary%20code.%20Check%20it%20out%3A%20https%3A%2F%2Fcoderabbit.ai)
- [Reddit](https://www.reddit.com/submit?title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&text=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code.%20Check%20it%20out%3A%20https%3A//coderabbit.ai)
- [LinkedIn](https://www.linkedin.com/sharing/share-offsite/?url=https%3A%2F%2Fcoderabbit.ai&mini=true&title=Great%20tool%20for%20code%20review%20-%20CodeRabbit&summary=I%20just%20used%20CodeRabbit%20for%20my%20code%20review%2C%20and%20it%27s%20fantastic%21%20It%27s%20free%20for%20OSS%20and%20offers%20a%20free%20trial%20for%20proprietary%20code)

</dd>
</dl>
</details>


<sub>Comment `@coderabbitai help` to get the list of available commands.</sub>

<!-- tips_end -->

## Comment by github-actions[bot], 2026-10-21

<!-- strata-guard-report -->
## 🛡️ Strata Guard — Cognitive Architecture & PR Review

> Automated architectural risk assessment powered by **Strata Cognitive Memory & Causal World Model**.

### 🧪 Analysis Status

✅ **Blast-radius analysis completed successfully.**

### 🎯 Causal Blast Radius & Risk Level

| Metric | Value | Status |
| :--- | :--- | :--- |
| **Pre-Code Risk Score** | `42%` | 🟡 **MODERATE RISK** |
| **Risk Classification** | **Moderate** | 🟡 |
| **Modified Targets** | `57` files | 📁 |
| **Impacted Architectural Nodes** | `47` nodes | 🌐 |
| **Breaking Change Risks** | `47` detected | ⚠️ Warning |

<details>
<summary><b>🔍 Touched Targets (57)</b></summary>

- `Cargo.lock`
- `Cargo.toml`
- `crates/strata-cli/Cargo.toml`
- `crates/strata-cli/src/commands/worker.rs`
- `crates/strata-cli/src/config.rs`
- `crates/strata-cli/src/main.rs`
- `crates/strata-cli/src/mcp/protocol.rs`
- `crates/strata-cli/src/mcp/server.rs`
- `crates/strata-cli/src/tui/theme.rs`
- `crates/strata-core/Cargo.toml`
- `crates/strata-core/src/blackboard.rs`
- `crates/strata-core/src/config.rs`
- `crates/strata-core/src/events.rs`
- `crates/strata-core/src/lib.rs`
- `crates/strata-core/src/schemas.rs`
- `crates/strata-core/src/state.rs`
- `crates/strata-core/src/traits.rs`
- `crates/strata-evals/src/scenarios/architecture_clustering.rs`
- `crates/strata-evals/src/scenarios/consolidation_ab_benchmark.rs`
- `crates/strata-evals/src/scenarios/hierarchical_episodic_pyramid.rs`
- `crates/strata-memory/Cargo.toml`
- `crates/strata-memory/src/call_graph.rs`
- `crates/strata-memory/src/community.rs`
- `crates/strata-memory/src/compiler.rs`
- `crates/strata-memory/src/consolidation.rs`
- `crates/strata-memory/src/context_rot.rs`
- `crates/strata-memory/src/embedding.rs`
- `crates/strata-memory/src/ipc.rs`
- `crates/strata-memory/src/lib.rs`
- `crates/strata-memory/src/metaplasticity.rs`
- `crates/strata-memory/src/pipeline.rs`
- `crates/strata-memory/src/procedural_mining.rs`
- `crates/strata-memory/src/pyramid.rs`
- `crates/strata-memory/src/retrieval.rs`
- `crates/strata-memory/src/spreading_activation.rs`
- `crates/strata-memory/src/store.rs`
- `crates/strata-memory/src/subconscious.rs`
- `crates/strata-memory/src/sync.rs`
- `crates/strata-memory/src/tests.rs`
- `crates/strata-memory/src/workspace.rs`
- `crates/strata-reasoning/Cargo.toml`
- `crates/strata-reasoning/src/adapters.rs`
- `crates/strata-reasoning/src/causal/graph.rs`
- `crates/strata-reasoning/src/mock.rs`
- `crates/strata-reasoning/src/planning/dag.rs`
- `crates/strata-reasoning/src/planning/decomposer.rs`
- `crates/strata-reasoning/src/planning/macros.rs`
- `crates/strata-reasoning/src/planning/recovery.rs`
- `crates/strata-reasoning/src/planning/types.rs`
- `crates/strata-reasoning/src/prompts.rs`
- `crates/strata-reasoning/src/self_editing.rs`
- `crates/strata-reasoning/src/training/types.rs`
- `crates/strata-tools/Cargo.toml`
- `crates/strata-tools/src/builtin.rs`
- `crates/strata-tools/src/gateway.rs`
- `crates/strata-tools/src/interceptor.rs`
- `crates/strata-tools/src/lib.rs`
</details>

<details>
<summary><b>🌲 Causal Dependency & Impact Ripple Tree (47 Direct, 0 Transitive)</b></summary>

| Node / Component | Kind | Distance | Coupling Weight | Breaking Risk |
| :--- | :--- | :--- | :--- | :--- |
| `File: crates/strata-cli/src/commands/worker.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-cli/src/main.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-cli/src/mcp/protocol.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-cli/src/mcp/server.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-cli/src/tui/theme.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-core/src/blackboard.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-core/src/config.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-core/src/events.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-core/src/schemas.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-core/src/state.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-core/src/traits.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-evals/src/scenarios/architecture_clustering.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-evals/src/scenarios/consolidation_ab_benchmark.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-evals/src/scenarios/hierarchical_episodic_pyramid.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/call_graph.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/community.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/compiler.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/consolidation.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/context_rot.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/embedding.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/ipc.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/lib.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/metaplasticity.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/pipeline.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/procedural_mining.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/pyramid.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/retrieval.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/spreading_activation.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/store.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/subconscious.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/sync.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/tests.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-memory/src/workspace.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-reasoning/src/adapters.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-reasoning/src/causal/graph.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-reasoning/src/mock.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-reasoning/src/planning/dag.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-reasoning/src/planning/decomposer.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-reasoning/src/planning/macros.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-reasoning/src/planning/recovery.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-reasoning/src/planning/types.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-reasoning/src/prompts.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-reasoning/src/self_editing.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-reasoning/src/training/types.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-tools/src/builtin.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-tools/src/interceptor.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |
| `File: crates/strata-tools/src/lib.rs` | `file` | Direct (d=1) | `100%` | ⚠️ **YES** |

</details>

### 🧠 Invariants & High-Importance Architectural Rules Checked

✅ **No contract invariants breached.** All high-importance architectural contracts and constraints remain intact.

### ⚠️ Known Failure Anti-Patterns & Mitigations

✅ **No known failure anti-patterns detected.** PR scope and touched modules do not match recurring failure signatures.

### 💡 Recommended Action

#### ⚠️ **Verdict: ATTENTION NEEDED**
This pull request introduces elevated ripple risk, potential contract violations, or touches sensitive architectural boundaries. Please review recommendations prior to merging.

**Actionable Recommendations:**
- 👉 Node 'Cargo.lock' not found in codebase causal graph.
- 👉 Node 'Cargo.toml' not found in codebase causal graph.
- 👉 Node 'crates/strata-cli/Cargo.toml' not found in codebase causal graph.
- 👉 ⚠️ Breaking Change Warning: One or more direct dependents have strict contract dependencies.
- 👉 Run targeted test suites covering: 1 direct dependent modules.
- 👉 Isolated node: modifying this component has zero upstream consumers.
- 👉 Node 'crates/strata-core/Cargo.toml' not found in codebase causal graph.
- 👉 Node 'crates/strata-memory/Cargo.toml' not found in codebase causal graph.
- 👉 Node 'crates/strata-reasoning/Cargo.toml' not found in codebase causal graph.
- 👉 Node 'crates/strata-tools/Cargo.toml' not found in codebase causal graph.
- 👉 Node 'crates/strata-tools/src/gateway.rs' not found in codebase causal graph.

---
*Automated review by [Strata Guard](https://github.com/phfarath/strata) • Cognitive Memory & Causal World Model Engine*

## Diff

The diff has 155881 characters, more than 120000. Its files:

- Cargo.lock
- Cargo.toml
- crates/strata-cli/Cargo.toml
- crates/strata-cli/src/commands/worker.rs
- crates/strata-cli/src/config.rs
- crates/strata-cli/src/main.rs
- crates/strata-cli/src/mcp/protocol.rs
- crates/strata-cli/src/mcp/server.rs
- crates/strata-cli/src/tui/theme.rs
- crates/strata-core/Cargo.toml
- crates/strata-core/src/blackboard.rs
- crates/strata-core/src/config.rs
- crates/strata-core/src/events.rs
- crates/strata-core/src/lib.rs
- crates/strata-core/src/schemas.rs
- crates/strata-core/src/state.rs
- crates/strata-core/src/traits.rs
- crates/strata-evals/src/scenarios/architecture_clustering.rs
- crates/strata-evals/src/scenarios/consolidation_ab_benchmark.rs
- crates/strata-evals/src/scenarios/hierarchical_episodic_pyramid.rs
- crates/strata-memory/Cargo.toml
- crates/strata-memory/src/call_graph.rs
- crates/strata-memory/src/community.rs
- crates/strata-memory/src/compiler.rs
- crates/strata-memory/src/consolidation.rs
- crates/strata-memory/src/context_rot.rs
- crates/strata-memory/src/embedding.rs
- crates/strata-memory/src/ipc.rs
- crates/strata-memory/src/lib.rs
- crates/strata-memory/src/metaplasticity.rs
- crates/strata-memory/src/pipeline.rs
- crates/strata-memory/src/procedural_mining.rs
- crates/strata-memory/src/pyramid.rs
- crates/strata-memory/src/retrieval.rs
- crates/strata-memory/src/spreading_activation.rs
- crates/strata-memory/src/store.rs
- crates/strata-memory/src/subconscious.rs
- crates/strata-memory/src/sync.rs
- crates/strata-memory/src/tests.rs
- crates/strata-memory/src/workspace.rs
- crates/strata-reasoning/Cargo.toml
- crates/strata-reasoning/src/adapters.rs
- crates/strata-reasoning/src/causal/graph.rs
- crates/strata-reasoning/src/mock.rs
- crates/strata-reasoning/src/planning/dag.rs
- crates/strata-reasoning/src/planning/decomposer.rs
- crates/strata-reasoning/src/planning/macros.rs
- crates/strata-reasoning/src/planning/recovery.rs
- crates/strata-reasoning/src/planning/types.rs
- crates/strata-reasoning/src/prompts.rs
- crates/strata-reasoning/src/self_editing.rs
- crates/strata-reasoning/src/training/types.rs
- crates/strata-tools/Cargo.toml
- crates/strata-tools/src/builtin.rs
- crates/strata-tools/src/gateway.rs
- crates/strata-tools/src/interceptor.rs
- crates/strata-tools/src/lib.rs
