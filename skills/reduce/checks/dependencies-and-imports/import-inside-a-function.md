# An import inside a function

**Signal.** An `import` or `require` inside a function, with no stated reason.

```python
def parse(text):
    import re                 # inside the function, no stated reason
    return re.findall(r"\d+", text)
```

**Decide with.** Move the import to the top of the module unless it serves a purpose.

**Keeps it when.** A lazy import saves start-up time, loads an optional dependency, or breaks a circular import. State which.

**Sources.** [Sentry deslop](https://www.aitmpl.com/component/skill/deslop).
