# A layer that only passes calls or values through

**Signal.** A function, method, class, hook, or component that only forwards its inputs to one other call. A value that travels through layers that never read it. A class with one method, or with fields only.

```python
class UserService:
    def get(self, user_id):
        return self.repo.get(user_id)       # pass-through

def handler(req, ctx):                       # ctx is threaded to the leaf
    return service(req, ctx)
def service(req, ctx):
    return repo(req, ctx)
def repo(req, ctx):
    return db.get(req.id)                    # ctx never read
```

```tsx
const OrderCard = (props: CardProps) => <Card {...props} />;   // adds no behavior
```

**Decide with.** Does complexity vanish when the layer goes, or does it reappear in every caller?
Pass-through layers usually mean two adjacent layers hold the same abstraction. Merge them into one deeper module.
A class that does not earn its upkeep (a "lazy class") is deleted. A data class that other classes operate on can take that logic.

**Keeps it when.** The layer is a seam with two real adapters. A seam with one adapter is hypothetical.

**Sources.** [Ousterhout summary](../../sources/web/danlebrero-com-2021-02-24-philosophy-of-software-design-summary.md), [Refactoring.guru dispensables](../../sources/web/refactoring-guru-refactoring-smells-dispensables.md).
