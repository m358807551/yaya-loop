# TodoMate TypeScript rules

> Applies to TypeScript 5.x with strict mode enabled.

## 1. Types

- Keep `strict` enabled and do not suppress strict-family errors.
- Model Todo state with the shared `Todo` type; do not duplicate its shape in components or tests.
- Use `unknown` for untrusted parsed JSON and narrow it before treating it as `Todo[]`.
- Do not introduce `any` or unchecked type assertions to bypass validation.

## 2. Naming and modules

- Use PascalCase for types and React components, camelCase for variables and functions, and UPPER_SNAKE_CASE for true constants.
- Prefer named exports for reusable data utilities.
- Keep modules focused and avoid barrel files while the project is this small.

## 3. Control flow and errors

- Prefer guard clauses for empty input, corrupt storage, and unavailable browser APIs.
- Catch only errors that can be handled with the documented fallback or an actionable message.
- Never leave an empty `catch` block.

## 4. Collections and immutability

- Use non-mutating array operations for add, toggle, and remove behavior.
- Use `map` for one-to-one transformations and `filter` for removal; avoid a dense `reduce` when simpler operations communicate intent.
- Preserve incomplete Todo ordering when completed entries are removed.

## 5. Asynchronous code

- Do not make synchronous localStorage helpers asynchronous.
- Await every Promise or deliberately return it to the caller; no floating Promises.
- Add cancellation before introducing asynchronous work that can outlive a component.

## 6. Verification

- Keep tests fully typed under the same strict configuration as application code.
- Test public behavior instead of private implementation details.
- Run the configured type check and test command after every implementation change.
