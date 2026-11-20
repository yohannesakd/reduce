# Creating Effects

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Effect team, effect.website
- Date: 2026-05-30
- License: MIT, as the site states
- Original location: https://effect.website/docs/v4/getting-started/creating-effects/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# Creating Effects

Effect provides different ways to create effects, which are units of computation that encapsulate side effects. In this guide, we will cover some of the common methods that you can use to create effects.

## 

In traditional programming, when an error occurs, it is often handled by throwing an exception:

However, throwing errors can be problematic. The type signatures of functions do not indicate that they can throw exceptions, making it difficult to reason about potential errors.

To address this issue, Effect introduces dedicated constructors for creating effects that represent both success and failure: `Effect.succeed` and `Effect.fail`. These constructors allow you to explicitly handle success and failure cases while **leveraging the type system to track errors**.

### 

Creates an `Effect` that always succeeds with a given value.

Use this function when you need an effect that completes successfully with a specific value without any errors or external dependencies.

**Example** (Creating a Successful Effect)

The type of `success` is `Effect<number, never, never>`, which means:

- It produces a value of type `number`.
- It does not generate any errors (`never` indicates no errors).
- It requires no additional data or dependencies (`never` indicates no requirements).

### 

Creates an `Effect` that represents an error that can be recovered from.

