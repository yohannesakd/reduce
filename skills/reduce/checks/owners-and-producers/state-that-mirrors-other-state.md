# State that mirrors other state

**Signal.** A second variable, store, or layer that copies a value another owner already holds.

```ts
const [isLoading, setIsLoading] = useState(false);
const query = useQuery(...);
useEffect(() => setIsLoading(query.status === "pending"), [query.status]);
```

**Decide with.** Trace the writers of the copy. If only the sync step writes it, derive the value where it is read: `const isLoading = query.status === "pending"`.
The effect, the state variable, and the render that follows the extra update all leave.
The two forms are not equal on every render. When `query.status` starts as `"pending"`, the copy is `false` on the first render and the derived value is `true`. The copy also lags by one render after each change.
Show that no consumer observes those values, such as a first-render flash, a test of the render count, or server output. If a consumer does, the change alters behavior. Classify it with [Fixed behavior](../../guides/fixed-behavior.md#fixed-behavior).

**Keeps it when.** The copy has a second writer, it must outlive the owner, or a consumer observes the first-render or lagging value.

**Sources.** [Debloating post](../../sources/web/dev-to-maximsaplin-debloating-the-ai-grown-codebase-2om.md).
