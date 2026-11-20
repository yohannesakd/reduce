# typescript-eslint: no-non-null-assertion

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The typescript-eslint team
- License: MIT
- Original location: https://typescript-eslint.io/rules/no-non-null-assertion/
- Copied: 2026-11-20, from the source file packages/eslint-plugin/docs/rules/no-non-null-assertion.mdx of typescript-eslint/typescript-eslint at commit c4bddb15e6c0, from the GitHub API

## Text
---
description: 'Disallow non-null assertions using the `!` postfix operator.'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

> 🛑 This file is source code, not the primary documentation location! 🛑
>
> See **https://typescript-eslint.io/rules/no-non-null-assertion** for documentation.

TypeScript's `!` non-null assertion operator asserts to the type system that an expression is non-nullable, as in not `null` or `undefined`.
Using assertions to tell the type system new information is often a sign that code is not fully type-safe.
It's generally better to structure program logic so that TypeScript understands when values may be nullable.

## Examples

<Tabs>
<TabItem value="❌ Incorrect">

```ts
interface Example {
  property?: string;
}

declare const example: Example;
const includesBaz = example.property!.includes('baz');
```

</TabItem>
<TabItem value="✅ Correct">

```ts
interface Example {
  property?: string;
}

declare const example: Example;
const includesBaz = example.property?.includes('baz') ?? false;
```

</TabItem>
</Tabs>

## When Not To Use It

If your project's types don't yet fully describe whether certain values may be nullable, such as if you're transitioning to `strictNullChecks`, this rule might create many false reports.
You might consider using [ESLint disable comments](https://eslint.org/docs/latest/use/configure/rules#use-configuration-comments) for those specific situations instead of completely disabling this rule.
