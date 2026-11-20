# Managing Layers

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Effect team, effect.website
- Date: 2026-05-30
- License: MIT, as the site states
- Original location: https://effect.website/docs/v4/requirements-management/layers/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# Managing Layers

In the [Managing Services](/docs/v4/requirements-management/services/) page, you learned how to create effects which depend on some service to be provided in order to execute, as well as how to provide that service to an effect.

However, what if we have a service within our effect program that has dependencies on other services in order to be built? We want to avoid leaking these implementation details into the service interface.

To represent the “dependency graph” of our program and manage these dependencies more effectively, we can utilize a powerful abstraction called “Layer”.

Layers act as **constructors for creating services**, allowing us to manage dependencies during construction rather than at the service level. This approach helps to keep our service interfaces clean and focused.

Let’s review some key concepts before diving into the details:

| Concept | Description | 
|---|---|
| **service** | A reusable component providing specific functionality, used across different parts of an application. | 
| **service key** | A unique identifier representing a **service**, allowing Effect to locate and use it. | 
| **context** | A collection of services, functioning like a map with **service keys** as keys and **services** as values. | 
| **layer** | An abstraction for constructing **services**, managing dependencies during construction rather than at the service level. | 

## 

Let’s imagine that we are building a web application. We could imagine that the dependency graph for an application where we need to manage configuration, logging, and database access might look something like this:

- The `Config` service provides application configuration.
- The `Logger` service depends on the `Config` service.
- The `Database` service depends on both the `Config` and `Logger` services.

Our goal is to build the `Database` service along with its direct and indirect dependencies. This means we need to ensure that the `Config` service is available for both `Logger` and `Database`, and then provide these dependencies to the `Database` service.

## 

When constructing the `Database` service, it’s important to avoid exposing the dependencies on `Config` and `Logger` within the `Database` interface.

You might be tempted to define the `Database` service as follows:

**Example** (Leaking Dependencies in the Service Interface)

Here, the `query` function of the `Database` service requires both `Config` and `Logger`. This design leaks implementation details, making the `Database` service aware of its dependencies, which complicates testing and makes it difficult to mock.

To demonstrate the problem, let’s create a test instance of the `Database` service:

**Example** (Creating a Test Instance with Leaked Dependencies)

Because the `Database` service interface directly includes dependencies on `Config` and `Logger`, it forces any test setup to include these services, even if they’re irrelevant to the test. This adds unnecessary complexity and makes it difficult to write simple, isolated unit tests.

Instead of directly tying dependencies to the `Database` service interface, dependencies should be managed at the construction phase.

We can use **layers** to properly construct the `Database` service and manage its dependencies without leaking details into the interface.

## 

The `Layer` type is structured as follows:

A `Layer` represents a blueprint for constructing a `RequirementsOut` (the service). It requires a `RequirementsIn` (dependencies) as input and may result in an error of type `Error` during the construction process.

| Parameter | Description | 
|---|---|
| `RequirementsOut` | The service or resource to be created. | 
| `Error` | The type of error that might occur during the construction of the service. | 
| `RequirementsIn` | The dependencies required to construct the service. | 

By using layers, you can better organize your services, ensuring that their dependencies are clearly defined and separated from their implementation details.

For simplicity, let’s assume that we won’t encounter any errors during the value construction (meaning `Error = never`).

Now, let’s determine how many layers we need to implement our dependency graph:

| Layer | Dependencies | Type | 
|---|---|---|
| `ConfigLive` | The `Config` service does not depend on any other services | `Layer<Config>` | 
| `LoggerLive` | The `Logger` service depends on the `Config` service | `Layer<Logger, never, Config>` | 
| `DatabaseLive` | The `Database` service depends on `Config` and `Logger` | `Layer<Database, never, Config \| Logger>` | 

When a service has multiple dependencies, they are represented as a **union type**. In our case, the `Database` service depends on both the `Config` and `Logger` services. Therefore, the type for the `DatabaseLive` layer will be:

### 

The `Config` service does not depend on any other services, so `ConfigLive` will be the simplest layer to implement. Just like in the [Managing Services](/docs/v4/requirements-management/services/) page, we must create a service key for the service. And because the service has no dependencies, we can create the layer directly using the `Layer.succeed` constructor:

Looking at the type of `ConfigLive` we can observe:

- `RequirementsOut` is `Config`, indicating that constructing the layer will produce a `Config` service
- `Error` is `never`, indicating that layer construction cannot fail
- `RequirementsIn` is `never`, indicating that the layer has no dependencies

Note that, to construct `ConfigLive`, we used the `Config.of`
constructor. However, this is merely a helper to ensure correct type inference
for the implementation. It’s possible to skip this helper and construct the
implementation directly as a simple object:

### 

Now we can move on to the implementation of the `Logger` service, which depends on the `Config` service to retrieve some configuration.

