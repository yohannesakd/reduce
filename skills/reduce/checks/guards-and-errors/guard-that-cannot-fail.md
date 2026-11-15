# A guard that cannot fail, or the same guard repeated

**Signal.** A `try`/`catch` around code that does not throw, a null check on a value that a contract already fixes, or the same check on one value in several places.

```python
try:
    total = sum(item.price for item in items)   # items: list[Item], built by parse_cart()
except Exception:
    total = 0
```

```ts
if (rows && rows.length > 0) {
  const first = rows && rows.length ? rows[0] : null;
  if (first && first.id) use(first.id);
}
```

**Decide with.** State how the code inside could fail. If it cannot, `remove` the guard. If it can, name the failure and the layer that can decide what to do.
For repeated checks, find the producer. One check at the entry point, or a type, replaces the rest.

```python
# After: the entry point rejects bad input once. Inner code trusts the type.
def parse_cart(raw: dict) -> list[Item]: ...
total = sum(item.price for item in items)
```

**Keeps it when.** The call parses external input. A batch must continue after one item fails. A salvage path must read what it can from a failing source. A third-party API forces the catch.
Removing a catch that hides a real failure changes the observable result. Classify that result before you plan the removal.

**Sources.** [Anaconda](https://www.anaconda.com/blog/deslopping-ai-code), [HN: defensive code](https://news.ycombinator.com/item?id=45530486), [Dagster rules](https://dagster.io/blog/dignified-python-10-rules-to-improve-your-llm-agents).
