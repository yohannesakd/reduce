# ESLint: no-useless-catch

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The ESLint team
- License: MIT
- Original location: https://eslint.org/docs/latest/rules/no-useless-catch
- Copied: 2026-11-20, from the source file docs/src/rules/no-useless-catch.md of eslint/eslint at commit e0148e30da66, from the GitHub API

## Text
---
title: no-useless-catch
rule_type: suggestion
---



A `catch` clause that only rethrows the original error is redundant, and has no effect on the runtime behavior of the program. These redundant clauses can be a source of confusion and code bloat, so it's better to disallow these unnecessary `catch` clauses.

## Rule Details

This rule reports `catch` clauses that only `throw` the caught error.

Examples of **incorrect** code for this rule:

::: incorrect

```js
/*eslint no-useless-catch: "error"*/

try {
  doSomethingThatMightThrow();
} catch (e) {
  throw e;
}

try {
  doSomethingThatMightThrow();
} catch (e) {
  throw e;
} finally {
  cleanUp();
}
```

:::

Examples of **correct** code for this rule:

::: correct

```js
/*eslint no-useless-catch: "error"*/

try {
  doSomethingThatMightThrow();
} catch (e) {
  doSomethingBeforeRethrow();
  throw e;
}

try {
  doSomethingThatMightThrow();
} catch (e) {
  handleError(e);
}

try {
  doSomethingThatMightThrow();
} finally {
  cleanUp();
}
```

:::

## Options

This rule has no options.

## When Not To Use It

If you don't want to be notified about unnecessary catch clauses, you can safely disable this rule.
