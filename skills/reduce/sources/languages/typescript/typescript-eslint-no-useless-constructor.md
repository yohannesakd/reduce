# typescript-eslint: no-useless-constructor

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The typescript-eslint team
- License: MIT
- Original location: https://typescript-eslint.io/rules/no-useless-constructor/
- Copied: 2026-11-20, from the source file packages/eslint-plugin/docs/rules/no-useless-constructor.mdx of typescript-eslint/typescript-eslint at commit c4bddb15e6c0, from the GitHub API

## Text
---
description: 'Disallow unnecessary constructors.'
---

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

> 🛑 This file is source code, not the primary documentation location! 🛑
>
> See **https://typescript-eslint.io/rules/no-useless-constructor** for documentation.

It adds support for:

- constructors marked as `protected` / `private` (i.e. marking a constructor as non-public),
- `public` constructors when there is no superclass,
- constructors with only parameter properties.

### Caveat

This lint rule will report on constructors whose sole purpose is to change visibility of a parent constructor.
See [discussion on this rule's lack of type information](https://github.com/typescript-eslint/typescript-eslint/issues/3820#issuecomment-917821240) for context.
