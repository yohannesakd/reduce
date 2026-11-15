# A function that grew by accretion

**Signal.** One function holds many branches, and each requirement added more. Agents extend their own code this way.

```python
def handle(event):
    if event.type == "a":
        if event.flag:
            ...
        elif event.legacy:
            ...
    elif event.type == "b":
        ...      # six more branches
```

**Decide with.** Compare branches, concepts, locality, and reader effort before and after. Do not use line count alone.
A one-use helper that only moves branches does not reduce them. Keep it when a concrete improvement justifies the added name.
Where each branch is a distinct reason to change, a table or one function per case can express the same logic with fewer branches.

**Keeps it when.** The branches are the requirement, and each one maps to an inventory entry.

**Evidence.** In one benchmark of repeated extension tasks, complexity concentrated in functions that were already complex in 77 percent of runs. Agent code was 2.3 times more verbose than open-source code.

**Sources.** [SlopCodeBench](https://arxiv.org/abs/2603.24755), [sloppylint](https://github.com/rsionnach/sloppylint).
