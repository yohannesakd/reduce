# Using Generators

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Effect team, effect.website
- Date: 2026-05-30
- License: MIT, as the site states
- Original location: https://effect.website/docs/v4/getting-started/using-generators/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# Using Generators

Effect offers a convenient syntax, similar to `async`/`await`, to write effectful code using [generators](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Generator).

## 

The `Effect.gen` utility simplifies the task of writing effectful code by utilizing JavaScript’s generator functions. This method helps your code appear and behave more like traditional synchronous code, which enhances both readability and error management.

**Example** (Performing Transactions with Discounts)

Let’s explore a practical program that performs a series of data transformations commonly found in application logic:

Key steps to follow when using `Effect.gen`:

- Wrap your logic in `Effect.gen`
- Use `yield*` to handle effects
- Return the final result

If any of the effects that you handle inside of the generator with `yield*`
fail, then the generator will stop and exit with that failure.

## 

If you are familiar with `async`/`await`, you may notice that the flow of writing code is similar.

Let’s compare the two approaches:

It’s important to note that although the code appears similar, the two programs are not identical. The purpose of comparing them side by side is just to highlight the resemblance in how they are written.

## 

One significant advantage of using `Effect.gen` in conjunction with generators is its capability to employ standard control flow constructs within the generator function. These constructs include `if`/`else`, `for`, `while`, and other branching and looping mechanisms, enhancing your ability to express complex control flow logic in your code.

**Example** (Using Control Flow)

## 

The `Effect.gen` API lets you integrate error handling directly into your workflow by yielding failed effects.
You can introduce errors with `Effect.fail`, as shown in the example below.

**Example** (Introducing an Error into the Flow)

## 

When working with `Effect.gen`, it is important to understand how it handles errors.
This API will stop execution at the **first error** it encounters and return that error.

How does this affect your code? If you have several operations in sequence, once any one of them fails, the remaining operations will not run, and the error will be returned.

In simpler terms, if something fails at any point, the program will stop right there and deliver the error to you.

If you don’t want to stop on an error, you can use the `Effect.result` method to encapsulate the error in the [Result](/docs/v4/data-types/result/) data type: see the [examples of managing expected errors](/docs/v4/error-management/expected-errors/#result).

**Example** (Halting Execution at the First Error)

Even though execution never reaches code after a failure, TypeScript may still assume that the code below the error is reachable unless you explicitly return after the failure.

For example, consider the following scenario where you want to narrow the type of a variable:

**Example** (Type Narrowing without Explicit Return)

In this example, TypeScript still considers `user` possibly `undefined` because there is no explicit return after the failure.

To fix this, explicitly return right after calling `Effect.fail`:

**Example** (Type Narrowing with Explicit Return)

## `this`

In some cases, you might need to pass a reference to the current object (`this`) into the body of your generator function.
You can achieve this by utilizing an overload that accepts the reference as the first argument:

**Example** (Passing `this` to Generator)
