# C rules

**Signal.** The feature has `.c`, `.h`, `.cu`, or `.cuh` files. The driver gives this check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. The assert form is `assert()`.

**Keeps it when.** The rule's **Keep when** holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

## Rules

- C1. Do not use a header file as a list of declarations. Treat a header as a source file. `simplify`
- C2. Do not write forward declarations. Define each function as close as possible to its first use. `simplify`
- C3. Preallocate all memory at initialization, and let the operating system free it at exit. `simplify`
- C4. Allocate at run time only rarely, and free the allocation in the same scope. `lead`
- C5. Remove redundant `static`, `const`, `inline`, and other keywords that change nothing. `remove`
- C6. Use macros only for constants and constant expressions. Do not use a macro for a conditional. `simplify`
- C7. Use struct initializer syntax, `foo = {.a = 1, .b = 2}`. Remove setter wrappers. `remove`
- C8. Do not add bare `{}` scoping blocks. Give the variables different names. `simplify`

**Sources.** [PufferLib `SKILL_ISSUES.md`](https://github.com/PufferAI/PufferLib/blob/5.0/SKILL_ISSUES.md), MIT.
