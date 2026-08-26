# C# best practices

> **Incomplete stub:** Collaboratively complete each section with the AI before treating this as a field-tested rules source.
> Applies to: C# 12 / .NET 8 and later

## 1. Static typing and nullable references

TODO: Enable nullable reference types; define the boundaries for `?` and `!`; explain when to use `required`.

## 2. Naming conventions

TODO: Define the boundaries between PascalCase and camelCase; the `I` prefix for interfaces; the `Async` suffix for asynchronous methods; and `_camelCase` for private fields.

## 3. Member order

TODO: Define the order of using directives, namespace declarations, classes, fields, constructors, properties, and methods, based on Microsoft's official guidance.

## 4. Control flow and exceptions

TODO: Define exceptions versus a `Result<T, E>` pattern; guard clauses versus a single exit; and the use of `using`, using declarations, and `IAsyncDisposable`.

## 5. Collections and LINQ

TODO: Define when to expose `IEnumerable`, `IReadOnlyList`, `IList`, or `List`; set performance boundaries for LINQ, especially lazy chains on hot paths; and choose between `ToList` and `ToArray`.

## 6. Asynchronous work and concurrency

TODO: Require async/await through the full call chain; define where `ConfigureAwait(false)` belongs; propagate `CancellationToken`; and restrict `ValueTask` to justified cases.

## 7. Memory and performance

TODO: Define `struct` versus `class`; appropriate uses of `Span<T>`, `Memory<T>`, and `ArrayPool`; and string construction with interpolation or `StringBuilder`.

## 8. Documentation and XML comments

TODO: Require `///` for public APIs and define minimum expectations for `<summary>`, `<param>`, and `<returns>`.

## 9. Linting and formatting

TODO: Choose a baseline using `dotnet format`, EditorConfig, and Roslyn analyzers, and document the tradeoffs of StyleCop and SonarLint.

## 10. Anti-pattern checklist

TODO: Cover `async void`, broad `catch (Exception)`, structs larger than 16 bytes, mutable structs, and missing Dispose patterns.

## 11. Community references

- [Microsoft C# coding conventions](https://learn.microsoft.com/dotnet/csharp/fundamentals/coding-style/coding-conventions)
- [C# language design](https://github.com/dotnet/csharplang)
- [.NET Framework design guidelines](https://learn.microsoft.com/dotnet/standard/design-guidelines/)
