# A constant or helper with one user

**Signal.** A named constant, helper, wrapper, or small function that one place uses, and its name adds no meaning to that place.

```python
QUERY_TIMEOUT = 30           # used once, as a default argument
EMPTY_COMPLETION = ""        # used once, in one other module

def run_query(sql, timeout=QUERY_TIMEOUT): ...
```

```ts
const isEmptyName = (s: string) => s.trim() === "";   // one caller, in one form
```

**Decide with.** List the users. One user and a name that adds no meaning: inline it.
Docstrings, named constants, and `try` blocks added for the look of care follow the same test: what observable result changes without them?

```python
def run_query(sql, timeout=30): ...
```

**Keeps it when.** The name documents a value that the code does not explain, such as a limit from an API contract. A test patches it. Another place must change when the value changes, and the constant keeps those places equal.

**Sources.** [Anaconda](../../sources/web/anaconda-com-blog-deslopping-ai-code.md).
