# Knip vs ts-prune vs unimported: Tested on One Repo

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: Raghav Chamadiya
- Date: 2026-10-29
- Original location: https://repowise.dev/blog/comparisons/knip-vs-ts-prune-vs-unimported
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
**Knip vs ts-prune is no longer a close call: use Knip.** It finds unused exports, unused files and unused dependencies in one pass, it is the only one of the three tools here still publishing releases, and on the Excalidraw monorepo it needed no config: 34 seconds on the first run, about 3 seconds after that. ts-prune still works for a plain export list on a simple project, and unimported is archived.

If you maintain an existing ts-prune or unimported setup, the numbers below explain why the tools disagree. We ran all three, plus `repowise dead-code`, on one commit of Excalidraw and checked each false positive named below with `git grep`. We build repowise; versions, release dates and timings are from October 29, 2026. For languages other than [JavaScript](/languages/javascript) and [TypeScript](/languages/typescript), see [the best dead code detection tools by language](/blog/comparisons/best-dead-code-detection-tools?src=blog_knip-vs-ts-prune-vs-unimported).

We build repowise, so weigh our entry accordingly. The measurements we publish about it, with their methods, are on the [benchmarks page](/benchmarks).

## At a glance

|  | Knip | ts-prune | unimported | repowise `dead-code` | 
|---|---|---|---|---|
| Status (Oct 29, 2026) | Active: 6.43.0, October 24, 2026 | npm 0.10.3 from December 2021; repo updated September 2026 | Archived; deprecated on npm | Active: 0.59.0 | 
| License | ISC | MIT | MIT | AGPL-3.0 | 
| Unused exports and types | Yes | Yes | No | Yes, with confidence tiers | 
| Unused files | Yes | No | Yes | Yes | 
| Unused and unlisted dependencies | Yes | No | Yes | Unused packages in a monorepo | 
| Monorepo workspaces | Yes | One tsconfig per run | Entries listed by hand | Yes, and across repos in a workspace | 
| Config needed on Excalidraw | None | None | An entry list | None | 
| First run on Excalidraw | 33.8 s | 20.8 s | 112 s | 160 s index | 
| Later runs | 3.1 to 3.5 s | 20.7 s | not repeated | 2.4 s report from the index | 
| Auto-fix | Yes ( `--fix`) | No | Not tested | No | 
| Languages | JavaScript, TypeScript | TypeScript | JavaScript, TypeScript | 28 languages | 

Scroll the table sideways to see every column.

## Maintenance status: which ones are deprecated?

unimported is archived. Its GitHub repository is read-only, npm marks 1.31.1 as deprecated, and the README opens with "This project is no longer maintained" and a link to Knip. Knip's [migration page](https://knip.dev/explanations/comparison-and-migration) gives the equivalent command: `knip --production --dependencies --files`.

