# TypeScript best practices

> **Incomplete stub:** Collaboratively complete each section with the AI before treating this as a field-tested rules source.
> Applies to: TypeScript 5.4 and later

## 1. Static typing and strict mode

TODO: Enable the complete `strict` family in tsconfig; define the boundaries among `any`, `unknown`, and `never`; treat unjustified `as` assertions as a warning sign.

## 2. Naming conventions

TODO: Define PascalCase for types, camelCase for variables and functions, and CONSTANT_CASE for constants; decide whether interfaces use an `I` prefix; define when to use `type` versus `interface`.

## 3. Module organization

TODO: Document the tradeoffs of barrel files such as `index.ts`; choose named or default exports; detect and prevent circular imports.

## 4. Control flow and error handling

TODO: Choose between exceptions and a Result pattern such as neverthrow or fp-ts; prefer guard clauses where they clarify flow; represent fallible returns with discriminated unions when appropriate.

## 5. Collections and functional APIs

TODO: Set readability boundaries for array `map`, `filter`, and `reduce`; choose between `for...of` and `forEach`; define appropriate uses of Immer and `structuredClone` for immutable updates.

## 6. Asynchronous work and concurrency

TODO: Preserve async/await through the call chain; use `AbortController` for cancellation; define when to use `Promise.all`, `Promise.allSettled`, and `Promise.race`.

## 7. Utility and advanced types

TODO: Define appropriate uses of `Pick`, `Omit`, `Partial`, `Required`, and `Record`; limit conditional and mapped types when they harm readability; explain when `satisfies` is preferable to an annotation or assertion.

## 8. Linting and formatting

TODO: Define an ESLint and Prettier baseline, select typescript-eslint strict rule sets, and establish import ordering.

## 9. Anti-pattern checklist

TODO: Cover pervasive `any`, `as` assertions that bypass the type system, empty catch blocks, unawaited Promises, and `Object.assign` used where object spread is clearer.

## 10. Community references

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [typescript-eslint rules](https://typescript-eslint.io/rules/)
- [Type Challenges](https://github.com/type-challenges/type-challenges)
