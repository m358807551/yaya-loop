# Rust best practices

> **Incomplete stub:** Collaboratively complete each section with the AI before treating this as a field-tested rules source.
> Applies to: Rust 1.75 and later (Edition 2021)

## 1. Type system and ownership

TODO: Establish a practical model for ownership, borrowing, and lifetimes; identify when `Clone` is a design smell; define the boundary for `Copy`; prefer `From` and `TryFrom` over unjustified `as` casts.

## 2. Naming conventions

TODO: Define snake_case for functions and variables, PascalCase for types and traits, SCREAMING_SNAKE_CASE for constants, getters without a `get_` prefix, and constructors named `new`, `with_xxx`, or `try_new`.

## 3. Project organization

TODO: Define how crates, modules, and files correspond; choose between `mod.rs` and same-named module files; identify when to use a workspace; set a minimum bar for feature flags.

## 4. Error handling

TODO: Propagate `Result<T, E>` through the call chain and use `?`; define application and library error types; choose between thiserror and anyhow; restrict panic to documented invariant failures.

## 5. Collections and iteration

TODO: Choose among `Vec`, `VecDeque`, `HashMap`, and `BTreeMap`; set readability boundaries for Iterator chains; document patterns such as `collect::<Result<_, _>>()`.

## 6. Asynchronous work and concurrency

TODO: Choose among Tokio, async-std, and smol; document `Send + Sync` constraints; select among mpsc, oneshot, and broadcast channels; define ownership and shutdown for spawned tasks.

## 7. Performance and memory

TODO: Choose among `Box`, `Rc`, and `Arc`; define appropriate uses of `Cow<'_, T>` and zero-copy `&str` or `&[u8]`; require evidence before adding `#[inline]`.

## 8. Unsafe boundaries

TODO: Define legitimate reasons for unsafe code, minimize each unsafe block, and document common undefined-behavior hazards such as aliasing, lifetime extension, and uninitialized memory.

## 9. Documentation and tests

TODO: Define `///` documentation and doctests, `#[cfg(test)]` modules, integration-test directory conventions, and cargo doc style.

## 10. Linting and formatting

TODO: Define rustfmt configuration and the default and recommended Clippy lints; require CI to run `cargo fmt --check` and `cargo clippy -- -D warnings`.

## 11. Anti-pattern checklist

TODO: Cover pervasive `unwrap`, unnecessary `Clone` and `mut`, over-generalized types and `where` clauses, `Arc<Mutex<_>>` used instead of borrowing, and ignored lifetime warnings.

## 12. Community references

- [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)
- [Rust by Example](https://doc.rust-lang.org/rust-by-example/)
- [The Rustonomicon](https://doc.rust-lang.org/nomicon/)
