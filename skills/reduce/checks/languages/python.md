# Python rules

**Signal.** The feature has `.py` or `.pyi` files, or scripts without an extension that start with a Python shebang. The driver gives this check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. A rule that names a Python version needs that version as the project's lowest supported version. The assert form is `assert`, only for internal invariants. Python removes `assert` under `-O`, so an `assert` never validates external input.

**Keeps it when.** The rule's **Unless** line holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

> A class with `__init__` and one method is a function. Stop writing classes.
> `except Exception: pass` is not error handling. It is hiding the body.
> Flat is better than nested. You read that in PEP 20. Now do it.

## Asserts and exceptions

- **P1** Never use `assert` to validate user input, files, network data, or public arguments. `lead` [PR, PC, RF, PG]
- **P2** Defensive `if ...: raise` checks of internal invariants become one `assert`. `simplify` [PR]
  Unless: the check guards external input, as P1 says.
- **P3** No bare `except:`, no `except Exception`, no `except BaseException`. `lead` [P8, PG, RF]
  Unless: the handler raises again, or logs the traceback at an isolation point.
- **P4** Delete a `try`/`except` whose handler only raises again. `remove` [RF]
- **P5** Write a bare `raise`, not `raise err`, to raise the caught exception again. `simplify` [RF]
- **P6** Inside `except`, raise a new exception with `from err` or `from None`. `lead` [RF]
- **P7** `try`/`except X: pass` is `contextlib.suppress(X)`. `simplify` [RF]
  Unless: the code is on a hot path. `suppress` is slower.
- **P8** Open files, locks, and sockets with `with`. Delete manual `close()` calls and their `finally` blocks. `simplify` [P8, PG, RF]

## Control flow

- **P9** No `else` after a branch that ends in `return`, `raise`, `continue`, or `break`. `simplify` [RF, P20]
- **P10** An `if` whose only statement is another `if` is one `if a and b`. `simplify` [RF, P20]
- **P11** Return the expression. Delete an assignment that only the next `return` uses. `remove` [RF]
- **P12** Return the condition, not `True` and `False` from an `if`/`else`. `remove` [RF]
- **P13** Loops that return `True` or `False` on a match are `any()` or `all()`. `reuse` [RF]
- **P14** `if key in d`/`else` is `d.get(key, default)`. Write `d.get(key)`, not `d.get(key, None)`. `reuse` [RF]
- **P15** Delete `pass`, `...`, and `return None` statements that change nothing. `remove` [RF]

## Comprehensions and builtins

- **P16** A loop that only appends to a new list or dict is a comprehension. `simplify` [RF, PG]
  Unless: it needs several `for` clauses or a complex filter.
- **P17** Delete redundant wrappers: `list()` around comprehensions, `dict()` for literals, `.keys()` in `in` tests and loops. `remove` [RF, PG]
- **P18** Format strings with f-strings. No `%` formatting, no `.format()`. `simplify` [RF]
- **P19** Use `pathlib.Path` in new code. No `os.path` joins and string paths. `simplify` [RF]

## Classes and functions

- **P20** A plain data class gets `@dataclass`. Delete the hand-written `__init__` and `__repr__`. `remove` [DC]
- **P21** Delete properties that only get and set one attribute. Make the attribute public. `remove` [PG]
- **P22** No `@staticmethod`. Write a module-level function. `simplify` [PG]
  Unless: an existing library API requires the method.
- **P23** A class with `__init__` and one other method is a function. `remove` [RD]
  Unless: the instance keeps state between calls, or a library requires the class.
- **P24** Call `super()` without arguments. `remove` [RF]
- **P25** Never use a mutable object as a default argument or as a dataclass field default. `lead` [RF, PG, DC]
- **P26** No `from module import *`. `lead` [P8, PG]

## Types and async code

- **P27** Write `list[int]` and `X | None`, not `typing.List`, `Union`, or `Optional`. `simplify` Python 3.10 [RF, TY]
- **P28** Delete each `cast()`, `isinstance()`, and `# type: ignore` that mypy or pyright reports as unnecessary. `remove` [MY, PY]
- **P29** Keep a reference to every `asyncio.create_task` result, or create the tasks in a `TaskGroup`. `lead` Python 3.11 [RF, PD]

**Sources.**
[P8] PEP 8, https://peps.python.org/pep-0008/. [P20] PEP 20, https://peps.python.org/pep-0020/.
[PG] Google Python Style Guide, https://google.github.io/styleguide/pyguide.html.
[PR] The `assert` statement, https://docs.python.org/3/reference/simple_stmts.html#the-assert-statement. [PC] Command line `-O`, https://docs.python.org/3/using/cmdline.html.
[DC] `dataclasses`, https://docs.python.org/3/library/dataclasses.html. [PD] Python 3.11 release notes, https://docs.python.org/3/whatsnew/3.11.html.
[TY] Typing best practices, https://typing.python.org/en/latest/reference/best_practices.html.
[RF] Ruff rules, https://docs.astral.sh/ruff/rules/: the S101, BLE, E722, TRY, B, SIM, RET, PIE, C4, PERF, UP, PTH, and RUF006 families.
[MY] mypy `--strict`, https://mypy.readthedocs.io/en/stable/command_line.html. [PY] pyright configuration, https://github.com/microsoft/pyright/blob/main/docs/configuration.md.
[RD] Rule of reduce: step 1 of the [refactoring check](../every-feature/refactoring.md).
Licenses are in [rule sources](../../guides/rule-sources.md).
