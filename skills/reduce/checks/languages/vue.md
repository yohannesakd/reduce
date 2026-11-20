# Vue rules

**Signal.** The feature has `.vue` files. The driver gives this check and the JavaScript and TypeScript check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. Apply the rules to the composables and stores that the components use, too. The rules assume Vue 3.5. A rule that names a version needs it.

**Keeps it when.** The rule's **Unless** line holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

> A watcher that copies one value into another is a `computed` that you were too lazy to write.
> Props go down. Events go up. Anything else is spaghetti with a reactivity system.
> A composable with no state is a function wearing a costume.

## Reactive state

- **V1** A ref plus a watcher that only assigns a derived value is one `computed()`. `remove`
- **V2** No side effects in a `computed()` getter: no state changes, no requests, no DOM. `lead`
- **V3** Do not assign to a computed value or its properties. Change the source. `lead`
- **V4** Do not destructure primitive properties from a `reactive()` object. Use `ref()` for that state. `lead`
- **V5** Delete explicit generics on `ref()` and `computed()` when inference gives the same type. `remove`
  Unless: the type is wider than the initial value.

## Watchers

- **V6** A `watch` with `immediate: true` whose callback reads its source again is a `watchEffect`. `simplify`
  Unless: other state that the callback reads must not trigger it.
- **V7** No `deep: true` when the callback reads known paths. Watch a getter for those paths. `simplify`
- **V8** Read every dependency of a `watchEffect` before its first `await`. `lead`
- **V9** Create watchers synchronously in setup. `lead`
  Unless: asynchronous creation is necessary. Then stop the watcher yourself.
- **V10** Stop the async work that a watcher starts, with `onWatcherCleanup` or `onCleanup`. `lead`

## Props, events, and v-model

- **V11** Never assign to a prop or its nested fields. Emit an event. `lead`
  Unless: the parent and the child are tightly coupled by design.
- **V12** Delete a copy of a prop that a watcher keeps in sync. Use the prop or a `computed()`. `remove`
- **V13** A `modelValue` prop, its `update:modelValue` emit, and a writable computed are one `defineModel()`. `remove` Vue 3.4
- **V14** Use `defineProps<T>()` with destructured defaults. Delete `withDefaults` and duplicate runtime prop objects. `remove` Vue 3.5
- **V15** Pass a destructured prop to `watch` or to a composable as a getter, `() => foo`. `lead`
- **V16** Do not reach into a child through `$parent` or a template ref. Use props and emits. `lead`
  Unless: the parent and the child are tightly coupled by design.

## Templates

- **V17** Never put `v-if` and `v-for` on the same element. Filter in a `computed()`, or move `v-if` to a wrapper. `simplify`
- **V18** Every `v-for` gets a `:key` that is unique and stable for each item. `lead`
- **V19** A template expression that does more than read or call one value goes in a `computed()` or a function. `simplify`

## Composables and shared state

- **V20** Do not wrap stateless logic in a `use*` composable. Write a plain function. `remove`
- **V21** Read ref, getter, and plain-value arguments with `toValue()`. Delete `isRef` branches. `simplify`
- **V22** Return a plain object of refs from a composable. Not a `reactive()` object, not a `.value` copy. `lead`
- **V23** Call composables only synchronously, in `<script setup>` or `setup()`. `lead`
  Unless: a lifecycle hook, such as `onMounted()`, calls the composable.
- **V24** A composable removes every listener and timer that it adds, in `onUnmounted()`. `lead`
- **V25** In server-rendered apps, no per-user state in reactive module-scope singletons. Provide it per app, or use Pinia. `lead`
- **V26** A composable that one component calls once is that component's code. Inline it. `simplify` [RD]
  Unless: it owns a subscription, a timer, or a listener with its cleanup.
- **V27** Do not put state in a Pinia store when one component and its children use it. Keep it in the component. `remove` [RD]
  Unless: the state must survive the component, or a server render must hydrate it.

**Sources.** [The Vue sources](../../sources/languages/vue.md) give, for each rule, the copied text that supports it. Rules marked [RD] are rules of reduce. Licenses are in [rule sources](../../guides/rule-sources.md).
