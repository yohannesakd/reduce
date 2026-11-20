# CUDA rules

**Signal.** The feature has `.cu` or `.cuh` files. The driver gives this check and the C check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. The rules are the `# CUDA` section of the PufferLib guide, copied 1:1. Each **Reduce:** line extends the rule above it.

**Keeps it when.** The rule's **Keep when** holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

## CUDA

- **CU1** Treat CUDA files as CUDA C99
  - **Reduce:** Apply CU2 to CU7 and the [C rules](c.md) to every `.cu` and `.cuh` file.
- **CU2** Do not use the C++ standard library, templates, or classes
  - **Reduce:** `simplify`. Replace them with C functions, structs, and arrays.
- **CU3** Do not use the C++ versions of C language features like nullptr and static_cast
  - **Reduce:** `simplify`. Write `NULL` and C casts.
- **CU4** Exception: existing/user-directed overloading for different numeric types
  - **Reduce:** This is the **Keep when** of CU2 and CU3. Keep the overloads that exist, or that the user asks for.
- **CU5** Do not null params with (void) (Wunused-parameter is disabled)
  - **Reduce:** `remove`. Remove the `(void)param;` lines.
  - Keep when: the build enables `-Wunused-parameter`.
- **CU6** Avoid redundant casts where autocast will do (Wnarrowing is disabled)
  - **Reduce:** `remove`. Remove a cast that the automatic conversion already does.
  - Keep when: the build enables `-Wnarrowing`, or the cast changes the value.
- **CU7** Follow the C style guide above
  - **Reduce:** The driver gives the [C rules](c.md) to every feature that has CUDA files.

**Sources.** [PufferLib `SKILL_ISSUES.md`](https://github.com/PufferAI/PufferLib/blob/5.0/SKILL_ISSUES.md), MIT. The rule lines are copied 1:1. The **Reduce:** and **Keep when** lines are additions of reduce.
