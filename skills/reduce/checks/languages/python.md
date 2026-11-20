# Python rules

**Signal.** The feature has `.py` or `.pyi` files, or scripts without an extension that start with a Python shebang. The driver gives this check.

**Decide with.** Apply every rule as [language rules](../every-feature/refactoring.md#language-rules) says. A rule that names a Python version needs that version as the project's lowest supported version. The assert form is `assert`, only for internal invariants. Python removes `assert` under `-O`, so an `assert` never validates external input.

**Keeps it when.** The rule's **Unless** line holds, or [the precedence](../every-feature/refactoring.md#precedence) overrides it.

> A class with `__init__` and one method is a function. Stop writing classes.
> `except Exception: pass` is not error handling. It is hiding the body.
> Flat is better than nested. You read that in PEP 20. Now do it.

## Asserts and exceptions

- **P1** Never use `assert` to validate user input, files, network data, or public arguments. `lead`
- **P2** Defensive `if ...: raise` checks of internal invariants become one `assert`. `simplify` [RD]
  Unless: the check guards external input, as P1 says.
- **P3** No bare `except:`, no `except Exception`, no `except BaseException`. `lead`
  Unless: the handler raises again, or logs the traceback at an isolation point.
- **P4** Delete a `try`/`except` whose handler only raises again. `remove`
- **P5** Write a bare `raise`, not `raise err`, to raise the caught exception again. `simplify`
- **P6** Inside `except`, raise a new exception with `from err` or `from None`. `lead`
- **P7** `try`/`except X: pass` is `contextlib.suppress(X)`. `simplify`
  Unless: the code is on a hot path. `suppress` is slower.
- **P8** Open files, locks, and sockets with `with`. Delete manual `close()` calls and their `finally` blocks. `simplify`

## Control flow

- **P9** No `else` after a branch that ends in `return`, `raise`, `continue`, or `break`. `simplify`
- **P10** An `if` whose only statement is another `if` is one `if a and b`. `simplify`
- **P11** Return the expression. Delete an assignment that only the next `return` uses. `remove`
- **P12** Return the condition, not `True` and `False` from an `if`/`else`. `remove`
- **P13** Loops that return `True` or `False` on a match are `any()` or `all()`. `reuse`
- **P14** `if key in d`/`else` is `d.get(key, default)`. Write `d.get(key)`, not `d.get(key, None)`. `reuse`
- **P15** Delete `pass`, `...`, and `return None` statements that change nothing. `remove`

## Comprehensions and builtins

- **P16** A loop that only appends to a new list or dict is a comprehension. `simplify`
  Unless: it needs several `for` clauses or a complex filter.
- **P17** Delete `.keys()` in `in` tests and loops. Write `{}`, not an empty `dict()` call. `remove`
- **P18** Format strings with f-strings. No `%` formatting, no `.format()`. `simplify`
- **P19** Join paths with `pathlib.Path` and `/` in new code, not `os.path.join`. `simplify`

## Classes and functions

- **P20** A plain data class gets `@dataclass`. Delete the hand-written `__init__` and `__repr__`. `remove`
- **P21** Delete properties that only get and set one attribute. Make the attribute public. `remove`
- **P22** No `@staticmethod`. Write a module-level function. `simplify`
  Unless: an existing library API requires the method.
- **P23** A class with `__init__` and one other method is a function. `remove` [RD]
  Unless: the instance keeps state between calls, or a library requires the class.
- **P24** Call `super()` without arguments. `remove`
- **P25** Never use a mutable object as a default argument or as a dataclass field default. `lead`
- **P26** No `from module import *`. `lead`

## Types and async code

- **P27** Write `list[int]` and `X | None`, not `typing.List`, `Union`, or `Optional`. `simplify` Python 3.10
- **P28** Delete each `cast()`, `isinstance()`, and `# type: ignore` that mypy or pyright reports as unnecessary. `remove`
- **P29** Keep a reference to every `asyncio.create_task` result, or create the tasks in a `TaskGroup`. `lead` Python 3.11

**Sources.** [The Python sources](../../sources/languages/python.md) give, for each rule, the copied text that supports it. Rules marked [RD] are rules of reduce. Licenses are in [rule sources](../../guides/rule-sources.md).
