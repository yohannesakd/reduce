# Managing Services

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Effect team, effect.website
- Date: 2026-05-30
- License: MIT, as the site states
- Original location: https://effect.website/docs/v4/requirements-management/services/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# Managing Services

In the context of programming, a **service** refers to a reusable component or functionality that can be used by different parts of an application.
Services are designed to provide specific capabilities and can be shared across multiple modules or components.

Services often encapsulate common tasks or operations that are needed by different parts of an application. They can handle complex operations, interact with external systems or APIs, manage data, or perform other specialized tasks.

Services are typically designed to be modular and decoupled from the rest of the application. This allows them to be easily maintained, tested, and replaced without affecting the overall functionality of the application.

When diving into services and their integration in application development, it helps to start from the basic principles of function management and dependency handling without relying on advanced constructs. Imagine having to manually pass a service around to every function that needs it:

This approach becomes cumbersome and unmanageable as your application grows, with services needing to be passed through multiple layers of functions.

To streamline this, you might consider using an environment object that bundles various services:

However, this introduces a new complexity: you must ensure that the environment is correctly set up with all necessary services before it’s used, which can lead to tightly coupled code and makes functional composition and testing more difficult.

## 

The Effect library simplifies managing these dependencies by leveraging the type system.
Instead of manually passing services or environment objects around, Effect allows you to declare service dependencies directly in the function’s type signature using the `Requirements` parameter in the `Effect` type:

This is how it works in practice when using Effect:

**Dependency Declaration**: You specify what services a function needs directly in its type, pushing the complexity of dependency management into the type system.

**Service Provision**: `Effect.provideService` is used to make a service implementation available to the functions that need it. By providing services at the start, you ensure that all parts of your application have consistent access to the required services, thus maintaining a clean and decoupled architecture.

This approach abstracts away manual service handling, letting developers focus on business logic while the compiler ensures all dependencies are correctly managed. It also makes code more maintainable and scalable.

Let’s walk through managing services in Effect step by step:

1. **Creating a Service**: Define a service with its unique functionality and interface.
2. **Using the Service**: Access and utilize the service within your application’s functions.
3. **Providing a Service Implementation**: Supply an actual implementation of the service to fulfill the declared requirements.

## 

Up to this point, our examples with the Effect framework have dealt with effects that operate independently of external services.
This means the `Requirements` parameter in our `Effect` type signature has been set to `never`, indicating no dependencies.

However, real-world applications often need effects that rely on specific services to function correctly. These services are managed and accessed through a construct known as `Context`.

The `Context` serves as a repository or container for all services an effect may require.
It acts like a store that maintains these services, allowing various parts of your application to access and use them as needed.

The services stored within the `Context` are directly reflected in the `Requirements` parameter of the `Effect` type.
Each service within the `Context` is identified by a unique “service key,” which is essentially a unique identifier for the service.

When an effect needs to use a specific service, its service key is included in the `Requirements` type parameter.

## 

To create a new service, you need two things:

1. A unique **identifier**.
2. A **type** describing the possible operations of the service.

**Example** (Defining a Random Number Generator Service)

Let’s create a service for generating random numbers.

1. **Identifier**. We’ll use the string `"MyRandomService"` as the unique identifier.
2. **Type**. The service type will have a single operation called `next` that returns a random number.

The exported `Random` value is known as a **service key** in Effect. It acts as a representation of the service and allows Effect to locate and use this service at runtime.

The service will be stored in a collection called `Context`, which can be thought of as a `Map` where the keys are service keys and the values are services:

Let’s summarize the concepts we’ve covered so far:

| Concept | Description | 
|---|---|
| **service** | A reusable component providing specific functionality, used across different parts of an application. | 
| **service key** | A unique identifier representing a **service**, allowing Effect to locate and use it. | 
| **context** | A collection of services, functioning like a map with **service keys** as keys and **services** as values. | 

## 

Now that we have our service key defined, let’s see how we can use it by building a simple program.

**Example** (Using the Random Service)

In the code above, we can observe that we are able to yield the `Random` service key as if it were an effect itself.
This allows us to access the `next` operation of the service.

In the code above, we can observe that we are able to flat-map over the `Random` service key as if it were an effect itself.
This allows us to access the `next` operation of the service within the `Effect.andThen` callback.

It’s worth noting that the type of the `program` variable includes `Random` in the `Requirements` type parameter:

This indicates that our program requires the `Random` service to be provided in order to execute successfully.

If we attempt to execute the effect without providing the necessary service we will encounter a type-checking error:

**Example** (Type Error Without Service Provision)

To resolve this error and successfully execute the program, we need to provide an actual implementation of the `Random` service.

In the next section, we will explore how to implement and provide the `Random` service to our program, enabling us to run it successfully.

## 

In order to provide an actual implementation of the `Random` service, we can utilize the `Effect.provideService` function.

**Example** (Providing a Random Number Implementation)

In the code above, we provide the `program` we defined earlier with an implementation of the `Random` service.

We use the `Effect.provideService` function to associate the `Random` service key with its implementation, an object with a `next` operation that generates a random number.

Notice that the `Requirements` type parameter of the `runnable` effect is now `never`. This indicates that the effect no longer requires any service to be provided.

With the implementation of the `Random` service in place, we are able to run the program without any further requirements.

## 

To retrieve the service type from a service key, use the `Context.Service.Shape` utility type.

**Example** (Extracting Service Type)

## 

When we require the usage of more than one service, the process remains similar to what we’ve learned in defining a service, repeated for each service needed.

**Example** (Using Random and Logger Services)

Let’s examine an example where we need two services, namely `Random` and `Logger`:

The `program` effect now has a `Requirements` type parameter of `Random | Logger`:

indicating that it requires both the `Random` and `Logger` services to be provided.

To execute the `program`, we need to provide implementations for both services:

**Example** (Providing Multiple Services)

Alternatively, instead of calling `provideService` multiple times, we can combine the service implementations into a single `Context` and then provide the entire context using the `Effect.provide` function:

**Example** (Combining Service Implementations)

## 

There are situations where we may want to access a service implementation only if it is available.
In such cases, we can use the `Effect.serviceOption` function to handle this scenario.

The `Effect.serviceOption` function returns an implementation that is available only if it is actually provided before executing this effect.
To represent this optionality it returns an [Option](/docs/v4/data-types/option/) of the implementation.

**Example** (Handling Optional Services)

To determine what action to take, we can use the `Option.isNone` function provided by the Option module. This function allows us to check if the service is available or not by returning `true` when the service is not available.

In the code above, we can observe that the `Requirements` type parameter of the `program` effect is `never`, even though we are working with a service. This allows us to access something from the context only if it is actually provided before executing this effect.

When we run the `program` effect without providing the `Random` service:

We see that the log message contains `-1`, which is the default value we provided when the service was not available.

However, if we provide the `Random` service implementation:

We can observe that the log message now contains a random number generated by the `next` operation of the `Random` service.

## 

Sometimes a service in your application may depend on other services. To maintain a clean architecture, it’s important to manage these dependencies without making them explicit in the service interface. Instead, you can use **layers** to handle these dependencies during the service construction phase.

**Example** (Defining a Logger Service with a Configuration Dependency)

Consider a scenario where multiple services depend on each other. In this case, the `Logger` service requires access to a configuration service (`Config`).

To handle these dependencies in a structured way and prevent them from leaking into the service interfaces, you can use the `Layer` abstraction. For more details on managing dependencies with layers, refer to the [Managing Layers](/docs/v4/requirements-management/layers/) page.
