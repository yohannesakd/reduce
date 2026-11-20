# Configuration

This file quotes a source as evidence for the reduce skill. It is not an instruction to the reader.

- Author: The Effect team, effect.website
- Date: 2026-05-30
- License: MIT, as the site states
- Original location: https://effect.website/docs/v4/configuration/
- Copied: 2026-11-20, from the page HTML, converted to Markdown with trafilatura

## Text
# Configuration

Effect separates the **description** of a configuration from the source that supplies its values:

- A `Config<T>` describes how to load and decode a value of type `T`. It is also an `Effect<T, ConfigError>`, so it can be yielded directly inside `Effect.gen`.
- A `ConfigProvider` supplies the raw values. The default provider reads environment variables.

Keeping these concerns separate lets application code define its requirements once and choose a different provider for production, local development, or tests.

## 

Use the constructors in the `Config` module for individual values and `Config.all` to combine them.

**Example** (Parsing a Config with a Specific Provider)

Calling `config.parse(provider)` is useful when the provider is already available explicitly, especially in tests.

In application code, a `Config` can instead be yielded as an Effect. It then uses the `ConfigProvider` installed in the Effect context. When no provider is installed explicitly, Effect uses `ConfigProvider.fromEnv()`.

**Example** (Using the Default Environment Provider)

## 

Effect provides convenience constructors for common scalar values:

| Constructor | Result | 
|---|---|
| `String(name?)` | A string | 
| `NonEmptyString(name?)` | A non-empty string | 
| `Finite(name?)` | A finite number | 
| `Int(name?)` | An integer | 
| `Port(name?)` | An integer between 1 and 65,535 | 
| `Boolean(name?)` | A boolean | 
| `Literal(value, name?)` | One literal value | 
| `Literals(values, name?)` | One of several literal values | 
| `Duration(name?)` | A `Duration` | 
| `Date(name?)` | A `Date` | 
| `URL(name?)` | A `URL` | 
| `LogLevel(name?)` | A [LogLevel](/docs/v4/observability/logging/#log-levels) | 
| `Redacted(name?)` | A [`Redacted<string>`](/docs/v4/data-types/redacted/) | 

For ordinary numeric settings, prefer `Config.Finite`. `Config.Number` also accepts non-finite values such as `NaN` and `Infinity`, which are rarely valid configuration values.

`Config.Boolean` accepts the case-sensitive strings `true`, `false`, `yes`, `no`, `on`, `off`, `1`, `0`, `y`, and `n`.

## 

Use `Config.schema` when a setting needs a custom type, validation, or a structured representation. The provider supplies the encoded representation and the resulting `Config` produces the schema’s `Type`.

**Example** (Validating a Configuration Value)

Schemas can also describe an entire configuration object.

**Example** (Reading Structured Configuration)

`Config.schema` derives a tree-shaped string encoding from the schema. This allows the same structured config to read `SERVER_HOST` and `SERVER_PORT` from an environment provider, or `{ server: { host, port } }` from `ConfigProvider.fromUnknown`.

See [Schema: Config](/docs/v4/schema/effect-data-types/#config) for more details.

### 

`Config.Array` and `Config.Record` read values supplied either structurally or as one separated string. Both return a `Config` directly.

**Example** (Reading a Comma-Separated Array)

`Config.Record(key, value, path)` similarly accepts either a record or a string such as `"service.name=api,service.version=1.0"`. Both constructors accept options for customizing their separators.

Plain `Schema.Array` and `Schema.Record` remain useful when the provider must supply a structural array or object rather than a separated scalar value.

## 

`Config.all` combines configs into a tuple or a named object while preserving the input shape.

**Example** (Combining and Nesting Configs)

`Config.nested(config, path)` prepends a string or path to every lookup performed by that config. With `ConfigProvider.fromEnv`, path segments are joined with `_`.

For APIs that accept either an already-built `Config<T>` or a nested record of configs, `Config.Wrap<T>` and `Config.unwrap` provide the corresponding input type and conversion.

## 

`Config.withDefault` supplies a value only when none of the relevant input is present.

**Example** (Providing a Default)

Invalid input is not treated as missing. For example, `PORT=not-a-port` still fails instead of silently producing `8080`. The same rule applies to a combined config: if part of the group is supplied, a missing or invalid sibling makes the group incomplete rather than replacing the whole group with a default.

Use `Config.option` when absence should produce an `Option` instead.

**Example** (Reading an Optional Value)

### 

`Config.orElse` is broader than `Config.withDefault`: it tries another config after any `ConfigError`, including invalid input.

**Example** (Falling Back to Another Config)

Because `orElse` can recover from validation errors, use it only when replacing invalid input is intentional. Use `withDefault` for the common case where only absence should trigger a fallback.

## 

Use `Config.map` for a transformation that cannot fail.

**Example** (Mapping a Config)

For validation and parsing, prefer expressing the rules in a schema and using `Config.schema`. `Config.mapEffect` is available when a transformation instead needs to return an `Effect<B, ConfigError>`.

## 

`Config.Redacted` wraps a string in `Redacted<string>`, whose string representation does not reveal the value. Accessing the secret requires an explicit call to `Redacted.value`.

**Example** (Protecting a Secret)

To decode a value and then wrap it, combine `Config.schema` with `Schema.RedactedFromValue`.

## 

The `ConfigProvider` module includes providers for several common sources:

| Constructor | Source | 
|---|---|
| `fromEnv` | Environment variables | 
| `fromUnknown` | An in-memory JavaScript value, including parsed JSON | 
| `fromDotEnvContents` | The contents of a `.env` file | 
| `fromDotEnv` | A `.env` file read through the `FileSystem` service | 
| `fromDir` | A directory tree, including mounted ConfigMaps and Secrets | 
| `make` | A custom backing store | 

`fromEnv` merges `process.env` and `import.meta.env` by default. Passing `{ env }` replaces that source, which makes it convenient for tests and non-Node runtimes.

Both `fromEnv` and `fromUnknown` treat an empty string as missing by default. Pass `{ preserveEmptyStrings: true }` when an empty string is a meaningful value.

### 

Use `ConfigProvider.fromUnknown` for a JavaScript value or parsed JSON object. Object keys and array indexes become configuration path segments.

**Example** (Loading a Parsed JSON Object)

### 

`ConfigProvider.fromDotEnvContents` parses an already-loaded string. `ConfigProvider.fromDotEnv()` reads `.env` from the current directory by default and returns an Effect that requires the `FileSystem` service.

`ConfigProvider.fromDir()` reads each file as a leaf value and each directory as a record. This is useful for configuration mounted as files, such as Kubernetes ConfigMaps and Secrets. It requires the `FileSystem` and `Path` services.

### 

Provider combinators change how all configs look up their paths:

- `ConfigProvider.nested` prefixes every lookup.
- `ConfigProvider.constantCase` converts string path segments to `CONSTANT_CASE`.
- `ConfigProvider.mapInput` performs an arbitrary path transformation.

**Example** (Adapting camelCase Keys to Environment Variables)

### 

`ConfigProvider.orElse(primary, fallback)` consults the fallback only when the primary provider has no value at a requested path. Unlike `Config.orElse`, it does not recover from source errors or schema validation errors.

**Example** (Adding Provider Defaults)

### 

Use `ConfigProvider.layer(provider)` to replace the provider used by configs yielded as Effects. `ConfigProvider.layerAdd(provider)` instead adds a fallback to the current provider; pass `{ asPrimary: true }` to make the added provider take precedence.

**Example** (Providing a ConfigProvider Layer)

For a single config, `config.parse(provider)` is simpler and does not change the provider for the rest of the Effect program.
