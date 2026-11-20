# An unused export, parameter, field, or branch

**Signal.** An export, parameter, field, or branch that no caller in the feature uses, or that a tool reports as unused.

```ts
// src/format.ts
export function formatLegacyDate(d: Date): string { ... }   // no importer
```

**Decide with.** A tool finding is a candidate. Trace the users the tool cannot see:
dynamic loading (`React.lazy`, plugin registries), string references, `eval`, reflection, package entry points, generated callers, and platform-specific entry points.
An export from a package entry point is a public interface. Its consumers decide the class. See [evidence sources](../../evidence/tools-and-evidence.md#consumer-evidence).

**Keeps it when.** The export is public, or a loader reaches it by name.

**Sources.** [Knip comparison](../../sources/web/repowise-dev-blog-comparisons-knip-vs-ts-prune-vs-unimported.md), [Vulture overview](../../sources/web/repowise-dev-blog-comparisons-best-dead-code-detection-tools.md).
