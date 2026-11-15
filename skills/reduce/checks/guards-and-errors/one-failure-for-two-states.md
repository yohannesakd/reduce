# One failure result stands for two different states

**Signal.** A helper returns the same value for a timeout and for an empty result, or an `except` returns a default that callers cannot tell from real data.

```python
def run_with_timeout(fn, seconds):
    try:
        return call_with_deadline(fn, seconds)
    except TimeoutError:
        return None          # callers cannot tell "timed out" from "no rows"
```

**Decide with.** This is not a reduction. A fix changes what callers see, so it is a behavior change. Record it as a suspected defect.
If the target's only purpose is to remove the helper, and the callers never read the distinction, the removal is still a contingent reduction until the callers are traced.

**Keeps it when.** Every caller treats both states the same way, and the trace shows that.

**Sources.** [Anaconda](https://www.anaconda.com/blog/deslopping-ai-code), [Silent Killers audit](https://ai.julianquick.com/ML/llm-audit.html).
