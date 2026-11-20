# The feature and its parts go down the ladder

**Signal.** Every feature. Apply the ladder to the feature as a whole first, then to each part of its code: function, branch, guard, type, field, constant, file, and layer.

**Decide with.** Start with the whole feature. Ask whether a change at its producer, schema, configuration, or shared owner removes the need for the feature or for several of its parts.
Then take each part. Answer the questions of each rung in order, from `remove` down. Stop at the first rung that the evidence supports.

| Rung | Questions |
|---|---|
| `remove` | Which preserved result or structural benefit needs it? Which caller or test proves this? Does the complexity reappear in the callers when it goes? Does compatibility serve a concrete contract, audit need, or instruction? |
| `prevent` | Can a fix upstream remove the symptom? Can validation at the entry point or a type remove the checks inside? Does the design create the need because it cannot express the requirement? |
| `reuse` | Does existing code, the framework, or a dependency already own this responsibility? Can the callers move to one path, so that the old path goes in the same change? |
| `simplify` | Does it add a concept, layer, branch, or state that the `required` behavior does not need? Can a restructure make it smaller without less meaning? |
| `keep` | Every rung above fails with evidence that is specific to this feature or part. |
| `unresolved` | Name the missing evidence and the check that decides it. |

**Keeps it when.** Each higher rung fails with evidence. Record the rung for each part, or a supported `keep` with its reason.

**Sources.** These questions adapt [Dylan Garcia](../../sources/x/_dylanga-2117400205314421058.md) and [Jarred Sumner](../../sources/x/jarredsumner-2117037940031496252.md).
