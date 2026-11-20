# A second copy next to the first

**Signal.** Two implementations of one behavior live side by side: an old and a new version, a copy that stays after the callers moved, or mocks and fixtures for an interface that is gone.

```text
src/userService.ts        # exported, 2 callers left
src/userService_v2.ts     # exported, 14 callers
tests/__mocks__/userServiceV1.ts
```

The names do not always show it. Compare by behavior:

```ts
function formatPrice(cents) { ... }              // 3 callers
function formatAmount(cents, currency) { ... }  // 9 callers; same result for USD
```

Other forms: two loaders for one configuration file, two components that render the same card, or two clients for one API.

**Decide with.** Run a call-site census of both. Move the remaining callers to one path. Delete the other path, its mocks, and its tests in the same phase
when no concrete compatibility contract requires both paths.
The result keeps the original name. Do not create a new `_v2` name.

**Keeps it when.** The old path is a public interface with outside consumers. Then its behavior entry is `unknown` and the unit is `unresolved` until the consumer evidence decides.

**Sources.** [isomorphic simplify listing](../../sources/x/doodlestein-2047808489838329993.md), [Karpathy](../../sources/x/karpathy-2015883857489522876.md), [vendor write-up](../../sources/web/digitalelliptical-com-blog-ai-generated-code-at-scale-preventing-maintenance-collapse.md).
