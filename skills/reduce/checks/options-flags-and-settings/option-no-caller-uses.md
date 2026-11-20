# An option that no caller uses

**Signal.** A parameter that every caller passes with one value, or never passes. An interface with one implementation.

```python
def fetch(url, retries=3, backoff=None, jitter=False): ...
# every caller: fetch(url)
```

**Decide with.** Build the table of values that callers pass. A column with one value is a constant. A column that no caller sets is `remove`.

```python
def fetch(url): ...
```

**Keeps it when.** The function is a public interface. Then the options are behavior, and their consumers decide the class.

**Sources.** [Refactoring.guru: Speculative Generality](../../sources/web/refactoring-guru-refactoring-smells-dispensables.md), [Fowler on YAGNI](../../sources/web/martinfowler-com-bliki-yagni-html.md).