Just like we did in the [Managing Services](/docs/v4/requirements-management/services/#using-the-service) page, we can yield the `Config` service key to “extract” the service from the context.

Given that using the `Config` service key is an effectful operation, we use `Layer.effect` to create a layer from the resulting effect.

Looking at the type of `LoggerLive`:

we can observe that:

- `RequirementsOut` is `Logger`
- `Error` is `never`, indicating that layer construction cannot fail
- `RequirementsIn` is `Config`, indicating that the layer has a requirement

### 

Finally, we can use our `Config` and `Logger` services to implement the `Database` service.

Looking at the type of `DatabaseLive`:

we can observe that the `RequirementsIn` type is `Config | Logger`, i.e., the `Database` service requires both `Config` and `Logger` services.

## 

Layers can be combined in two primary ways: **merging** and **composing**.

### 

Layers can be combined through merging using the `Layer.merge` function:

When we merge two layers, the resulting layer:

- requires all the services that both of them require (`"In1" | "In2"`).
- produces all services that both of them produce (`"Out1" | "Out2"`).

For example, in our web application above, we can merge our `ConfigLive` and `LoggerLive` layers into a single `AppConfigLive` layer, which retains the requirements of both layers (`never | Config = Config`) and the outputs of both layers (`Config | Logger`):

### 

Layers can be composed using the `Layer.provide` function:

Sequential composition of layers implies that the output of one layer is supplied as the input for the inner layer, resulting in a single layer with the requirements of the outer layer and the output of the inner.

Now we can compose the `AppConfigLive` layer with the `DatabaseLive` layer:

We obtained a `MainLive` layer that produces the `Database` service:

This layer is the fully resolved layer for our application.

### 

Let’s say we want our `MainLive` layer to return both the `Config` and `Database` services. We can achieve this with `Layer.provideMerge`:

## 

Now that we have assembled the fully resolved `MainLive` for our application,
we can provide it to our program to satisfy the program’s requirements using `Effect.provide`:

Note that the `runnable` requirements type is `never`, indicating that the program does not require any additional services to run.

## 

Sometimes your entire application might be a Layer, for example, an HTTP server. You can convert that layer to an effect with `Layer.launch`. It constructs the layer and keeps it alive until interrupted.

**Example** (Launching an HTTP Server Layer)

## 

The `Layer.tap` and `Layer.tapError` functions allow you to perform additional effects based on the success or failure of a layer. These operations do not modify the layer’s signature but are useful for logging or performing side effects during layer construction.

- `Layer.tap`: Executes a specified effect when the layer is successfully acquired.
- `Layer.tapError`: Executes a specified effect when the layer fails to acquire.

**Example** (Logging Success and Failure During Layer Acquisition)

## 

When constructing layers, it is important to handle potential errors. `Layer.catch` can inspect an acquisition error and return a fallback layer.

### 

The `Layer.catch` function allows you to recover from errors during layer construction by specifying a fallback layer. This can be useful for handling specific error cases and ensuring the application can continue with an alternative setup.

**Example** (Recovering from Errors During Layer Construction)

If the fallback does not need the error, ignore the argument passed to `Layer.catch`.

**Example** (Falling Back to an Alternative Layer)

## 

`Context.Service` can define a service key and its construction effect together as a single class. You can then expose layers as static fields on that class.

### 

The following example defines a `Cache` service that depends on a file system.

**Example** (Defining a Cache Service)

### 

Declare a service’s layers as static class fields, built from `this.make` with `Layer.effect`. The field names below are just a convention, not part of the API.

| Static field | Description | 
|---|---|
| `Cache.layer` | Provides the `Cache` service with its dependencies already included. | 
| `Cache.layerWithoutDependencies` | Provides the `Cache` service but requires dependencies to be provided separately. | 

### 

A service created with `Context.Service` can be accessed like any other Effect service.

**Example** (Accessing the Cache Service)

Since this example uses `Cache.layer`, it interacts with the real file system. If the file does not exist, it results in an error.

### 

To test the program without depending on the real file system, we can inject a test file system using the `Cache.layerWithoutDependencies` layer.

**Example** (Using a Test File System)

### 

Alternatively, you can mock the `Cache` service itself instead of replacing its dependencies.

**Example** (Mocking the Cache Service)

### `make`

`Context.Service`’s `make` field accepts any `Effect`, allowing services to use different construction styles:

| Style | How to build `make` | 
|---|---|
| Static value | `Effect.succeed(...)`: a constant implementation. | 
| Synchronous | `Effect.sync(() => ...)`: a synchronous constructor. | 
| Effectful | `Effect.gen(function* () { ... })` (or any other `Effect`): a constructor that itself depends on other services. | 
| Scoped | `Effect.gen(...)` using `Effect.acquireRelease`/`Effect.addFinalizer` inside `make`: lifecycle management, no separate option. | 

**Example** (Defining a Service with a Static Implementation)

This is the simplest way to define a service. It is useful when you want to provide a constant value for the service.

**Example** (Defining a Service with a Synchronous Constructor)

**Example** (Managing a Service with Lifecycle Control)

The `Scoped.layer` layer does not require `Scope` as a dependency, since `Scoped` itself manages its lifecycle.
