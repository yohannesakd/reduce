# Rule sources

The [refactoring check](../checks/every-feature/refactoring.md) and the [language checks](../checks/README.md#languages) adapt the sources below. Each source keeps its copyright and license.

## Changes

- The refactoring check copies the PufferLib guide 1:1, without its C and CUDA sections. Its tables and the precedence are additions of reduce. The language rules paraphrase their sources and condense them into rules. Rules marked [RD] are rules of reduce.
- Each rule has a reduce rung or the tag `lead`. Exceptions, version limits, the assert form, and the precedence are additions of reduce.
- The language checks quote no long passages. The [sources folder](../sources/README.md) holds the full text of each source page, copied 1:1. A per-language index names the pages that support each rule.

## Sources and licenses

| Checks | Copied source text | License |
|---|---|---|
| refactoring | [PufferLib `SKILL_ISSUES.md`](../sources/github/pufferai-pufferlib-skill-issues-md.md), PufferAI | MIT, notice below |
| JavaScript and TypeScript | [TypeScript sources](../sources/languages/typescript.md): typescript-eslint and ESLint rule pages, TSConfig and release-note pages, the Google TypeScript Style Guide | MIT; CC BY 4.0; CC BY 3.0 |
| React | [React sources](../sources/languages/react.md): react.dev pages | CC BY 4.0 |
| Vue | [Vue sources](../sources/languages/vue.md): Vue.js documentation pages | CC BY 4.0 |
| Effect | [Effect sources](../sources/languages/effect.md): effect.website pages and `effect-smol` repository files | MIT |
| Go | [Go sources](../sources/languages/go.md): Effective Go, Code Review Comments, release notes, the Google and Uber style guides, Go Proverbs, `modernize` | CC BY 4.0; CC BY 3.0; Apache-2.0; MIT; BSD-3-Clause |
| Python | [Python sources](../sources/languages/python.md): PEP 8, PEP 20, Python documentation, the Google Python Style Guide, Ruff, mypy, and pyright pages | Public domain; PSF License 2.0; CC BY 3.0; MIT |

Each copied file states its own author, license, and original location.

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
