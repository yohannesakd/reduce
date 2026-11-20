# Best Dead Code Detection Tools by Language (2026)

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Raghav Chamadiya
- Date: 2026-05-20
- Original location: https://repowise.dev/blog/comparisons/best-dead-code-detection-tools
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
**The best dead code detection tool depends on your language: Knip for JavaScript and TypeScript, Vulture for Python, the official `deadcode` command for Go, PHPStan with dead-code-detector for PHP, the compiler's own lint for Rust, PMD rules plus an IDE inspection for Java, and the SDK analyzers for C#.** For a repository that mixes languages, `repowise dead-code` reads one dependency graph and reports unreachable files, unused exports and unused packages in a single pass. Almost every codebase needs one of these: when we analysed 190 popular open-source repositories, 96% carried dead code in production files.

| Language | Start with | Also worth knowing | Unused dependencies | 
|---|---|---|---|
| Python | [Vulture](https://pypi.org/project/vulture/) | [deadcode](https://github.com/albertas/deadcode) (has `--fix`) | [deptry](https://github.com/fpgmaas/deptry) | 
| JavaScript / TypeScript | [Knip](https://knip.dev/) | [ts-prune](https://github.com/nadeesha/ts-prune) (exports only) | Knip does it | 
| Go | [`deadcode`](https://go.dev/blog/deadcode) | staticcheck U1000 | `go mod tidy` | 
| Java | IntelliJ "Unused declaration" | [PMD](https://pmd.github.io/pmd/pmd_rules_java_bestpractices.html) Unused\* rules | [`mvn dependency:analyze`](https://maven.apache.org/plugins/maven-dependency-plugin/analyze-mojo.html); Gradle [Dependency Analysis Plugin](https://github.com/autonomousapps/dependency-analysis-gradle-plugin) | 
| C# | Roslyn IDE0051 / IDE0052 | Rider and ReSharper inspections | None built in | 
| PHP | [dead-code-detector](https://github.com/shipmonk-rnd/dead-code-detector) for [PHPStan](https://phpstan.org/) | PHPStan's own unused private member rules | [composer-dependency-analyser](https://github.com/shipmonk-rnd/composer-dependency-analyser) | 
| Rust | the compiler's `dead_code` lint |  | [cargo-machete](https://github.com/bnjbvr/cargo-machete), [cargo-udeps](https://github.com/est31/cargo-udeps) | 
| Mixed-language repo | repowise `dead-code` | the per-language tools above | Unused packages in monorepos | 

Scroll the table sideways to see every column.

*Pricing: every tool in this post except repowise's hosted dashboard is free and open source. Versions and facts below are from each project's own page or package registry, read on 10 November 2026.*

We build repowise, so weigh our entry accordingly. The measurements we publish about it, with their methods, are on the [benchmarks page](/benchmarks).

## How we evaluated

We compared tools on four things a team feels in practice:

- **What it finds.** Unreachable files, unused exports and members, unused dependencies, or some mix.
- **How it decides.** Entry-point awareness, framework plugins, and whether it reports confidence.
- **How it acts.** CI fit, auto-fix, and how it handles known false positives.
- **How far it reaches.** One language or the whole repository.

## What counts as dead code

**Dead code is valid code that no entry point reaches.** It comes in three kinds that need different checks, which is why one tool rarely covers all of them.

- **Unreachable files:** nothing imports the file and it is not an entry point. Only a project graph can show this; tools that read one file at a time cannot.
- **Unused exports:** functions, classes, types or constants that no other file imports. This is the easiest place to start.
- **Zombie packages and dependencies:** entries in `package.json`, `requirements.txt` or `Cargo.toml` that the code no longer uses. They cost build time, add security surface and make upgrades noisier.

## How much dead code do popular repos carry?

**96% of popular open-source repositories carry dead code in production files: 182 of the 190 we analysed (1,000+ GitHub stars each, November 2026) had at least one finding, and 139 of them (73%) had at least one high-confidence finding.** The [method](#how-we-measured) is below; every number counts production source files only, so tests, generated code and vendored copies are left out.

Whole dead files are the most common surprise. 170 of 190 repos (89%) contain at least one production file flagged as unreachable, meaning nothing imports it and it is not an entry point. In the median repo that is 3.2% of production files, and in 44 repos (23%) it is 10% or more.

| Finding (190 repos) | Repos with at least one | Pooled across all repos | 
|---|---|---|
| Any dead code finding | 182 (96%) | 59,726 findings, 3.5 million lines | 
| Unused export | 91% | 39,863 | 
| Unreachable production file | 170 (89%) | 19,697 | 
| Zombie workspace package | 72 (38%) | 166 | 

Scroll the table sideways to see every column.

The median repo has 16.2 findings per 100 production files, 1.8 of them high confidence (0.7 and above). Across all findings, 58% are high confidence, which is the share a team can start deleting with the least review.

The mix depends on the language. Go repos have the lowest share of unreachable files, and most Go findings are unused exported symbols; JavaScript repos have the highest share of files nothing imports.

| Primary language | Repos | Unreachable share of production files (median) | Findings per 100 production files (median) | 
|---|---|---|---|
| TypeScript | 52 | 1.7% | 10.1 | 
| Python | 51 | 3.9% | 15.7 | 
| Go | 22 | 0.6% | 21.4 | 
| Rust | 15 | 1.8% | 5.0 | 
| JavaScript | 13 | 14.6% | 26.6 | 
| All repos | 190 | 3.2% | 16.2 | 

Scroll the table sideways to see every column.

JavaScript is the smallest group here (13 repos), so read its row as indicative. What the table says for every stack: a cleanup that starts with whole unreachable files removes the most lines per decision, since one finding is a whole file.

### How we measured

We analysed 195 public, non-fork GitHub repositories with 1,000+ stars that are indexed on [repowise.dev](/explore): 253,688 production source files and 79.7 million lines of code, each measured at its latest completed index (May to November 2026, data pulled 10 November 2026). Files are classified by repowise's code-origin rules, and only production source files in code languages count. Dead-code figures cover the 190 repos with dead-code data and count repowise findings at confidence 0.4 and above, as candidates for review, not verified deletions. Medians are taken across repos, so each repository counts once. The full report, with every table by language and repository size, is [State of open-source code health 2026](/research/code-health-2026).

## Python: Vulture and deadcode

**Vulture is the standard Python dead code finder.** It walks the AST for unused classes, functions, methods, variables, imports, attributes and unreachable code. Version 2.16, released in March 2026, is still the latest on PyPI as of 10 November 2026 and needs Python 3.9 or newer ([PyPI](https://pypi.org/project/vulture/)).

Every finding carries a confidence: 100% for unused arguments and unreachable code, 90% for imports, 60% for functions, classes, attributes and variables that dynamic code might reach. `--min-confidence 80` hides the noisy tier, and `--make-whitelist` records today's false positives so the next run shows only new ones.

```
pip install vulture
vulture src/ --min-confidence 80
```
**Pick Vulture if** you want a lightweight Python check for CI with a built-in way to manage false positives. Decorators and framework magic (Django views, FastAPI routes, Celery tasks, pytest fixtures) are its usual false-positive sources, so whitelist them. Settings strings are another: running Vulture 2.16 on Scrapy, 56 of the 80 classes it flagged were middlewares and handlers that Scrapy's default settings load by dotted path.

**deadcode** ([GitHub](https://github.com/albertas/deadcode)) is a newer option for whole-codebase checks that Ruff and flake8 do not do. Version 2.6.0 needs Python 3.10 or newer. It reports unused variables, functions, classes, imports, empty files and unreachable blocks under `DCxxx` codes, and `deadcode . --fix` removes them; `--fix --dry` shows the diff first. Use `--dry` every time, because auto-fix is only as good as its view of your entry points.

Add [deptry](https://github.com/fpgmaas/deptry) for packages: it reports missing (DEP001), unused (DEP002) and misplaced dev (DEP004) dependencies and works with pip, Poetry, PDM, uv and PEP 621.

## JavaScript and TypeScript: Knip

**Knip is the strongest open source choice for JavaScript and TypeScript.** It finds and fixes unused files, exports and dependencies in one pass, and its 200+ plugins teach it the entry points of Next.js, Vite, Vitest, Jest, ESLint, Astro, Cypress, Storybook and more ([knip.dev](https://knip.dev/)). It handles monorepos and workspaces, it can auto-fix when you are ready ([auto-fix](https://knip.dev/features/auto-fix)), and npm served version 6.44 as of 10 November 2026.

```
npx knip                 # unused files, exports, dependencies
npx knip --production    # only code reachable from production entry points
```
The trade-off of any smart analyzer applies: configure entry files correctly. Miss one and Knip reports used code as unused; make entries too broad and you hide dead code ([configuring project files](https://knip.dev/guides/configuring-project-files)).

**Pick Knip if** your project is JavaScript or TypeScript and you want files, exports and dependencies from one tool.

**ts-prune** prints unused exports from your `tsconfig` and nothing else. Its [repository](https://github.com/nadeesha/ts-prune) is active again (commits through October 2026), but npm still serves 0.10.3 from December 2021, which bundles TypeScript 4.5. unimported, the file-level counterpart, is archived and its README points to Knip. We ran all three on one monorepo in [Knip vs ts-prune vs unimported](/blog/comparisons/knip-vs-ts-prune-vs-unimported?src=blog_best-dead-code-detection-tools). ts-prune still makes sense when you only want an export list; for a new setup Knip covers the same job and more.

## Go: deadcode and staticcheck

**The official `deadcode` command reports functions that no execution from `main` can reach.** The Go team introduced it in December 2023; it uses Rapid Type Analysis over direct and interface calls ([go.dev](https://go.dev/blog/deadcode)).

```
go install golang.org/x/tools/cmd/deadcode@latest
deadcode ./...
deadcode -test ./...    # count tests as entry points, for libraries
```
It needs a `main` entry point, so libraries run it with `-test`, and it cannot see functions reached only from assembly or `go:linkname`. [staticcheck](https://staticcheck.io/changes/2023.1/) U1000 reports unused functions, types, fields and constants per package, treats exported names as used, and runs inside golangci-lint as the `unused` linter. That last point matters: in our data, unused exported symbols are most of the dead code in Go repos, and U1000 does not report them.

**Pick both if** you maintain Go services: U1000 in CI for the per-package view, `deadcode` occasionally for the whole-program view. `go mod tidy` handles unused modules.

## Java and C#: IDE inspections and analyzers

**Java has no single standard CLI for whole-program dead code, so teams combine an IDE inspection with CI rules.**

- IntelliJ's "Unused declaration" inspection works best run project-wide and with your framework's entry-point annotations configured (Spring, JAX-RS, test frameworks) ([JetBrains](https://intellij-support.jetbrains.com/hc/en-us/community/posts/13160500986386-Analyze-Dead-Code-in-the-Project)).
- PMD's `UnusedPrivateMethod`, `UnusedPrivateField`, `UnusedLocalVariable`, `UnusedFormalParameter` and `UnusedAssignment` rules run on every build. They cover private and local code only, which is why they are safe to enforce ([PMD](https://pmd.github.io/pmd/pmd_rules_java_bestpractices.html)).

For dependencies, the Maven Dependency Plugin's `mvn dependency:analyze` reports "Unused declared dependencies" and "Used undeclared dependencies" from bytecode, and Gradle builds get the same report from the Dependency Analysis Gradle Plugin. Both can miss a library that is only loaded by reflection or at runtime, so read the list before you prune `pom.xml`.

Reflection, dependency injection and serialization are the usual false positives, so declare your annotations before trusting a list.

**For C#, start with the analyzers in the SDK.** IDE0051 flags unused private members and IDE0052 flags private members written but never read ([Microsoft Learn](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/style-rules/ide0051)). Set both to `warning` in `.editorconfig`. Unused public and internal code needs a solution-wide pass from Rider or ReSharper.

## PHP: PHPStan and dead-code-detector

**For PHP, the most complete dead code detector is shipmonk's dead-code-detector, a PHPStan extension that finds unused methods, constants, properties and enum cases across the whole project.** It ships built-in support for Symfony, Laravel, Doctrine, PHPUnit, Twig and more, so framework entry points such as controllers, event subscribers and Doctrine callbacks count as used ([GitHub](https://github.com/shipmonk-rnd/dead-code-detector)). Version 1.4.2 shipped in September 2026.

```
composer require --dev shipmonk/dead-code-detector   # with phpstan/extension-installer, or include its rules.neon
vendor/bin/phpstan analyse
vendor/bin/phpstan analyse --error-format removeDeadCode   # delete what it found
```
It can also remove what it finds: the `removeDeadCode` error format deletes dead methods and constants, and when you exclude test-only usages it leaves those tests intact and lists them in the output. For packages, the same team's composer-dependency-analyser reports unused, shadow and misplaced Composer dependencies.

**Pick it if** you already run PHPStan. It reads PHPStan's type information, so its view of method calls is far better than a text search.

## Rust: the compiler and cargo-machete

**Rust reports unused private items at compile time.** The [`dead_code` lint](https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html) is on by default. For dependencies, cargo-machete scans source for crates in `Cargo.toml` that nothing references, quickly but imprecisely by its own description. cargo-udeps gives the precise answer from compiler output and needs a nightly toolchain. A common setup is cargo-machete in CI and cargo-udeps now and then.

## Unused dependencies

**An unused dependency is dead code in your manifest.** It still gets installed, scanned and upgraded.

| Ecosystem | Tool | What it reports | 
|---|---|---|
| JS / TS | [Knip](https://knip.dev/typescript/unused-dependencies) | Unused and unlisted dependencies, plus files and exports | 
| JS / TS | [depcheck](https://github.com/depcheck/depcheck) | Unused dependencies; the repository is archived and its README points to Knip | 
| Python | deptry | Missing, unused and misplaced dev dependencies | 
| PHP | composer-dependency-analyser | Unused, shadow and misplaced Composer dependencies | 
| Rust | cargo-machete, cargo-udeps | Unused crates | 
| Go | `go mod tidy` | Removes modules nothing imports | 
| Java | `mvn dependency:analyze`, Dependency Analysis Gradle Plugin | Unused declared and used undeclared dependencies | 

Scroll the table sideways to see every column.

If depcheck still runs in your CI, moving to Knip is a cheap win. At the workspace level, 38% of the repos we analysed had at least one declared workspace package that nothing else in the repository uses.

## Mixed-language repos: repowise dead-code

**`repowise dead-code` reports unreachable files, unused exports and unused packages across every language in the repository from one dependency graph.** Every tool above stops at its language boundary, which is fine for a single-language repo and a gap in a TypeScript frontend, Python service and shared packages. repowise parses 28 languages into one graph, so a single report covers them all. It is the engine behind every number in the data section above.

Each finding is scored from `0.0` to `1.0` and tiered high (0.7 and above), medium or low, with the evidence behind the score. Unreachable files are scored from git activity: a file untouched for a year starts at 1.00, one still being committed to starts at 0.40. A finding is marked deletion-ready only for unused exports with strong evidence: confidence 0.7 or higher, no runtime-load path and no docs or example code. Unreachable files always get a human look first. The analysis is graph traversal plus git history: no LLM key and no network calls ([dead code docs](https://docs.repowise.dev/intelligence/dead-code)).

```
uv tool install repowise
repowise init
repowise dead-code --safe-only
```
```
 Kind              File / Symbol            Confidence  Ready?  Lines  Reason
 unused_export     formatLegacyDate               100%    ✓       14  Public symbol 'formatLegacyDate' has no importers
 unreachable_file  src/legacy/parser.ts           100%    ✗      212  File has no importers (in_degree=0)
```
The same findings appear in the dashboard's Dead code view with a triage status per finding. In a workspace, a finding is checked against cross-repo data, so a file another repository depends on is lowered in confidence. repowise is open source under AGPL-3.0 and self-hostable.

**Pick repowise if** your repository spans languages, you want git-aware confidence, or you want findings shared with agents and reviewers. Tiers and views are on the [dead code feature page](/features/dead-code). Keep Knip or Vulture in CI for framework-specific depth. To see the output on a real codebase, open the [FastAPI architecture map](/repo/fastapi/fastapi/architecture) or browse [live examples](/explore).

## Finding dead code with Claude Code and other AI agents

**An AI coding agent finds dead code reliably when it reads a dependency graph instead of grepping for each symbol.** A grep for a function name misses re-exports and dynamic imports, and checking thousands of exports one by one burns the agent's context. Give the agent the list, then let it do the deletion and run the tests.

repowise serves its findings to agents through the `get_dead_code` tool, one of its ten MCP tools, so Claude Code, Cursor, Codex or any MCP client gets the same tiered list as the CLI. `get_dead_code(tier="high", safe_only=True)` returns only deletion-ready findings. In Claude Code, the repowise plugin adds a slash command for the same report:

```
/plugin install repowise@repowise
/repowise:dead-code safe
```
A good loop is one finding kind per pull request: ask the agent to delete the high-confidence unreachable files, run the full test suite, and open the PR. Then do unused exports in the next one.

## Side-by-side comparison

| Tool | Language | Unused exports / members | Unused files | Unused deps | Auto-fix | 
|---|---|---|---|---|---|
| Vulture | Python | Yes, with confidence | No | No | No | 
| deadcode | Python | Yes | Empty files | No | Yes ( `--fix`) | 
| deptry | Python | No | No | Yes | No | 
| Knip | JS / TS | Yes | Yes | Yes | Yes | 
| ts-prune | TS | Exports only | No | No | No | 
| `deadcode` | Go | Unreachable functions | No | No | No | 
| staticcheck U1000 | Go | Unexported only | No | No | No | 
| PMD Unused\* rules | Java | Private and local only | No | No | No | 
| IntelliJ inspection | Java, Kotlin | Yes | Partly | No | Quick-fix | 
| Roslyn IDE0051/52 | C# | Private members | No | No | Code fix | 
| dead-code-detector | PHP | Methods, constants, properties, enum cases | No | Separate tool | Yes ( `removeDeadCode`) | 
| repowise `dead-code` | 28 languages | Yes, tiered | Yes | Unused packages | Through an agent | 

Scroll the table sideways to see every column.

## How to choose

- **Single-language repo:** run that language's tool in CI and add a whitelist or baseline for known exceptions.
- **Polyglot repo or monorepo:** run repowise for the cross-language view, and keep the per-language tools for their framework knowledge.
- **Library you publish:** exports have no importer inside the repo. Tag them (`@public` in Knip) and check dependents before deleting.
- **Cleanup sprint:** start with one signal type, delete high-confidence leaf code first, and remove in small patches. Whole unreachable files are the fastest win, since one decision removes a whole file. The [find dead code guide](/blog/guides/find-dead-code-repository) walks through it on a real repo.

## FAQ

- What is dead code analysis?
- Dead code analysis finds code that can never run or is never used: unreachable functions, unused exports, files nothing imports and dependencies nothing references. Static tools build a graph from entry points; runtime tools such as production coverage find code that is reachable but never called.
- How common is dead code in open-source projects?
- Very common. In our analysis of 190 public GitHub repositories with 1,000+ stars (November 2026), 96% had at least one dead code finding in production code and 89% had at least one production file flagged as unreachable. In the median repo, 3.2% of production files were unreachable.
- What is the best dead code detection tool for Python?
- Vulture is the standard starting point, with confidence values and a whitelist file for false positives. deadcode can also delete what it finds with `--fix`, and deptry covers unused packages.
- What is the best dead code detection tool for JavaScript and TypeScript?
- Knip. It finds unused files, exports and dependencies in one pass, supports monorepos and has 200+ plugins for frameworks and tools.
- How do I find dead code in PHP?
- Install shipmonk's dead-code-detector as a PHPStan extension and run `phpstan analyse`. It finds unused methods, constants, properties and enum cases, understands Symfony, Laravel and Doctrine entry points, and can delete what it finds with the `removeDeadCode` error format.
- What is the difference between dead code and unused code?
- Unused code is a declaration nothing references, such as an import, a variable or an export. Dead code also covers branches that can never run and whole files no entry point reaches.
- What tools detect unused dependencies and dead code in Java projects?
- PMD's Unused\* rules and IntelliJ's "Unused declaration" inspection cover the code, and `mvn dependency:analyze` (or the Dependency Analysis Gradle Plugin) covers dependencies. `repowise dead-code` adds unreachable files and unused exports across [Java](/languages/java), [Kotlin](/languages/kotlin) and every other language in the same repository.
- Is ts-prune deprecated?
- Not officially. The repository is not archived and has seen commits through October 2026, but npm has had no release since 0.10.3 in December 2021. For new projects Knip covers files and dependencies as well as exports.
- How do I find unused dependencies?
- Use Knip for JavaScript and TypeScript, deptry for Python, composer-dependency-analyser for PHP, cargo-machete or cargo-udeps for Rust, `go mod tidy` for Go and `mvn dependency:analyze` for Maven projects. Avoid depcheck in new setups: its repository is archived.
- Can Claude Code find dead code?
- Yes, and it does it best with a dependency graph to read. Connect repowise over MCP and the agent calls `get_dead_code` for a tiered list of unreachable files and unused exports, then deletes the high-confidence ones and runs your tests. Without a graph, the agent has to grep for each symbol, which misses re-exports and dynamic imports.
- How do I find dead code across several languages?
- Run a graph-based tool that parses all of them. `repowise dead-code` reports unreachable files, unused exports and unused packages from one dependency graph and tiers each finding by confidence.
- Is it safe to delete what a dead code tool reports?
- Delete the highest-confidence findings after a full test run and review the rest. Static tools cannot see code loaded by string, reflection or an outside caller, so check files near dynamic loaders and exports of published libraries by hand. For deciding what to clean up first, see [how to prioritize technical debt by impact per effort](/blog/guides/prioritize-technical-debt).
