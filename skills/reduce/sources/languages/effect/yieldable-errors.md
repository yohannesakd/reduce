# Yieldable Errors

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Effect team, effect.website
- Date: 2026-05-30
- License: MIT, as the site states
- Original location: https://effect.website/docs/v4/error-management/yieldable-errors/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# Yieldable Errors

Errors created with `Data.Error` and `Data.TaggedError` are yieldable. Inside [`Effect.gen`](/docs/v4/getting-started/using-generators/), yielding one is equivalent to passing it to [`Effect.fail`](/docs/v4/getting-started/creating-effects/#fail).

## 

Use `Data.Error` when the error does not need a discriminant tag.

**Example** (Yielding a Custom Error)

## 

`Data.TaggedError` adds a readonly `_tag` field. Tagged errors form discriminated unions that can be handled precisely with [`Effect.catchTag`](/docs/v4/error-management/expected-errors/#catchtag) and [`Effect.catchTags`](/docs/v4/error-management/expected-errors/#catchtags).

**Example** (Handling Tagged Errors)

Use tagged errors for domain errors that callers may need to distinguish. The class is both the error’s constructor and its TypeScript type.
