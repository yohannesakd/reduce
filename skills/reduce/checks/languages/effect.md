# Effect rules

**Signal.** The feature has JavaScript, TypeScript, or Vue files that import `effect` or an `@effect/` package. The driver gives this check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. The rules use Effect 4 names, and give the Effect 3 name where it differs. Use the names of the installed version. The assert form is `Effect.die` or `Effect.orDie`, for states that only a bug produces. A failure that a caller can cause stays a typed error.

**Keeps it when.** The rule's **Unless** line holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

> Effect is not a personality. Pure code that cannot fail does not need to be an Effect.
> Run it once, at the edge. Every `runPromise` in the middle of your app is a leak in the abstraction you paid for.
> If the type says it cannot fail, stop catching it.

## Functions and generators

- **E1** No function whose only body is `return Effect.gen(...)`. Use `Effect.fn("name")` or `Effect.fnUntraced`. `remove` [LL]
- **E2** The `Effect.fn` name string equals the name of the constant that it creates. `lead` [LL]
- **E3** Pass combinators as arguments of `Effect.fn`. Do not call `.pipe` on the function that it returns. `simplify` [LL]
- **E4** Yield a tagged error directly, `yield* new E(...)`. Delete the `Effect.fail(...)` around it. `remove` [YE]
- **E5** Write `return yield*` for each failure in a generator. A bare `yield*` does not narrow the types. `lead` [GE, LL]
- **E6** No hand-written type guards such as `isString` or `isRecord`. Use the `Predicate` module. `reuse` [LL]
- **E7** No point-free named functions, as in `Effect.map(fn)`. Write `Effect.map((x) => fn(x))`. `lead` [CS]
- **E8** Do not wrap pure synchronous code that cannot fail in an Effect. Return the value. `remove` [RD]
  Unless: the code reads a service, a clock, or randomness that tests must control.

## Errors

- **E9** One tagged error class for each domain error. Delete error type aliases and hand-written `_tag` fields. `remove` [YE, LL]
- **E10** Every tagged error class has its own tag. `lead` [YE]
- **E11** No catch handler that switches on `_tag`. Use `Effect.catchTag` or `Effect.catchTags`. `simplify` [EX]
- **E12** Impossible states are defects: `Effect.die` or `Effect.orDie`. Delete their typed error classes and handlers. `remove` [UN]
- **E13** Do not catch defects or causes in domain logic: `catchDefect`, `catchCause`, or `exit` (v3: `catchAllDefect`, `catchAllCause`). `lead` [TW, UN]
  Unless: the line is an application boundary or a test.
- **E14** Code that can throw goes in `Effect.try` or `Effect.tryPromise`. `Effect.sync` and `Effect.promise` are only for code that cannot fail. `lead` [CR]
- **E15** No hand-written retry or polling loops. Use `Effect.retry` or `Effect.repeat` with a schedule. `remove` [RT, SC]

## Services and layers

- **E16** Define each service with the class form: `Context.Service` (v3: `Context.Tag` or `Effect.Service`). `simplify` [LL, MS]
- **E17** Take a service type from its key. Do not write it again as an interface. `reuse` [LL, SV]
- **E18** Service methods have the requirements type `never`. Dependencies go in the layer that builds the service. `simplify` [LY]
- **E19** Get a service with `yield* Service`, not `Service.use(...)` or static accessors. `lead` [MS]
- **E20** Create each layer value once, and reuse it. Do not call a layer factory twice for the same layer. `reuse` [LM, MM]
- **E21** Compose one application layer, and provide it once. Delete sibling `Effect.provide` calls of the same layer. `remove` [MM, LM]
- **E22** A service with one implementation and no test double is a module. Export the functions. `remove` [RD]
  Unless: the service owns a resource, configuration, or a lifecycle that a layer must build.

## Edges, resources, and input

- **E23** Call `Effect.run*` only in entry points, framework handlers, and tests. Use `runMain` or `ManagedRuntime` there. `lead` [RN, CS, LL]
- **E24** Release resources with `Effect.acquireRelease` or `Effect.addFinalizer` in a scope. Delete manual `try`/`finally` cleanup. `remove` [RM]
- **E25** Read settings through `Config`. Write `Config.withDefault` for absent values, not `Config.orElse`. `lead` [CF]
  Unless: the code replaces invalid input on purpose.
- **E26** Decode untrusted input with `Schema`, and take the types from it. Delete hand-written guards, parsers, and duplicate types. `remove` [LL, SH]
- **E27** Give `Effect.all` and `Effect.forEach` a `concurrency` option when the effects are independent. The default is one at a time. `lead` [CC]

**Sources.** Effect documentation, https://effect.website/docs/v4:
[GE] /getting-started/using-generators/. [CR] /getting-started/creating-effects/. [RN] /getting-started/running-effects/.
[TW] /error-management/two-error-types/. [EX] /error-management/expected-errors/. [YE] /error-management/yieldable-errors/. [UN] /error-management/unexpected-errors/. [RT] /error-management/retrying/.
[CS] /code-style/guidelines/. [SV] /requirements-management/services/. [LY] /requirements-management/layers/. [LM] /requirements-management/layer-memoization/.
[SC] /scheduling/using-schedules/. [RM] /resource-management/introduction/. [CF] /configuration/. [SH] /schema/introduction/. [CC] /concurrency/basic-concurrency/.
Effect repository, https://github.com/Effect-TS/effect: [LL] `LLMS.md`. [MS] `migration/services.md`. [MM] `migration/layer-memoization.md`.
[RD] Rule of reduce: steps 1 and 2 of the [refactoring check](../every-feature/refactoring.md).
Licenses are in [rule sources](../../guides/rule-sources.md).
