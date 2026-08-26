# TodoMate web-frontend rules

> Applies to the TodoMate Vite and React 18 application.

## 1. Project structure

- Keep domain data and localStorage access under `src/data/`.
- Keep React rendering and interaction orchestration in components under `src/`.
- The data layer must not import React or browser presentation code.

## 2. React lifecycle and state

- Initialize Todo state through the F002 loading API instead of reading localStorage during render.
- Keep derived values, such as the completed count, derived from the current Todo array rather than storing duplicate state.
- Clean up any effect that registers a listener or owns another external resource.

## 3. Events and persistence

- Route every Todo mutation through one explicit handler before persisting the updated array.
- Do not mutate Todo objects or arrays in place.
- Keep the stable localStorage key `todomate:todos:v1`; changing it requires an explicit migration Feature.
- If localStorage is unavailable, preserve the documented in-memory fallback and warning.

## 4. Rendering and accessibility

- Use semantic form, list, button, label, and checkbox elements before adding ARIA attributes.
- Every checkbox must have an accessible name associated with its Todo text.
- Disabled controls must remain visibly and programmatically disabled.
- Use stable Todo IDs as React keys; never use the array index.

## 5. Styling

- Keep the Product-defined white, black, and blue-gray palette in shared CSS variables.
- Completed Todo text uses strikethrough and 50% opacity.
- Do not add animation, shadows, or a second accent color without a Product change.

## 6. Verification

- Cover data utilities with unit tests and user-observable component behavior with Testing Library tests.
- Run `npm run typecheck && npm test` before requesting human acceptance.
- Verify keyboard submission, empty input, the 200-character limit, completion toggling, clearing completed Todos, and persistence at the Feature that introduces each behavior.
