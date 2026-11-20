# What's New In Python 3.11

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Python Software Foundation
- Date: 2012-05-08
- License: PSF License 2.0
- Original location: https://docs.python.org/3/whatsnew/3.11.html
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# What’s New In Python 3.11[¶](#what-s-new-in-python-3-11)

- Editor:
- Pablo Galindo Salgado

This article explains the new features in Python 3.11, compared to 3.10.
Python 3.11 was released on October 24, 2022.
For full details, see the [changelog](changelog.html#changelog).

## Summary – Release highlights[¶](#summary-release-highlights)

- Python 3.11 is between 10-60% faster than Python 3.10.
On average, we measured a 1.25x speedup on the standard benchmark suite.
See [Faster CPython](#whatsnew311-faster-cpython) for details.

New syntax features:

New built-in features:

New standard library modules:

Interpreter improvements:

- [PEP 657: Fine-grained error locations in tracebacks](#whatsnew311-pep657)
- New [`-P`](../using/cmdline.html#cmdoption-P) command line option and [`PYTHONSAFEPATH`](../using/cmdline.html#envvar-PYTHONSAFEPATH) environment
variable to [disable automatically prepending potentially unsafe paths](#whatsnew311-pythonsafepath) to `sys.path`

New typing features:

- [PEP 646: Variadic generics](#whatsnew311-pep646)
- [PEP 655: Marking individual TypedDict items as required or not-required](#whatsnew311-pep655)
- [PEP 673: Self type](#whatsnew311-pep673)
- [PEP 675: Arbitrary literal string type](#whatsnew311-pep675)
- [PEP 681: Data class transforms](#whatsnew311-pep681)

Important deprecations, removals and restrictions:

- [**PEP 594**](https://peps.python.org/pep-0594/): [Many legacy standard library modules have been deprecated](#whatsnew311-pep594) and will be removed in Python 3.13
- [**PEP 624**](https://peps.python.org/pep-0624/): [Py\_UNICODE encoder APIs have been removed](#whatsnew311-pep624)
- [**PEP 670**](https://peps.python.org/pep-0670/): [Macros converted to static inline functions](#whatsnew311-pep670)

## New Features[¶](#new-features)

### PEP 657: Fine-grained error locations in tracebacks[¶](#pep-657-fine-grained-error-locations-in-tracebacks)

When printing tracebacks, the interpreter will now point to the exact expression that caused the error, instead of just the line. For example:

```
Traceback (most recent call last):
  File "distance.py", line 11, in <module>
    print(manhattan_distance(p1, p2))
          ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "distance.py", line 6, in manhattan_distance
    return abs(point_1.x - point_2.x) + abs(point_1.y - point_2.y)
                           ^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'x'
```
Previous versions of the interpreter would point to just the line, making it
ambiguous which object was `None`. These enhanced errors can also be helpful
when dealing with deeply nested [`dict`](../builtins/stdtypes.html#dict) objects and multiple function calls:

```
Traceback (most recent call last):
  File "query.py", line 37, in <module>
    magic_arithmetic('foo')
  File "query.py", line 18, in magic_arithmetic
    return add_counts(x) / 25
           ^^^^^^^^^^^^^
  File "query.py", line 24, in add_counts
    return 25 + query_user(user1) + query_user(user2)
                ^^^^^^^^^^^^^^^^^
  File "query.py", line 32, in query_user
    return 1 + query_count(db, response['a']['b']['c']['user'], retry=True)
                               ~~~~~~~~~~~~~~~~~~^^^^^
TypeError: 'NoneType' object is not subscriptable
```
As well as complex arithmetic expressions:

```
Traceback (most recent call last):
  File "calculation.py", line 54, in <module>
    result = (x / y / z) * (a / b / c)
              ~~~~~~^~~
ZeroDivisionError: division by zero
```
Additionally, the information used by the enhanced traceback feature
is made available via a general API, that can be used to correlate
[bytecode](../glossary.html#term-bytecode) [instructions](../library/dis.html#bytecodes) with source code location.
This information can be retrieved using:

- The [`codeobject.co_positions()`](../reference/datamodel.html#codeobject.co_positions) method in Python.
- The [`PyCode_Addr2Location()`](../c-api/code.html#c.PyCode_Addr2Location) function in the C API.

See [**PEP 657**](https://peps.python.org/pep-0657/) for more details. (Contributed by Pablo Galindo, Batuhan Taskaya
and Ammar Askar in [bpo-43950](https://bugs.python.org/issue?@action=redirect&bpo=43950).)

Note

This feature requires storing column positions in [Code Objects](../c-api/code.html#codeobjects),
which may result in a small increase in interpreter memory usage
and disk usage for compiled Python files.
To avoid storing the extra information
and deactivate printing the extra traceback information,
use the [`-X no_debug_ranges`](../using/cmdline.html#cmdoption-X) command line option
or the [`PYTHONNODEBUGRANGES`](../using/cmdline.html#envvar-PYTHONNODEBUGRANGES) environment variable.

### PEP 654: Exception Groups and `except*`[¶](#pep-654-exception-groups-and-except)

[**PEP 654**](https://peps.python.org/pep-0654/) introduces language features that enable a program
to raise and handle multiple unrelated exceptions simultaneously.
The builtin types [`ExceptionGroup`](../builtins/exceptions.html#ExceptionGroup) and [`BaseExceptionGroup`](../builtins/exceptions.html#BaseExceptionGroup)
make it possible to group exceptions and raise them together,
and the new [`except*`](../reference/compound_stmts.html#except-star) syntax generalizes
[`except`](../reference/compound_stmts.html#except) to match subgroups of exception groups.

See [**PEP 654**](https://peps.python.org/pep-0654/) for more details.

(Contributed by Irit Katriel in [bpo-45292](https://bugs.python.org/issue?@action=redirect&bpo=45292). PEP written by
Irit Katriel, Yury Selivanov and Guido van Rossum.)

### PEP 678: Exceptions can be enriched with notes[¶](#pep-678-exceptions-can-be-enriched-with-notes)

The [`add_note()`](../builtins/exceptions.html#BaseException.add_note) method is added to [`BaseException`](../builtins/exceptions.html#BaseException).
It can be used to enrich exceptions with context information
that is not available at the time when the exception is raised.
The added notes appear in the default traceback.

See [**PEP 678**](https://peps.python.org/pep-0678/) for more details.

(Contributed by Irit Katriel in [bpo-45607](https://bugs.python.org/issue?@action=redirect&bpo=45607).
PEP written by Zac Hatfield-Dodds.)

### Windows `py.exe` launcher improvements[¶](#windows-py-exe-launcher-improvements)

The copy of the [Python install manager](../using/windows.html#launcher) included with Python 3.11 has been significantly
updated. It now supports company/tag syntax as defined in [**PEP 514**](https://peps.python.org/pep-0514/) using the
`-V:` argument instead of the limited *\<company>*/*\<tag>*`-`.
This allows launching distributions other than *\<major>*.*\<minor>*`PythonCore`,
the one hosted on [python.org](https://www.python.org).

When using `-V:` selectors, either company or tag can be omitted, but all
installs will be searched. For example, `-V:OtherPython/` will select the
“best” tag registered for `OtherPython`, while `-V:3.11` or `-V:/3.11`
will select the “best” distribution with tag `3.11`.

When using the legacy `-`, *\<major>*`-`,
*\<major>*.*\<minor>*`-` or *\<major>*-*\<bitness>*`-` arguments,
all existing behaviour should be preserved from past versions,
and only releases from *\<major>*.*\<minor>*-*\<bitness>*`PythonCore` will be selected.
However, the `-64` suffix now implies “not 32-bit” (not necessarily x86-64),
as there are multiple supported 64-bit platforms.
32-bit runtimes are detected by checking the runtime’s tag for a `-32` suffix.
All releases of Python since 3.5 have included this in their 32-bit builds.

## Other Language Changes[¶](#other-language-changes)

- Starred unpacking expressions can now be used in [`for`](../reference/compound_stmts.html#for) statements.
(See [bpo-46725](https://bugs.python.org/issue?@action=redirect&bpo=46725) for more details.)
- Asynchronous [comprehensions](../reference/expressions.html#comprehensions) are now allowed
inside comprehensions in [asynchronous functions](../reference/compound_stmts.html#async-def).
Outer comprehensions implicitly become asynchronous in this case.
(Contributed by Serhiy Storchaka in [bpo-33346](https://bugs.python.org/issue?@action=redirect&bpo=33346).)
- A [`TypeError`](../builtins/exceptions.html#TypeError) is now raised instead of an [`AttributeError`](../builtins/exceptions.html#AttributeError) in [`with`](../reference/compound_stmts.html#with) statements and [`contextlib.ExitStack.enter_context()`](../library/contextlib.html#contextlib.ExitStack.enter_context) for objects that do not support the [context manager](../glossary.html#term-context-manager) protocol,
and in [`async with`](../reference/compound_stmts.html#async-with) statements and [`contextlib.AsyncExitStack.enter_async_context()`](../library/contextlib.html#contextlib.AsyncExitStack.enter_async_context) for objects not supporting the [asynchronous context manager](../glossary.html#term-asynchronous-context-manager) protocol.
(Contributed by Serhiy Storchaka in [bpo-12022](https://bugs.python.org/issue?@action=redirect&bpo=12022) and [bpo-44471](https://bugs.python.org/issue?@action=redirect&bpo=44471).)
- Added [`object.__getstate__()`](../library/pickle.html#object.__getstate__), which provides the default
implementation of the `__getstate__()` method. [`copy`](../library/copy.html#module-copy)ing
and [`pickle`](../library/pickle.html#module-pickle)ing instances of subclasses of builtin types [`bytearray`](../builtins/stdtypes.html#bytearray), [`set`](../builtins/stdtypes.html#set), [`frozenset`](../builtins/stdtypes.html#frozenset), [`collections.OrderedDict`](../library/collections.html#collections.OrderedDict), [`collections.deque`](../library/collections.html#collections.deque), [`weakref.WeakSet`](../library/weakref.html#weakref.WeakSet), and [`datetime.tzinfo`](../library/datetime.html#datetime.tzinfo) now copies and
pickles instance attributes implemented as [slots](../glossary.html#term-__slots__).
This change has an unintended side effect: It trips up a small minority
of existing Python projects not expecting `object.__getstate__()` to
exist. See the later comments on [gh-70766](https://github.com/python/cpython/issues/70766) for discussions of what
workarounds such code may need.
(Contributed by Serhiy Storchaka in [bpo-26579](https://bugs.python.org/issue?@action=redirect&bpo=26579).)

- Added a [`-P`](../using/cmdline.html#cmdoption-P) command line option
and a [`PYTHONSAFEPATH`](../using/cmdline.html#envvar-PYTHONSAFEPATH) environment variable,
which disable the automatic prepending to [`sys.path`](../library/sys.html#sys.path) of the script’s directory when running a script,
or the current directory when using [`-c`](../using/cmdline.html#cmdoption-c) and [`-m`](../using/cmdline.html#cmdoption-m).
This ensures only stdlib and installed modules
are picked up by [`import`](../reference/simple_stmts.html#import),
and avoids unintentionally or maliciously shadowing modules
with those in a local (and typically user-writable) directory.
(Contributed by Victor Stinner in [gh-57684](https://github.com/python/cpython/issues/57684).)
- A `"z"` option was added to the [Format specification mini-language](../library/string.html#formatspec) that
coerces negative to positive zero after rounding to the format precision.
See [**PEP 682**](https://peps.python.org/pep-0682/) for more details.
(Contributed by John Belmonte in [gh-90153](https://github.com/python/cpython/issues/90153).)
- Bytes are no longer accepted on [`sys.path`](../library/sys.html#sys.path).  Support broke sometime
between Python 3.2 and 3.6, with no one noticing until after Python 3.10.0
was released. In addition, bringing back support would be problematic due to
interactions between [`-b`](../using/cmdline.html#cmdoption-b) and [`sys.path_importer_cache`](../library/sys.html#sys.path_importer_cache) when
there is a mixture of [`str`](../builtins/stdtypes.html#str) and [`bytes`](../builtins/stdtypes.html#bytes) keys.
(Contributed by Thomas Grainger in [gh-91181](https://github.com/python/cpython/issues/91181).)

## Other CPython Implementation Changes[¶](#other-cpython-implementation-changes)

- The special methods [`__complex__()`](../reference/datamodel.html#object.__complex__) for [`complex`](../builtins/functions.html#complex) and [`__bytes__()`](../reference/datamodel.html#object.__bytes__) for [`bytes`](../builtins/stdtypes.html#bytes) are implemented to support
the [`typing.SupportsComplex`](../library/typing.html#typing.SupportsComplex) and [`typing.SupportsBytes`](../library/typing.html#typing.SupportsBytes) protocols.
(Contributed by Mark Dickinson and Donghee Na in [bpo-24234](https://bugs.python.org/issue?@action=redirect&bpo=24234).)
- `siphash13` is added as a new internal hashing algorithm.
It has similar security properties as `siphash24`,
but it is slightly faster for long inputs. [`str`](../builtins/stdtypes.html#str), [`bytes`](../builtins/stdtypes.html#bytes), and some other types
now use it as the default algorithm for [`hash()`](../builtins/functions.html#hash). **PEP 552**[hash-based .pyc files](../reference/import.html#pyc-invalidation) now use `siphash13` too.
(Contributed by Inada Naoki in [bpo-29410](https://bugs.python.org/issue?@action=redirect&bpo=29410).)
- When an active exception is re-raised by a [`raise`](../reference/simple_stmts.html#raise) statement with no parameters,
the traceback attached to this exception is now always `sys.exc_info()[1].__traceback__`.
This means that changes made to the traceback in the current [`except`](../reference/compound_stmts.html#except) clause are
reflected in the re-raised exception.
(Contributed by Irit Katriel in [bpo-45711](https://bugs.python.org/issue?@action=redirect&bpo=45711).)
- The interpreter state’s representation of handled exceptions
(aka `exc_info` or `_PyErr_StackItem`)
now only has the `exc_value` field; `exc_type` and `exc_traceback` have been removed, as they can be derived from `exc_value`.
(Contributed by Irit Katriel in [bpo-45711](https://bugs.python.org/issue?@action=redirect&bpo=45711).)
- A new [command line option](../using/windows.html#install-quiet-option), `AppendPath`,
has been added for the Windows installer.
It behaves similarly to `PrependPath`,
but appends the install and scripts directories instead of prepending them.
(Contributed by Bastian Neuburger in [bpo-44934](https://bugs.python.org/issue?@action=redirect&bpo=44934).)
- The [`PyConfig.module_search_paths_set`](../c-api/init_config.html#c.PyConfig.module_search_paths_set) field must now be set to `1` for
initialization to use [`PyConfig.module_search_paths`](../c-api/init_config.html#c.PyConfig.module_search_paths) to initialize [`sys.path`](../library/sys.html#sys.path). Otherwise, initialization will recalculate the path and replace
any values added to `module_search_paths`.
- The output of the [`--help`](../using/cmdline.html#cmdoption-help) option now fits in 50 lines/80 columns.
Information about [Python environment variables](../using/cmdline.html#using-on-envvars) and [`-X`](../using/cmdline.html#cmdoption-X) options is now available using the respective [`--help-env`](../using/cmdline.html#cmdoption-help-env) and [`--help-xoptions`](../using/cmdline.html#cmdoption-help-xoptions) flags,
and with the new [`--help-all`](../using/cmdline.html#cmdoption-help-all).
(Contributed by Éric Araujo in [bpo-46142](https://bugs.python.org/issue?@action=redirect&bpo=46142).)
- Converting between [`int`](../builtins/functions.html#int) and [`str`](../builtins/stdtypes.html#str) in bases other than 2
(binary), 4, 8 (octal), 16 (hexadecimal), or 32 such as base 10 (decimal)
now raises a [`ValueError`](../builtins/exceptions.html#ValueError) if the number of digits in string form is
above a limit to avoid potential denial of service attacks due to the
algorithmic complexity. This is a mitigation for [**CVE 2020-10735**](https://www.cve.org/CVERecord?id=CVE-2020-10735).
This limit can be configured or disabled by environment variable, command
line flag, or [`sys`](../library/sys.html#module-sys) APIs. See the [integer string conversion
length limitation](../builtins/stdtypes.html#int-max-str-digits) documentation.  The default limit
is 4300 digits in string form.

## New Modules[¶](#new-modules)

## Improved Modules[¶](#improved-modules)

### asyncio[¶](#asyncio)

- Added the [`TaskGroup`](../library/asyncio-task.html#asyncio.TaskGroup) class,
an [asynchronous context manager](../reference/datamodel.html#async-context-managers) holding a group of tasks that will wait for all of them upon exit.
For new code this is recommended over using [`create_task()`](../library/asyncio-task.html#asyncio.create_task) and [`gather()`](../library/asyncio-task.html#asyncio.gather) directly.
(Contributed by Yury Selivanov and others in [gh-90908](https://github.com/python/cpython/issues/90908).)
- Added [`timeout()`](../library/asyncio-task.html#asyncio.timeout), an asynchronous context manager for
setting a timeout on asynchronous operations. For new code this is
recommended over using [`wait_for()`](../library/asyncio-task.html#asyncio.wait_for) directly.
(Contributed by Andrew Svetlov in [gh-90927](https://github.com/python/cpython/issues/90927).)
- Added the [`Runner`](../library/asyncio-runner.html#asyncio.Runner) class, which exposes the machinery
used by [`run()`](../library/asyncio-runner.html#asyncio.run).
(Contributed by Andrew Svetlov in [gh-91218](https://github.com/python/cpython/issues/91218).)
- Added the [`Barrier`](../library/asyncio-sync.html#asyncio.Barrier) class to the synchronization
primitives in the asyncio library, and the related [`BrokenBarrierError`](../library/asyncio-sync.html#asyncio.BrokenBarrierError) exception.
(Contributed by Yves Duprat and Andrew Svetlov in [gh-87518](https://github.com/python/cpython/issues/87518).)
- Added keyword argument *all\_errors* to [`asyncio.loop.create_connection()`](../library/asyncio-eventloop.html#asyncio.loop.create_connection) so that multiple connection errors can be raised as an [`ExceptionGroup`](../builtins/exceptions.html#ExceptionGroup).
- Added the [`asyncio.StreamWriter.start_tls()`](../library/asyncio-stream.html#asyncio.StreamWriter.start_tls) method for
upgrading existing stream-based connections to TLS.
(Contributed by Ian Good in [bpo-34975](https://bugs.python.org/issue?@action=redirect&bpo=34975).)
- Added raw datagram socket functions to the event loop:
[`sock_sendto()`](../library/asyncio-eventloop.html#asyncio.loop.sock_sendto), [`sock_recvfrom()`](../library/asyncio-eventloop.html#asyncio.loop.sock_recvfrom) and [`sock_recvfrom_into()`](../library/asyncio-eventloop.html#asyncio.loop.sock_recvfrom_into).
These have implementations in [`SelectorEventLoop`](../library/asyncio-eventloop.html#asyncio.SelectorEventLoop) and [`ProactorEventLoop`](../library/asyncio-eventloop.html#asyncio.ProactorEventLoop).
(Contributed by Alex Grönholm in [bpo-46805](https://bugs.python.org/issue?@action=redirect&bpo=46805).)
- Added [`cancelling()`](../library/asyncio-task.html#asyncio.Task.cancelling) and [`uncancel()`](../library/asyncio-task.html#asyncio.Task.uncancel) methods to [`Task`](../library/asyncio-task.html#asyncio.Task).
These are primarily intended for internal use,
notably by [`TaskGroup`](../library/asyncio-task.html#asyncio.TaskGroup).

### contextlib[¶](#contextlib)

### dataclasses[¶](#dataclasses)

### datetime[¶](#datetime)

- Add [`datetime.UTC`](../library/datetime.html#datetime.UTC), a convenience alias for [`datetime.timezone.utc`](../library/datetime.html#datetime.timezone.utc). (Contributed by Kabir Kwatra in [gh-91973](https://github.com/python/cpython/issues/91973).)
- [`datetime.date.fromisoformat()`](../library/datetime.html#datetime.date.fromisoformat), [`datetime.time.fromisoformat()`](../library/datetime.html#datetime.time.fromisoformat) and [`datetime.datetime.fromisoformat()`](../library/datetime.html#datetime.datetime.fromisoformat) can now be used to parse most ISO 8601
formats (barring only those that support fractional hours and minutes).
(Contributed by Paul Ganssle in [gh-80010](https://github.com/python/cpython/issues/80010).)

### enum[¶](#enum)

- Renamed `EnumMeta` to [`EnumType`](../library/enum.html#enum.EnumType) (`EnumMeta` kept as an alias).
- Added [`StrEnum`](../library/enum.html#enum.StrEnum),
with members that can be used as (and must be) strings.
- Added [`ReprEnum`](../library/enum.html#enum.ReprEnum),
which only modifies the [`__repr__()`](../reference/datamodel.html#object.__repr__) of members
while returning their literal values (rather than names)
for [`__str__()`](../reference/datamodel.html#object.__str__) and [`__format__()`](../reference/datamodel.html#object.__format__) (used by [`str()`](../builtins/stdtypes.html#str), [`format()`](../builtins/functions.html#format) and [f-string](../glossary.html#term-f-string)s).
- Changed [`Enum.__format__()`](../library/enum.html#enum.Enum.__format__) (the default for [`format()`](../builtins/functions.html#format), [`str.format()`](../builtins/stdtypes.html#str.format) and [f-string](../glossary.html#term-f-string)s) to always produce
the same result as [`Enum.__str__()`](../library/enum.html#enum.Enum.__str__):  for enums inheriting from [`ReprEnum`](../library/enum.html#enum.ReprEnum) it will be the member’s value; for all other enums
it will be the enum and member name (e.g. `Color.RED`).
- Added a new *boundary* class parameter to [`Flag`](../library/enum.html#enum.Flag) enums
and the [`FlagBoundary`](../library/enum.html#enum.FlagBoundary) enum with its options,
to control how to handle out-of-range flag values.
- Added the [`verify()`](../library/enum.html#enum.verify) enum decorator
and the [`EnumCheck`](../library/enum.html#enum.EnumCheck) enum with its options,
to check enum classes against several specific constraints.
- Added the [`member()`](../library/enum.html#enum.member) and [`nonmember()`](../library/enum.html#enum.nonmember) decorators,
to ensure the decorated object is/is not converted to an enum member.
- Added the [`@property`](../library/enum.html#enum.property) decorator,
which works like [`@property`](../builtins/functions.html#property) except for enums.
Use this instead of [`types.DynamicClassAttribute()`](../library/types.html#types.DynamicClassAttribute).
- Added the [`global_enum()`](../library/enum.html#enum.global_enum) enum decorator,
which adjusts [`__repr__()`](../reference/datamodel.html#object.__repr__) and [`__str__()`](../reference/datamodel.html#object.__str__) to show values as members of their module rather than the enum class.
For example, `'re.ASCII'` for the [`ASCII`](../library/re.html#re.ASCII) member
of [`re.RegexFlag`](../library/re.html#re.RegexFlag) rather than `'RegexFlag.ASCII'`.
- Enhanced [`Flag`](../library/enum.html#enum.Flag) to support [`len()`](../builtins/functions.html#len), iteration and [`in`](../reference/expressions.html#in)/[`not in`](../reference/expressions.html#not-in) on its members.
For example, the following now works: `len(AFlag(3)) == 2 and list(AFlag(3)) == (AFlag.ONE, AFlag.TWO)`
- Changed [`Enum`](../library/enum.html#enum.Enum) and [`Flag`](../library/enum.html#enum.Flag) so that members are now defined
before [`__init_subclass__()`](../reference/datamodel.html#object.__init_subclass__) is called; [`dir()`](../builtins/functions.html#dir) now includes methods, etc., from mixed-in data types.
- Changed [`Flag`](../library/enum.html#enum.Flag) to only consider primary values (power of two) canonical
while composite values (`3`, `6`, `10`, etc.) are considered aliases;
inverted flags are coerced to their positive equivalent.

### fcntl[¶](#fcntl)

- On FreeBSD, the `F_DUP2FD` and `F_DUP2FD_CLOEXEC` flags respectively
are supported, the former equals to `dup2` usage while the latter set
the `FD_CLOEXEC` flag in addition.

### fractions[¶](#fractions)

### functools[¶](#functools)

- [`@functools.singledispatch`](../library/functools.html#functools.singledispatch) now supports [`types.UnionType`](../library/types.html#types.UnionType) and [`typing.Union`](../library/typing.html#typing.Union) as annotations to the dispatch argument.:
\>>> from functools import singledispatch >>> @singledispatch ... def fun(arg, verbose=False): ... if verbose: ... print("Let me just say,", end=" ") ... print(arg) ... >>> @fun.register ... def \_(arg: int | float, verbose=False): ... if verbose: ... print("Strength in numbers, eh?", end=" ") ... print(arg) ... >>> from typing import Union >>> @fun.register ... def \_(arg: Union\[list, set\], verbose=False): ... if verbose: ... print("Enumerate this:") ... for i, elem in enumerate(arg): ... print(i, elem) ... (Contributed by Yurii Karabas in [bpo-46014](https://bugs.python.org/issue?@action=redirect&bpo=46014).)

### gzip[¶](#gzip)

- The [`gzip.compress()`](../library/gzip.html#gzip.compress) function is now faster when used with the **mtime=0** argument as it delegates the compression entirely to a single [`zlib.compress()`](../library/zlib.html#zlib.compress) operation. There is one side effect of this change: The
gzip file header contains an “OS” byte in its header. That was traditionally
always set to a value of 255 representing “unknown” by the [`gzip`](../library/gzip.html#module-gzip) module. Now, when using `compress()` with **mtime=0**, it may be
set to a different value by the underlying zlib C library Python was linked
against.
(See [gh-112346](https://github.com/python/cpython/issues/112346) for details on the side effect.)

### hashlib[¶](#hashlib)

- [`hashlib.blake2b()`](../library/hashlib.html#hashlib.blake2b) and [`hashlib.blake2s()`](../library/hashlib.html#hashlib.blake2s) now prefer [libb2](https://www.blake2.net/) over Python’s vendored copy.
(Contributed by Christian Heimes in [bpo-47095](https://bugs.python.org/issue?@action=redirect&bpo=47095).)
- The internal `_sha3` module with SHA3 and SHAKE algorithms now uses *tiny\_sha3* instead of the *Keccak Code Package* to reduce code and binary
size. The [`hashlib`](../library/hashlib.html#module-hashlib) module prefers optimized SHA3 and SHAKE
implementations from OpenSSL. The change affects only installations without
OpenSSL support.
(Contributed by Christian Heimes in [bpo-47098](https://bugs.python.org/issue?@action=redirect&bpo=47098).)
- Add [`hashlib.file_digest()`](../library/hashlib.html#hashlib.file_digest), a helper function for efficient hashing
of files or file-like objects.
(Contributed by Christian Heimes in [gh-89313](https://github.com/python/cpython/issues/89313).)

### IDLE and idlelib[¶](#whatsnew311-idle)

### inspect[¶](#inspect)

- Add [`getmembers_static()`](../library/inspect.html#inspect.getmembers_static) to return all members without
triggering dynamic lookup via the descriptor protocol. (Contributed by
Weipeng Hong in [bpo-30533](https://bugs.python.org/issue?@action=redirect&bpo=30533).)
- Add [`ismethodwrapper()`](../library/inspect.html#inspect.ismethodwrapper) for checking if the type of an object is a [`MethodWrapperType`](../library/types.html#types.MethodWrapperType).
(Contributed by Hakan Çelik in [bpo-29418](https://bugs.python.org/issue?@action=redirect&bpo=29418).)
- Change the frame-related functions in the [`inspect`](../library/inspect.html#module-inspect) module to return new [`FrameInfo`](../library/inspect.html#inspect.FrameInfo) and [`Traceback`](../library/inspect.html#inspect.Traceback) class instances
(backwards compatible with the previous [named tuple](../glossary.html#term-named-tuple)-like interfaces)
that includes the extended [**PEP 657**](https://peps.python.org/pep-0657/) position information (end
line number, column and end column). The affected functions are:
  - `inspect.getframeinfo()`
  - `inspect.getouterframes()`
  - [`inspect.getinnerframes()`](../library/inspect.html#inspect.getinnerframes),
  - `inspect.stack()`
  - `inspect.trace()`
(Contributed by Pablo Galindo in [gh-88116](https://github.com/python/cpython/issues/88116).)

### locale[¶](#locale)

- Add [`locale.getencoding()`](../library/locale.html#locale.getencoding) to get the current locale encoding. It is similar to `locale.getpreferredencoding(False)` but ignores the [Python UTF-8 Mode](../library/os.html#utf8-mode).

### logging[¶](#logging)

- Added [`getLevelNamesMapping()`](../library/logging.html#logging.getLevelNamesMapping) to return a mapping from logging level names (e.g. `'CRITICAL'`)
to the values of their corresponding [Logging Levels](../library/logging.html#levels) (e.g. `50`, by default).
(Contributed by Andrei Kulakovin in [gh-88024](https://github.com/python/cpython/issues/88024).)
- Added a [`createSocket()`](../library/logging.handlers.html#logging.handlers.SysLogHandler.createSocket) method
to [`SysLogHandler`](../library/logging.handlers.html#logging.handlers.SysLogHandler), to match [`SocketHandler.createSocket()`](../library/logging.handlers.html#logging.handlers.SocketHandler.createSocket).
It is called automatically during handler initialization
and when emitting an event, if there is no active socket.
(Contributed by Kirill Pinchuk in [gh-88457](https://github.com/python/cpython/issues/88457).)

### math[¶](#math)

- Add [`math.exp2()`](../library/math.html#math.exp2): return 2 raised to the power of x.
(Contributed by Gideon Mitchell in [bpo-45917](https://bugs.python.org/issue?@action=redirect&bpo=45917).)
- Add [`math.cbrt()`](../library/math.html#math.cbrt): return the cube root of x.
(Contributed by Ajith Ramachandran in [bpo-44357](https://bugs.python.org/issue?@action=redirect&bpo=44357).)
- The behaviour of two [`math.pow()`](../library/math.html#math.pow) corner cases was changed, for
consistency with the IEEE 754 specification. The operations `math.pow(0.0, -math.inf)` and `math.pow(-0.0, -math.inf)` now return `inf`. Previously they raised [`ValueError`](../builtins/exceptions.html#ValueError). (Contributed by Mark
Dickinson in [bpo-44339](https://bugs.python.org/issue?@action=redirect&bpo=44339).)
- The [`math.nan`](../library/math.html#math.nan) value is now always available.
(Contributed by Victor Stinner in [bpo-46917](https://bugs.python.org/issue?@action=redirect&bpo=46917).)

### operator[¶](#operator)

- A new function `operator.call` has been added, such that `operator.call(obj, *args, **kwargs) == obj(*args, **kwargs)`.
(Contributed by Antony Lee in [bpo-44019](https://bugs.python.org/issue?@action=redirect&bpo=44019).)

### os[¶](#os)

- On Windows, [`os.urandom()`](../library/os.html#os.urandom) now uses `BCryptGenRandom()`,
instead of `CryptGenRandom()` which is deprecated.
(Contributed by Donghee Na in [bpo-44611](https://bugs.python.org/issue?@action=redirect&bpo=44611).)

### pathlib[¶](#pathlib)

### re[¶](#re)

- Atomic grouping (`(?>...)`) and possessive quantifiers (`*+`, `++`, `?+`, `{m,n}+`) are now supported in regular expressions.
(Contributed by Jeffrey C. Jacobs and Serhiy Storchaka in [bpo-433030](https://bugs.python.org/issue?@action=redirect&bpo=433030).)

### shutil[¶](#shutil)

- Add optional parameter *dir\_fd* in [`shutil.rmtree()`](../library/shutil.html#shutil.rmtree).
(Contributed by Serhiy Storchaka in [bpo-46245](https://bugs.python.org/issue?@action=redirect&bpo=46245).)

### socket[¶](#socket)

- Add CAN Socket support for NetBSD.
(Contributed by Thomas Klausner in [bpo-30512](https://bugs.python.org/issue?@action=redirect&bpo=30512).)
- [`create_connection()`](../library/socket.html#socket.create_connection) has an option to raise, in case of
failure to connect, an [`ExceptionGroup`](../builtins/exceptions.html#ExceptionGroup) containing all errors
instead of only raising the last error.
(Contributed by Irit Katriel in [bpo-29980](https://bugs.python.org/issue?@action=redirect&bpo=29980).)

### sqlite3[¶](#sqlite3)

- You can now disable the authorizer by passing [`None`](../builtins/constants.html#None) to [`set_authorizer()`](../library/sqlite3.html#sqlite3.Connection.set_authorizer).
(Contributed by Erlend E. Aasland in [bpo-44491](https://bugs.python.org/issue?@action=redirect&bpo=44491).)
- Collation name [`create_collation()`](../library/sqlite3.html#sqlite3.Connection.create_collation) can now
contain any Unicode character.  Collation names with invalid characters
now raise [`UnicodeEncodeError`](../builtins/exceptions.html#UnicodeEncodeError) instead of [`sqlite3.ProgrammingError`](../library/sqlite3.html#sqlite3.ProgrammingError).
(Contributed by Erlend E. Aasland in [bpo-44688](https://bugs.python.org/issue?@action=redirect&bpo=44688).)
- [`sqlite3`](../library/sqlite3.html#module-sqlite3) exceptions now include the SQLite extended error code as [`sqlite_errorcode`](../library/sqlite3.html#sqlite3.Error.sqlite_errorcode) and the SQLite error name as [`sqlite_errorname`](../library/sqlite3.html#sqlite3.Error.sqlite_errorname).
(Contributed by Aviv Palivoda, Daniel Shahaf, and Erlend E. Aasland in [bpo-16379](https://bugs.python.org/issue?@action=redirect&bpo=16379) and [bpo-24139](https://bugs.python.org/issue?@action=redirect&bpo=24139).)
- Add [`setlimit()`](../library/sqlite3.html#sqlite3.Connection.setlimit) and [`getlimit()`](../library/sqlite3.html#sqlite3.Connection.getlimit) to [`sqlite3.Connection`](../library/sqlite3.html#sqlite3.Connection) for
setting and getting SQLite limits by connection basis.
(Contributed by Erlend E. Aasland in [bpo-45243](https://bugs.python.org/issue?@action=redirect&bpo=45243).)
- [`sqlite3`](../library/sqlite3.html#module-sqlite3) now sets [`sqlite3.threadsafety`](../library/sqlite3.html#sqlite3.threadsafety) based on the default
threading mode the underlying SQLite library has been compiled with.
(Contributed by Erlend E. Aasland in [bpo-45613](https://bugs.python.org/issue?@action=redirect&bpo=45613).)
- [`sqlite3`](../library/sqlite3.html#module-sqlite3) C callbacks now use unraisable exceptions if callback
tracebacks are enabled. Users can now register an [`unraisable hook handler`](../library/sys.html#sys.unraisablehook) to improve their debug
experience.
(Contributed by Erlend E. Aasland in [bpo-45828](https://bugs.python.org/issue?@action=redirect&bpo=45828).)
- Fetch across rollback no longer raises [`InterfaceError`](../library/sqlite3.html#sqlite3.InterfaceError).
Instead we leave it to the SQLite library to handle these cases.
(Contributed by Erlend E. Aasland in [bpo-44092](https://bugs.python.org/issue?@action=redirect&bpo=44092).)
- Add [`serialize()`](../library/sqlite3.html#sqlite3.Connection.serialize) and [`deserialize()`](../library/sqlite3.html#sqlite3.Connection.deserialize) to [`sqlite3.Connection`](../library/sqlite3.html#sqlite3.Connection) for
serializing and deserializing databases.
(Contributed by Erlend E. Aasland in [bpo-41930](https://bugs.python.org/issue?@action=redirect&bpo=41930).)
- Add [`create_window_function()`](../library/sqlite3.html#sqlite3.Connection.create_window_function) to [`sqlite3.Connection`](../library/sqlite3.html#sqlite3.Connection) for creating aggregate window functions.
(Contributed by Erlend E. Aasland in [bpo-34916](https://bugs.python.org/issue?@action=redirect&bpo=34916).)
- Add [`blobopen()`](../library/sqlite3.html#sqlite3.Connection.blobopen) to [`sqlite3.Connection`](../library/sqlite3.html#sqlite3.Connection). [`sqlite3.Blob`](../library/sqlite3.html#sqlite3.Blob) allows incremental I/O operations on blobs.
(Contributed by Aviv Palivoda and Erlend E. Aasland in [bpo-24905](https://bugs.python.org/issue?@action=redirect&bpo=24905).)

### string[¶](#string)

- Add [`get_identifiers()`](../library/string.html#string.Template.get_identifiers) and [`is_valid()`](../library/string.html#string.Template.is_valid) to [`string.Template`](../library/string.html#string.Template),
which respectively return all valid placeholders,
and whether any invalid placeholders are present.
(Contributed by Ben Kehoe in [gh-90465](https://github.com/python/cpython/issues/90465).)

### sys[¶](#sys)

- [`sys.exc_info()`](../library/sys.html#sys.exc_info) now derives the `type` and `traceback` fields
from the `value` (the exception instance), so when an exception is
modified while it is being handled, the changes are reflected in
the results of subsequent calls to `exc_info()`.
(Contributed by Irit Katriel in [bpo-45711](https://bugs.python.org/issue?@action=redirect&bpo=45711).)
- Add [`sys.exception()`](../library/sys.html#sys.exception) which returns the active exception instance
(equivalent to `sys.exc_info()[1]`).
(Contributed by Irit Katriel in [bpo-46328](https://bugs.python.org/issue?@action=redirect&bpo=46328).)
- Add the [`sys.flags.safe_path`](../library/sys.html#sys.flags) flag.
(Contributed by Victor Stinner in [gh-57684](https://github.com/python/cpython/issues/57684).)

### sysconfig[¶](#sysconfig)

- Three new [installation schemes](../library/sysconfig.html#installation-paths) (*posix\_venv*, *nt\_venv* and *venv*) were added and are used when Python
creates new virtual environments or when it is running from a virtual
environment.
The first two schemes (*posix\_venv* and *nt\_venv*) are OS-specific
for non-Windows and Windows, the *venv* is essentially an alias to one of
them according to the OS Python runs on.
This is useful for downstream distributors who modify [`sysconfig.get_preferred_scheme()`](../library/sysconfig.html#sysconfig.get_preferred_scheme).
Third party code that creates new virtual environments should use the new *venv* installation scheme to determine the paths, as does [`venv`](../library/venv.html#module-venv).
(Contributed by Miro Hrončok in [bpo-45413](https://bugs.python.org/issue?@action=redirect&bpo=45413).)

### tempfile[¶](#tempfile)

- [`SpooledTemporaryFile`](../library/tempfile.html#tempfile.SpooledTemporaryFile) objects now fully implement the methods
of [`io.BufferedIOBase`](../library/io.html#io.BufferedIOBase) or [`io.TextIOBase`](../library/io.html#io.TextIOBase) (depending on file mode).
This lets them work correctly with APIs that expect file-like objects,
such as compression modules.
(Contributed by Carey Metcalfe in [gh-70363](https://github.com/python/cpython/issues/70363).)

### threading[¶](#threading)

- On Unix, if the `sem_clockwait()` function is available in the C library
(glibc 2.30 and newer), the [`threading.Lock.acquire()`](../library/threading.html#threading.Lock.acquire) method now uses
the monotonic clock ([`time.CLOCK_MONOTONIC`](../library/time.html#time.CLOCK_MONOTONIC)) for the timeout, rather
than using the system clock ([`time.CLOCK_REALTIME`](../library/time.html#time.CLOCK_REALTIME)), to not be affected
by system clock changes.
(Contributed by Victor Stinner in [bpo-41710](https://bugs.python.org/issue?@action=redirect&bpo=41710).)

### time[¶](#time)

- On Unix, [`time.sleep()`](../library/time.html#time.sleep) now uses the `clock_nanosleep()` or `nanosleep()` function, if available, which has a resolution of 1 nanosecond
(10<sup>-9</sup> seconds), rather than using `select()` which has a resolution
of 1 microsecond (10<sup>-6</sup> seconds).
(Contributed by Benjamin Szőke and Victor Stinner in [bpo-21302](https://bugs.python.org/issue?@action=redirect&bpo=21302).)
- On Windows 8.1 and newer, [`time.sleep()`](../library/time.html#time.sleep) now uses a waitable timer based
on [high-resolution timers](https://docs.microsoft.com/en-us/windows-hardware/drivers/kernel/high-resolution-timers) which has a resolution of 100 nanoseconds (10<sup>-7</sup> seconds). Previously,
it had a resolution of 1 millisecond (10<sup>-3</sup> seconds).
(Contributed by Benjamin Szőke, Donghee Na, Eryk Sun and Victor Stinner in [bpo-21302](https://bugs.python.org/issue?@action=redirect&bpo=21302) and [bpo-45429](https://bugs.python.org/issue?@action=redirect&bpo=45429).)

### tkinter[¶](#tkinter)

- Added method `info_patchlevel()` which returns the exact version of
the Tcl library as a named tuple similar to [`sys.version_info`](../library/sys.html#sys.version_info).
(Contributed by Serhiy Storchaka in [gh-91827](https://github.com/python/cpython/issues/91827).)

### traceback[¶](#traceback)

- Add [`traceback.StackSummary.format_frame_summary()`](../library/traceback.html#traceback.StackSummary.format_frame_summary) to allow users
to override which frames appear in the traceback, and how they are
formatted.
(Contributed by Ammar Askar in [bpo-44569](https://bugs.python.org/issue?@action=redirect&bpo=44569).)
- Add [`traceback.TracebackException.print()`](../library/traceback.html#traceback.TracebackException.print), which prints the
formatted [`TracebackException`](../library/traceback.html#traceback.TracebackException) instance to a file.
(Contributed by Irit Katriel in [bpo-33809](https://bugs.python.org/issue?@action=redirect&bpo=33809).)

### typing[¶](#typing)

For major changes, see [New Features Related to Type Hints](#new-feat-related-type-hints-311).

- Add [`typing.assert_never()`](../library/typing.html#typing.assert_never) and [`typing.Never`](../library/typing.html#typing.Never). `typing.assert_never()` is useful for asking a type checker to confirm
that a line of code is not reachable. At runtime, it raises an [`AssertionError`](../builtins/exceptions.html#AssertionError).
(Contributed by Jelle Zijlstra in [gh-90633](https://github.com/python/cpython/issues/90633).)
- Add [`typing.reveal_type()`](../library/typing.html#typing.reveal_type). This is useful for asking a type checker
what type it has inferred for a given expression. At runtime it prints
the type of the received value.
(Contributed by Jelle Zijlstra in [gh-90572](https://github.com/python/cpython/issues/90572).)
- Add [`typing.assert_type()`](../library/typing.html#typing.assert_type). This is useful for asking a type checker
to confirm that the type it has inferred for a given expression matches
the given type. At runtime it simply returns the received value.
(Contributed by Jelle Zijlstra in [gh-90638](https://github.com/python/cpython/issues/90638).)
- [`typing.TypedDict`](../library/typing.html#typing.TypedDict) types can now be generic. (Contributed by
Samodya Abeysiriwardane in [gh-89026](https://github.com/python/cpython/issues/89026).)
- [`NamedTuple`](../library/typing.html#typing.NamedTuple) types can now be generic.
(Contributed by Serhiy Storchaka in [bpo-43923](https://bugs.python.org/issue?@action=redirect&bpo=43923).)
- Allow subclassing of [`typing.Any`](../library/typing.html#typing.Any). This is useful for avoiding
type checker errors related to highly dynamic class, such as mocks.
(Contributed by Shantanu Jain in [gh-91154](https://github.com/python/cpython/issues/91154).)
- The [`@typing.final`](../library/typing.html#typing.final) decorator now sets the `__final__` attributed on
the decorated object.
(Contributed by Jelle Zijlstra in [gh-90500](https://github.com/python/cpython/issues/90500).)
- The [`typing.get_overloads()`](../library/typing.html#typing.get_overloads) function can be used for introspecting
the overloads of a function. [`typing.clear_overloads()`](../library/typing.html#typing.clear_overloads) can be used
to clear all registered overloads of a function.
(Contributed by Jelle Zijlstra in [gh-89263](https://github.com/python/cpython/issues/89263).)
- The [`__init__()`](../reference/datamodel.html#object.__init__) method of [`Protocol`](../library/typing.html#typing.Protocol) subclasses
is now preserved. (Contributed by Adrian Garcia Badarasco in [gh-88970](https://github.com/python/cpython/issues/88970).)
- The representation of empty tuple types (`Tuple[()]`) is simplified.
This affects introspection, e.g. `get_args(Tuple[()])` now evaluates
to `()` instead of `((),)`.
(Contributed by Serhiy Storchaka in [gh-91137](https://github.com/python/cpython/issues/91137).)
- Loosen runtime requirements for type annotations by removing the callable
check in the private `typing._type_check` function. (Contributed by
Gregory Beauregard in [gh-90802](https://github.com/python/cpython/issues/90802).)
- [`typing.get_type_hints()`](../library/typing.html#typing.get_type_hints) now supports evaluating strings as forward
references in [PEP 585 generic aliases](../builtins/stdtypes.html#types-genericalias).
(Contributed by Niklas Rosenstein in [gh-85542](https://github.com/python/cpython/issues/85542).)
- [`typing.get_type_hints()`](../library/typing.html#typing.get_type_hints) no longer adds [`Optional`](../library/typing.html#typing.Optional) to parameters with `None` as a default. (Contributed by Nikita Sobolev
in [gh-90353](https://github.com/python/cpython/issues/90353).)
- [`typing.get_type_hints()`](../library/typing.html#typing.get_type_hints) now supports evaluating bare stringified [`ClassVar`](../library/typing.html#typing.ClassVar) annotations. (Contributed by Gregory Beauregard
in [gh-90711](https://github.com/python/cpython/issues/90711).)
- [`@typing.no_type_check`](../library/typing.html#typing.no_type_check) no longer modifies external classes and functions.
It also now correctly marks classmethods as not to be type checked. (Contributed
by Nikita Sobolev in [gh-90729](https://github.com/python/cpython/issues/90729).)

### unicodedata[¶](#unicodedata)

- The Unicode database has been updated to version 14.0.0.
(Contributed by Benjamin Peterson in [bpo-45190](https://bugs.python.org/issue?@action=redirect&bpo=45190)).

### unittest[¶](#unittest)

- Added methods [`enterContext()`](../library/unittest.html#unittest.TestCase.enterContext) and [`enterClassContext()`](../library/unittest.html#unittest.TestCase.enterClassContext) of class [`TestCase`](../library/unittest.html#unittest.TestCase), method [`enterAsyncContext()`](../library/unittest.html#unittest.IsolatedAsyncioTestCase.enterAsyncContext) of
class [`IsolatedAsyncioTestCase`](../library/unittest.html#unittest.IsolatedAsyncioTestCase) and function [`unittest.enterModuleContext()`](../library/unittest.html#unittest.enterModuleContext).
(Contributed by Serhiy Storchaka in [bpo-45046](https://bugs.python.org/issue?@action=redirect&bpo=45046).)

### venv[¶](#venv)

- When new Python virtual environments are created, the *venv* [sysconfig installation scheme](../library/sysconfig.html#installation-paths) is used
to determine the paths inside the environment.
When Python runs in a virtual environment, the same installation scheme
is the default.
That means that downstream distributors can change the default sysconfig install
scheme without changing behavior of virtual environments.
Third party code that also creates new virtual environments should do the same.
(Contributed by Miro Hrončok in [bpo-45413](https://bugs.python.org/issue?@action=redirect&bpo=45413).)

### warnings[¶](#warnings)

- [`warnings.catch_warnings()`](../library/warnings.html#warnings.catch_warnings) now accepts arguments for [`warnings.simplefilter()`](../library/warnings.html#warnings.simplefilter),
providing a more concise way to locally ignore warnings or convert them to errors.
(Contributed by Zac Hatfield-Dodds in [bpo-47074](https://bugs.python.org/issue?@action=redirect&bpo=47074).)

### zipfile[¶](#zipfile)

- Added support for specifying member name encoding for reading metadata
in a [`ZipFile`](../library/zipfile.html#zipfile.ZipFile)’s directory and file headers.
(Contributed by Stephen J. Turnbull and Serhiy Storchaka in [bpo-28080](https://bugs.python.org/issue?@action=redirect&bpo=28080).)
- Added [`ZipFile.mkdir()`](../library/zipfile.html#zipfile.ZipFile.mkdir) for creating new directories inside ZIP archives.
(Contributed by Sam Ezeh in [gh-49083](https://github.com/python/cpython/issues/49083).)
- Added [`stem`](../library/zipfile.html#zipfile.Path.stem), [`suffix`](../library/zipfile.html#zipfile.Path.suffix) and [`suffixes`](../library/zipfile.html#zipfile.Path.suffixes) to [`zipfile.Path`](../library/zipfile.html#zipfile.Path).
(Contributed by Miguel Brito in [gh-88261](https://github.com/python/cpython/issues/88261).)

## Optimizations[¶](#optimizations)

This section covers specific optimizations independent of the
[Faster CPython](#whatsnew311-faster-cpython) project, which is covered in its own section.

- The compiler now optimizes simple
[printf-style % formatting](../builtins/stdtypes.html#old-string-formatting) on string literals
containing only the format codes `%s`, `%r` and `%a` and makes it as
fast as a corresponding [f-string](../glossary.html#term-f-string) expression.
(Contributed by Serhiy Storchaka in [bpo-28307](https://bugs.python.org/issue?@action=redirect&bpo=28307).)
- Integer division (`//`) is better tuned for optimization by compilers.
It is now around 20% faster on x86-64 when dividing an [`int`](../builtins/functions.html#int) by a value smaller than `2**30`.
(Contributed by Gregory P. Smith and Tim Peters in [gh-90564](https://github.com/python/cpython/issues/90564).)
- [`sum()`](../builtins/functions.html#sum) is now nearly 30% faster for integers smaller than `2**30`.
(Contributed by Stefan Behnel in [gh-68264](https://github.com/python/cpython/issues/68264).)
- Resizing lists is streamlined for the common case,
speeding up [`list.append()`](../builtins/stdtypes.html#list.append) by ≈15%
and simple [list comprehension](../glossary.html#term-list-comprehension)s by up to 20-30%
(Contributed by Dennis Sweeney in [gh-91165](https://github.com/python/cpython/issues/91165).)
- Dictionaries don’t store hash values when all keys are Unicode objects,
decreasing [`dict`](../builtins/stdtypes.html#dict) size.
For example, `sys.getsizeof(dict.fromkeys("abcdefg"))` is reduced from 352 bytes to 272 bytes (23% smaller) on 64-bit platforms.
(Contributed by Inada Naoki in [bpo-46845](https://bugs.python.org/issue?@action=redirect&bpo=46845).)
- Using [`asyncio.DatagramProtocol`](../library/asyncio-protocol.html#asyncio.DatagramProtocol) is now orders of magnitude faster
when transferring large files over UDP,
with speeds over 100 times higher for a ≈60 MiB file.
(Contributed by msoxzw in [gh-91487](https://github.com/python/cpython/issues/91487).)
- [`math`](../library/math.html#module-math) functions [`comb()`](../library/math.html#math.comb) and [`perm()`](../library/math.html#math.perm) are now
≈10 times faster for large arguments (with a larger speedup for larger *k*).
(Contributed by Serhiy Storchaka in [bpo-37295](https://bugs.python.org/issue?@action=redirect&bpo=37295).)
- The [`statistics`](../library/statistics.html#module-statistics) functions [`mean()`](../library/statistics.html#statistics.mean), [`variance()`](../library/statistics.html#statistics.variance) and [`stdev()`](../library/statistics.html#statistics.stdev) now consume
iterators in one pass rather than converting them to a [`list`](../builtins/stdtypes.html#list) first.
This is twice as fast and can save substantial memory.
(Contributed by Raymond Hettinger in [gh-90415](https://github.com/python/cpython/issues/90415).)
- [`unicodedata.normalize()`](../library/unicodedata.html#unicodedata.normalize) now normalizes pure-ASCII strings in constant time.
(Contributed by Donghee Na in [bpo-44987](https://bugs.python.org/issue?@action=redirect&bpo=44987).)

## Faster CPython[¶](#faster-cpython)

CPython 3.11 is an average of
[25% faster](https://github.com/faster-cpython/ideas#published-results)
than CPython 3.10 as measured with the
[pyperformance](https://github.com/python/pyperformance) benchmark suite,
when compiled with GCC on Ubuntu Linux.
Depending on your workload, the overall speedup could be 10-60%.

This project focuses on two major areas in Python:
[Faster Startup](#whatsnew311-faster-startup) and [Faster Runtime](#whatsnew311-faster-runtime).
Optimizations not covered by this project are listed separately under
[Optimizations](#whatsnew311-optimizations).

### Faster Startup[¶](#faster-startup)

#### Frozen imports / Static code objects[¶](#frozen-imports-static-code-objects)

Python caches [bytecode](../glossary.html#term-bytecode) in the [\_\_pycache\_\_](../tutorial/modules.html#tut-pycache)
directory to speed up module loading.

Previously in 3.10, Python module execution looked like this:

```
Read __pycache__ -> Unmarshal -> Heap allocated code object -> Evaluate
```
In Python 3.11, the core modules essential for Python startup are “frozen”.
This means that their [Code Objects](../c-api/code.html#codeobjects) (and bytecode)
are statically allocated by the interpreter.
This reduces the steps in module execution process to:

```
Statically allocated code object -> Evaluate
```
Interpreter startup is now 10-15% faster in Python 3.11. This has a big impact for short-running programs using Python.

(Contributed by Eric Snow, Guido van Rossum and Kumar Aditya in many issues.)

### Faster Runtime[¶](#faster-runtime)

#### Cheaper, lazy Python frames[¶](#cheaper-lazy-python-frames)

Python frames, holding execution information, are created whenever Python calls a Python function. The following are new frame optimizations:

- Streamlined the frame creation process.
- Avoided memory allocation by generously re-using frame space on the C stack.
- Streamlined the internal frame struct to contain only essential information. Frames previously held extra debugging and memory management information.

Old-style [frame objects](../reference/datamodel.html#frame-objects)
are now created only when requested by debuggers
or by Python introspection functions such as [`sys._getframe()`](../library/sys.html#sys._getframe) and
[`inspect.currentframe()`](../library/inspect.html#inspect.currentframe). For most user code, no frame objects are
created at all. As a result, nearly all Python functions calls have sped
up significantly. We measured a 3-7% speedup in pyperformance.

(Contributed by Mark Shannon in [bpo-44590](https://bugs.python.org/issue?@action=redirect&bpo=44590).)

#### Inlined Python function calls[¶](#inlined-python-function-calls)

During a Python function call, Python will call an evaluating C function to interpret that function’s code. This effectively limits pure Python recursion to what’s safe for the C stack.

In 3.11, when CPython detects Python code calling another Python function, it sets up a new frame, and “jumps” to the new code inside the new frame. This avoids calling the C interpreting function altogether.

Most Python function calls now consume no C stack space, speeding them up.
In simple recursive functions like fibonacci or
factorial, we observed a 1.7x speedup. This also means recursive functions
can recurse significantly deeper
(if the user increases the recursion limit with [`sys.setrecursionlimit()`](../library/sys.html#sys.setrecursionlimit)).
We measured a 1-3% improvement in pyperformance.

(Contributed by Pablo Galindo and Mark Shannon in [bpo-45256](https://bugs.python.org/issue?@action=redirect&bpo=45256).)

#### PEP 659: Specializing Adaptive Interpreter[¶](#pep-659-specializing-adaptive-interpreter)

[**PEP 659**](https://peps.python.org/pep-0659/) is one of the key parts of the Faster CPython project. The general
idea is that while Python is a dynamic language, most code has regions where
objects and types rarely change. This concept is known as *type stability*.

At runtime, Python will try to look for common patterns and type stability
in the executing code. Python will then replace the current operation with a
more specialized one. This specialized operation uses fast paths available only
to those use cases/types, which generally outperform their generic
counterparts. This also brings in another concept called *inline caching*, where
Python caches the results of expensive operations directly in the
[bytecode](../glossary.html#term-bytecode).

The specializer will also combine certain common instruction pairs into one superinstruction, reducing the overhead during execution.

Python will only specialize when it sees code that is “hot” (executed multiple times). This prevents Python from wasting time on run-once code. Python can also de-specialize when code is too dynamic or when the use changes. Specialization is attempted periodically, and specialization attempts are not too expensive, allowing specialization to adapt to new circumstances.

(PEP written by Mark Shannon, with ideas inspired by Stefan Brunthaler.
See [**PEP 659**](https://peps.python.org/pep-0659/) for more information. Implementation by Mark Shannon and Brandt
Bucher, with additional help from Irit Katriel and Dennis Sweeney.)

| Operation | Form | Specialization | Operation speedup (up to) | Contributor(s) | 
|---|---|---|---|---|
| Binary operations | `x + x` `x - x` `x * x` | Binary add, multiply and subtract for common types such as [`int`](../builtins/functions.html#int), [`float`](../builtins/functions.html#float) and [`str`](../builtins/stdtypes.html#str) take custom fast paths for their underlying types. | 10% | Mark Shannon, Donghee Na, Brandt Bucher, Dennis Sweeney | 
| Subscript | `a[i]` | Subscripting container types such as [`list`](../builtins/stdtypes.html#list), [`tuple`](../builtins/stdtypes.html#tuple) and [`dict`](../builtins/stdtypes.html#dict) directly index the underlying data structures. Subscripting custom [`__getitem__()`](../reference/datamodel.html#object.__getitem__) is also inlined similar to [Inlined Python function calls](#inline-calls). | 10-25% | Irit Katriel, Mark Shannon | 
| Store subscript | `a[i] = z` | Similar to subscripting specialization above. | 10-25% | Dennis Sweeney | 
| Calls | `f(arg)` `C(arg)` | Calls to common builtin (C) functions and types such as [`len()`](../builtins/functions.html#len) and [`str`](../builtins/stdtypes.html#str) directly call their underlying C version. This avoids going through the internal calling convention. | 20% | Mark Shannon, Ken Jin | 
| Load global variable | `print` `len` | The object’s index in the globals/builtins namespace is cached. Loading globals and builtins require zero namespace lookups. | [\[1\]](#load-global) | Mark Shannon | 
| Load attribute | `o.attr` | Similar to loading global variables. The attribute’s index inside the class/object’s namespace is cached. In most cases, attribute loading will require zero namespace lookups. | [\[2\]](#load-attr) | Mark Shannon | 
| Load methods for call | `o.meth()` | The actual address of the method is cached. Method loading now has no namespace lookups – even for classes with long inheritance chains. | 10-20% | Ken Jin, Mark Shannon | 
| Store attribute | `o.attr = z` | Similar to load attribute optimization. | 2% in pyperformance | Mark Shannon | 
| Unpack Sequence | `*seq` | Specialized for common containers such as [`list`](../builtins/stdtypes.html#list) and [`tuple`](../builtins/stdtypes.html#tuple). Avoids internal calling convention. | 8% | Brandt Bucher | 

### Misc[¶](#misc)

- Objects now require less memory due to lazily created object namespaces.
Their namespace dictionaries now also share keys more freely.
(Contributed Mark Shannon in [bpo-45340](https://bugs.python.org/issue?@action=redirect&bpo=45340) and [bpo-40116](https://bugs.python.org/issue?@action=redirect&bpo=40116).)
- “Zero-cost” exceptions are implemented, eliminating the cost
of [`try`](../reference/compound_stmts.html#try) statements when no exception is raised.
(Contributed by Mark Shannon in [bpo-40222](https://bugs.python.org/issue?@action=redirect&bpo=40222).)
- A more concise representation of exceptions in the interpreter reduced the
time required for catching an exception by about 10%.
(Contributed by Irit Katriel in [bpo-45711](https://bugs.python.org/issue?@action=redirect&bpo=45711).)
- [`re`](../library/re.html#module-re)’s regular expression matching engine has been partially refactored,
and now uses computed gotos (or “threaded code”) on supported platforms. As a
result, Python 3.11 executes the [pyperformance regular expression benchmarks](https://pyperformance.readthedocs.io/benchmarks.html#regex-dna) up to 10%
faster than Python 3.10.
(Contributed by Brandt Bucher in [gh-91404](https://github.com/python/cpython/issues/91404).)

### FAQ[¶](#faq)

#### How should I write my code to utilize these speedups?[¶](#how-should-i-write-my-code-to-utilize-these-speedups)

Write Pythonic code that follows common best practices; you don’t have to change your code. The Faster CPython project optimizes for common code patterns we observe.

#### Will CPython 3.11 use more memory?[¶](#will-cpython-3-11-use-more-memory)

Maybe not; we don’t expect memory use to exceed 20% higher than 3.10. This is offset by memory optimizations for frame objects and object dictionaries as mentioned above.

#### I don’t see any speedups in my workload. Why?[¶](#i-don-t-see-any-speedups-in-my-workload-why)

Certain code won’t have noticeable benefits. If your code spends most of its time on I/O operations, or already does most of its computation in a C extension library like NumPy, there won’t be significant speedups. This project currently benefits pure-Python workloads the most.

Furthermore, the pyperformance figures are a geometric mean. Even within the pyperformance benchmarks, certain benchmarks have slowed down slightly, while others have sped up by nearly 2x!

#### Is there a JIT compiler?[¶](#is-there-a-jit-compiler)

No. We’re still exploring other optimizations.

### About[¶](#about)

Faster CPython explores optimizations for [CPython](../glossary.html#term-CPython). The main team is
funded by Microsoft to work on this full-time. Pablo Galindo Salgado is also
funded by Bloomberg LP to work on the project part-time. Finally, many
contributors are volunteers from the community.

## CPython bytecode changes[¶](#cpython-bytecode-changes)

The bytecode now contains inline cache entries,
which take the form of the newly-added [`CACHE`](../library/dis.html#opcode-CACHE) instructions.
Many opcodes expect to be followed by an exact number of caches,
and instruct the interpreter to skip over them at runtime.
Populated caches can look like arbitrary instructions,
so great care should be taken when reading or modifying
raw, adaptive bytecode containing quickened data.

### New opcodes[¶](#new-opcodes)

- `ASYNC_GEN_WRAP`, [`RETURN_GENERATOR`](../library/dis.html#opcode-RETURN_GENERATOR) and [`SEND`](../library/dis.html#opcode-SEND),
used in generators and co-routines.
- [`COPY_FREE_VARS`](../library/dis.html#opcode-COPY_FREE_VARS),
which avoids needing special caller-side code for closures.
- [`JUMP_BACKWARD_NO_INTERRUPT`](../library/dis.html#opcode-JUMP_BACKWARD_NO_INTERRUPT),
for use in certain loops where handling interrupts is undesirable.
- [`MAKE_CELL`](../library/dis.html#opcode-MAKE_CELL), to create [Cell Objects](../c-api/cell.html#cell-objects).
- [`CHECK_EG_MATCH`](../library/dis.html#opcode-CHECK_EG_MATCH) and `PREP_RERAISE_STAR`,
to handle the [new exception groups and except\*](#whatsnew311-pep654) added in [**PEP 654**](https://peps.python.org/pep-0654/).
- [`PUSH_EXC_INFO`](../library/dis.html#opcode-PUSH_EXC_INFO), for use in exception handlers.
- [`RESUME`](../library/dis.html#opcode-RESUME), a no-op,
for internal tracing, debugging and optimization checks.

### Replaced opcodes[¶](#replaced-opcodes)

| Replaced Opcode(s) | New Opcode(s) | Notes | 
|---|---|---|
| `BINARY_*``INPLACE_*` | `BINARY_OP` | Replaced all numeric binary/in-place opcodes with a single opcode | 
| `CALL_FUNCTION``CALL_FUNCTION_KW``CALL_METHOD` |  | Decouples argument shifting for methods from handling of keyword arguments; allows better specialization of calls | 
| `DUP_TOP``DUP_TOP_TWO``ROT_TWO``ROT_THREE``ROT_FOUR``ROT_N` |  | Stack manipulation instructions | 
| `JUMP_IF_NOT_EXC_MATCH` |  | Now performs check but doesn’t jump | 
| `JUMP_ABSOLUTE``POP_JUMP_IF_FALSE``POP_JUMP_IF_TRUE` |  | See [\[3\]](#bytecode-jump); `TRUE`, `FALSE`, `NONE` and `NOT_NONE` variants for each direction | 
| `SETUP_WITH``SETUP_ASYNC_WITH` | `BEFORE_WITH` | [`with`](../reference/compound_stmts.html#with) block setup | 

[3](#id4)\]

All jump opcodes are now relative, including the
existing `JUMP_IF_TRUE_OR_POP` and `JUMP_IF_FALSE_OR_POP`.
The argument is now an offset from the current instruction
rather than an absolute location.

### Changed/removed opcodes[¶](#changed-removed-opcodes)

- Changed [`MATCH_CLASS`](../library/dis.html#opcode-MATCH_CLASS) and [`MATCH_KEYS`](../library/dis.html#opcode-MATCH_KEYS) to no longer push an additional boolean value to indicate success/failure.
Instead, `None` is pushed on failure
in place of the tuple of extracted values.
- Changed opcodes that work with exceptions to reflect them
now being represented as one item on the stack instead of three
(see [gh-89874](https://github.com/python/cpython/issues/89874)).
- Removed `COPY_DICT_WITHOUT_KEYS`, `GEN_START`, `POP_BLOCK`, `SETUP_FINALLY` and `YIELD_FROM`.

## Deprecated[¶](#deprecated)

This section lists Python APIs that have been deprecated in Python 3.11.

Deprecated C APIs are [listed separately](#whatsnew311-c-api-deprecated).

### Language/Builtins[¶](#language-builtins)

- Chaining [`classmethod`](../builtins/functions.html#classmethod) descriptors (introduced in [bpo-19072](https://bugs.python.org/issue?@action=redirect&bpo=19072))
is now deprecated.  It can no longer be used to wrap other descriptors
such as [`property`](../builtins/functions.html#property).  The core design of this feature was flawed
and caused a number of downstream problems.  To “pass-through” a `classmethod`, consider using the `__wrapped__` attribute
that was added in Python 3.10.
(Contributed by Raymond Hettinger in [gh-89519](https://github.com/python/cpython/issues/89519).)
- Octal escapes in string and bytes literals with values larger than `0o377` (255 in decimal) now produce a [`DeprecationWarning`](../builtins/exceptions.html#DeprecationWarning).
In a future Python version, they will raise a [`SyntaxWarning`](../builtins/exceptions.html#SyntaxWarning) and
eventually a [`SyntaxError`](../builtins/exceptions.html#SyntaxError).
(Contributed by Serhiy Storchaka in [gh-81548](https://github.com/python/cpython/issues/81548).)
- The delegation of [`int()`](../builtins/functions.html#int) to [`__trunc__()`](../reference/datamodel.html#object.__trunc__) is now deprecated.
Calling `int(a)` when `type(a)` implements `__trunc__()` but not [`__int__()`](../reference/datamodel.html#object.__int__) or [`__index__()`](../reference/datamodel.html#object.__index__) now raises
a [`DeprecationWarning`](../builtins/exceptions.html#DeprecationWarning).
(Contributed by Zackery Spytz in [bpo-44977](https://bugs.python.org/issue?@action=redirect&bpo=44977).)

### Modules[¶](#modules)

- [**PEP 594**](https://peps.python.org/pep-0594/) led to the deprecations of the following modules
slated for removal in Python 3.13:
`aifc`
`chunk`
`msilib`
`pipes`
`telnetlib`
`audioop`
`crypt`
`nis`
`sndhdr`
`uu`
`cgi`
`imghdr`
`nntplib`
`spwd`
`xdrlib`
`cgitb`
`mailcap`
`ossaudiodev`
`sunau`
(Contributed by Brett Cannon in [bpo-47061](https://bugs.python.org/issue?@action=redirect&bpo=47061) and Victor Stinner in [gh-68966](https://github.com/python/cpython/issues/68966).)
- The `asynchat`, `asyncore` and `smtpd` modules have been
deprecated since at least Python 3.6. Their documentation and deprecation
warnings have now been updated to note they will be removed in Python 3.12.
(Contributed by Hugo van Kemenade in [bpo-47022](https://bugs.python.org/issue?@action=redirect&bpo=47022).)
- The `lib2to3` package and `2to3` tool
are now deprecated and may not be able to parse Python 3.10 or newer.
See [**PEP 617**](https://peps.python.org/pep-0617/), introducing the new PEG parser, for details.
(Contributed by Victor Stinner in [bpo-40360](https://bugs.python.org/issue?@action=redirect&bpo=40360).)
- Undocumented modules `sre_compile`, `sre_constants` and `sre_parse` are now deprecated.
(Contributed by Serhiy Storchaka in [bpo-47152](https://bugs.python.org/issue?@action=redirect&bpo=47152).)

### Standard Library[¶](#standard-library)

- The following have been deprecated in [`configparser`](../library/configparser.html#module-configparser) since Python 3.2.
Their deprecation warnings have now been updated to note they will be removed
in Python 3.12:
  - the `configparser.SafeConfigParser` class
  - the `configparser.ParsingError.filename` property
  - the `configparser.RawConfigParser.readfp()` method
(Contributed by Hugo van Kemenade in [bpo-45173](https://bugs.python.org/issue?@action=redirect&bpo=45173).)
- `configparser.LegacyInterpolation` has been deprecated in the docstring
since Python 3.2, and is not listed in the [`configparser`](../library/configparser.html#module-configparser) documentation.
It now emits a [`DeprecationWarning`](../builtins/exceptions.html#DeprecationWarning) and will be removed
in Python 3.13. Use [`configparser.BasicInterpolation`](../library/configparser.html#configparser.BasicInterpolation) or [`configparser.ExtendedInterpolation`](../library/configparser.html#configparser.ExtendedInterpolation) instead.
(Contributed by Hugo van Kemenade in [bpo-46607](https://bugs.python.org/issue?@action=redirect&bpo=46607).)
- The older set of [`importlib.resources`](../library/importlib.resources.html#module-importlib.resources) functions were deprecated
in favor of the replacements added in Python 3.9
and will be removed in a future Python version,
due to not supporting resources located within package subdirectories:
  - `importlib.resources.contents()`
  - `importlib.resources.is_resource()`
  - `importlib.resources.open_binary()`
  - `importlib.resources.open_text()`
  - `importlib.resources.read_binary()`
  - `importlib.resources.read_text()`
  - `importlib.resources.path()`
- The [`locale.getdefaultlocale()`](../library/locale.html#locale.getdefaultlocale) function is deprecated and will be
removed in Python 3.15. Use [`locale.setlocale()`](../library/locale.html#locale.setlocale), [`locale.getpreferredencoding(False)`](../library/locale.html#locale.getpreferredencoding) and [`locale.getlocale()`](../library/locale.html#locale.getlocale) functions instead.
(Contributed by Victor Stinner in [gh-90817](https://github.com/python/cpython/issues/90817).)
- The `locale.resetlocale()` function is deprecated and will be
removed in Python 3.13. Use `locale.setlocale(locale.LC_ALL, "")` instead.
(Contributed by Victor Stinner in [gh-90817](https://github.com/python/cpython/issues/90817).)
- Stricter rules will now be applied for numerical group references
and group names in [regular expressions](../library/re.html#re-syntax).
Only sequences of ASCII digits will now be accepted as a numerical reference,
and the group name in [`bytes`](../builtins/stdtypes.html#bytes) patterns and replacement strings
can only contain ASCII letters, digits and underscores.
For now, a deprecation warning is raised for syntax violating these rules.
(Contributed by Serhiy Storchaka in [gh-91760](https://github.com/python/cpython/issues/91760).)
- In the [`re`](../library/re.html#module-re) module, the `re.template()` function
and the corresponding `re.TEMPLATE` and `re.T` flags
are deprecated, as they were undocumented and lacked an obvious purpose.
They will be removed in Python 3.13.
(Contributed by Serhiy Storchaka and Miro Hrončok in [gh-92728](https://github.com/python/cpython/issues/92728).)
- `turtle.settiltangle()` has been deprecated since Python 3.1;
it now emits a deprecation warning and will be removed in Python 3.13. Use [`turtle.tiltangle()`](../library/turtle.html#turtle.tiltangle) instead (it was earlier incorrectly marked
as deprecated, and its docstring is now corrected).
(Contributed by Hugo van Kemenade in [bpo-45837](https://bugs.python.org/issue?@action=redirect&bpo=45837).)
- [`typing.Text`](../library/typing.html#typing.Text), which exists solely to provide compatibility support
between Python 2 and Python 3 code, is now deprecated. Its removal is
currently unplanned, but users are encouraged to use [`str`](../builtins/stdtypes.html#str) instead
wherever possible.
(Contributed by Alex Waygood in [gh-92332](https://github.com/python/cpython/issues/92332).)
- The keyword argument syntax for constructing [`typing.TypedDict`](../library/typing.html#typing.TypedDict) types
is now deprecated. Support will be removed in Python 3.13. (Contributed by
Jingchen Ye in [gh-90224](https://github.com/python/cpython/issues/90224).)
- `webbrowser.MacOSX` is deprecated and will be removed in Python 3.13.
It is untested, undocumented, and not used by [`webbrowser`](../library/webbrowser.html#module-webbrowser) itself.
(Contributed by Donghee Na in [bpo-42255](https://bugs.python.org/issue?@action=redirect&bpo=42255).)
- The behavior of returning a value from a [`TestCase`](../library/unittest.html#unittest.TestCase) and [`IsolatedAsyncioTestCase`](../library/unittest.html#unittest.IsolatedAsyncioTestCase) test methods (other than the
default `None` value) is now deprecated.
- Deprecated the following not-formally-documented [`unittest`](../library/unittest.html#module-unittest) functions,
scheduled for removal in Python 3.13:
  - `unittest.findTestCases()`
  - `unittest.makeSuite()`
  - `unittest.getTestCaseNames()`
Use [`TestLoader`](../library/unittest.html#unittest.TestLoader) methods instead:
  - `unittest.TestLoader.loadTestsFromModule()`
  - `unittest.TestLoader.loadTestsFromTestCase()`
  - `unittest.TestLoader.getTestCaseNames()`
(Contributed by Erlend E. Aasland in [bpo-5846](https://bugs.python.org/issue?@action=redirect&bpo=5846).)
- `unittest.TestProgram.usageExit()` is marked deprecated, to be removed
in 3.13.
(Contributed by Carlos Damázio in [gh-67048](https://github.com/python/cpython/issues/67048).)

## Pending Removal in Python 3.12[¶](#pending-removal-in-python-3-12)

The following Python APIs have been deprecated in earlier Python releases, and will be removed in Python 3.12.

C APIs pending removal are
[listed separately](#whatsnew311-c-api-pending-removal).

- The `asynchat` module
- The `asyncore` module
- The [entire distutils package](3.10.html#distutils-deprecated)
- The `imp` module
- The [`typing.io`](../library/typing.html#typing.IO) namespace
- The [`typing.re`](../library/typing.html#typing.Pattern) namespace
- `cgi.log()`
- `importlib.find_loader()`
- `importlib.abc.Loader.module_repr()`
- `importlib.abc.MetaPathFinder.find_module()`
- `importlib.abc.PathEntryFinder.find_loader()`
- `importlib.abc.PathEntryFinder.find_module()`
- `importlib.machinery.BuiltinImporter.find_module()`
- `importlib.machinery.BuiltinImporter.module_repr()`
- `importlib.machinery.FileFinder.find_loader()`
- `importlib.machinery.FileFinder.find_module()`
- `importlib.machinery.FrozenImporter.find_module()`
- `importlib.machinery.FrozenImporter.module_repr()`
- `importlib.machinery.PathFinder.find_module()`
- `importlib.machinery.WindowsRegistryFinder.find_module()`
- `importlib.util.module_for_loader()`
- `importlib.util.set_loader()`
- `importlib.util.set_package()`
- `pkgutil.ImpImporter`
- `pkgutil.ImpLoader`
- `pathlib.Path.link_to()`
- `sqlite3.enable_shared_cache()`
- `sqlite3.OptimizedUnicode()`
- `PYTHONTHREADDEBUG` environment variable
- The following deprecated aliases in [`unittest`](../library/unittest.html#module-unittest):
Deprecated alias Method Name Deprecated in `failUnless`
`assertTrue()`
3.1 `failIf`
`assertFalse()`
3.1 `failUnlessEqual`
`assertEqual()`
3.1 `failIfEqual`
`assertNotEqual()`
3.1 `failUnlessAlmostEqual`
`assertAlmostEqual()`
3.1 `failIfAlmostEqual`
`assertNotAlmostEqual()`
3.1 `failUnlessRaises`
`assertRaises()`
3.1 `assert_`
`assertTrue()`
3.2 `assertEquals`
`assertEqual()`
3.2 `assertNotEquals`
`assertNotEqual()`
3.2 `assertAlmostEquals`
`assertAlmostEqual()`
3.2 `assertNotAlmostEquals`
`assertNotAlmostEqual()`
3.2 `assertRegexpMatches`
`assertRegex()`
3.2 `assertRaisesRegexp`
`assertRaisesRegex()`
3.2 `assertNotRegexpMatches`
`assertNotRegex()`
3.5

## Removed[¶](#removed)

This section lists Python APIs that have been removed in Python 3.11.

Removed C APIs are [listed separately](#whatsnew311-c-api-removed).

- Removed the `@asyncio.coroutine()` [decorator](../glossary.html#term-decorator) enabling legacy generator-based coroutines to be compatible with [`async`](../reference/compound_stmts.html#async) / [`await`](../reference/expressions.html#await) code.
The function has been deprecated since Python 3.8 and the removal was
initially scheduled for Python 3.10. Use [`async def`](../reference/compound_stmts.html#async-def) instead.
(Contributed by Illia Volochii in [bpo-43216](https://bugs.python.org/issue?@action=redirect&bpo=43216).)
- Removed `asyncio.coroutines.CoroWrapper` used for wrapping legacy
generator-based coroutine objects in the debug mode.
(Contributed by Illia Volochii in [bpo-43216](https://bugs.python.org/issue?@action=redirect&bpo=43216).)
- Due to significant security concerns, the *reuse\_address* parameter of [`asyncio.loop.create_datagram_endpoint()`](../library/asyncio-eventloop.html#asyncio.loop.create_datagram_endpoint), disabled in Python 3.9, is
now entirely removed. This is because of the behavior of the socket option `SO_REUSEADDR` in UDP.
(Contributed by Hugo van Kemenade in [bpo-45129](https://bugs.python.org/issue?@action=redirect&bpo=45129).)
- Removed the `binhex` module, deprecated in Python 3.9.
Also removed the related, similarly-deprecated [`binascii`](../library/binascii.html#module-binascii) functions:
  - `binascii.a2b_hqx()`
  - `binascii.b2a_hqx()`
  - `binascii.rlecode_hqx()`
  - `binascii.rldecode_hqx()`
The [`binascii.crc_hqx()`](../library/binascii.html#binascii.crc_hqx) function remains available.
(Contributed by Victor Stinner in [bpo-45085](https://bugs.python.org/issue?@action=redirect&bpo=45085).)
- Removed the `distutils` `bdist_msi` command deprecated in Python 3.9.
Use `bdist_wheel` (wheel packages) instead.
(Contributed by Hugo van Kemenade in [bpo-45124](https://bugs.python.org/issue?@action=redirect&bpo=45124).)
- Removed the [`__getitem__()`](../reference/datamodel.html#object.__getitem__) methods of [`xml.dom.pulldom.DOMEventStream`](../library/xml.dom.pulldom.html#xml.dom.pulldom.DOMEventStream), [`wsgiref.util.FileWrapper`](../library/wsgiref.html#wsgiref.util.FileWrapper) and [`fileinput.FileInput`](../library/fileinput.html#fileinput.FileInput), deprecated since Python 3.9.
(Contributed by Hugo van Kemenade in [bpo-45132](https://bugs.python.org/issue?@action=redirect&bpo=45132).)
- Removed the deprecated [`gettext`](../library/gettext.html#module-gettext) functions `lgettext()`, `ldgettext()`, `lngettext()` and `ldngettext()`.
Also removed the `bind_textdomain_codeset()` function,
the `NullTranslations.output_charset()` and `NullTranslations.set_output_charset()` methods,
and the *codeset* parameter of `translation()` and `install()`,
since they are only used for the `l*gettext()` functions.
(Contributed by Donghee Na and Serhiy Storchaka in [bpo-44235](https://bugs.python.org/issue?@action=redirect&bpo=44235).)
- Removed from the [`inspect`](../library/inspect.html#module-inspect) module:
  - The `getargspec()` function, deprecated since Python 3.0;
use [`inspect.signature()`](../library/inspect.html#inspect.signature) or [`inspect.getfullargspec()`](../library/inspect.html#inspect.getfullargspec) instead.
  - The `formatargspec()` function, deprecated since Python 3.5;
use the [`inspect.signature()`](../library/inspect.html#inspect.signature) function
or the [`inspect.Signature`](../library/inspect.html#inspect.Signature) object directly.
  - The undocumented `Signature.from_builtin()` and `Signature.from_function()` methods, deprecated since Python 3.5;
use the [`Signature.from_callable()`](../library/inspect.html#inspect.Signature.from_callable) method instead.
(Contributed by Hugo van Kemenade in [bpo-45320](https://bugs.python.org/issue?@action=redirect&bpo=45320).)
- Removed the [`__class_getitem__()`](../reference/datamodel.html#object.__class_getitem__) method
from [`pathlib.PurePath`](../library/pathlib.html#pathlib.PurePath),
because it was not used and added by mistake in previous versions.
(Contributed by Nikita Sobolev in [bpo-46483](https://bugs.python.org/issue?@action=redirect&bpo=46483).)
- Removed the `MailmanProxy` class in the `smtpd` module,
as it is unusable without the external `mailman` package.
(Contributed by Donghee Na in [bpo-35800](https://bugs.python.org/issue?@action=redirect&bpo=35800).)
- Removed the deprecated `split()` method of `_tkinter.TkappType`.
(Contributed by Erlend E. Aasland in [bpo-38371](https://bugs.python.org/issue?@action=redirect&bpo=38371).)
- Removed namespace package support from [`unittest`](../library/unittest.html#module-unittest) discovery.
It was introduced in Python 3.4 but has been broken since Python 3.7.
(Contributed by Inada Naoki in [bpo-23882](https://bugs.python.org/issue?@action=redirect&bpo=23882).)
- Removed the undocumented private `float.__set_format__()` method,
previously known as `float.__setformat__()` in Python 3.7.
Its docstring said: “You probably don’t want to use this function.
It exists mainly to be used in Python’s test suite.”
(Contributed by Victor Stinner in [bpo-46852](https://bugs.python.org/issue?@action=redirect&bpo=46852).)
- The `--experimental-isolated-subinterpreters` configure flag
(and corresponding `EXPERIMENTAL_ISOLATED_SUBINTERPRETERS` macro)
have been removed.
- [Pynche](https://pypi.org/project/Pynche/) — The Pythonically Natural Color and Hue Editor — has been moved out
of `Tools/scripts` and is [being developed independently](https://gitlab.com/warsaw/pynche/-/tree/main) from the Python source tree.

## Porting to Python 3.11[¶](#porting-to-python-3-11)

This section lists previously described changes and other bugfixes in the Python API that may require changes to your Python code.

Porting notes for the C API are
[listed separately](#whatsnew311-c-api-porting).

- [`open()`](../builtins/functions.html#open), [`io.open()`](../library/io.html#io.open), [`codecs.open()`](../library/codecs.html#codecs.open) and [`fileinput.FileInput`](../library/fileinput.html#fileinput.FileInput) no longer accept `'U'` (“universal newline”)
in the file mode. In Python 3, “universal newline” mode is used by default
whenever a file is opened in text mode,
and the `'U'` flag has been deprecated since Python 3.3.
The [newline parameter](../builtins/functions.html#open-newline-parameter) to these functions controls how universal newlines work.
(Contributed by Victor Stinner in [bpo-37330](https://bugs.python.org/issue?@action=redirect&bpo=37330).)
- [`ast.AST`](../library/ast.html#ast.AST) node positions are now validated when provided to [`compile()`](../builtins/functions.html#compile) and other related functions. If invalid positions are detected,
a [`ValueError`](../builtins/exceptions.html#ValueError) will be raised. (Contributed by Pablo Galindo in [gh-93351](https://github.com/python/cpython/issues/93351))
- Prohibited passing non-[`concurrent.futures.ThreadPoolExecutor`](../library/concurrent.futures.html#concurrent.futures.ThreadPoolExecutor) executors to [`asyncio.loop.set_default_executor()`](../library/asyncio-eventloop.html#asyncio.loop.set_default_executor) following a deprecation in Python 3.8.
(Contributed by Illia Volochii in [bpo-43234](https://bugs.python.org/issue?@action=redirect&bpo=43234).)
- [`calendar`](../library/calendar.html#module-calendar): The [`calendar.LocaleTextCalendar`](../library/calendar.html#calendar.LocaleTextCalendar) and [`calendar.LocaleHTMLCalendar`](../library/calendar.html#calendar.LocaleHTMLCalendar) classes now use [`locale.getlocale()`](../library/locale.html#locale.getlocale), instead of using [`locale.getdefaultlocale()`](../library/locale.html#locale.getdefaultlocale),
if no locale is specified.
(Contributed by Victor Stinner in [bpo-46659](https://bugs.python.org/issue?@action=redirect&bpo=46659).)
- The [`pdb`](../library/pdb.html#module-pdb) module now reads the `.pdbrc` configuration file with
the `'UTF-8'` encoding.
(Contributed by Srinivas Reddy Thatiparthy (శ్రీనివాస్  రెడ్డి తాటిపర్తి) in [bpo-41137](https://bugs.python.org/issue?@action=redirect&bpo=41137).)
- The *population* parameter of [`random.sample()`](../library/random.html#random.sample) must be a sequence,
and automatic conversion of [`set`](../builtins/stdtypes.html#set)s to [`list`](../builtins/stdtypes.html#list)s
is no longer supported. Also, if the sample size
is larger than the population size, a [`ValueError`](../builtins/exceptions.html#ValueError) is raised.
(Contributed by Raymond Hettinger in [bpo-40465](https://bugs.python.org/issue?@action=redirect&bpo=40465).)
- The *random* optional parameter of [`random.shuffle()`](../library/random.html#random.shuffle) was removed.
It was previously an arbitrary random function to use for the shuffle;
now, [`random.random()`](../library/random.html#random.random) (its previous default) will always be used.
- In `re`[Regular expression syntax](../library/re.html#re-syntax), global inline flags (e.g. `(?i)`)
can now only be used at the start of regular expressions.
Using them elsewhere has been deprecated since Python 3.6.
(Contributed by Serhiy Storchaka in [bpo-47066](https://bugs.python.org/issue?@action=redirect&bpo=47066).)
- In the [`re`](../library/re.html#module-re) module, several long-standing bugs where fixed that,
in rare cases, could cause capture groups to get the wrong result.
Therefore, this could change the captured output in these cases.
(Contributed by Ma Lin in [bpo-35859](https://bugs.python.org/issue?@action=redirect&bpo=35859).)

## Build Changes[¶](#build-changes)

- CPython now has **PEP 11**[**Tier 3 support**](https://peps.python.org/pep-0011/#tier-3) for
cross compiling to the [WebAssembly](https://webassembly.org/) platforms [Emscripten](https://emscripten.org/) (`wasm32-unknown-emscripten`, i.e. Python in the browser)
and [WebAssembly System Interface (WASI)](https://wasi.dev/) (`wasm32-unknown-wasi`).
The effort is inspired by previous work like [Pyodide](https://pyodide.org/).
These platforms provide a limited subset of POSIX APIs; Python standard
libraries features and modules related to networking, processes, threading,
signals, mmap, and users/groups are not available or don’t work.
(Emscripten contributed by Christian Heimes and Ethan Smith in [gh-84461](https://github.com/python/cpython/issues/84461) and WASI contributed by Christian Heimes in [gh-90473](https://github.com/python/cpython/issues/90473);
platforms promoted in [gh-95085](https://github.com/python/cpython/issues/95085))
- Building CPython now requires:
- The `Py_NO_NAN` macro has been removed.
Since CPython now requires IEEE 754 floats, NaN values are always available.
(Contributed by Victor Stinner in [bpo-46656](https://bugs.python.org/issue?@action=redirect&bpo=46656).)
- The [`tkinter`](../library/tkinter.html#module-tkinter) package now requires [Tcl/Tk](https://www.tcl.tk) version 8.5.12 or newer.
(Contributed by Serhiy Storchaka in [bpo-46996](https://bugs.python.org/issue?@action=redirect&bpo=46996).)
- Build dependencies, compiler flags, and linker flags for most stdlib
extension modules are now detected by **configure**. libffi, libnsl,
libsqlite3, zlib, bzip2, liblzma, libcrypt, Tcl/Tk, and uuid flags
are detected by [pkg-config](https://www.freedesktop.org/wiki/Software/pkg-config/) (when available). [`tkinter`](../library/tkinter.html#module-tkinter) now requires a pkg-config command
to detect development settings for [Tcl/Tk](https://www.tcl.tk) headers and libraries.
(Contributed by Christian Heimes and Erlend Egeberg Aasland in [bpo-45847](https://bugs.python.org/issue?@action=redirect&bpo=45847), [bpo-45747](https://bugs.python.org/issue?@action=redirect&bpo=45747), and [bpo-45763](https://bugs.python.org/issue?@action=redirect&bpo=45763).)
- libpython is no longer linked against libcrypt.
(Contributed by Mike Gilbert in [bpo-45433](https://bugs.python.org/issue?@action=redirect&bpo=45433).)
- CPython can now be built with the
[ThinLTO](https://clang.llvm.org/docs/ThinLTO.html) option
via passing `thin` to [`--with-lto`](../using/configure.html#cmdoption-with-lto), i.e. `--with-lto=thin`.
(Contributed by Donghee Na and Brett Holman in [bpo-44340](https://bugs.python.org/issue?@action=redirect&bpo=44340).)
- Freelists for object structs can now be disabled. A new **configure** option `--without-freelists` can be used to disable all freelists
except empty tuple singleton.
(Contributed by Christian Heimes in [bpo-45522](https://bugs.python.org/issue?@action=redirect&bpo=45522).)
- `Modules/Setup` and `Modules/makesetup` have been improved and tied up.
Extension modules can now be built through `makesetup`. All except some
test modules can be linked statically into a main binary or library.
(Contributed by Brett Cannon and Christian Heimes in [bpo-45548](https://bugs.python.org/issue?@action=redirect&bpo=45548), [bpo-45570](https://bugs.python.org/issue?@action=redirect&bpo=45570), [bpo-45571](https://bugs.python.org/issue?@action=redirect&bpo=45571), and [bpo-43974](https://bugs.python.org/issue?@action=redirect&bpo=43974).)
Note Use the environment variables `TCLTK_CFLAGS` and `TCLTK_LIBS` to manually specify the location of Tcl/Tk headers
and libraries. The **configure** options `--with-tcltk-includes` and `--with-tcltk-libs` have been removed.
On RHEL 7 and CentOS 7 the development packages do not provide `tcl.pc` and `tk.pc`; use `TCLTK_LIBS="-ltk8.5 -ltkstub8.5 -ltcl8.5"`.
The directory `Misc/rhel7` contains `.pc` files and instructions
on how to build Python with RHEL 7’s and CentOS 7’s Tcl/Tk and OpenSSL.
- CPython will now use 30-bit digits by default for the Python [`int`](../builtins/functions.html#int) implementation. Previously, the default was to use 30-bit digits on platforms
with `SIZEOF_VOID_P >= 8`, and 15-bit digits otherwise. It’s still possible
to explicitly request use of 15-bit digits via either the [`--enable-big-digits`](../using/configure.html#cmdoption-enable-big-digits) option to the configure script
or (for Windows) the `PYLONG_BITS_IN_DIGIT` variable in `PC/pyconfig.h`,
but this option may be removed at some point in the future.
(Contributed by Mark Dickinson in [bpo-45569](https://bugs.python.org/issue?@action=redirect&bpo=45569).)

## C API Changes[¶](#c-api-changes)

### New Features[¶](#whatsnew311-c-api-new-features)

- Add a new [`PyType_GetName()`](../c-api/type.html#c.PyType_GetName) function to get type’s short name.
(Contributed by Hai Shi in [bpo-42035](https://bugs.python.org/issue?@action=redirect&bpo=42035).)
- Add a new [`PyType_GetQualName()`](../c-api/type.html#c.PyType_GetQualName) function to get type’s qualified name.
(Contributed by Hai Shi in [bpo-42035](https://bugs.python.org/issue?@action=redirect&bpo=42035).)
- Add new [`PyThreadState_EnterTracing()`](../c-api/threads.html#c.PyThreadState_EnterTracing) and [`PyThreadState_LeaveTracing()`](../c-api/threads.html#c.PyThreadState_LeaveTracing) functions to the limited C API to
suspend and resume tracing and profiling.
(Contributed by Victor Stinner in [bpo-43760](https://bugs.python.org/issue?@action=redirect&bpo=43760).)
- Added the [`Py_Version`](../c-api/apiabiversion.html#c.Py_Version) constant which bears the same value as [`PY_VERSION_HEX`](../c-api/apiabiversion.html#c.PY_VERSION_HEX).
(Contributed by  Gabriele N. Tornetta in [bpo-43931](https://bugs.python.org/issue?@action=redirect&bpo=43931).)
- [`Py_buffer`](../c-api/buffer.html#c.Py_buffer) and APIs are now part of the limited API and the stable
ABI:
(Contributed by Christian Heimes in [bpo-45459](https://bugs.python.org/issue?@action=redirect&bpo=45459).)
- Added the [`PyType_GetModuleByDef()`](../c-api/type.html#c.PyType_GetModuleByDef) function, used to get the module
in which a method was defined, in cases where this information is not
available directly (via [`PyCMethod`](../c-api/structures.html#c.PyCMethod)).
(Contributed by Petr Viktorin in [bpo-46613](https://bugs.python.org/issue?@action=redirect&bpo=46613).)
- Add new functions to pack and unpack C double (serialize and deserialize):
[`PyFloat_Pack2()`](../c-api/float.html#c.PyFloat_Pack2), [`PyFloat_Pack4()`](../c-api/float.html#c.PyFloat_Pack4), [`PyFloat_Pack8()`](../c-api/float.html#c.PyFloat_Pack8), [`PyFloat_Unpack2()`](../c-api/float.html#c.PyFloat_Unpack2), [`PyFloat_Unpack4()`](../c-api/float.html#c.PyFloat_Unpack4) and [`PyFloat_Unpack8()`](../c-api/float.html#c.PyFloat_Unpack8).
(Contributed by Victor Stinner in [bpo-46906](https://bugs.python.org/issue?@action=redirect&bpo=46906).)
- Add new functions to get frame object attributes:
[`PyFrame_GetBuiltins()`](../c-api/frame.html#c.PyFrame_GetBuiltins), [`PyFrame_GetGenerator()`](../c-api/frame.html#c.PyFrame_GetGenerator), [`PyFrame_GetGlobals()`](../c-api/frame.html#c.PyFrame_GetGlobals), [`PyFrame_GetLasti()`](../c-api/frame.html#c.PyFrame_GetLasti).
- Added two new functions to get and set the active exception instance:
[`PyErr_GetHandledException()`](../c-api/exceptions.html#c.PyErr_GetHandledException) and [`PyErr_SetHandledException()`](../c-api/exceptions.html#c.PyErr_SetHandledException).
These are alternatives to [`PyErr_SetExcInfo()`](../c-api/exceptions.html#c.PyErr_SetExcInfo) and [`PyErr_GetExcInfo()`](../c-api/exceptions.html#c.PyErr_GetExcInfo) which work with the legacy 3-tuple
representation of exceptions.
(Contributed by Irit Katriel in [bpo-46343](https://bugs.python.org/issue?@action=redirect&bpo=46343).)
- Added the [`PyConfig.safe_path`](../c-api/init_config.html#c.PyConfig.safe_path) member.
(Contributed by Victor Stinner in [gh-57684](https://github.com/python/cpython/issues/57684).)

### Porting to Python 3.11[¶](#whatsnew311-c-api-porting)

- Some macros have been converted to static inline functions to avoid
[macro pitfalls](https://gcc.gnu.org/onlinedocs/cpp/Macro-Pitfalls.html).
The change should be mostly transparent to users,
as the replacement functions will cast their arguments to the expected types
to avoid compiler warnings due to static type checks.
However, when the limited C API is set to >=3.11,
these casts are not done,
and callers will need to cast arguments to their expected types.
See [**PEP 670**](https://peps.python.org/pep-0670/) for more details.
(Contributed by Victor Stinner and Erlend E. Aasland in [gh-89653](https://github.com/python/cpython/issues/89653).)
- [`PyErr_SetExcInfo()`](../c-api/exceptions.html#c.PyErr_SetExcInfo) no longer uses the `type` and `traceback` arguments, the interpreter now derives those values from the exception
instance (the `value` argument). The function still steals references
of all three arguments.
(Contributed by Irit Katriel in [bpo-45711](https://bugs.python.org/issue?@action=redirect&bpo=45711).)
- [`PyErr_GetExcInfo()`](../c-api/exceptions.html#c.PyErr_GetExcInfo) now derives the `type` and `traceback` fields of the result from the exception instance (the `value` field).
(Contributed by Irit Katriel in [bpo-45711](https://bugs.python.org/issue?@action=redirect&bpo=45711).)
- [`_frozen`](../c-api/import.html#c._frozen) has a new `is_package` field to indicate whether
or not the frozen module is a package.  Previously, a negative value
in the `size` field was the indicator.  Now only non-negative values
be used for `size`.
(Contributed by Kumar Aditya in [bpo-46608](https://bugs.python.org/issue?@action=redirect&bpo=46608).)
- [`_PyFrameEvalFunction()`](../c-api/subinterpreters.html#c._PyFrameEvalFunction) now takes `_PyInterpreterFrame*` as its second parameter, instead of `PyFrameObject*`.
See [**PEP 523**](https://peps.python.org/pep-0523/) for more details of how to use this function pointer type.
- `PyCode_New()` and `PyCode_NewWithPosOnlyArgs()` now take
an additional `exception_table` argument.
Using these functions should be avoided, if at all possible.
To get a custom code object: create a code object using the compiler,
then get a modified version with the `replace` method.
- [`PyCodeObject`](../c-api/code.html#c.PyCodeObject) no longer has the `co_code`, `co_varnames`, `co_cellvars` and `co_freevars` fields.  Instead, use [`PyCode_GetCode()`](../c-api/code.html#c.PyCode_GetCode), [`PyCode_GetVarnames()`](../c-api/code.html#c.PyCode_GetVarnames), [`PyCode_GetCellvars()`](../c-api/code.html#c.PyCode_GetCellvars) and [`PyCode_GetFreevars()`](../c-api/code.html#c.PyCode_GetFreevars) respectively
to access them via the C API.
(Contributed by Brandt Bucher in [bpo-46841](https://bugs.python.org/issue?@action=redirect&bpo=46841) and Ken Jin in [gh-92154](https://github.com/python/cpython/issues/92154) and [gh-94936](https://github.com/python/cpython/issues/94936).)
- The old trashcan macros (`Py_TRASHCAN_SAFE_BEGIN`/`Py_TRASHCAN_SAFE_END`)
are now deprecated. They should be replaced by the new macros `Py_TRASHCAN_BEGIN` and `Py_TRASHCAN_END`.
A tp\_dealloc function that has the old macros, such as: static void mytype\_dealloc(mytype \*p) { PyObject\_GC\_UnTrack(p); Py\_TRASHCAN\_SAFE\_BEGIN(p); ... Py\_TRASHCAN\_SAFE\_END(p) } should migrate to the new macros as follows: static void mytype\_dealloc(mytype \*p) { PyObject\_GC\_UnTrack(p); Py\_TRASHCAN\_BEGIN(p, mytype\_dealloc) ... Py\_TRASHCAN\_END } Note that `Py_TRASHCAN_BEGIN` has a second argument which
should be the deallocation function it is in.
To support older Python versions in the same codebase, you
can define the following macros and use them throughout
the code (credit: these were copied from the `mypy` codebase):
#if PY\_VERSION\_HEX >= 0x03080000 # define CPy\_TRASHCAN\_BEGIN(op, dealloc) Py\_TRASHCAN\_BEGIN(op, dealloc) # define CPy\_TRASHCAN\_END(op) Py\_TRASHCAN\_END #else # define CPy\_TRASHCAN\_BEGIN(op, dealloc) Py\_TRASHCAN\_SAFE\_BEGIN(op) # define CPy\_TRASHCAN\_END(op) Py\_TRASHCAN\_SAFE\_END(op) #endif
- The [`PyType_Ready()`](../c-api/type.html#c.PyType_Ready) function now raises an error if a type is defined
with the [`Py_TPFLAGS_HAVE_GC`](../c-api/typeobj.html#c.Py_TPFLAGS_HAVE_GC) flag set but has no traverse function
([`PyTypeObject.tp_traverse`](../c-api/typeobj.html#c.PyTypeObject.tp_traverse)).
(Contributed by Victor Stinner in [bpo-44263](https://bugs.python.org/issue?@action=redirect&bpo=44263).)
- Heap types with the [`Py_TPFLAGS_IMMUTABLETYPE`](../c-api/typeobj.html#c.Py_TPFLAGS_IMMUTABLETYPE) flag can now inherit
the [**PEP 590**](https://peps.python.org/pep-0590/) vectorcall protocol.  Previously, this was only possible for [static types](../c-api/typeobj.html#static-types).
(Contributed by Erlend E. Aasland in [bpo-43908](https://bugs.python.org/issue?@action=redirect&bpo=43908))
- Since [`Py_TYPE()`](../c-api/structures.html#c.Py_TYPE) is changed to a inline static function, `Py_TYPE(obj) = new_type` must be replaced with `Py_SET_TYPE(obj, new_type)`: see the [`Py_SET_TYPE()`](../c-api/structures.html#c.Py_SET_TYPE) function
(available since Python 3.9). For backward compatibility, this macro can be
used:
#if PY\_VERSION\_HEX \< 0x030900A4 && !defined(Py\_SET\_TYPE) static inline void \_Py\_SET\_TYPE(PyObject \*ob, PyTypeObject \*type) { ob->ob\_type = type; } #define Py\_SET\_TYPE(ob, type) \_Py\_SET\_TYPE((PyObject\*)(ob), type) #endif (Contributed by Victor Stinner in [bpo-39573](https://bugs.python.org/issue?@action=redirect&bpo=39573).)
- Since [`Py_SIZE()`](../c-api/structures.html#c.Py_SIZE) is changed to a inline static function, `Py_SIZE(obj) = new_size` must be replaced with `Py_SET_SIZE(obj, new_size)`: see the [`Py_SET_SIZE()`](../c-api/structures.html#c.Py_SET_SIZE) function
(available since Python 3.9). For backward compatibility, this macro can be
used:
#if PY\_VERSION\_HEX \< 0x030900A4 && !defined(Py\_SET\_SIZE) static inline void \_Py\_SET\_SIZE(PyVarObject \*ob, Py\_ssize\_t size) { ob->ob\_size = size; } #define Py\_SET\_SIZE(ob, size) \_Py\_SET\_SIZE((PyVarObject\*)(ob), size) #endif (Contributed by Victor Stinner in [bpo-39573](https://bugs.python.org/issue?@action=redirect&bpo=39573).)
- `<Python.h>` no longer includes the header files `<stdlib.h>`, `<stdio.h>`, `<errno.h>` and `<string.h>` when the `Py_LIMITED_API` macro is set to `0x030b0000` (Python 3.11) or higher. C extensions should
explicitly include the header files after `#include <Python.h>`.
(Contributed by Victor Stinner in [bpo-45434](https://bugs.python.org/issue?@action=redirect&bpo=45434).)
- The non-limited API files `cellobject.h`, `classobject.h`, `code.h`, `context.h`, `funcobject.h`, `genobject.h` and `longintrepr.h` have been moved to
the `Include/cpython` directory. Moreover, the `eval.h` header file was
removed. These files must not be included directly, as they are already
included in `Python.h`: [Include Files](../c-api/intro.html#api-includes). If they have
been included directly, consider including `Python.h` instead.
(Contributed by Victor Stinner in [bpo-35134](https://bugs.python.org/issue?@action=redirect&bpo=35134).)
- The `PyUnicode_CHECK_INTERNED()` macro has been excluded from the
limited C API. It was never usable there, because it used internal structures
which are not available in the limited C API.
(Contributed by Victor Stinner in [bpo-46007](https://bugs.python.org/issue?@action=redirect&bpo=46007).)
- The following frame functions and type are now directly available with
`#include <Python.h>`, it’s no longer needed to add `#include <frameobject.h>`:
  - `PyFrame_Check()`
  - `PyFrame_GetBack()`
  - `PyFrame_GetBuiltins()`
  - `PyFrame_GetGenerator()`
  - `PyFrame_GetGlobals()`
  - `PyFrame_GetLasti()`
  - `PyFrame_GetLocals()`
  - `PyFrame_Type`
(Contributed by Victor Stinner in [gh-93937](https://github.com/python/cpython/issues/93937).)

- The [`PyFrameObject`](../c-api/frame.html#c.PyFrameObject) structure members have been removed from the
public C API.
While the documentation notes that the [`PyFrameObject`](../c-api/frame.html#c.PyFrameObject) fields are
subject to change at any time, they have been stable for a long time and were
used in several popular extensions.
In Python 3.11, the frame struct was reorganized to allow performance optimizations. Some fields were removed entirely, as they were details of the old implementation. [`PyFrameObject`](../c-api/frame.html#c.PyFrameObject) fields:
  - `f_back`: use [`PyFrame_GetBack()`](../c-api/frame.html#c.PyFrame_GetBack).
  - `f_blockstack`: removed.
  - `f_builtins`: use [`PyFrame_GetBuiltins()`](../c-api/frame.html#c.PyFrame_GetBuiltins).
  - `f_code`: use [`PyFrame_GetCode()`](../c-api/frame.html#c.PyFrame_GetCode).
  - `f_gen`: use [`PyFrame_GetGenerator()`](../c-api/frame.html#c.PyFrame_GetGenerator).
  - `f_globals`: use [`PyFrame_GetGlobals()`](../c-api/frame.html#c.PyFrame_GetGlobals).
  - `f_iblock`: removed.
  - `f_lasti`: use [`PyFrame_GetLasti()`](../c-api/frame.html#c.PyFrame_GetLasti).
Code using `f_lasti` with `PyCode_Addr2Line()` should use [`PyFrame_GetLineNumber()`](../c-api/frame.html#c.PyFrame_GetLineNumber) instead; it may be faster.
  - `f_lineno`: use `PyFrame_GetLineNumber()`
  - `f_locals`: use [`PyFrame_GetLocals()`](../c-api/frame.html#c.PyFrame_GetLocals).
  - `f_stackdepth`: removed.
  - `f_state`: no public API (renamed to `f_frame.f_state`).
  - `f_trace`: no public API.
  - `f_trace_lines`: use `PyObject_GetAttrString((PyObject*)frame, "f_trace_lines")`.
  - `f_trace_opcodes`: use `PyObject_GetAttrString((PyObject*)frame, "f_trace_opcodes")`.
  - `f_localsplus`: no public API (renamed to `f_frame.localsplus`).
  - `f_valuestack`: removed.
The Python frame object is now created lazily. A side effect is that the
[`f_back`](../reference/datamodel.html#frame.f_back) member must not be accessed directly,
since its value is now also
computed lazily. The [`PyFrame_GetBack()`](../c-api/frame.html#c.PyFrame_GetBack) function must be called
instead.
Debuggers that accessed the [`f_locals`](../reference/datamodel.html#frame.f_locals) directly *must* call [`PyFrame_GetLocals()`](../c-api/frame.html#c.PyFrame_GetLocals) instead. They no longer need to call `PyFrame_FastToLocalsWithError()` or `PyFrame_LocalsToFast()`,
in fact they should not call those functions. The necessary updating of the
frame is now managed by the virtual machine.
Code defining `PyFrame_GetCode()` on Python 3.8 and older:
#if PY\_VERSION\_HEX \< 0x030900B1 static inline PyCodeObject\* PyFrame\_GetCode(PyFrameObject \*frame) { Py\_INCREF(frame->f\_code); return frame->f\_code; } #endif Code defining `PyFrame_GetBack()` on Python 3.8 and older:
#if PY\_VERSION\_HEX \< 0x030900B1 static inline PyFrameObject\* PyFrame\_GetBack(PyFrameObject \*frame) { Py\_XINCREF(frame->f\_back); return frame->f\_back; } #endif Or use the [pythoncapi\_compat project](https://github.com/python/pythoncapi-compat) to get these two
functions on older Python versions.
- Changes of the [`PyThreadState`](../c-api/threads.html#c.PyThreadState) structure members:
  - `frame`: removed, use [`PyThreadState_GetFrame()`](../c-api/threads.html#c.PyThreadState_GetFrame) (function added
to Python 3.9 by [bpo-40429](https://bugs.python.org/issue?@action=redirect&bpo=40429)).
Warning: the function returns a [strong reference](../glossary.html#term-strong-reference), need to call [`Py_XDECREF()`](../c-api/refcounting.html#c.Py_XDECREF).
  - `tracing`: changed, use [`PyThreadState_EnterTracing()`](../c-api/threads.html#c.PyThreadState_EnterTracing) and [`PyThreadState_LeaveTracing()`](../c-api/threads.html#c.PyThreadState_LeaveTracing) (functions added to Python 3.11 by [bpo-43760](https://bugs.python.org/issue?@action=redirect&bpo=43760)).
  - `recursion_depth`: removed,
use `(tstate->recursion_limit - tstate->recursion_remaining)` instead.
  - `stackcheck_counter`: removed.
Code defining `PyThreadState_GetFrame()` on Python 3.8 and older:
#if PY\_VERSION\_HEX \< 0x030900B1 static inline PyFrameObject\* PyThreadState\_GetFrame(PyThreadState \*tstate) { Py\_XINCREF(tstate->frame); return tstate->frame; } #endif Code defining `PyThreadState_EnterTracing()` and `PyThreadState_LeaveTracing()` on Python 3.10 and older:
#if PY\_VERSION\_HEX \< 0x030B00A2 static inline void PyThreadState\_EnterTracing(PyThreadState \*tstate) { tstate->tracing++; #if PY\_VERSION\_HEX >= 0x030A00A1 tstate->cframe->use\_tracing = 0; #else tstate->use\_tracing = 0; #endif } static inline void PyThreadState\_LeaveTracing(PyThreadState \*tstate) { int use\_tracing = (tstate->c\_tracefunc != NULL || tstate->c\_profilefunc != NULL); tstate->tracing--; #if PY\_VERSION\_HEX >= 0x030A00A1 tstate->cframe->use\_tracing = use\_tracing; #else tstate->use\_tracing = use\_tracing; #endif } #endif Or use [the pythoncapi-compat project](https://github.com/python/pythoncapi-compat) to get these functions
on old Python functions.
- Distributors are encouraged to build Python with the optimized Blake2
library [libb2](https://www.blake2.net/).
- The [`PyConfig.module_search_paths_set`](../c-api/init_config.html#c.PyConfig.module_search_paths_set) field must now be set to 1 for
initialization to use [`PyConfig.module_search_paths`](../c-api/init_config.html#c.PyConfig.module_search_paths) to initialize [`sys.path`](../library/sys.html#sys.path). Otherwise, initialization will recalculate the path and replace
any values added to `module_search_paths`.
- [`PyConfig_Read()`](../c-api/init_config.html#c.PyConfig_Read) no longer calculates the initial search path, and will not
fill any values into [`PyConfig.module_search_paths`](../c-api/init_config.html#c.PyConfig.module_search_paths). To calculate default
paths and then modify them, finish initialization and use [`PySys_GetObject()`](../c-api/sys.html#c.PySys_GetObject) to retrieve [`sys.path`](../library/sys.html#sys.path) as a Python list object and modify it directly.

### Deprecated[¶](#whatsnew311-c-api-deprecated)

- Deprecate the following functions to configure the Python initialization: 
  - `PySys_AddWarnOptionUnicode()`
  - `PySys_AddWarnOption()`
  - `PySys_AddXOption()`
  - `PySys_HasWarnOptions()`
  - `PySys_SetArgvEx()`
  - `PySys_SetArgv()`
  - `PySys_SetPath()`
  - `Py_SetPath()`
  - `Py_SetProgramName()`
  - `Py_SetPythonHome()`
  - `Py_SetStandardStreamEncoding()`
  - `_Py_SetProgramFullPath()`
Use the new [`PyConfig`](../c-api/init_config.html#c.PyConfig) API of the [Python Initialization Configuration](../c-api/init_config.html#init-config) instead ([**PEP 587**](https://peps.python.org/pep-0587/)).
(Contributed by Victor Stinner in [gh-88279](https://github.com/python/cpython/issues/88279).)
- Deprecate the `ob_shash` member of the [`PyBytesObject`](../c-api/bytes.html#c.PyBytesObject). Use [`PyObject_Hash()`](../c-api/object.html#c.PyObject_Hash) instead.
(Contributed by Inada Naoki in [bpo-46864](https://bugs.python.org/issue?@action=redirect&bpo=46864).)

### Pending Removal in Python 3.12[¶](#whatsnew311-c-api-pending-removal)

The following C APIs have been deprecated in earlier Python releases, and will be removed in Python 3.12.

- `PyUnicode_AS_DATA()`
- `PyUnicode_AS_UNICODE()`
- `PyUnicode_AsUnicodeAndSize()`
- `PyUnicode_AsUnicode()`
- `PyUnicode_FromUnicode()`
- `PyUnicode_GET_DATA_SIZE()`
- `PyUnicode_GET_SIZE()`
- `PyUnicode_GetSize()`
- `PyUnicode_IS_COMPACT()`
- `PyUnicode_IS_READY()`
- `PyUnicode_READY()`
- `PyUnicode_WSTR_LENGTH()`
- `_PyUnicode_AsUnicode()`
- `PyUnicode_WCHAR_KIND`
- `PyUnicodeObject`
- `PyUnicode_InternImmortal()`

### Removed[¶](#whatsnew311-c-api-removed)

- `PyFrame_BlockSetup()` and `PyFrame_BlockPop()` have been
removed.
(Contributed by Mark Shannon in [bpo-40222](https://bugs.python.org/issue?@action=redirect&bpo=40222).)
- Remove the following math macros using the `errno` variable:
  - `Py_ADJUST_ERANGE1()`
  - `Py_ADJUST_ERANGE2()`
  - `Py_OVERFLOWED()`
  - `Py_SET_ERANGE_IF_OVERFLOW()`
  - `Py_SET_ERRNO_ON_MATH_ERROR()`
(Contributed by Victor Stinner in [bpo-45412](https://bugs.python.org/issue?@action=redirect&bpo=45412).)
- Remove `Py_UNICODE_COPY()` and `Py_UNICODE_FILL()` macros, deprecated
since Python 3.3. Use `PyUnicode_CopyCharacters()` or `memcpy()` (`wchar_t*` string), and `PyUnicode_Fill()` functions instead.
(Contributed by Victor Stinner in [bpo-41123](https://bugs.python.org/issue?@action=redirect&bpo=41123).)
- Remove the `pystrhex.h` header file. It only contains private functions.
C extensions should only include the main `<Python.h>` header file.
(Contributed by Victor Stinner in [bpo-45434](https://bugs.python.org/issue?@action=redirect&bpo=45434).)
- Remove the `Py_FORCE_DOUBLE()` macro. It was used by the `Py_IS_INFINITY()` macro.
(Contributed by Victor Stinner in [bpo-45440](https://bugs.python.org/issue?@action=redirect&bpo=45440).)
- The following items are no longer available when [`Py_LIMITED_API`](../c-api/stable.html#c.Py_LIMITED_API) is defined:
  - `PyMarshal_WriteLongToFile()`
  - `PyMarshal_WriteObjectToFile()`
  - `PyMarshal_ReadObjectFromString()`
  - `PyMarshal_WriteObjectToString()`
  - the `Py_MARSHAL_VERSION` macro
These are not part of the [limited API](../c-api/stable.html#limited-api-list).
(Contributed by Victor Stinner in [bpo-45474](https://bugs.python.org/issue?@action=redirect&bpo=45474).)
- Exclude `PyWeakref_GET_OBJECT()` from the limited C API. It never
worked since the `PyWeakReference` structure is opaque in the
limited C API.
(Contributed by Victor Stinner in [bpo-35134](https://bugs.python.org/issue?@action=redirect&bpo=35134).)
- Remove the `PyHeapType_GET_MEMBERS()` macro. It was exposed in the
public C API by mistake, it must only be used by Python internally.
Use the `PyTypeObject.tp_members` member instead.
(Contributed by Victor Stinner in [bpo-40170](https://bugs.python.org/issue?@action=redirect&bpo=40170).)
- Remove the `HAVE_PY_SET_53BIT_PRECISION` macro (moved to the internal C
API).
(Contributed by Victor Stinner in [bpo-45412](https://bugs.python.org/issue?@action=redirect&bpo=45412).)

- Remove the [`Py_UNICODE`](../c-api/unicode.html#c.Py_UNICODE) encoder APIs,
as they have been deprecated since Python 3.3,
are little used
and are inefficient relative to the recommended alternatives.
The removed functions are: 
  - `PyUnicode_Encode()`
  - `PyUnicode_EncodeASCII()`
  - `PyUnicode_EncodeLatin1()`
  - `PyUnicode_EncodeUTF7()`
  - `PyUnicode_EncodeUTF8()`
  - `PyUnicode_EncodeUTF16()`
  - `PyUnicode_EncodeUTF32()`
  - `PyUnicode_EncodeUnicodeEscape()`
  - `PyUnicode_EncodeRawUnicodeEscape()`
  - `PyUnicode_EncodeCharmap()`
  - `PyUnicode_TranslateCharmap()`
  - `PyUnicode_EncodeDecimal()`
  - `PyUnicode_TransformDecimalToASCII()`
See [**PEP 624**](https://peps.python.org/pep-0624/) for details and [**migration guidance**](https://peps.python.org/pep-0624/#alternative-apis).
(Contributed by Inada Naoki in [bpo-44029](https://bugs.python.org/issue?@action=redirect&bpo=44029).)

## Notable changes in 3.11.4[¶](#notable-changes-in-3-11-4)

### tarfile[¶](#tarfile)

- The extraction methods in [`tarfile`](../library/tarfile.html#module-tarfile), and [`shutil.unpack_archive()`](../library/shutil.html#shutil.unpack_archive),
have a new a *filter* argument that allows limiting tar features than may be
surprising or dangerous, such as creating files outside the destination
directory.
See [Extraction filters](../library/tarfile.html#tarfile-extraction-filter) for details.
In Python 3.12, use without the *filter* argument will show a [`DeprecationWarning`](../builtins/exceptions.html#DeprecationWarning).
In Python 3.14, the default will switch to `'data'`.
(Contributed by Petr Viktorin in [**PEP 706**](https://peps.python.org/pep-0706/).)

## Notable changes in 3.11.5[¶](#notable-changes-in-3-11-5)

### OpenSSL[¶](#openssl)

- Windows builds and macOS installers from python.org now use OpenSSL 3.0.
