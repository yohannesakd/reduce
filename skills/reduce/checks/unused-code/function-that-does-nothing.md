# A function that does nothing, a result that is fixed, or an empty handler

**Signal.** A function or handler that does nothing, or returns a fixed value on a production path: `pass`, an empty callback, a validator that always passes, a `TODO` stub, or mock data outside tests.

```python
def validate_email(email): pass
def dashboard_totals(): return {"orders": 1234, "revenue": 56789}
```

```ts
<button onClick={() => {}}>Export</button>
const isAllowed = (user: User) => true;
```

**Decide with.** Trace each unit to its callers and to what users see.

- A no-op with callers: the unit and its call sites form a group. They leave together, and no behavior changes.
- A placeholder chain that is fully wired and does nothing, such as a config value that reaches a manager whose `send` is empty: remove the whole chain in one phase.
- A hardcoded result that users see is observable behavior and probably a defect. Report it. Do not "reduce" it.

**Keeps it when.** A source marks it as a stub for planned work and the plan owner has not cancelled that work. Record that constraint, and mark the unit `unresolved` until the owner decides.

**Sources.** [sloppylint](../../sources/github/rsionnach-sloppylint.md), [slopscore](../../sources/github/vinay-o-slopscore.md), [Debloating post](../../sources/web/dev-to-maximsaplin-debloating-the-ai-grown-codebase-2om.md).
