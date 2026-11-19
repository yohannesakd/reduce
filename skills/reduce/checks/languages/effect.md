# Effect rules

**Signal.** The feature has JavaScript, TypeScript, or Vue files that import `effect` or an `@effect/` package. The driver gives this check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. The rules use Effect 4 names, and give the Effect 3 name where it differs. Use the names of the installed version.
The assert form is `Effect.die` or `Effect.orDie`, for states that only a bug produces. A failure that a caller can cause stays a typed error.

**Keeps it when.** The rule's **Keep when** holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

## Functions and generators

- E1. Do not write a function whose only body is `return Effect.gen(...)`. Use `Effect.fn("name")` or `Effect.fnUntraced`. `remove` [LL]
- E2. Make each `Effect.fn` name string equal to the name of the constant that it creates. `lead` [LL]
- E3. Pass more combinators as arguments of `Effect.fn`. Do not call `.pipe` on the function that it returns. `simplify` [LL]
- E4. Yield a tagged error directly, `yield* new E(...)`. Remove the `Effect.fail(...)` around it. `remove` [YE]
- E5. Write `return yield*` for each failure in a generator. A bare `yield*` failure does not narrow the types. `lead` [GE, LL]
- E6. Do not write type guards such as `isString` or `isRecord`. Use the `Predicate` module. `reuse` [LL]
- E7. Do not pass a named function point-free, as in `Effect.map(fn)`. Write `Effect.map((x) => fn(x))`. `lead` [CS]

## Errors

- E8. Declare each domain error as one tagged error class. Remove separate error type aliases and hand-written `_tag` fields. `remove` [YE, LL]
- E9. Give each tagged error class a tag that no other error class uses. `lead` [YE]
- E10. Replace a catch handler that switches on `_tag` with `Effect.catchTag` or `Effect.catchTags`. `simplify` [EX]
- E11. Model impossible states with `Effect.die` or `Effect.orDie`. Remove their typed error classes and handlers. `remove` [UN]
- E12. Do not catch defects or causes in domain logic: `catchDefect`, `catchCause`, or `exit` (v3: `catchAllDefect`, `catchAllCause`). `lead` [TW, UN]
  Keep when: the line is an application boundary or a test.
- E13. Wrap code that can throw in `Effect.try` or `Effect.tryPromise`. Use `Effect.sync` and `Effect.promise` only for code that cannot fail. `lead` [CR]
- E14. Replace hand-written retry and polling loops with `Effect.retry` or `Effect.repeat` and a schedule. `remove` [RT, SC]

## Services and layers

- E15. Define each service with the class form: `Context.Service` (v3: `Context.Tag` or `Effect.Service`). `simplify` [LL, MS]
- E16. Take a service type from its key. Do not write it again as an interface. `reuse` [LL, SV]
- E17. Give each service method the requirements type `never`. Move its dependencies into the layer that builds the service. `simplify` [LY]
- E18. Get a service with `yield* Service`, not with `Service.use(...)` or static accessors. `lead` [MS]
- E19. Create each layer value once, and reuse it. Do not call a layer factory twice for the same layer. `reuse` [LM, MM]
- E20. Compose the layers into one application layer, and provide it once. Remove sibling `Effect.provide` calls of the same layer. `remove` [MM, LM]

## Edges, resources, and input

- E21. Call `Effect.run*` only in entry points, framework handlers, and tests. Use `runMain` or `ManagedRuntime` there. `lead` [RN, CS, LL]
- E22. Release each resource with `Effect.acquireRelease` or `Effect.addFinalizer` in a scope. Remove manual `try`/`finally` cleanup. `remove` [RM]
- E23. Read settings through `Config`. Write `Config.withDefault` for absent values, not `Config.orElse`. `lead` [CF]
  Keep when: the code replaces invalid input on purpose.
- E24. Decode untrusted input with `Schema`, and take the types from it. Remove hand-written guards, parsers, and duplicate types. `remove` [LL, SH]
- E25. Give `Effect.all` and `Effect.forEach` a `concurrency` option when the effects are independent. They run in sequence by default. `lead` [CC]

**Sources.** Effect documentation, https://effect.website/docs/v4:
[GE] /getting-started/using-generators/. [CR] /getting-started/creating-effects/. [RN] /getting-started/running-effects/.
[TW] /error-management/two-error-types/. [EX] /error-management/expected-errors/. [YE] /error-management/yieldable-errors/. [UN] /error-management/unexpected-errors/. [RT] /error-management/retrying/.
[CS] /code-style/guidelines/. [SV] /requirements-management/services/. [LY] /requirements-management/layers/. [LM] /requirements-management/layer-memoization/.
[SC] /scheduling/using-schedules/. [RM] /resource-management/introduction/. [CF] /configuration/. [SH] /schema/introduction/. [CC] /concurrency/basic-concurrency/.
Effect repository, https://github.com/Effect-TS/effect: [LL] `LLMS.md`. [MS] `migration/services.md`. [MM] `migration/layer-memoization.md`.
Licenses are in [rule sources](../../guides/rule-sources.md).
