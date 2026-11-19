# Vue rules

**Signal.** The feature has `.vue` files. The driver gives this check and the JavaScript and TypeScript check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. Apply the rules to the composables and stores that the components use, too. The rules assume Vue 3.5. A rule that names a version needs it.

**Keeps it when.** The rule's **Keep when** holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

## Reactive state

- V1. Replace a ref and a watcher that only assigns a derived value with one `computed()`. `remove` [CO, WA]
- V2. Do not mutate state, send requests, or change the DOM in a `computed()` getter. `lead` [CO]
- V3. Do not assign to a computed value or to its properties. Change the source state. `lead` [CO]
- V4. Do not destructure primitive properties from a `reactive()` object. Use `ref()` for that state. `lead` [RE]
- V5. Remove explicit generics on `ref()` and `computed()` when inference gives the same type. `remove` [TS]
  Keep when: the type is wider than the initial value.

## Watchers

- V6. Replace `watch` with `immediate: true` and a source that the callback reads again with `watchEffect`. `simplify` [WA]
  Keep when: other state that the callback reads must not trigger it.
- V7. Remove `deep: true` when the callback reads known paths. Watch a getter for those paths. `simplify` [WA]
- V8. Read every dependency of a `watchEffect` before its first `await`. `lead` [WA]
- V9. Create each watcher synchronously in setup. `lead` [WA]
  Keep when: asynchronous creation is necessary; then stop the watcher yourself.
- V10. Stop asynchronous work that a watcher starts with `onWatcherCleanup` or `onCleanup`. `lead` [WA]

## Props, events, and v-model

- V11. Do not assign to a prop or to its nested fields. Emit an event. `lead` [PR, CA]
  Keep when: the parent and the child are tightly coupled by design.
- V12. Replace a copy of a prop that a watcher keeps in sync with the prop or a `computed()`. `remove` [PR]
- V13. Replace a `modelValue` prop, its `update:modelValue` emit, and a writable computed with `defineModel()`. `remove` Vue 3.4 [VM]
- V14. Use `defineProps<T>()` with destructured defaults. Remove `withDefaults` and duplicate runtime prop objects. `remove` Vue 3.5 [TS, PR]
- V15. Pass a destructured prop to `watch` or to a composable as a getter, `() => foo`. `lead` [PR]
- V16. Do not read or write child state through `$parent` or a template ref. Use props and emits. `lead` [CA, TR]

## Templates

- V17. Never put `v-if` and `v-for` on the same element. Filter in a `computed()`, or move `v-if` to a wrapper. `simplify` [ES]
- V18. Give each `v-for` a `:key` that is unique and stable for each item. `lead` [ES]
- V19. Move a template expression that does more than read or call one value into a `computed()` or a function. `simplify` [SR]

## Composables and shared state

- V20. Do not wrap stateless logic in a `use*` composable. Write a plain function. `remove` [CM]
- V21. Read ref, getter, and plain-value arguments with `toValue()`. Remove `isRef` branches. `simplify` [CM]
- V22. Return a plain object of refs from a composable. Do not return a `reactive()` object or a `.value` copy. `lead` [CM]
- V23. Call composables only synchronously, in `<script setup>` or `setup()`. `lead` [CM]
- V24. In a composable, remove each listener and timer that it adds, in `onUnmounted()`. `lead` [CM]
- V25. In server-rendered apps, do not keep per-user state in reactive module-scope singletons. Provide it per app, or use Pinia. `lead` [SM, SS]

**Sources.** Vue.js documentation, https://vuejs.org:
[ES] /style-guide/rules-essential.html. [SR] /style-guide/rules-strongly-recommended.html. [CA] /style-guide/rules-use-with-caution.html.
[RE] /guide/essentials/reactivity-fundamentals.html. [CO] /guide/essentials/computed.html. [WA] /guide/essentials/watchers.html.
[PR] /guide/components/props.html. [VM] /guide/components/v-model.html. [CM] /guide/reusability/composables.html.
[SM] /guide/scaling-up/state-management.html. [SS] /guide/scaling-up/ssr.html. [TS] /guide/typescript/composition-api.html. [TR] /guide/essentials/template-refs.html.
Licenses are in [rule sources](../../guides/rule-sources.md).
