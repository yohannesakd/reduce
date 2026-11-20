# phfarath/Strata commit 72045cc07e

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: phfarath
- Date: 2026-10-21
- Original location: https://github.com/phfarath/Strata/commit/72045cc07e8459ff97d861c46cffcac57b30d7ce
- Copied: 2026-11-20, from the commit data and diff of the GitHub API

## Text
refactor(workspace): remove dead code, unused deps and AI-slop (-1932 lines)

- Remove ~120 zero-reference pub fns/builders/consts across all 6 crates
  (verified workspace-wide via grep before each deletion)
- Remove orphaned ToolGateway abstraction (trait + DefaultToolGateway +
  gateway.rs + tests; MCP server hand-rolls its own dispatch)
- Drop unused deps: futures, tower-http (workspace), thiserror (memory,
  tools, reasoning, cli), anyhow (tools), hex (core)
- Remove unread config fields (SyncConfig.max_retries/base_backoff_ms,
  learning_rate_guidance, allowed_working_dirs) and dead EventStore::
  append_batch default method
- Apply clippy --fix + fmt (~70 mechanical warnings), collapse identical
  branches, paranoid guards, struct-literal instead of Default+assign
- Clean comments: emoji in tracing logs, trivial getter docs, docs
  restating fn signatures, duplicated banner line

Behavior locked: 354/354 tests green after every pass (4 gateway tests
removed with their subsystem); cargo fmt --check clean; clippy has only
design hints left (too-many-args, complex-type).

## Diff

The diff has 160632 characters, more than 120000. Its files:

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
- crates/strata-memory/src/alignment.rs
- crates/strata-memory/src/call_graph.rs
- crates/strata-memory/src/community.rs
- crates/strata-memory/src/compiler.rs
- crates/strata-memory/src/consolidation.rs
- crates/strata-memory/src/context_rot.rs
- crates/strata-memory/src/embedding.rs
- crates/strata-memory/src/ipc.rs
- crates/strata-memory/src/jtms.rs
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
- crates/strata-reasoning/src/causal/world_model.rs
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
