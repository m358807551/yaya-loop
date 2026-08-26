# {{LANGUAGE_NAME}} best practices

> **Incomplete stub:** Collaboratively complete this document with the AI during the first three Features.
> Installation: During BOOTSTRAP STEP 3, the AI copies this file to `docs/coding-rules/language-rules.md` and asks the user to complete the key sections.
> Applies to: {{LANGUAGE_VERSION}}

## Required sections

Complete the sections in order. Remove a section's `TODO` marker when that section is complete. This document becomes a field-tested rules source only after every TODO has been resolved.

---

## 1. Static typing and type checking

TODO: Document the strength of this language's type system (static, gradual, or dynamic), whether strict mode must be enabled, and how generics should be used.

## 2. Naming conventions

TODO: Define casing for variables, functions, classes, constants, modules, and filenames, including conventions for Boolean values and function names.

## 3. Member order and code organization

TODO: Define the standard order within a module, such as imports, constants, types, functions, and the main entry point. Distinguish official guidance from community convention.

## 4. Control flow and error handling

TODO: Define the error-handling model (exceptions, Result, or null), resource cleanup (finally, defer, context manager, or Drop), and the preference between guard clauses and a single exit.

## 5. Collections and iteration

TODO: Document the standard collection types and their performance characteristics, mutation hazards during iteration, and the readability and performance boundaries for functional APIs such as map, filter, and reduce.

## 6. Concurrency and asynchronous work

TODO: Document the asynchronous model (async/await, goroutines, actors, or event loop), common deadlock and race hazards, and cancellation semantics.

## 7. Memory and lifetimes

TODO: Explain garbage collection, manual management, or ownership; reference versus copy semantics; and common leak patterns.

## 8. Documentation conventions

TODO: Define comment and documentation syntax, which APIs require documentation, and tool-recognized forms such as `///`, `"""`, `##`, JSDoc, or rustdoc.

## 9. Standard linting and formatting tools

TODO: Identify the project's linter and formatter and the essential rule sets to enable.

## 10. Anti-pattern checklist

TODO: List common language-specific traps, such as mutable Python defaults, JavaScript `this` binding, or incorrect Rust lifetime alignment.

## 11. Community references

- [TODO: official documentation]
- [TODO: style guide, such as PEP 8, Microsoft C# conventions, or the Rust API Guidelines]
- [TODO: a respected reference project]
