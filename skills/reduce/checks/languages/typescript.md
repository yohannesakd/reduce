# JavaScript and TypeScript rules

**Signal.** The feature has `.js`, `.mjs`, `.cjs`, `.jsx`, `.ts`, `.mts`, `.cts`, `.tsx`, or `.vue` files. The driver gives this check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. The type rules apply to TypeScript only.
TS8 and TS9 need `strict` and `noUncheckedIndexedAccess`. Without them, a type can hide `undefined`, and a removal is wrong. `strict` is the default from TypeScript 6.0.
The assert form is a thrown `Error`, or `assert` from `node:assert` in Node code.

**Keeps it when.** The rule's **Keep when** holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

## Types that add nothing

- TS1. Remove a type assertion that does not change the type of the expression. `remove` [TE]
- TS2. Remove type annotations on locals and parameters that a literal initializes. `remove` [TE, G]
  Keep when: the symbol is exported, and `isolatedDeclarations` needs the annotation.
- TS3. Remove type arguments that equal the default of their type parameter. `remove` [TE]
- TS4. Remove a type parameter that the signature uses once. Write the type, such as `unknown`, in its place. `remove` [TE]
- TS5. Remove conversions, such as `String(s)` or `!!b`, that change neither the type nor the value. `remove` [TE]
- TS6. Replace a template literal that only wraps one string expression with the expression. `remove` [TE]
- TS7. Write `x` for `x === true` and `!x` for `x === false` when `x` is a `boolean`. `simplify` [TE]

## Checks that the types already prove

- TS8. Remove conditions, guards, and `?.` on values whose type is never nullish or falsy. `remove` [TE, TC]
- TS9. Remove default values of parameters and properties whose type excludes `undefined`. `remove` [TE]
  Keep when: the runtime `.length` of the function matters, as in Express error handlers.
- TS10. Replace `a && a.b && a.b.c` with `a?.b?.c`. `simplify` [TE]
- TS11. Write `??` in place of `||` when only `null` or `undefined` must select the fallback. `simplify` [TE]
- TS12. Replace `.filter(fn)[0]` with `.find(fn)`. `simplify` [TE]
  Keep when: `fn` has side effects that must run for every element.

## Escape hatches

- TS13. Do not write `any`. Write `unknown`, and narrow it. `lead` [TE, G]
  Keep when: an external package has no types.
- TS14. Do not write the `!` non-null assertion. Narrow the value, or fix the type. `lead` [TE, G]
- TS15. Do not assert an object literal with `as`. Annotate the type of the variable. `lead` [G]
- TS16. Do not write `@ts-ignore` or `@ts-nocheck`. Write `@ts-expect-error` only with a reason. `lead` [TE]

## Async code

- TS17. Await, return, or `.catch()` every promise. `void promise` does not handle the rejection. `lead` [TE]
- TS18. Do not pass a function that returns a promise where a condition or a `void` callback is expected. `lead` [TE]
- TS19. Remove `async` from a function that has no `await` and returns no promise. `remove` [TE]
- TS20. Write `return await` inside `try`, inside `catch` that has a `finally`, and in `using` scopes. `lead` [TE]

## Errors

- TS21. Throw and reject only with `Error` instances. `lead` [TE, G]
- TS22. Remove `catch` branches that handle values that are not `Error` instances. `remove` [G]
  Keep when: the called API throws other values; write a comment that names it.
- TS23. Move statements that cannot throw out of the `try` block. `simplify` [G]

## Classes and modules

- TS24. Replace a class that has only static members, or no members, with exported functions and constants. `remove` [TE, G]
- TS25. Remove a constructor that is empty or only passes its arguments to `super`. `remove` [TE, G]
  Keep when: the constructor has parameter properties, a visibility modifier, or parameter decorators.
- TS26. Replace a getter and setter that only wrap a private field with a public or `readonly` property. `remove` [G]
- TS27. Do not write `namespace`. Use modules. `remove` [G]
  Keep when: third-party code needs the namespace.
- TS28. With `erasableSyntaxOnly`, do not write `enum`, parameter properties, `import =`, or `export =`. `lead` TypeScript 5.8 [TC, TR]
- TS29. Write `import type` and `export type` for names that the module uses only as types. `lead` [G, TC]
- TS30. Remove unused variables, imports, and trailing unused parameters. `remove` [TE, G]
  Keep when: a later parameter needs the position; prefix the unused name with `_`.
- TS31. Do not write default exports. Use named exports. `lead` [G]
  Keep when: a framework requires a default export, such as a route or page file.

**Sources.**
[TE] typescript-eslint `strict-type-checked` and `stylistic-type-checked` configurations and rule pages, https://typescript-eslint.io/users/configs/ (v8).
[TC] TSConfig reference, https://www.typescriptlang.org/tsconfig/.
[TR] TypeScript 5.8 release notes, https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-8.html.
[G] Google TypeScript Style Guide, https://google.github.io/styleguide/tsguide.html.
Licenses are in [rule sources](../../guides/rule-sources.md).
