# React rules

**Signal.** The feature has `.jsx` or `.tsx` files, or JavaScript or TypeScript files that import `react`. The driver gives this check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. The rules assume React 19. A rule that names a later version needs it.

**Keeps it when.** The rule's **Keep when** holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

## Effects

- R1. Remove an Effect that only sets state that props or state compute. Compute the value during render. `remove` [EF, LI]
  Keep when: the value comes from a ref, such as a DOM measurement in `useLayoutEffect`.
- R2. Replace an Effect that resets all state when a prop changes with `key={thatProp}` on the child. `remove` [EF]
- R3. Move code that a user action causes from an Effect into its event handler. `remove` [EF]
  Keep when: the code runs because the component appeared, such as an analytics event for a view.
- R4. Call the parent's `onChange` in the handler that sets the state, not in an Effect. `remove` [EF]
- R5. Replace a chain of Effects that set state to trigger other Effects with one update in the handler. `remove` [EF]
  Keep when: each step synchronizes with the network, such as dependent drop-down lists.
- R6. Replace a manual subscription to an external store in an Effect with `useSyncExternalStore`. `simplify` [EF]
- R7. Give every Effect that fetches data a cleanup that ignores late responses. `lead` [EF]
- R8. Call a `useEffectEvent` function only from Effects. Do not pass it down or list it in dependencies. `lead` React 19.2 [EE]

## State

- R9. Do not store state that props or other state can compute. `remove` [ST]
- R10. Store the ID of the selected item in state, not a copy of the item. `simplify` [ST]
- R11. Do not copy a prop into state with `useState(prop)`. `remove` [ST]
  Keep when: the prop is named `initialX` or `defaultX`, and later changes must be ignored.
- R12. Replace two booleans that must never both be true with one status union. `simplify` [ST]
- R13. Do not call a state setter unconditionally during render. `lead` [LI]
  Keep when: a comparison with the previous prop value guards the call.
- R14. Do not mutate props, state, Hook arguments, Hook results, or values that JSX already received. `lead` [RU, LI]

## Refs

- R15. Do not read or write `ref.current` during render. `lead` [LI]
  Keep when: `ref.current === null` guards a one-time lazy initialization.
- R16. Replace `forwardRef` wrappers with `ref` as a normal prop. `remove` [R19]
- R17. Return a cleanup function from a ref callback, in place of handling a `null` call. `simplify` [R19]

## Memoization

- R18. With React Compiler, do not add `useMemo`, `useCallback`, or `memo` in new code. `remove` [RC]
  Keep when: the memoized value is an Effect dependency that must not change without cause.
- R19. Without React Compiler, do not add `useMemo` unless a measurement shows a slow calculation. `remove` [EF]

## Components and Hooks

- R20. Define components at module level. Never define a component inside another component. `lead` [LI]
- R21. Render components with JSX. Never call a component function directly. `lead` [RU]
- R22. Call Hooks at the top level, before any early return, and never in loops or conditions. `lead` [RU]
  Keep when: the call is `use()`, which React 19 allows in conditions.
- R23. Render `<Context value={v}>` in place of `<Context.Provider value={v}>`. `remove` [R19]
- R24. Replace hand-written pending and error state of form submits with `useActionState` or form Actions. `remove` [R19]
- R25. Render `<title>`, `<meta>`, and `<link>` in the component, not from an Effect or a helper library. `remove` [R19]
  Keep when: the page needs metadata features that the built-in support does not give.

**Sources.**
[EF] https://react.dev/learn/you-might-not-need-an-effect.
[ST] https://react.dev/learn/choosing-the-state-structure.
[RU] https://react.dev/reference/rules.
[R19] https://react.dev/blog/2024/12/05/react-19.
[LI] https://react.dev/reference/eslint-plugin-react-hooks and its lint pages.
[EE] https://react.dev/reference/react/useEffectEvent and https://react.dev/blog/2025/10/01/react-19-2.
[RC] https://react.dev/learn/react-compiler/introduction and https://react.dev/blog/2025/10/07/react-compiler-1.
Licenses are in [rule sources](../../guides/rule-sources.md).
