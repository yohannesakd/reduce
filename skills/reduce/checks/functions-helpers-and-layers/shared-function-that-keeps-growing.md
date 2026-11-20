# A shared function whose parameters and branches keep growing

**Signal.** A helper that every new requirement extended with another flag.

```python
def render(item, mode=None, legacy=False, compact=False, with_tags=True): ...
# three callers, each passes a fixed combination
```

**Decide with.** List the argument combinations that the callers pass. If each caller uses one fixed combination, inline the function into each caller and delete the options that the caller does not use.
Then look for what the callers still share. The shared part is often small and has a plain name. A wrong abstraction is cheaper to undo than to extend.

**Keeps it when.** The callers use the same behavior, no flag differs between them, and one reason changes all of them. The abstraction then has a single reason to change.

**Sources.** [Sandi Metz summaries](../../sources/web/understandlegacycode-com-blog-refactoring-rule-of-three.md), [nwiizo](../../sources/x/nwiizo-2115387095548354712.md), [Fowler on YAGNI](../../sources/web/martinfowler-com-bliki-yagni-html.md).
