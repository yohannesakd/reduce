# A dependency that the code does not need

**Signal.** The feature adds, imports, or keeps a dependency: a whole library for one call, a library for a language or platform feature, or a package that no reachable import uses.

```ts
import _ from "lodash";
const city = _.get(user, "address.city");
```

**Decide with.** Check the supported runtimes for the language or platform feature. If all of them support it, `reuse` the feature and remove the dependency.

```ts
const city = user?.address?.city;
```

Check that a reachable import needs each dependency. Separate production dependencies from test and build dependencies.
For each added dependency, check that it exists in its registry and is the intended package (`npm view <name> name version`). A name that does not resolve is a defect, not a reduction.
Most bloat is transitive. A study of 9,639 Maven artifacts found 2.7 percent of direct dependencies bloated and 57 percent of transitive ones.

**Keeps it when.** A reachable import needs it on a supported runtime, and the language, the platform, or an existing dependency does not give the same result there. Or the library carries tested edge-case behavior that the target needs.

**Sources.** [slopscore](../../sources/github/vinay-o-slopscore.md), [DepClean study](../../sources/papers/arxiv-2001.07808.md).
