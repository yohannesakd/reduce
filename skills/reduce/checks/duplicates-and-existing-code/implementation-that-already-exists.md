# An implementation that already exists

**Signal.** New code does work that the language, platform, framework, a dependency, or other code in the repository already does. This includes a helper, a regular expression, a constant, a hand-written loop, or a small utility.

```python
# new, in utils.py
def run_with_timeout(fn, seconds): ...
# existing, in core/timeouts.py
def with_timeout(fn, seconds): ...
```

```ts
// new: a hand-written group-by, debounce, deep clone, or date format
const byDay = {}; for (const e of events) (byDay[e.day] ??= []).push(e);
// existing: Object.groupBy(events, e => e.day), or the project's own helper
```

**Decide with.** Search the repository by name, by behavior, and by body. Check language, platform, framework, and dependency capabilities on every supported runtime.
When documentation is unavailable, inspect the pinned source and record the limit.
Confirm that the existing implementation gives the required result for the inventory inputs, including its failure results. Reusing an implementation with the same flaw keeps the flaw.

**Keeps it when.** The existing implementation does not give every `required` result. Or it runs in another place with another user, directory, variables, PATH, or permissions, and no run there decides it.

**Sources.** [Anaconda](https://www.anaconda.com/blog/deslopping-ai-code), [More Code, Less Reuse](https://arxiv.org/abs/2601.21276v1), [GitClear](https://www.gitclear.com/ai_assistant_code_quality_2025_research).
