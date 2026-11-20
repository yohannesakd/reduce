# A fix at the call sites instead of the source

**Signal.** The same conversion, default, or normalization appears at several call sites, because the producer gives the wrong value.

```python
name = get_name(row).strip()        # call site 1
title = get_title(row).strip()      # call site 2
label = get_label(row).strip()      # call site 3
```

**Decide with.** Find the producer. If `get_*` returns untrimmed data because the source column has trailing spaces, one fix at the producer, or at the schema, removes all three call-site fixes.

```python
def get_value(row, key):
    return row[key].strip()
```

**Keeps it when.** Another consumer of the producer needs the raw value. Then the fix stays at the call sites that need it.

**Sources.** [Anaconda](../../sources/web/anaconda-com-blog-deslopping-ai-code.md).