ts-prune is not archived, but it has not shipped to npm since December 2021. The [GitHub repository](https://github.com/nadeesha/ts-prune) got a modernisation commit on September 14, 2026, and a v0.11.0 tag; `package.json` on the main branch says 0.11.0 and needs Node 22.18 or newer. As of October 29, 2026, npm's latest version is still 0.10.3, so `npx ts-prune` installs the 2021 code. That is the version we tested, because it is the one people run. Knip's migration page still lists ts-prune as archived.

Knip is actively developed. Version 6.43.0 shipped on October 24, 2026, [knip.dev](https://knip.dev/) lists 190+ plugins, and its [issue types](https://knip.dev/reference/issue-types) run from unused files to duplicate exports and cycles. The repository had commits on the day we ran this.

## What we ran

The test repository is [excalidraw/excalidraw](https://github.com/excalidraw/excalidraw) at commit `e7b5346`, the same checkout we used for [madge vs dependency-cruiser](/blog/comparisons/madge-vs-dependency-cruiser?src=blog_knip-vs-ts-prune-vs-unimported). The layout matters here: the app in `excalidraw-app/`, the library in `packages/*`, examples in `examples/*`, and a Docusaurus site in `dev-docs/` that is not one of the workspaces. The library is published to npm with wildcard subpath exports (`"./*"` in `packages/excalidraw/package.json`), so every file in that package is importable by outside users. That last detail explains most of the disagreement below.

Each tool ran with its defaults first. We then tried the one change a user would reach for, and verified the interesting findings with `git grep`. Commands and versions are in [How we measured](#how-we-measured).

## The results side by side

| Finding | Knip (default) | Knip `--include-entry-exports` | ts-prune 0.10.3 | unimported 1.31.1 | repowise (confidence 0.4+) | 
|---|---|---|---|---|---|
| Unused exports | 5 | 260 | 275 (plus 140 "used in module") | n/a | 46 | 
| Unused exported types | 3 | 75 | counted above | n/a | counted above | 
| Unused files | 13 | 13 | n/a | 45 | 8 | 
| Unused dependencies | 14 (+29 dev) | 14 (+29 dev) | n/a | 0 | 1 unused package ( `dev-docs`) | 
| Unlisted dependencies | 132 | 132 | n/a | n/a | n/a | 
| Run time | 3.1 to 3.5 s (33.8 s first run) | 3.4 s | 20.8 s | 112 s (single run) | 2.4 s (after a 160 s index) | 

Scroll the table sideways to see every column.

Most of the gap comes from one design decision: what counts as public API.

## Knip: the default respects your public API

Knip ran with zero config and reported only 5 unused exports and 3 unused types, because it treats a published package's exports as entry points. Excalidraw's `"./*"` wildcard export makes every file in `packages/excalidraw` public, so Knip assumes outside users may import any of it. For a library you publish, that is the right default.

```
npx knip
```
```
Unused files (13)
Unused dependencies (14)
Unused devDependencies (29)
Unlisted dependencies (132)
Unlisted binaries (4)
Unused exports (5)
Unused exported types (3)
Duplicate exports (5)
```
The first run took 33.8 seconds and left a jiti cache in `node_modules/.cache`; later runs took 3.1 to 3.5 seconds.

`--include-entry-exports` turns the public-API view off. It reported 260 unused exports and 75 unused types, led by 55 in `packages/excalidraw/index.tsx`, the package's front door. Those are exports nothing inside the repository imports, which is a different question from "dead".

Knip is the only tool here that reports unlisted dependencies. It found 132. 69 of them are imports of `@excalidraw/excalidraw` from lower packages, and 75 of the 132 come from `packages/element`, whose `package.json` declares only `common`, `math` and `fractional-indexing`. That works today through tsconfig path aliases and hoisting, and it would break for anyone consuming `@excalidraw/element` on its own. Those upward imports also show up as cycles in our [madge vs dependency-cruiser test](/blog/comparisons/madge-vs-dependency-cruiser?src=blog_knip-vs-ts-prune-vs-unimported). On the other side, `packages/utils/package.json` lists packages such as `pako` and `png-chunks-extract` that Knip reports as unused.

Its 13 unused files are the 10 `dev-docs` files (a Docusaurus site that is not in the workspace list, so Knip has no entry for it), `public/service-worker.js`, `scripts/buildDocs.js` and `scripts/buildWasm.js`. `--production` widens that to 28 by dropping test and tooling entries. Zero config runs, but before gating CI on it you would still add an ignore for `dev-docs` and decide what to do about the 132 unlisted imports; we did not tune a `knip.json` for this test.

**Pick Knip if** you want one tool for exports, files and dependencies, you work in a monorepo, or you want `--fix` to remove findings once you trust them.

## ts-prune: exports only, and an old TypeScript

ts-prune reported 275 unused exports in 20.8 seconds, plus 140 more marked "(used in module)". It reads your tsconfig and lists every export nothing else in the project imports. It has no notion of a package's public API, so the list is close to Knip's `--include-entry-exports` mode: 130 findings appear in both.

```
npx ts-prune -p tsconfig.json
```
```
\excalidraw-app\data\index.ts:58 - getSyncableElements
\excalidraw-app\data\index.ts:74 - EncryptedData
\excalidraw-app\data\index.ts:133 - isCollaborationLink
```
The first and third lines are wrong. `getSyncableElements` is imported and called in `excalidraw-app/collab/Collab.tsx`, and `isCollaborationLink` in `excalidraw-app/App.tsx`, both through a directory import (`from "../data"`). We found eight false positives of this kind in `excalidraw-app/data/index.ts`.

The cause is the bundled compiler. ts-prune 0.10.3 depends on ts-morph 13, which ships TypeScript 4.5. Excalidraw's tsconfig uses `"moduleResolution": "bundler"`, added in TypeScript 5.0. When we pointed ts-prune at a copy of the tsconfig with `"moduleResolution": "node"`, those eight false positives disappeared and `EncryptedData` and `SocketUpdateDataIncoming`, which Knip also flags, stayed. We did not build and test the unreleased 0.11.0 code from the main branch.

ts-prune does not look at files or dependencies. It supports a `// ts-prune-ignore-next` comment above an export, and `-e` makes it exit non-zero for CI.

**Pick ts-prune if** you have a simple TypeScript project on `node` module resolution, you only want an export list, and an existing CI job already depends on it. Otherwise move to `knip --include exports,types,nsExports,nsTypes`, which Knip documents as the equivalent.

## unimported: needs entries, then walks into node\_modules

unimported would not run on Excalidraw without config. With no `main` or `source` field in the root `package.json`, it stopped with "Unable to locate entry points for this node project". We wrote a `.unimportedrc.json` listing eight entries: the app's `index.tsx` and each package's `index`.

It then took 112 seconds and reported 45 unimported files, 0 unused dependencies and 3 unresolved imports, two of them inside `node_modules/ws`. It followed imports into installed packages, which probably accounts for part of that time; we did not profile it.

Of the 45 files, four are plain false positives that Knip's default run did not make:

- `packages/excalidraw/components/LinkButton.tsx` and `ShareableLinkDialog.tsx` are imported by the app through the alias form `@excalidraw/excalidraw/components/LinkButton`, which unimported did not resolve.
- `Sidebar/siderbar.test.helpers.tsx` is imported by two test files. unimported only follows production entries.
- `packages/excalidraw/index-node.ts` is named as a build entry in `scripts/build-node.js` line 28, a string an import graph cannot see.

Another 25 (thirteen `scripts/*` files and twelve `examples/*` files) depend on our entry list: nothing we listed reaches them, and a longer list would clear them.

It did catch files that look truly dead: `ButtonIconCycle.tsx`, `Paragraph.tsx` and `data/ai/types.ts` in `packages/excalidraw` have no importers anywhere in the repository, and Knip's default run reports none of them.

**Keep unimported only if** an existing CI job depends on it and you cannot change it yet. It will not get fixes for new TypeScript or bundler features.

## repowise dead-code: confidence and history

`repowise dead-code` reported 55 findings at its default 0.4 confidence floor: 8 unreachable files, 46 unused exports and 1 unused package, each tiered and scored from the dependency graph and git history. It reads the index that `repowise init` builds (160 seconds on Excalidraw, including the full git history), and the report itself took 2.4 seconds.

```
repowise init
repowise dead-code
```
```
| unreachable_file | packages/excalidraw/data/ai/types.ts  |  100% |  ✗  |  300 | File has no importers (in_degree=0) |
| unused_export    | actionChangeArrowType                 |  100% |  ✓  |  246 | Public symbol 'actionChangeArrowType' has no importers |
| unreachable_file | public/service-worker.js              |   40% |  ✗  |   20 | File has no importers (in_degree=0) |
```
Confidence is where it differs from the other three. An unreachable file starts high when its last commit is old and low when someone is still editing it, and it is pulled down to 40% when the path looks like config or bootstrap code, or a runtime loader sits in the same directory. That is why `public/service-worker.js` (fetched by URL in the browser, and flagged by every file-level tool here) sits in the review tier, while `packages/excalidraw/data/ai/types.ts`, which nothing imports and nobody has committed to in over a year, is at 100%. Knip's default run did not report that file, because the wildcard export makes it public API.

Of repowise's 46 unused exports, 35 are also in Knip's `--include-entry-exports` list, 35 are in ts-prune's, and 34 are in all three. The [dead code docs](https://docs.repowise.dev/intelligence/dead-code) explain the scoring. It has no framework plugins and does not report unlisted dependencies, so on a JavaScript-only repository it sits next to Knip, not in place of it.

## What every export checker got wrong the same way

Knip (with `--include-entry-exports`), ts-prune and repowise all flagged five Excalidraw actions as unused exports. All three are right about the export and wrong about the code. Each looks like this:

```
export const actionTogglePolygon = register({
  name: "togglePolygon",
  // ...
});
```
Nothing imports `actionTogglePolygon` by name; `git grep` finds only its own definition. But `register()` appends the action to Excalidraw's action list when the module loads, and the editor picks it up from there. Removing the `export` keyword leaves that registration in place; deleting the declaration removes the feature. Knip's `--fix` does the safe thing here: it removes the `export` keyword and leaves the declaration.

That is the general limit of static dead-code analysis: it proves nothing *imports* a name, not that nothing *uses* it. Registries and files fetched by URL both look dead to an import graph. Before deleting an export, grep for the string name the code registers it under (`togglePolygon` here), not only the identifier, then delete in small pull requests, and add a known exception (Knip's `ignore` options, `// ts-prune-ignore-next`, or a false-positive status in the repowise dashboard) once you have checked a finding.

## Config effort

|  | Knip | ts-prune | unimported | repowise | 
|---|---|---|---|---|
| What we had to change | Nothing; one flag to include entry exports | A tsconfig copy with `node` resolution to drop false positives | An eight-entry `.unimportedrc.json` | Nothing | 
| Ignore mechanism | `knip.json` `ignore`, `ignoreDependencies`, JSDoc tags | `-i`, `-s`, `// ts-prune-ignore-next` | `.unimportedrc.json` ignore lists | Dashboard triage status per finding; no ignore file | 
| CI exit code | Non-zero on findings | `-e` | Non-zero on findings | Use the JSON output | 

Scroll the table sideways to see every column.

## How to choose

- **New project or new CI job:** Knip. Start with `npx knip`, fix configuration hints first, then turn findings into errors.
- **Published library:** Knip's default, which treats package exports as public. Run `--include-entry-exports` occasionally to review the API surface itself.
- **Existing ts-prune job:** keep it only if your tsconfig uses `node` or `node16` resolution and the list matches reality. Otherwise switch to `knip --include exports,types,nsExports,nsTypes`.
- **Existing unimported job:** switch to `knip --production --dependencies --files`. The project is archived and will not track new TypeScript features.
- **A cleanup backlog of hundreds of exports:** sort by how long each file has gone without a commit before deleting anything; `repowise dead-code` puts that age into its confidence score. The [find dead code guide](/blog/guides/find-dead-code-repository?src=blog_knip-vs-ts-prune-vs-unimported) walks through a safe deletion order.

## How we measured

- **Repository:** excalidraw/excalidraw at `e7b534668a60add7f725531f3c9abf32508c7b4e` (October 28, 2026), dependencies installed with `yarn install --frozen-lockfile --ignore-scripts`. Every tool ran from the repository root.
- **Versions:** Knip 6.43.0, ts-prune 0.10.3, unimported 1.31.1, repowise 0.59.0, TypeScript 5.9.3, Node 22.19.0, on Windows 11 with an AMD Ryzen 9 8940HX and 31 GB RAM, on October 29, 2026.
- **Commands:** `knip`, `knip --include-entry-exports`, `knip --production`; `ts-prune -p tsconfig.json`; `unimported` with an eight-entry `.unimportedrc.json`; `repowise init` then `repowise dead-code` and `repowise dead-code --format json`.
- **Overlap:** we keyed each export finding by file and symbol name and intersected the sets. False positives named in this post were checked with `git grep` against the same commit.
- **Status:** release dates, deprecation flags and archive status come from the npm registry and GitHub on the same day. What this does not show: precision across many repositories, behaviour on Yarn PnP or pnpm's strict layout, or Knip with a hand-tuned `knip.json`.

## FAQ

- Is ts-prune deprecated?
- Not officially. The repository is not archived and got a modernisation commit in September 2026, but npm has had no release since 0.10.3 in December 2021, and that version bundles TypeScript 4.5. For new setups, Knip covers the same export check.
- Is unimported still maintained?
- No. It is archived and deprecated on npm; the equivalent Knip command is `knip --production --dependencies --files`.
- How do I find unused exports in TypeScript?
- Run `npx knip` from the project root. It reports unused exports, unused exported types and enum members along with unused files and dependencies. In a library whose package exports make files public, add `--include-entry-exports` to see exports nothing inside the repository imports.
- Why does Knip report fewer unused exports than ts-prune?
- Knip treats files exposed through `package.json` exports and other entry points as public API and does not report their exports by default. ts-prune has no such concept and lists every export nothing in the project imports. On Excalidraw that was 5 against 275.
- What is the best ts-prune alternative?
- Knip, using `knip --include exports,types,nsExports,nsTypes` for the closest match to ts-prune's output. ts-unused-exports is another export-only option. For a repository with more than one language, `repowise dead-code` reports unused exports across all of them with a confidence score.
- Can Knip remove unused code automatically?
- Yes. `knip --fix` removes the `export` keyword from unused exports and types, removes unused enum members and unused dependencies, and deletes unused files only when you add `--allow-remove-files`. Review the diff and run your tests first, since registries and dynamic loading are invisible to any import graph.
