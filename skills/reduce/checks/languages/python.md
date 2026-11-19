# Python rules

**Signal.** The feature has `.py` or `.pyi` files, or scripts without an extension that start with a Python shebang. The driver gives this check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. A rule that names a Python version needs that version as the project's lowest supported version.
The assert form is `assert`, only for internal invariants. Python removes `assert` under `-O`, so an `assert` never validates external input.

**Keeps it when.** The rule's **Keep when** holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

## Asserts and exceptions

- P1. Never use `assert` to validate user input, files, network data, or public arguments. `lead` [PR, PC, RF, PG]
- P2. Replace defensive `if ...: raise` checks of internal invariants with one `assert`. `simplify` [PR]
  Keep when: the check guards external input, as P1 says.
- P3. Do not write bare `except:`, `except Exception`, or `except BaseException`. `lead` [P8, PG, RF]
  Keep when: the handler raises again, or logs the traceback at an isolation point.
- P4. Remove a `try`/`except` whose handler only raises again. `remove` [RF]
- P5. Write a bare `raise`, not `raise err`, to raise the caught exception again. `simplify` [RF]
- P6. Inside `except`, raise a new exception with `from err` or `from None`. `lead` [RF]
- P7. Replace `try`/`except X: pass` with `contextlib.suppress(X)`. `simplify` [RF]
  Keep when: the code is on a hot path; `suppress` is slower.
- P8. Open files, locks, and sockets with `with`. Remove manual `close()` calls and their `finally` blocks. `simplify` [P8, PG, RF]

## Control flow

- P9. Remove `else` after a branch that ends in `return`, `raise`, `continue`, or `break`. `simplify` [RF, P20]
- P10. Merge an `if` whose only statement is another `if` into one `if a and b`. `simplify` [RF, P20]
- P11. Return the expression directly. Remove an assignment that only the next `return` uses. `remove` [RF]
- P12. Return the condition, not `True` and `False` from an `if`/`else`. `remove` [RF]
- P13. Replace loops that return `True` or `False` on a match with `any()` or `all()`. `reuse` [RF]
- P14. Replace an `if key in d`/`else` fallback with `d.get(key, default)`. Write `d.get(key)`, not `d.get(key, None)`. `reuse` [RF]
- P15. Remove `pass`, `...`, and `return None` statements that change nothing. `remove` [RF]

## Comprehensions and builtins

- P16. Replace a loop that only appends to a new list or dict with a comprehension. `simplify` [RF, PG]
  Keep when: it needs several `for` clauses or a complex filter.
- P17. Remove redundant wrappers: `list()` around comprehensions, `dict()` for literals, and `.keys()` in `in` tests and loops. `remove` [RF, PG]

## Classes and functions

- P18. Replace a hand-written `__init__` and `__repr__` of a plain data class with `@dataclass`. `remove` [DC]
- P19. Remove properties that only get and set one attribute. Make the attribute public. `remove` [PG]
- P20. Replace `@staticmethod` with a module-level function. `simplify` [PG]
  Keep when: an existing library API requires the method.
- P21. Call `super()` without arguments. `remove` [RF]
- P22. Never use a mutable object as a default argument or as a dataclass field default. `lead` [RF, PG, DC]

## Types and async code

- P23. Write `list[int]` and `X | None`, not `typing.List`, `Union`, or `Optional`. `simplify` Python 3.10 [RF, TY]
- P24. Remove each `cast()`, `isinstance()`, and `# type: ignore` that mypy or pyright reports as unnecessary. `remove` [MY, PY]
- P25. Keep a reference to every `asyncio.create_task` result, or create the tasks in a `TaskGroup`. `lead` Python 3.11 [RF, PD]

**Sources.**
[P8] PEP 8, https://peps.python.org/pep-0008/. [P20] PEP 20, https://peps.python.org/pep-0020/.
[PG] Google Python Style Guide, https://google.github.io/styleguide/pyguide.html.
[PR] The `assert` statement, https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement. [PC] Command line `-O`, https://docs.python.org/3/using/cmdline.html.
[DC] `dataclasses`, https://docs.python.org/3/library/dataclasses.html. [PD] Python 3.11 release notes, https://docs.python.org/3/whatsnew/3.11.html.
[TY] Typing best practices, https://typing.python.org/en/latest/reference/best_practices.html.
[RF] Ruff rules, https://docs.astral.sh/ruff/rules/: the S101, BLE, E722, TRY, B, SIM, RET, PIE, C4, PERF, UP, and RUF006 families.
[MY] mypy `--strict`, https://mypy.readthedocs.io/en/stable/command_line.html. [PY] pyright configuration, https://github.com/microsoft/pyright/blob/main/docs/configuration.md.
Licenses are in [rule sources](../../guides/rule-sources.md).
