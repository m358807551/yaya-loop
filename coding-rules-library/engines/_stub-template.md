# {{ENGINE_NAME}} best practices

> **Incomplete stub:** This file has not been filled in. The AI and user should complete it during the first three Features.
> **Installation:** Bootstrap Stage 3 copies this file to `docs/coding-rules/engine-rules.md` and guides the user through the essential sections.
> **Supported version:** {{ENGINE_VERSION}}

## Required sections

Complete the sections in order. Remove a section's `TODO` marker when that section is filled. When no TODO markers remain, remove the incomplete-stub warning and treat the file as a project-tested rule source.

## 1. Core model and project structure

TODO: What is the engine or platform's primary organization model—scene tree, component/ECS, Actor, routing hierarchy, or something else? Does the project organize by feature or file type?

## 2. Lifecycle and frames

TODO: Which callbacks run each frame? Where is the boundary between fixed and variable timesteps? How do coroutine, `await`, or `async` behavior and pause semantics work?

## 3. Resource management

TODO: How are resources loaded, instantiated, and referenced? Can they hot-reload? When should the engine's native data system, such as Unity ScriptableObject or Godot Resource, be preferred?

## 4. Events and messaging

TODO: What is the preferred event mechanism—signals, events, observables, or pub-sub? What should cross-scene communication use—an event bus, service locator, or another mechanism?

## 5. Editor integration

TODO: How are fields exposed in the editor, such as `@export` or `[SerializeField]`? What is the prefab or blueprint workflow? When should the project add gizmos or custom inspectors?

## 6. Performance traps

TODO: What engine-specific hotspots matter, such as per-frame string allocation, `GetComponent`, or node lookup? When is object pooling justified?

## 7. Debugging tools

TODO: How should the built-in profiler and monitors be used? What signals a leak, such as rising Orphan Nodes? How reliable is hot reload?

## 8. Anti-pattern checklist

TODO: Record the engine community's strongest avoid-at-all-costs patterns.

## 9. References

- [TODO: official documentation]
- [TODO: community best-practices guide]
- [TODO: recognized sample project]
