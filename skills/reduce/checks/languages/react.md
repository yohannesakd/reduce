# React rules

**Signal.** The feature has `.jsx` or `.tsx` files, or JavaScript or TypeScript files that import `react`. The driver gives this check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. A rule that names a React version needs it. On an earlier version, the rule does not apply.

**Keeps it when.** The rule's **Unless** line holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

> You probably do not need an Effect. You definitely do not need three of them chained together.
> State that can be computed is a bug waiting for a sync to fail.
> Render is a pure function. Treat it like one or React will make you pay.

## Effects

- **R1** Delete an Effect that only sets state computed from props or state. Compute it during render. `remove`
  Unless: the value comes from a ref, such as a DOM measurement in `useLayoutEffect`.
- **R2** Do not reset state in an Effect when a prop changes. Put `key={thatProp}` on the child. `remove`
- **R3** Code that a user action causes goes in the event handler, not in an Effect. `remove`
  Unless: the code runs because the component appeared, such as an analytics event for a view.
- **R4** Call the parent's `onChange` in the handler that sets the state, not in an Effect. `remove`
- **R5** No chains of Effects that set state to trigger other Effects. Do one update in the handler. `remove`
  Unless: each step synchronizes with the network, such as dependent drop-down lists.
- **R6** No hand-written store subscriptions in an Effect. Use `useSyncExternalStore`. `simplify`
- **R7** Every Effect that fetches data needs a cleanup that ignores late responses. `lead`
- **R8** Call a `useEffectEvent` function only from Effects. Do not pass it down or list it as a dependency. `lead` React 19.2

## State

- **R9** Do not store state that props or other state can compute. `remove`
- **R10** Store the ID of the selected item, not a copy of the item. `simplify`
- **R11** Do not copy a prop into state with `useState(prop)`. `remove`
  Unless: the prop is named `initialX` or `defaultX`, and later changes must be ignored.
- **R12** Two booleans that can never both be true are one status union. `simplify`
- **R13** Do not call a state setter unconditionally during render. `lead`
  Unless: a comparison with the previous prop value guards the call.
- **R14** Do not mutate props, state, Hook arguments, Hook results, or values that JSX already received. `lead`

## Refs

- **R15** Do not read or write `ref.current` during render. `lead`
  Unless: `ref.current === null` guards a one-time lazy initialization.
- **R16** Delete `forwardRef`. `ref` is a normal prop. `remove` React 19
- **R17** Return a cleanup function from a ref callback. Do not handle a `null` call. `simplify` React 19

## Memoization

- **R18** With React Compiler, do not add `useMemo`, `useCallback`, or `memo` in new code. `remove` React Compiler 1.0
  Unless: the memoized value is an Effect dependency that must not change without cause.
- **R19** Without React Compiler, no `useMemo` unless a measurement shows a slow calculation. `remove`

## Components and Hooks

- **R20** Define components at module level. Never define a component inside another component. `lead`
- **R21** Render components with JSX. Never call a component function directly. `lead`
- **R22** Call Hooks at the top level, before any early return. Never in loops or conditions. `lead`
  Unless: the call is `use()`, which React 19 allows in conditions.
- **R23** Write `<Context value={v}>`, not `<Context.Provider value={v}>`. `remove` React 19
- **R24** Delete hand-written pending and error state of form submits. Use `useActionState` or form Actions. `remove` React 19
- **R25** Render `<title>`, `<meta>`, and `<link>` in the component, not from an Effect or a helper library. `remove` React 19
  Unless: the page needs metadata features that the built-in support does not give.
- **R26** A custom Hook that one component uses once is that component's code. Inline it. `simplify` [RD]
  Unless: it hides a subscription or Effect that the component would otherwise repeat.
- **R27** Give list items a stable `key` from the data. No array index when the list can reorder, insert, or delete. `lead`

**Sources.** [The React sources](../../sources/languages/react.md) give, for each rule, the copied text that supports it. Rules marked [RD] are rules of reduce. Licenses are in [rule sources](../../guides/rule-sources.md).
