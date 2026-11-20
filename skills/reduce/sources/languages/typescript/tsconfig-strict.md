# TSConfig reference: strict

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The TypeScript team
- License: CC BY 4.0
- Original location: https://www.typescriptlang.org/tsconfig/
- Copied: 2026-11-20, from the source file packages/tsconfig-reference/copy/en/options/strict.md of microsoft/TypeScript-Website at commit 24166845f5de, from the GitHub API

## Text
---
display: "Strict"
oneline: "Enable all strict type-checking options."
---

The `strict` flag enables a wide range of type checking behavior that results in stronger guarantees of program correctness.
Turning this on is equivalent to enabling all of the _strict mode family_ options, which are outlined below.
You can then turn off individual strict mode family checks as needed.

Future versions of TypeScript may introduce additional stricter checking under this flag, so upgrades of TypeScript might result in new type errors in your program.
When appropriate and possible, a corresponding flag will be added to disable that behavior.
