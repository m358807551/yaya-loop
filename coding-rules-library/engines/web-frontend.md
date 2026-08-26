# Web frontend best practices

> **Incomplete stub:** Complete each TODO section with the AI before treating this as project-tested guidance.
> **Applies to:** React 18+, Vue 3, and Svelte 4+. Add framework-specific sections when needed.

## 1. Core model and project structure

TODO: Choose feature-first or type-first component organization and define the boundaries among pages, components, hooks, and stores.

## 2. Rendering lifecycle

TODO: Cover mount, update, and unmount hooks such as `useEffect`, `onMounted`, and `onMount`; clean up side effects; and define when memoization is justified.

## 3. State management

TODO: Define selection criteria for local state, context, and global stores such as Zustand, Pinia, and Svelte stores. Isolate server state through TanStack Query or SWR.

## 4. Events and cross-component communication

TODO: Define props-down/events-up communication, when an event bus or pub-sub is justified, and why excessive `forwardRef` plus `useImperativeHandle` should be avoided.

## 5. Styling conventions

TODO: Choose among CSS Modules, Tailwind, styled-components, and vanilla-extract, and define where design tokens live.

## 6. Performance traps

TODO: Cover unnecessary rerenders, incorrect `useEffect` dependencies, unstable list keys, and image and font loading strategies.

## 7. Accessibility and SEO

TODO: Define semantic HTML, appropriate ARIA usage, and how SSR, SSG, or ISR choices affect SEO.

## 8. Testing

TODO: Define the boundary among unit tests with Vitest or Jest, component tests with Testing Library, and E2E tests with Playwright or Cypress.

## 9. Anti-pattern checklist

TODO: Pervasive `any`, uncancelled fetches inside `useEffect`, props drilling beyond three levels, and global CSS pollution.

## 10. References

- [React documentation](https://react.dev)
- [Vue style guide](https://vuejs.org/style-guide/)
- [Svelte tutorial](https://svelte.dev/tutorial)
