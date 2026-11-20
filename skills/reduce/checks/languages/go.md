# Go rules

**Signal.** The feature has `.go` files. The driver gives this check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. gofmt owns the layout, so G2 to G6 of the general style do not apply. A rule that names a Go version needs that version in the `go` line of `go.mod`. The assert form is `panic`, only for states that only a bug produces. A failure that a caller can cause returns an `error`.

**Keeps it when.** The rule's **Unless** line holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

> Go is not Java. Stop writing interfaces for one struct, factories for zero values, and packages called `util`.
> `if err != nil { return fmt.Errorf("failed: %w", err) }` forty times is not error handling. It is noise with extra steps.
> A little copying is better than a little dependency.

## Errors and panics

- **GO1** Error returns for states that only a bug produces become one `panic`. Delete the callers' checks. `remove` [GBP]
- **GO2** Input, I/O, and other failures that a caller can cause return an `error`. Never panic for them. `lead` [CRC, GD, UB, EG]
  Unless: setup cannot continue, or a `Must` function runs at program start.
- **GO3** Never throw away a returned `error` with `_`. `lead` [CRC, EG]
- **GO4** Delete error wraps that only say that something failed. Return `err`. `remove` [GBP]
- **GO5** Log an error or return it. Never both. `remove` [GBP, UB]
- **GO6** Combine errors with `errors.Join` or several `%w`. No custom multi-error type. `reuse` Go 1.20 [GO]

## Control flow

- **GO7** No `else` after an `if` block that ends in `return`, `break`, `continue`, or `goto`. `simplify` [EG, CRC]
- **GO8** Invert an `if` that wraps the rest of a function or loop body. Return or continue early. `simplify` [CRC, UB]
- **GO9** An `if`-`else` that sets one variable in both arms is a default and one `if`. `simplify` [UB]
- **GO10** An `if`-`else if` chain on one value is a `switch`. Join shared cases with commas. `simplify` [EG]
- **GO11** Write counting loops as `for i := range n`. `simplify` Go 1.22 [GO, MOD]
- **GO12** No naked `return` in a function longer than a few lines. `lead` [CRC]

## Standard library

- **GO13** Delete `x := x` copies of loop variables. `remove` Go 1.22 [GO, MOD]
- **GO14** No hand-written min, max, contains, index, sort, or map-copy loops. Use builtins, `slices`, or `maps`. `reuse` Go 1.21 [GO, MOD]
- **GO15** `wg.Add(1)`, `go`, and `defer wg.Done()` are one `wg.Go`. `reuse` Go 1.25 [GO, MOD]
- **GO16** In tests, use `t.Context()` for contexts and `b.Loop()` for `b.N` loops. `reuse` Go 1.24 [GO, MOD]
- **GO17** `strings.Index` slicing is `strings.Cut`. `HasPrefix` plus `TrimPrefix` is `CutPrefix`. `reuse` Go 1.20 [MOD]

## Values and declarations

- **GO18** Build a struct with one composite literal. No field-by-field assignments, no setter wrappers. `simplify` [EG, GD]
- **GO19** Delete constructors and setup when the zero value is ready. A `sync.Mutex` field is a plain value. `remove` [EG, UB, PV]
- **GO20** Return a `nil` slice, not `[]T{}`. Test emptiness with `len(s) == 0`. `simplify` [CRC, GD, UB]
  Unless: the JSON output must be `[]`.
- **GO21** Pass small values directly. Do not use a pointer only to save bytes. `simplify` [CRC, GD]
- **GO22** Name getters `Owner()`, not `GetOwner()`. `lead` [EG]
- **GO23** No `init()` that does work beyond setting package variables to constants. `lead` [UB]
- **GO24** `context.Context` is the first parameter. Never store it in a struct. `lead` [CRC]

## Abstraction

- **GO25** Delete an interface declared next to its only implementation. Consumers use the concrete type, and declare an interface only when they need one. `remove` [GD, CRC, PV]
- **GO26** Delete type parameters that only one concrete type instantiates. `remove` [GD]
- **GO27** No `util`, `common`, or `helper` packages. Move each function into the package that uses it. `simplify` [GD, GBP]

## Concurrency

- **GO28** Every `go` statement has a visible exit: a cancelled context, a closed channel, or a waited `WaitGroup`. `lead` [CRC, UB]
- **GO29** Delete internal goroutines and channels when the caller only waits for the result. Return the result. `remove` [CRC]

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
