# JavaScript and TypeScript rules

**Signal.** The feature has `.js`, `.mjs`, `.cjs`, `.jsx`, `.ts`, `.mts`, `.cts`, `.tsx`, or `.vue` files. The driver gives this check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. The type rules apply to TypeScript only. TS9 and TS10 need `strict` and `noUncheckedIndexedAccess`: without them, a type can hide `undefined`, and the removal is wrong. `strict` is the default from TypeScript 6.0. The assert form is a thrown `Error`, or `assert` from `node:assert` in Node code.

**Keeps it when.** The rule's **Unless** line holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

> The type checker already proved it. Stop proving it again at runtime.
> Every `as`, `!`, and `any` is you losing an argument with the compiler and lying about it.
> If a line exists only to make you feel safe, delete it.

## Types that add nothing

- **TS1** Delete type assertions that do not change the type. `remove` [TE]
- **TS2** Do not annotate locals and parameters that a literal initializes. Inference is not a bug. `remove` [TE, G]
  Unless: the symbol is exported, and `isolatedDeclarations` needs the annotation.
- **TS3** Delete type arguments that equal the default. `remove` [TE]
- **TS4** A type parameter used once is not generic. Write the type, such as `unknown`. `remove` [TE]
- **TS5** Delete conversions that change nothing, such as `String(s)` on a string or `!!b` on a boolean. `remove` [TE]
- **TS6** Do not wrap one string in a template literal. `remove` [TE]
- **TS7** Write `x`, not `x === true`. Write `!x`, not `x === false`, when `x` is a `boolean`. `simplify` [TE]
- **TS8** Do not write `Object`, `{}`, `Function`, or `String` as types. Write the real shape. `lead` [TE]

## Checks that the types already prove

- **TS9** Delete conditions, guards, and `?.` on values that can never be nullish or falsy. `remove` [TE, TC]
- **TS10** Delete defaults for parameters and properties whose type excludes `undefined`. `remove` [TE]
  Unless: the runtime `.length` of the function matters, as in Express error handlers.
- **TS11** Write `a?.b?.c`, not `a && a.b && a.b.c`. `simplify` [TE]
- **TS12** Write `??`, not `||`, when only `null` or `undefined` must fall back. `simplify` [TE]
- **TS13** Write `.find(fn)`, not `.filter(fn)[0]`. `simplify` [TE]
  Unless: `fn` has side effects that must run for every element.

## Escape hatches

- **TS14** No `any`. Write `unknown`, and narrow it. `lead` [TE, G]
  Unless: an external package has no types. Then wrap it once, at the boundary.
- **TS15** No `!` non-null assertions. Narrow the value, or fix the type. `lead` [TE, G]
- **TS16** Do not cast an object literal with `as`. Annotate the variable. `lead` [G]
- **TS17** No `@ts-ignore` and no `@ts-nocheck`. `@ts-expect-error` only, with a reason. `lead` [TE]

## Async code

- **TS18** Await, return, or `.catch()` every promise. `void promise` is not handling it. `lead` [TE]
- **TS19** Do not pass a promise-returning function where a condition or a `void` callback goes. `lead` [TE]
- **TS20** Delete `async` from a function with no `await` that returns no promise. `remove` [TE]
- **TS21** Write `return await` inside `try`, inside a `catch` with a `finally`, and in `using` scopes. `lead` [TE]

## Errors

- **TS22** Throw and reject only `Error` instances. `lead` [TE, G]
- **TS23** Delete `catch` branches for values that are not `Error` instances. `remove` [G]
  Unless: the called API throws other values. Name it in a comment.
- **TS24** Delete a `try`/`catch` whose `catch` only throws the error again, or only logs it and throws it again. `remove` [ES]
- **TS25** Move statements that cannot throw out of the `try` block. `simplify` [G]

## Classes and modules

- **TS26** A class with only static members, or with no members, is a module. Export functions and constants. `remove` [TE, G]
- **TS27** Delete constructors that are empty or only pass their arguments to `super`. `remove` [TE, G]
  Unless: the constructor has parameter properties, a visibility modifier, or parameter decorators.
- **TS28** Delete getters and setters that only wrap a private field. Make the property public or `readonly`. `remove` [G]
- **TS29** No `namespace`. Use modules. `remove` [G]
  Unless: third-party code needs the namespace.
- **TS30** No `enum`. Write a union of string literals, or an `as const` object. `simplify` [TC, TR]
  Unless: the project does not set `erasableSyntaxOnly`, and other code depends on the enum's runtime object.
- **TS31** With `erasableSyntaxOnly`, no parameter properties, no `import =`, and no `export =`. `lead` TypeScript 5.8 [TC, TR]
- **TS32** Write `import type` and `export type` for names that are only types. `lead` [G, TC]
- **TS33** Delete unused variables, imports, and trailing unused parameters. `remove` [TE, G]
  Unless: a later parameter needs the position. Prefix the unused name with `_`.
- **TS34** No default exports. Use named exports. `lead` [G]
  Unless: a framework requires a default export, such as a route or page file.
- **TS35** Delete an `index.ts` that only re-exports its folder. Import from the file that defines the name. `remove` [RD]
  Unless: the folder is a published package entry point.

**Sources.**
[TE] typescript-eslint `strict-type-checked` and `stylistic-type-checked` configurations and rule pages, https://typescript-eslint.io/users/configs/ (v8).
[ES] ESLint `no-useless-catch`, https://eslint.org/docs/latest/rules/no-useless-catch.
[TC] TSConfig reference, https://www.typescriptlang.org/tsconfig/.
[TR] TypeScript 5.8 release notes, https://www.typescriptlang.org/docs/handbook/release-notes/typescript-5-8.html.
[G] Google TypeScript Style Guide, https://google.github.io/styleguide/tsguide.html.
[RD] Rule of reduce: step 1 of the [refactoring check](../every-feature/refactoring.md), applied to a layer that only forwards.
Licenses are in [rule sources](../../guides/rule-sources.md).
