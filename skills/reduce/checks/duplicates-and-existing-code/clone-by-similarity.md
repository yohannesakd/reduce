# A clone, by degree of similarity

**Signal.** Two units with similar structure. Classify the clone before you merge it.

| Type | Meaning | Decision |
| --- | --- | --- |
| I | Exact copy | Merge. |
| II | Same code with different names or literals | Merge with a parameter. |
| III | Same code with added or removed statements | Merge when the differences are data. |
| IV | Different code, same behavior | Merge only after an equivalence proof. |
| V | Similar shape, different reason to change | Never merge. |

```python
def retry_payment(fn):    # retries 3 times to keep the charge idempotent
    for _ in range(3): ...
def retry_cache_fill(fn): # retries 3 times because the cache may be cold
    for _ in range(3): ...
```

These two are Type V. They share a shape and no reason to change. A shared helper couples two policies, and the next change to one breaks the other.

**Decide with.** Textual tools find Types I to III. Embedding tools find candidates for Type IV, and each candidate needs a proof.
Ask what changes the first unit and what changes the second. If the answers differ, stop.

**Keeps it when.** The reasons to change differ.

**Sources.** [isomorphic simplify listing](https://x.com/doodlestein/status/2047808489838329993), [More Code, Less Reuse](https://arxiv.org/abs/2601.21276v1), [tef](https://programmingisterrible.com/post/139222674273/write-code-that-is-easy-to-delete-not-easy-to).