Use this function to explicitly signal an error in an `Effect`. The error
will keep propagating unless it is handled. You can handle the error with
functions like [Effect.catch](/docs/v4/error-management/expected-errors/#catching-every-typed-error) or
[Effect.catchTag](/docs/v4/error-management/expected-errors/#catchtag).

**Example** (Creating a Failed Effect)

The type of `failure` is `Effect<never, Error, never>`, which means:

- It never produces a value (`never` indicates that no successful result will be produced).
- It fails with an error, specifically an `Error`.
- It requires no additional data or dependencies (`never` indicates no requirements).

Although you can use `Error` objects with `Effect.fail`, you can also pass strings, numbers, or more complex objects depending on your error management strategy.

Using “tagged” errors (objects with a `_tag` field) can help identify error types and works well with standard Effect functions, like [Effect.catchTag](/docs/v4/error-management/expected-errors/#catchtag).

**Example** (Using Tagged Errors)

## 

With `Effect.succeed` and `Effect.fail`, you can explicitly handle success and failure cases and the type system will ensure that errors are tracked and accounted for.

**Example** (Rewriting a Division Function)

Here’s how you can rewrite the [`divide`](#why-not-throw-errors) function using Effect, making error handling explicit.

In this example, the `divide` function indicates in its return type `Effect<number, Error>` that the operation can either succeed with a `number` or fail with an `Error`.

This clear type signature helps ensure that errors are handled properly and that anyone calling the function is aware of the possible outcomes.

**Example** (Simulating a User Retrieval Operation)

Let’s imagine another scenario where we use `Effect.succeed` and `Effect.fail` to model a simple user retrieval operation where the user data is hardcoded, which could be useful in testing scenarios or when mocking data:

In this example, `exampleUserEffect`, which has the type `Effect<User, Error>`, will either produce a `User` object or an `Error`, depending on whether the user exists in the mocked database.

For a deeper dive into managing errors in your applications, refer to the [Error Management Guide](/docs/v4/error-management/expected-errors/).

## 

In JavaScript, you can delay the execution of synchronous computations using “thunks”.

Thunks are useful for delaying the computation of a value until it is needed.

To model synchronous side effects, Effect provides the `Effect.sync` and `Effect.try` constructors, which accept a thunk.

### 

Creates an `Effect` that represents a synchronous side-effectful computation.

Use `Effect.sync` when you are sure the operation will not fail.

The provided function (`thunk`) must not throw errors; if it does, the error will be treated as a [“defect”](/docs/v4/error-management/unexpected-errors/).

This defect is not a standard error but indicates a flaw in the logic that was expected to be error-free.
You can think of it similar to an unexpected crash in the program, which can be further managed or logged using tools like [Effect.catchDefect](/docs/v4/error-management/unexpected-errors/#catchdefect).
This feature ensures that even unexpected failures in your application are not lost and can be handled appropriately.

**Example** (Logging a Message)

In the example below, `Effect.sync` is used to defer the side-effect of writing to the console.

The side effect (logging to the console) encapsulated within `program` won’t occur until the effect is explicitly run (see the [Running Effects](/docs/v4/getting-started/running-effects/) section for more details). This allows you to define side effects at one point in your code and control when they are activated, improving manageability and predictability of side effects in larger applications.

### 

Creates an `Effect` that represents a synchronous computation that might fail.

In situations where you need to perform synchronous operations that might fail, such as parsing JSON, you can use the `Effect.try` constructor.
This constructor is designed to handle operations that could throw exceptions by capturing those exceptions and transforming them into manageable errors.

**Example** (Safe JSON Parsing)

Suppose you have a function that attempts to parse a JSON string. This operation can fail and throw an error if the input string is not properly formatted as JSON:

In this example:

- `parse` is a function that creates an effect encapsulating the JSON parsing operation.
- If `JSON.parse(input)` throws an error due to invalid input, `Effect.try` catches this error and the effect represented by `program` will fail with an `UnknownError`. This ensures that errors are not silently ignored but are instead handled within the structured flow of effects.

#### 

You might want to transform the caught exception into a more specific error or perform additional operations when catching an error. `Effect.try` supports an overload that allows you to specify how caught exceptions should be transformed:

**Example** (Custom Error Handling)

You can think of this as a similar pattern to the traditional try-catch block in JavaScript:

## 

In traditional programming, we often use `Promise`s to handle asynchronous computations. However, dealing with errors in promises can be problematic. By default, `Promise<Value>` only provides the type `Value` for the resolved value, which means errors are not reflected in the type system. This limits the expressiveness and makes it challenging to handle and track errors effectively.

To overcome these limitations, Effect introduces dedicated constructors for creating effects that represent both success and failure in an asynchronous context: `Effect.promise` and `Effect.tryPromise`. These constructors allow you to explicitly handle success and failure cases while **leveraging the type system to track errors**.

### 

Creates an `Effect` that represents an asynchronous computation guaranteed to succeed.

Use `Effect.promise` when you are sure the operation will not reject.

The provided function (`thunk`) returns a `Promise` that should never reject; if it does, the error will be treated as a [“defect”](/docs/v4/error-management/unexpected-errors/).

This defect is not a standard error but indicates a flaw in the logic that was expected to be error-free.
You can think of it similar to an unexpected crash in the program, which can be further managed or logged using tools like [Effect.catchDefect](/docs/v4/error-management/unexpected-errors/#catchdefect).
This feature ensures that even unexpected failures in your application are not lost and can be handled appropriately.

**Example** (Delayed Message)

The `program` value has the type `Effect<string, never, never>` and can be interpreted as an effect that:

- succeeds with a value of type `string`
- does not produce any expected error (`never`)
- does not require any context (`never`)

### 

Creates an `Effect` that represents an asynchronous computation that might fail.

Unlike `Effect.promise`, this constructor is suitable when the underlying `Promise` might reject.
It provides a way to catch errors and handle them appropriately.
By default if an error occurs, it will be caught and propagated to the error channel as an `UnknownError`.

**Example** (Fetching a TODO Item)

The `program` value has the type `Effect<Response, UnknownError, never>` and can be interpreted as an effect that:

- succeeds with a value of type `Response`
- might produce an error (`UnknownError`)
- does not require any context (`never`)

#### 

If you want more control over what gets propagated to the error channel, you can use an overload of `Effect.tryPromise` that takes a remapping function:

**Example** (Custom Error Handling)

## 

Creates an `Effect` from a callback-based asynchronous function.

Sometimes you have to work with APIs that don’t support `async/await` or `Promise` and instead use the callback style.
To handle callback-based APIs, Effect provides the `Effect.callback` constructor.

**Example** (Wrapping a Callback API)

Let’s wrap the `readFile` function from Node.js’s `fs` module into an Effect-based API (make sure `@types/node` is installed):

In the above example, we manually annotate the types when calling `Effect.callback`:

because TypeScript cannot infer the type parameters for a callback
based on the return value inside the callback body. Annotating the types ensures that the values provided to `resume` match the expected types.

The `resume` function inside `Effect.callback` should be called exactly once. Calling it more than once will result in the extra calls being ignored.

**Example** (Ignoring Subsequent `resume` Calls)

### 

For more advanced use cases, the callback passed to Effect.callback may return an Effect that will be executed if the fiber running this effect is interrupted. This can be used to perform cleanup when the operation is cancelled.

**Example** (Handling Interruption with Cleanup)

In this example:

- The `writeFileWithCleanup` function writes data to a file.
- If the fiber running this effect is interrupted, the cleanup effect (which deletes the file) is executed.
- This ensures that resources like open file handles are cleaned up properly when the operation is canceled.

If the operation you’re wrapping supports interruption, the `resume` function can receive an `AbortSignal` to handle interruption requests directly.

**Example** (Handling Interruption with `AbortSignal`)

## 

`Effect.suspend` is used to delay the creation of an effect.
It allows you to defer the evaluation of an effect until it is actually needed.
The `Effect.suspend` function takes a thunk that represents the effect, and it wraps it in a suspended effect.

**Syntax**

Let’s explore some common scenarios where `Effect.suspend` proves useful.

### 

When you want to defer the evaluation of an effect until it is required. This can be useful for optimizing the execution of effects, especially when they are not always needed or when their computation is expensive.

Also, when effects with side effects or scoped captures are created, use `Effect.suspend` to re-execute on each invocation.

**Example** (Lazy Evaluation with Side Effects)

In this example, `bad` is the result of calling `Effect.succeed(i++)` a single time, which increments the scoped variable but [returns its original value](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Operators/Increment#postfix_increment). `Effect.runSync(bad)` does not result in any new computation, because `Effect.succeed(i++)` has already been called. On the other hand, each time `Effect.runSync(good)` is called, the thunk passed to `Effect.suspend()` will be executed, outputting the scoped variable’s most recent value.

### 

`Effect.suspend` is helpful in managing circular dependencies between effects, where one effect depends on another, and vice versa.
For example it’s fairly common for `Effect.suspend` to be used in recursive functions to escape an eager call.

**Example** (Recursive Fibonacci)

The `blowsUp` function creates a recursive Fibonacci sequence without deferring execution. Each call to `blowsUp` triggers further immediate recursive calls, rapidly increasing the JavaScript call stack size.

Conversely, `allGood` avoids stack overflow by using `Effect.suspend` to defer the recursive calls. This mechanism doesn’t immediately execute the recursive effects but schedules them to be run later, thus keeping the call stack shallow and preventing a crash.

### 

In situations where TypeScript struggles to unify the returned effect type, `Effect.suspend` can be employed to resolve this issue.

**Example** (Using `Effect.suspend` to Help TypeScript Infer Types)

## 

The table provides a summary of the available constructors, along with their input and output types, allowing you to choose the appropriate function based on your needs.

| API | Given | Result | 
|---|---|---|
| `succeed` | `A` | `Effect<A>` | 
| `fail` | `E` | `Effect<never, E>` | 
| `sync` | `() => A` | `Effect<A>` | 
| `try` | `() => A` | `Effect<A, UnknownError>` | 
| `try` (overload) | `() => A`, `unknown => E` | `Effect<A, E>` | 
| `promise` | `() => Promise<A>` | `Effect<A>` | 
| `tryPromise` | `() => Promise<A>` | `Effect<A, UnknownError>` | 
| `tryPromise` (overload) | `() => Promise<A>`, `unknown => E` | `Effect<A, E>` | 
| `callback` | `(Effect<A, E> => void) => void` | `Effect<A, E>` | 
| `suspend` | `() => Effect<A, E, R>` | `Effect<A, E, R>` | 

For the complete list of constructors, visit the [Effect Constructors Documentation](/docs/v4/api/effect/Effect#category-constructors).
