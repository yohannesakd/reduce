# A suppression directive that hides a cause

**Signal.** `# noqa`, `eslint-disable`, `@ts-ignore`, `as any`, or a cast that silences a real finding or type error.

```python
try:
    row = db.fetch(key)
except DatabaseError as e:
    raise RetryableError("failed")   # noqa: B904
```

**Decide with.** Find what the rule found. `B904` reports a `raise` inside `except` with no explicit cause. The suppression sits on the `raise` line.
Python already keeps the original error as `__context__`. `raise ... from e` also sets `__cause__` and `__suppress_context__`. `raise ... from None` keeps `__context__`, leaves `__cause__` empty, and sets `__suppress_context__`.
The forms differ in `__cause__` or in the traceback text.
Choose the form that keeps the observable result. If a caller or a log reads the chain, a change is a behavior change. Report it separately.
Prove that the suppressed problem no longer occurs before you plan the removal. Remove a cast by fixing the type that it hides.

**Keeps it when.** The directive states why it is necessary, and the trace agrees.

**Sources.** [Anaconda](https://www.anaconda.com/blog/deslopping-ai-code), [Sentry deslop](https://www.aitmpl.com/component/skill/deslop), [HN: defensive code](https://news.ycombinator.com/item?id=45530486).
