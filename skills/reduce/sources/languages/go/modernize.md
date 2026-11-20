# modernize analyzer documentation

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Go Authors
- Date: 2026-11-17
- License: BSD-3-Clause
- Original location: https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
## Documentation
      [¶](#section-documentation)

### Overview [¶](#pkg-overview)

Package modernize provides a suite of analyzers that suggest simplifications to Go code, using modern language and library features.

Each diagnostic provides a fix. Our intent is that these fixes may be safely applied en masse without changing the behavior of your program. In some cases the suggested fixes are imperfect and may lead to (for example) unused imports or unused local variables, causing build breakage. However, these problems are generally trivial to fix. We regard any modernizer whose fix changes program behavior to have a serious bug and will endeavor to fix it.

Since Go 1.26, the 'go fix' command has included the modernize suite, so to apply all modernization fixes en masse, you can use the following command:

$ go fix ./...

If you need to run a modernizer added or modified since the Go release, you can use this standalone command:

$ go run golang.org/x/tools/go/analysis/passes/modernize/cmd/modernize@latest -fix ./...

If the tool warns of conflicting fixes, you may need to run it more than once until it has applied all fixes cleanly. This command is not an officially supported interface and may change in the future.

Changes produced by this tool should be reviewed as usual before being merged. In some cases, a loop may be replaced by a simple function call, causing comments within the loop to be discarded. Human judgment may be required to avoid losing comments of value.

The modernize suite contains many analyzers. Diagnostics from some, such as "any" (which replaces "interface{}" with "any" where it is safe to do so), are particularly numerous. It may ease the burden of code review to apply fixes in two steps, the first consisting only of fixes from the "any" analyzer, the second consisting of all other analyzers. This can be achieved using flags, as in this example:

$ modernize -any=true  -fix ./...
$ modernize -any=false -fix ./...

#### Analyzer appendclipped [¶](#hdr-Analyzer_appendclipped)

appendclipped: simplify append chains using slices.Concat

The appendclipped analyzer suggests replacing chains of append calls with a single call to slices.Concat, which was added in Go 1.21. For example, append(append(s, s1...), s2...) would be simplified to slices.Concat(s, s1, s2).

In the simple case of appending to a newly allocated slice, such as append(\[\]T(nil), s...), the analyzer suggests the more concise slices.Clone(s). For byte slices, it will prefer bytes.Clone if the "bytes" package is already imported.

Since the replacement (slices.Concat, or slices.Clone) allocates a new slice, any slices.Clone or bytes.Clone wrapping one of the operands is redundant and is removed, e.g. append(append(\[\]T{}, slices.Clone(s)...), t...) becomes slices.Concat(s, t). The clone of os.Environ in append(\[\]string(nil), os.Environ()...) is likewise elided.

This fix is only applied when the base of the append tower is a "clipped" slice, meaning its length and capacity are equal (e.g. x\[:0:0\] or \[\]T{}). This is to avoid changing program behavior by eliminating intended side effects on the base slice's underlying array.

This analyzer is currently disabled by default as the
transformation does not preserve the nilness of the base slice in
all cases; see [https://go.dev/issue/73557](https://go.dev/issue/73557).

#### Analyzer atomictypes [¶](#hdr-Analyzer_atomictypes)

atomictypes: replace basic types in sync/atomic calls with atomic types

The atomictypes analyzer suggests replacing the primitive sync/atomic functions with the strongly typed atomic wrapper types introduced in Go1.19 (e.g. atomic.Int32). For example,

var x int32
atomic.AddInt32(&x, 1)

would become

var x atomic.Int32
x.Add(1)

The atomic types are safer because they don't allow non-atomic access, which is a common source of bugs. These types also resolve memory alignment issues that plagued the old atomic functions on 32-bit architectures.

#### Analyzer bloop [¶](#hdr-Analyzer_bloop)

bloop: replace for-range over b.N with b.Loop

The bloop analyzer suggests replacing benchmark loops of the form \`for i := 0; i \< b.N; i++\` or \`for range b.N\` with the more modern \`for b.Loop()\`, which was added in Go 1.24.

This change makes benchmark code more readable and also removes the need for manual timer control, so any preceding calls to b.StartTimer, b.StopTimer, or b.ResetTimer within the same function will also be removed.

Caveats: The b.Loop() method is designed to prevent the compiler from optimizing away the benchmark loop, which can occasionally result in slower execution due to increased allocations in some specific cases. Since its fix may change the performance of nanosecond-scale benchmarks, bloop is disabled by default in the \`go fix\` analyzer suite; see golang/go#74967.

#### Analyzer any [¶](#hdr-Analyzer_any)

any: replace interface{} with any

The any analyzer suggests replacing uses of the empty interface type, \`interface{}\`, with the \`any\` alias, which was introduced in Go 1.18. This is a purely stylistic change that makes code more readable.

#### Analyzer embedlit [¶](#hdr-Analyzer_embedlit)

embedlit: simplify references to embedded fields in composite literals

The embedlit analyzer suggests removing redundant embedded field type specifiers from composite literals. Go1.27 introduced the ability to directly initialize fields promoted from embedded struct types without a nested literal. For example, given the following structs:

```
type T struct {
	U
}
type U struct {
	x int
}
```
A composite literal such as

```
t := T{U: U{x: 1}}
```
would become

```
t := T{x: 1}
```
#### Analyzer errorsastype [¶](#hdr-Analyzer_errorsastype)

errorsastype: replace errors.As with errors.AsType\[T\]

This analyzer suggests fixes to simplify uses of [errors.As](/errors#As) of
this form:

```
var myerr *MyErr
if errors.As(err, &myerr) {
	handle(myerr)
}
```
by using the less error-prone generic [errors.AsType](/errors#AsType) function,
introduced in Go 1.26:

```
if myerr, ok := errors.AsType[*MyErr](err); ok {
	handle(myerr)
}
```
The fix is only offered if the var declaration has the form shown and there are no uses of myerr outside the if statement.

#### Analyzer fmtappendf [¶](#hdr-Analyzer_fmtappendf)

fmtappendf: replace \[\]byte(fmt.Sprintf) with fmt.Appendf

The fmtappendf analyzer suggests replacing \`\[\]byte(fmt.Sprintf(...))\` with \`fmt.Appendf(nil, ...)\`. This avoids the intermediate allocation of a string by Sprintf, making the code more efficient. The suggestion also applies to fmt.Sprint and fmt.Sprintln.

Since its fix is not a Pareto improvement, fmtappendf is disabled by default in the \`go fix\` analyzer suite; see golang/go#77581.

#### Analyzer forvar [¶](#hdr-Analyzer_forvar)

forvar: remove redundant re-declaration of loop variables

The forvar analyzer removes unnecessary shadowing of loop variables. Before Go 1.22, it was common to write \`for \_, x := range s { x := x ... }\` to create a fresh variable for each iteration. Go 1.22 changed the semantics of \`for\` loops, making this pattern redundant. This analyzer removes the unnecessary \`x := x\` statement.

This fix only applies to \`range\` loops.

#### Analyzer importcomment [¶](#hdr-Analyzer_importcomment)

importcomment: remove obsolete comments specifying canonical import path

The importcomment analyzer removes comments specifying the canonical import path, such as

package foo // import "example.com/foo"

The go command enforced these comments in GOPATH mode via "go get", but ignores them in module mode, so they are obsolete once the package belongs to a module. The fix removes the comment.

#### Analyzer mapsloop [¶](#hdr-Analyzer_mapsloop)

mapsloop: replace explicit loops over maps with calls to maps package

The mapsloop analyzer replaces loops of the form

```
for k, v := range x { m[k] = v }
```
with a single call to a function from the \`maps\` package, added in Go 1.23. Depending on the context, this could be \`maps.Copy\`, \`maps.Insert\`, \`maps.Clone\`, or \`maps.Collect\`.

The transformation to \`maps.Clone\` is applied conservatively, as it preserves the nilness of the source map, which may be a subtle change in behavior if the original code did not handle a nil map in the same way.

#### Analyzer minmax [¶](#hdr-Analyzer_minmax)

minmax: replace if/else statements with calls to min or max

The minmax analyzer simplifies conditional assignments by suggesting the use of the built-in \`min\` and \`max\` functions, introduced in Go 1.21. For example,

```
if a < b { x = a } else { x = b }
```
is replaced by

x = min(a, b).

This analyzer avoids making suggestions for floating-point types, as the behavior of \`min\` and \`max\` with NaN values can differ from the original if/else statement.

#### Analyzer newexpr [¶](#hdr-Analyzer_newexpr)

newexpr: simplify code by using go1.26's new(expr)

This analyzer finds declarations of functions of this form:

```
func varOf(x int) *int { return &x }
```
and suggests a fix to turn them into inlinable wrappers around go1.26's built-in new(expr) function:

```
//go:fix inline
func varOf(x int) *int { return new(x) }
```
(The directive comment causes the 'inline' analyzer to suggest that calls to such functions are inlined.)

In addition, this analyzer suggests a fix for each call to one of the functions before it is transformed, so that

use(varOf(123))

is replaced by:

use(new(123))

Wrapper functions such as varOf are common when working with Go serialization packages such as for JSON or protobuf, where pointers are often used to express optionality.

#### Analyzer omitzero [¶](#hdr-Analyzer_omitzero)

omitzero: suggest replacing omitempty with omitzero for struct fields

The omitzero analyzer identifies uses of the \`omitempty\` JSON struct tag on fields that are themselves structs. For struct-typed fields, the \`omitempty\` tag has no effect on the behavior of json.Marshal and json.Unmarshal. The analyzer offers two suggestions: either remove the tag, or replace it with \`omitzero\` (added in Go 1.24), which correctly omits the field if the struct value is zero.

However, some other serialization packages (notably kubebuilder, see
[https://book.kubebuilder.io/reference/markers.html](https://book.kubebuilder.io/reference/markers.html)) may have their own
interpretation of the \`json:",omitzero"\` tag, so removing it may affect
program behavior. For this reason, the omitzero modernizer will not
make changes in any package that contains +kubebuilder annotations.

Replacing \`omitempty\` with \`omitzero\` is a change in behavior. The original code would always encode the struct field, whereas the modified code will omit it if it is a zero-value.

#### Analyzer plusbuild [¶](#hdr-Analyzer_plusbuild)

plusbuild: remove obsolete //+build comments

The plusbuild analyzer suggests a fix to remove obsolete build tags of the form:

//+build linux,amd64

in files that also contain a Go 1.18-style tag such as:

//go:build linux && amd64

(It does not check that the old and new tags are consistent; that is the job of the 'buildtag' analyzer in the vet suite.)

#### Analyzer rangeint [¶](#hdr-Analyzer_rangeint)

rangeint: replace 3-clause for loops with for-range over integers

The rangeint analyzer suggests replacing traditional for loops such as

```
for i := 0; i < n; i++ { ... }
```
with the more idiomatic Go 1.22 style:

```
for i := range n { ... }
```
This transformation is applied only if (a) the loop variable is not modified within the loop body and (b) the loop's limit expression is not modified within the loop, as \`for range\` evaluates its operand only once.

#### Analyzer reflecttypefor [¶](#hdr-Analyzer_reflecttypefor)

reflecttypefor: replace reflect.TypeOf(x) with TypeFor\[T\]()

This analyzer suggests fixes to replace uses of reflect.TypeOf(x) with reflect.TypeFor, introduced in go1.22, when the desired runtime type is known at compile time, for example:

reflect.TypeOf(uint32(0))        -> reflect.TypeFor\[uint32\]()
reflect.TypeOf((\*ast.File)(nil)) -> reflect.TypeFor\[\*ast.File\]()

It also offers a fix to simplify the constructions below, which use reflect.TypeOf to return the runtime type for an interface type,

reflect.TypeOf((\*io.Reader)(nil)).Elem()

or:

reflect.TypeOf(\[\]io.Reader(nil)).Elem()

to:

reflect.TypeFor\[io.Reader\]()

No fix is offered in cases when the runtime type is dynamic, such as:

var r io.Reader = ...
reflect.TypeOf(r)

or when the operand has potential side effects.

Nor is a fix offered when the operand refers to a non-type symbol such as a variable, constant, function, or field, as in:

```
reflect.TypeOf(pkg.Var)
reflect.TypeOf(x.Field)
reflect.TypeOf([arrayLen]byte{})
```
Replacing these with TypeFor\[T\]() would erase the reference to the symbol, breaking any intended coupling between the reflected type and the type of that symbol.

#### Analyzer reflecttypeassert [¶](#hdr-Analyzer_reflecttypeassert)

reflecttypeassert: replace v.Interface().(T) with reflect.TypeAssert\[T\](v)

This analyzer suggests fixes to replace two-valued type assertions on the result of (reflect.Value).Interface with reflect.TypeAssert, introduced in go1.25, which avoids the intermediate allocation of an interface value, for example:

x, ok := v.Interface().(string)  ->  x, ok := reflect.TypeAssert\[string\](v)

No fix is offered for single-valued assertions, since they panic when the assertion fails whereas reflect.TypeAssert does not. Nor is a fix offered for a type switch.

#### Analyzer slicesbackward [¶](#hdr-Analyzer_slicesbackward)

slicesbackward: replace backward loops over slices with slices.Backward

The slicesbackward analyzer suggests replacing manually-written backward loops of the form

```
for i := len(s) - 1; i >= 0; i-- {
    use(s[i])
}
```
with the more readable Go 1.23 style using slices.Backward:

```
for _, v := range slices.Backward(s) {
    use(v)
}
```
If the loop index is needed beyond just indexing into the slice, both the index and value variables are kept:

```
for i, v := range slices.Backward(s) { ... }
```
#### Analyzer slicesclip [¶](#hdr-Analyzer_slicesclip)

slicesclip: replace three-index slice expressions with slices.Clip

The slicesclip analyzer suggests replacing a full slice expression of the form

x\[:len(x):len(x)\]

which clips the capacity of a slice to its length, with the simpler and more readable

slices.Clip(x)

added in Go 1.21.

#### Analyzer slicescontains [¶](#hdr-Analyzer_slicescontains)

slicescontains: replace loops with slices.Contains or slices.ContainsFunc

The slicescontains analyzer simplifies loops that check for the existence of an element in a slice. It replaces them with calls to \`slices.Contains\` or \`slices.ContainsFunc\`, which were added in Go 1.21.

If the expression for the target element has side effects, this transformation will cause those effects to occur only once, not once per tested slice element.

#### Analyzer slicesdelete [¶](#hdr-Analyzer_slicesdelete)

slicesdelete: replace append-based slice deletion with slices.Delete

The slicesdelete analyzer suggests replacing the idiom

s = append(s\[:i\], s\[j:\]...)

with the more explicit

s = slices.Delete(s, i, j)

introduced in Go 1.21.

This analyzer is disabled by default. The \`slices.Delete\` function
zeros the elements between the new length and the old length of the
slice to prevent memory leaks, which is a subtle difference in
behavior compared to the append-based idiom; see [https://go.dev/issue/73686](https://go.dev/issue/73686).

#### Analyzer slicessort [¶](#hdr-Analyzer_slicessort)

slicessort: replace sort.Slice with slices.Sort for basic types

The slicessort analyzer simplifies sorting slices of basic ordered types. It replaces

```
sort.Slice(s, func(i, j int) bool { return s[i] < s[j] })
```
with the simpler \`slices.Sort(s)\`, which was added in Go 1.21.

#### Analyzer stditerators [¶](#hdr-Analyzer_stditerators)

stditerators: use iterators instead of Len/At-style APIs

This analyzer suggests a fix to replace each loop of the form:

```
for i := 0; i < x.Len(); i++ {
	use(x.At(i))
}
```
or its "for elem := range x.Len()" equivalent by a range loop over an iterator offered by the same data type:

```
for elem := range x.All() {
	use(elem)
}
```
where x is one of various well-known types in the standard library.

#### Analyzer stringscut [¶](#hdr-Analyzer_stringscut)

stringscut: replace strings.Index etc. with strings.Cut

This analyzer replaces certain patterns of use of [strings.Index](/strings#Index) and string slicing by [strings.Cut](/strings#Cut), added in go1.18.
It also replaces analogous uses of [strings.LastIndex](/strings#LastIndex) by [strings.CutLast](/strings#CutLast), added in go1.27.

For example:

```
idx := strings.Index(s, substr)
if idx >= 0 {
    return s[:idx]
}
```
is replaced by:

```
before, _, ok := strings.Cut(s, substr)
if ok {
    return before
}
```
And:

```
idx := strings.LastIndex(s, substr)
if idx >= 0 {
    return s[:idx]
}
```
is replaced by:

```
before, _, ok := strings.CutLast(s, substr)
if ok {
    return before
}
```
And:

```
idx := strings.Index(s, substr)
if idx >= 0 {
    return
}
```
is replaced by:

```
found := strings.Contains(s, substr)
if found {
    return
}
```
(LastIndex used only as a presence check is also rewritten to Contains.)

It also handles variants using [strings.IndexByte](/strings#IndexByte) or [strings.LastIndexByte](/strings#LastIndexByte)
instead of Index/LastIndex, or the bytes package instead of strings.

Fixes are offered only in cases in which there are no potential modifications of the idx, s, or substr expressions between their definition and use. CutLast fixes are offered only when the file's Go version is at least 1.27.

It also replaces [strings.SplitN](/strings#SplitN)(s, sep, 2)\[0\] and [strings.Split](/strings#Split)(s, sep)\[0\] with the "before" result of strings.Cut, when sep is a non-empty string constant:

x := strings.SplitN(s, sep, 2)\[0\]

is replaced by:

x, \_, \_ := strings.Cut(s, sep)

The fix is only offered when sep is a non-empty string literal. When sep is a variable or the empty string, the semantics differ (strings.Split(s, "")\[0\] returns the first character of s, but strings.Cut(s, "").before is ""), so no fix is suggested.

#### Analyzer stringscutprefix [¶](#hdr-Analyzer_stringscutprefix)

stringscutprefix: replace HasPrefix/TrimPrefix with CutPrefix

The stringscutprefix analyzer simplifies a common pattern where code first checks for a prefix with \`strings.HasPrefix\` and then removes it with \`strings.TrimPrefix\`. It replaces this two-step process with a single call to \`strings.CutPrefix\`, introduced in Go 1.20. The analyzer also handles the equivalent functions in the \`bytes\` package.

For example, this input:

```
if strings.HasPrefix(s, prefix) {
    use(strings.TrimPrefix(s, prefix))
}
```
is fixed to:

```
if after, ok := strings.CutPrefix(s, prefix); ok {
    use(after)
}
```
The analyzer also offers fixes to use CutSuffix in a similar way. This input:

```
if strings.HasSuffix(s, suffix) {
    use(strings.TrimSuffix(s, suffix))
}
```
is fixed to:

```
if before, ok := strings.CutSuffix(s, suffix); ok {
    use(before)
}
```
#### Analyzer stringsseq [¶](#hdr-Analyzer_stringsseq)

stringsseq: replace ranging over Split/Fields with SplitSeq/FieldsSeq

The stringsseq analyzer improves the efficiency of iterating over substrings. It replaces

for range strings.Split(...)

with the more efficient

for range strings.SplitSeq(...)

which was added in Go 1.24 and avoids allocating a slice for the substrings. The analyzer also handles strings.Fields and the equivalent functions in the bytes package.

#### Analyzer stringsbuilder [¶](#hdr-Analyzer_stringsbuilder)

stringsbuilder: replace += with strings.Builder

This analyzer replaces repeated string += string concatenation operations with calls to Go 1.10's strings.Builder.

For example:

```
var s = "["
for x := range seq {
	s += x
	s += "."
}
s += "]"
use(s)
```
is replaced by:

```
var s strings.Builder
s.WriteString("[")
for x := range seq {
	s.WriteString(x)
	s.WriteString(".")
}
s.WriteString("]")
use(s.String())
```
This avoids quadratic memory allocation and improves performance.

No diagnostics are issued in tests, where data sizes are often small and asymptotic performance is not a security concern.

The analyzer requires that all references to s before the final uses are += operations. To avoid warning about trivial cases, at least one must appear within a loop. The variable s must be a local variable, not a global or parameter.

All uses of the finished string must come after the last += operation. Each such use will be replaced by a call to strings.Builder's String method. (These may appear within an intervening loop or function literal, since even if s.String() is called repeatedly, it does not allocate memory.)

Often the addend is a call to fmt.Sprintf, as in this example:

```
var s string
for x := range seq {
	s += fmt.Sprintf("%v", x)
}
```
which, once the suggested fix is applied, becomes:

```
var s strings.Builder
for x := range seq {
	s.WriteString(fmt.Sprintf("%v", x))
}
```
The WriteString call can be further simplified to the more efficient
fmt.Fprintf(&s, "%v", x), avoiding the allocation of an intermediary.
However, stringsbuilder does not perform this simplification;
it requires staticcheck analyzer QF1012. (See [https://go.dev/issue/76918](https://go.dev/issue/76918).)

#### Analyzer testingcontext [¶](#hdr-Analyzer_testingcontext)

testingcontext: replace context.WithCancel with t.Context in tests

The testingcontext analyzer simplifies context management in tests. It replaces the manual creation of a cancellable context,

ctx, cancel := context.WithCancel(context.Background())
defer cancel()

with a single call to t.Context(), which was added in Go 1.24.

This change is only suggested if the \`cancel\` function is not used for any other purpose.

#### Analyzer unsafefuncs [¶](#hdr-Analyzer_unsafefuncs)

unsafefuncs: replace unsafe pointer arithmetic with function calls

The unsafefuncs analyzer simplifies pointer arithmetic expressions by replacing them with calls to helper functions such as unsafe.Add, added in Go 1.17.

Example:

unsafe.Pointer(uintptr(ptr) + uintptr(n))

where ptr is an unsafe.Pointer, is replaced by:

unsafe.Add(ptr, n)

#### Analyzer waitgroupgo [¶](#hdr-Analyzer_waitgroupgo)

waitgroupgo: replace wg.Add(1)/go/wg.Done() with wg.Go

The waitgroupgo analyzer simplifies goroutine management with \`sync.WaitGroup\`. It replaces the common pattern

```
wg.Add(1)
go func() {
	defer wg.Done()
	...
}()
```
with a single call to

```
wg.Go(func(){ ... })
```
which was added in Go 1.25.

### Index [¶](#pkg-index)

### Constants [¶](#pkg-constants)

This section is empty.

### Variables [¶](#pkg-variables)

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/any.go;l=16)

var AnyAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name:     "any",
	Doc:      [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "any"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer)},
	Run:      runAny,
	URL:      "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_any",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/slices.go;l=25)

var AppendClippedAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name:     "appendclipped",
	Doc:      [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "appendclipped"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer)},
	Run:      appendclipped,
	URL:      "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_appendclipped",
}

Warning: this analyzer is not safe to enable by default.

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/atomictypes.go;l=28)

var AtomicTypesAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "atomictypes",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "atomictypes"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
		[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer),
		[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer),
	},
	Run: runAtomic,
	URL: "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_atomictypes",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/bloop.go;l=28)

var BLoopAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "bloop",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "bloop"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
		[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer),
		[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer),
	},
	Run: bloop,
	URL: "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_bloop",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/embedlit.go;l=27)

var EmbedLitAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "embedlit",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "embedlit"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
		[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer),
		[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer),
	},
	Run: runEmbedLit,
	URL: "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_embedlit",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/errorsastype.go;l=27)

var ErrorsAsTypeAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name:     "errorsastype",
	Doc:      [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "errorsastype"),
	URL:      "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_errorsastype",
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer)},
	Run:      errorsastype,
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/fmtappendf.go;l=25)

var FmtAppendfAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "fmtappendf",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "fmtappendf"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
		[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer),
		[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer),
	},
	Run: fmtappendf,
	URL: "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_fmtappendf",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/forvar.go;l=19)

var ForVarAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name:     "forvar",
	Doc:      [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "forvar"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer)},
	Run:      forvar,
	URL:      "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_forvar",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/maps.go;l=26)

var MapsLoopAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name:     "mapsloop",
	Doc:      [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "mapsloop"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer)},
	Run:      mapsloop,
	URL:      "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_mapsloop",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/minmax.go;l=28)

var MinMaxAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "minmax",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "minmax"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
		[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer),
		[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer),
	},
	Run: minmax,
	URL: "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_minmax",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/newexpr.go;l=26)

var NewExprAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name:      "newexpr",
	Doc:       [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "newexpr"),
	URL:       "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_newexpr",
	Requires:  \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer)},
	Run:       run,
	FactTypes: \[\][analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Fact](/golang.org/x/tools@v0.53.0/go/analysis#Fact){&newLike{}},
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/omitzero.go;l=22)

var OmitZeroAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name:     "omitzero",
	Doc:      [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "omitzero"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer)},
	Run:      omitzero,
	URL:      "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_omitzero",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/plusbuild.go;l=17)

var PlusBuildAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "plusbuild",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "plusbuild"),
	URL:  "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_plusbuild",
	Run:  plusbuild,
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/rangeint.go;l=26)

var RangeIntAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "rangeint",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "rangeint"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
		[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer),
		[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer),
	},
	Run: rangeint,
	URL: "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_rangeint",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/reflect.go;l=25)

var ReflectTypeForAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "reflecttypefor",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "reflecttypefor"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
		[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer),
		[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer),
	},
	Run: reflecttypefor,
	URL: "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_reflecttypefor",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/slicescontains.go;l=27)

var SlicesContainsAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "slicescontains",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "slicescontains"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
		[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer),
		[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer),
	},
	Run: slicescontains,
	URL: "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_slicescontains",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/slicesdelete.go;l=23)

var SlicesDeleteAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name:     "slicesdelete",
	Doc:      [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "slicesdelete"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer)},
	Run:      slicesdelete,
	URL:      "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_slicesdelete",
}

Warning: this analyzer is not safe to enable by default (not nil-preserving).

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/sortslice.go;l=24)

var SlicesSortAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "slicessort",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "slicessort"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
		[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer),
		[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer),
	},
	Run: slicessort,
	URL: "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_slicessort",
}

(Not to be confused with go/analysis/passes/sortslice.)

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/stditerators.go;l=24)

var StdIteratorsAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "stditerators",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "stditerators"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
		[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer),
	},
	Run: stditerators,
	URL: "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_stditerators",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/stringsbuilder.go;l=29)

var StringsBuilderAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "stringsbuilder",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "stringsbuilder"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
		[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer),
		[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer),
	},
	Run: stringsbuilder,
	URL: "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_stringsbuilder",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/stringscut.go;l=31)

var StringsCutAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "stringscut",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "stringscut"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
		[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer),
		[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer),
	},
	Run: stringscut,
	URL: "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_stringscut",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/stringscutprefix.go;l=26)

var StringsCutPrefixAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "stringscutprefix",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "stringscutprefix"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
		[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer),
		[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer),
	},
	Run: stringscutprefix,
	URL: "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_stringscutprefix",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/stringsseq.go;l=23)

var StringsSeqAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "stringsseq",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "stringsseq"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
		[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer),
		[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer),
	},
	Run: stringsseq,
	URL: "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_stringsseq",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/modernize.go;l=34)

var Suite = \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	[AnyAnalyzer](#AnyAnalyzer),
	[AtomicTypesAnalyzer](#AtomicTypesAnalyzer),
	[EmbedLitAnalyzer](#EmbedLitAnalyzer),
	[ErrorsAsTypeAnalyzer](#ErrorsAsTypeAnalyzer),
	[ForVarAnalyzer](#ForVarAnalyzer),
	importCommentAnalyzer,
	[MapsLoopAnalyzer](#MapsLoopAnalyzer),
	[MinMaxAnalyzer](#MinMaxAnalyzer),
	[NewExprAnalyzer](#NewExprAnalyzer),
	[OmitZeroAnalyzer](#OmitZeroAnalyzer),
	[PlusBuildAnalyzer](#PlusBuildAnalyzer),
	[RangeIntAnalyzer](#RangeIntAnalyzer),
	reflectTypeAssertAnalyzer,
	[ReflectTypeForAnalyzer](#ReflectTypeForAnalyzer),
	slicesBackwardAnalyzer,
	slicesClipAnalyzer,
	[SlicesContainsAnalyzer](#SlicesContainsAnalyzer),
	[SlicesSortAnalyzer](#SlicesSortAnalyzer),
	[StdIteratorsAnalyzer](#StdIteratorsAnalyzer),
	[StringsCutAnalyzer](#StringsCutAnalyzer),
	[StringsCutPrefixAnalyzer](#StringsCutPrefixAnalyzer),
	[StringsSeqAnalyzer](#StringsSeqAnalyzer),
	[StringsBuilderAnalyzer](#StringsBuilderAnalyzer),
	[TestingContextAnalyzer](#TestingContextAnalyzer),
	unsafeFuncsAnalyzer,
	[WaitGroupGoAnalyzer](#WaitGroupGoAnalyzer),
}

Suite lists all modernize analyzers.

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/testingcontext.go;l=30)

var TestingContextAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "testingcontext",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "testingcontext"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
		[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer),
		[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer),
	},
	Run: testingContext,
	URL: "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_testingcontext",
}

[View Source](https://cs.opensource.google/go/x/tools/+/v0.53.0:go/analysis/passes/modernize/waitgroupgo.go;l=26)

var WaitGroupGoAnalyzer = &[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
	Name: "waitgroupgo",
	Doc:  [analyzerutil](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil).[MustExtractDoc](/golang.org/x/tools@v0.53.0/internal/analysis/analyzerutil#MustExtractDoc)(doc, "waitgroupgo"),
	Requires: \[\]\*[analysis](/golang.org/x/tools@v0.53.0/go/analysis).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis#Analyzer){
		[inspect](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect).[Analyzer](/golang.org/x/tools@v0.53.0/go/analysis/passes/inspect#Analyzer),
		[typeindexanalyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex).[Analyzer](/golang.org/x/tools@v0.53.0/internal/analysis/typeindex#Analyzer),
	},
	Run: waitgroup,
	URL: "https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize#hdr-Analyzer\_waitgroupgo",
}

### Functions [¶](#pkg-functions)

This section is empty.

### Types [¶](#pkg-types)

This section is empty.
