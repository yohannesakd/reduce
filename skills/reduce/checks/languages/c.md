# C rules

**Signal.** The feature has `.c`, `.h`, `.cu`, or `.cuh` files. The driver gives this check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. The rules are the `# C` section of the PufferLib guide, copied 1:1. Each **Reduce:** line extends the rule above it. The assert form is `assert()`.

**Keeps it when.** The rule's **Keep when** holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

## C

- **C1** Do not use header files as lists of declarations. Treat them as source files.
  - **Reduce:** `simplify`. Put the definitions in the header, and include it once, in the file that uses it.
  - Keep when: a public library API that other projects include needs the declarations.
- **C2** Avoid forward declarations. Define functions as close as possible to first use.
  - **Reduce:** `simplify`. Move the definition above its first caller, and remove the forward declaration.
  - Keep when: two functions call each other.
- **C3** Preallocate all memory at init by default and let the OS free it on close
  - **Reduce:** `simplify`. Remove `free` calls and cleanup functions that run only at program exit.
  - Keep when: the code is a library, or it runs more than once in one process.
- **C4** Runtime allocations should be rare and freed in the same scope
  - **Reduce:** `lead`. Record each allocation in a loop or a hot path, and each allocation that another scope frees.
- **C5** Avoid keyword bloat, such as redundant static, const, inline, etc.
  - **Reduce:** `remove`. Remove a keyword that changes nothing that the build or the callers need.
  - Keep when: `static` keeps a name out of a shared link, or `const` is part of a public API.
- **C6** Use macros only for constants and constant expressions, not for conditionals
  - **Reduce:** `simplify`. Replace a macro that hides a condition or control flow with plain code or a function.
  - Keep when: the macro is a build-time switch, such as a platform check or an include guard.
- **C7** Use struct initializer syntax foo = {.a = 1, .b = 2} instead of setter wrappers
  - **Reduce:** `remove`. Remove the setter wrappers and the field-by-field assignments that one initializer replaces.
- **C8** Do not use additional scoping blocks, i.e. bare {}. Dedupe names instead.
  - **Reduce:** `simplify`. Remove the bare block, and give the variables different names.
  - Keep when: a `case` label declares a variable and needs the block.

**Sources.** [PufferLib `SKILL_ISSUES.md`](https://github.com/PufferAI/PufferLib/blob/5.0/SKILL_ISSUES.md), MIT. The rule lines are copied 1:1. The **Reduce:** and **Keep when** lines are additions of reduce.
