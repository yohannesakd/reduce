# A comment or document that repeats the code, tells history, or hedges

**Signal.** A comment, docstring, or documentation passage restates the code, narrates a change, admits doubt, or describes code that is gone.

```python
# Maximum number of retries
MAX_RETRIES = 3

def get_user(user_id):
    """Get user."""
    ...

# Removed the legacy cache path in PR 123.
x = calculate()  # should work hopefully
```

**Decide with.** Compare each passage with the code that it describes. A comment's claim is not proof. Then apply the rungs:

| Rung | Text decision |
|---|---|
| `remove` | It repeats or contradicts the code, is commented-out code, describes obsolete behavior, or tells history that no reader needs. |
| `prevent` | A name, a type, validation, or a fix to the underlying lint or type error expresses the constraint. |
| `reuse` | Refer to the existing documentation. |
| `simplify` | Shorten it to the constraint or the reason. |
| `keep` | It states a constraint or reason that is not obvious from the code. |

A hedge is different: it marks a claim that nobody verified. Trace what `calculate()` must return, and put that claim in the proof map. Do not delete the hedge as if it were noise.
When a task deletes code, the documentation describes the current state, not the deletion. Change behavior documentation together with its behavior.

```diff
- The `legacy_sync` endpoint was removed in v3 because clients moved to `/sync`.
+ Clients call `/sync`.
```

**Keeps it when.** The text states a constraint or reason that code cannot express, or readers need it: a contract, usage, operations, or a notice. A migration guide or changelog is the contract for readers who upgrade, so it keeps its history.

**Sources.** [Anaconda](https://www.anaconda.com/blog/deslopping-ai-code), [@quasicoh](https://x.com/quasicoh/status/2100393667311906993), [sloppylint](https://github.com/rsionnach/sloppylint).
