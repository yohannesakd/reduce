# Go rules

**Signal.** The feature has `.go` files. The driver gives this check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. gofmt owns the layout, so G2 to G6 of the general style do not apply. A rule that names a Go version needs that version in the `go` line of `go.mod`.
The assert form is `panic`, only for states that only a bug produces. A failure that a caller can cause returns an `error`.

**Keeps it when.** The rule's **Keep when** holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

## Errors and panics

- GO1. Replace error returns for unreachable states or API misuse with one `panic`. Remove the callers' checks. `remove` [GBP]
- GO2. Return an `error` for input, I/O, and other failures that a caller can cause. Do not panic. `lead` [CRC, GD, UB, EG]
  Keep when: setup cannot continue, or a `Must` function runs at program start.
- GO3. Never discard a returned `error` with `_`. `lead` [CRC, EG]
- GO4. Remove error wraps that only say that something failed. Return `err` unchanged. `remove` [GBP]
- GO5. Do not log an error and also return it. `remove` [GBP, UB]
- GO6. Combine errors with `errors.Join` or several `%w`, not a custom multi-error type. `reuse` Go 1.20 [GO]

## Control flow

- GO7. Remove `else` after an `if` block that ends in `return`, `break`, `continue`, or `goto`. `simplify` [EG, CRC]
- GO8. Invert an `if` that wraps the rest of a function or loop body. Return or continue early. `simplify` [CRC, UB]
- GO9. Replace an `if`-`else` that sets one variable in both arms with a default and one `if`. `simplify` [UB]
- GO10. Replace an `if`-`else if` chain on one value with a `switch`. Join shared cases with commas. `simplify` [EG]
- GO11. Write counting loops as `for i := range n`. `simplify` Go 1.22 [GO, MOD]

## Standard library

- GO12. Remove `x := x` copies of loop variables. `remove` Go 1.22 [GO, MOD]
- GO13. Replace hand-written min, max, contains, index, sort, and map-copy loops with builtins, `slices`, or `maps`. `reuse` Go 1.21 [GO, MOD]
- GO14. Replace `wg.Add(1)`, `go`, and `defer wg.Done()` with `wg.Go`. `reuse` Go 1.25 [GO, MOD]
- GO15. In tests, use `t.Context()` for contexts and `b.Loop()` for `b.N` loops. `reuse` Go 1.24 [GO, MOD]
- GO16. Replace `strings.Index` slicing with `strings.Cut`, and `HasPrefix` with `TrimPrefix` with `CutPrefix`. `reuse` Go 1.20 [MOD]

## Values and declarations

- GO17. Build a struct with one composite literal, not field assignments or setter wrappers. `simplify` [EG, GD]
- GO18. Remove constructors and setup when the zero value is ready. Declare a `sync.Mutex` field as a plain value. `remove` [EG, UB, PV]
- GO19. Return a `nil` slice, not `[]T{}`, and test emptiness with `len(s) == 0`. `simplify` [CRC, GD, UB]
  Keep when: the JSON output must be `[]`.
- GO20. Pass small values directly. Do not use a pointer only to save bytes. `simplify` [CRC, GD]

## Abstraction

- GO21. Remove an interface that is declared next to its only implementation. Consumers use the concrete type. `remove` [GD, CRC, PV]
- GO22. Remove type parameters that only one concrete type instantiates. `remove` [GD]
- GO23. Move functions out of `util`, `common`, and `helper` packages into the package that uses them. `simplify` [GD, GBP]

## Concurrency

- GO24. Give every `go` statement a visible exit: a cancelled context, a closed channel, or a waited `WaitGroup`. `lead` [CRC, UB]
- GO25. Remove internal goroutines and channels when the caller only waits for the result. Return the result directly. `remove` [CRC]

**Sources.**
[EG] Effective Go, https://go.dev/doc/effective_go.
[CRC] Go Code Review Comments, https://go.dev/wiki/CodeReviewComments.
[GD] Google Go Style decisions, https://google.github.io/styleguide/go/decisions.
[GBP] Google Go Style best practices, https://google.github.io/styleguide/go/best-practices.
[UB] Uber Go Style Guide, https://github.com/uber-go/guide/blob/master/style.md.
[PV] Go Proverbs, https://go-proverbs.github.io/.
[GO] Go release notes, https://go.dev/doc/go1.20 to https://go.dev/doc/go1.26.
[MOD] The `modernize` analyzers, https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize.
Licenses are in [rule sources](../../guides/rule-sources.md).
