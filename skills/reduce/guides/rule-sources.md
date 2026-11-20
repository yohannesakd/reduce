# Rule sources

The [refactoring check](../checks/every-feature/refactoring.md) and the [language checks](../checks/README.md#languages) adapt the sources below. Each source keeps its copyright and license.

## Changes

- The refactoring check copies the PufferLib guide 1:1, without its C and CUDA sections. Its tables and the precedence are additions of reduce. The language rules paraphrase their sources and condense them into rules. Rules marked [RD] are rules of reduce.
- Each rule has a reduce rung or the tag `lead`. Exceptions, version limits, the assert form, and the precedence are additions of reduce.
- The language checks quote no long passages. Each rule cites the source pages that support it.

## Sources and licenses

| Checks | Source | License |
|---|---|---|
| refactoring | [PufferLib `SKILL_ISSUES.md`](https://github.com/PufferAI/PufferLib/blob/5.0/SKILL_ISSUES.md), PufferAI | MIT, notice below |
| JavaScript and TypeScript | [typescript-eslint](https://typescript-eslint.io) | MIT |
| JavaScript and TypeScript | [ESLint](https://eslint.org) | MIT |
| JavaScript and TypeScript | [TypeScript documentation](https://www.typescriptlang.org/docs/) | CC BY 4.0 |
| JavaScript and TypeScript | [Google TypeScript Style Guide](https://google.github.io/styleguide/tsguide.html) | CC BY 3.0 |
| React | [react.dev](https://react.dev) | CC BY 4.0 |
| Vue | [Vue.js documentation](https://vuejs.org) | CC BY 4.0 |
| Effect | [Effect documentation](https://effect.website) | Paraphrased only; the site states MIT, and its repository has no license file |
| Effect | [Effect repository](https://github.com/Effect-TS/effect) | MIT |
| Go | [Effective Go](https://go.dev/doc/effective_go), [Code Review Comments](https://go.dev/wiki/CodeReviewComments), [release notes](https://go.dev/doc/devel/release) | CC BY 4.0 |
| Go | [Google Go Style Guide](https://google.github.io/styleguide/go/) | CC BY 3.0 |
| Go | [Uber Go Style Guide](https://github.com/uber-go/guide) | Apache-2.0 |
| Go | [Go Proverbs](https://go-proverbs.github.io/) | MIT |
| Go | [`modernize` analyzers](https://pkg.go.dev/golang.org/x/tools/go/analysis/passes/modernize) | BSD-3-Clause |
| Python | [PEP 8 and PEP 20](https://peps.python.org) | Public domain |
| Python | [Python documentation](https://docs.python.org/3/) and [typing documentation](https://typing.python.org) | PSF License 2.0 |
| Python | [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html) | CC BY 3.0 |
| Python | [Ruff](https://docs.astral.sh/ruff/rules/), [mypy](https://mypy.readthedocs.io), [pyright](https://github.com/microsoft/pyright) | MIT |

## PufferLib

```text
MIT License

Copyright (c) 2022 PufferAI

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
