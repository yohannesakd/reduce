# CUDA rules

**Signal.** The feature has `.cu` or `.cuh` files. The driver gives this check and the C check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. Treat CUDA files as CUDA C99, and apply the [C rules](c.md) too.

**Keeps it when.** The rule's **Keep when** holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

## Rules

- CU1. Do not use the C++ standard library, templates, or classes. `simplify`
  Keep when: the user directs it, or existing code overloads a function for different numeric types.
- CU2. Do not use the C++ forms of C features, such as `nullptr` and `static_cast`. `simplify`
- CU3. Do not mark unused parameters with `(void)`. `remove`
  Keep when: the build enables `-Wunused-parameter`.
- CU4. Remove casts that an automatic conversion already does. `remove`
  Keep when: the build enables `-Wnarrowing`, or the cast changes the value.

**Sources.** [PufferLib `SKILL_ISSUES.md`](https://github.com/PufferAI/PufferLib/blob/5.0/SKILL_ISSUES.md), MIT.
