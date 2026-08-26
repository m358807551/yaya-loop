# Backend service best practices

> **Incomplete stub:** Complete each TODO section with the AI before treating this as project-tested guidance.
> **Applies to:** REST, GraphQL, and RPC services implemented in any language.

## 1. Core model and project structure

TODO: Choose between business-domain organization, such as DDD-style modules, and technical layers such as controller, service, and repository. Define route-file boundaries.

## 2. Request lifecycle

TODO: Define middleware order, propagation of request-scoped context such as trace ID and user ID, and end-to-end timeout and cancellation behavior.

## 3. Persistence

TODO: Decide when to use an ORM or native SQL, where transactions begin and end, how connection pools are configured, and how migration tools and history are managed.

## 4. Error handling and logging

TODO: Classify client and server errors, define HTTP status semantics, use structured JSON logs, and connect traces, metrics, and logs.

## 5. Authentication and authorization

TODO: Choose among sessions, JWT, and OAuth. Define route-, resource-, or field-level authorization and CSRF/XSS defenses.

## 6. Performance and observability

TODO: Detect N+1 queries, define local/Redis/CDN cache layers, select APM tooling, and configure slow-query logs.

## 7. Concurrency and rate limiting

TODO: Select token-bucket, leaky-bucket, or sliding-window rate limiting; define idempotency behavior and the boundaries of distributed locks.

## 8. Testing

TODO: Define unit versus integration test boundaries, contract tests, and per-test data isolation through schemas or transaction rollback.

## 9. Anti-pattern checklist

TODO: Business logic in controllers, accidental cascade deletion through ORM relationships, N+1 queries, and error messages that leak internal details.

## 10. References

- [The Twelve-Factor App](https://12factor.net/)
- [Microsoft REST API Guidelines](https://github.com/microsoft/api-guidelines)
- [Google API Design Guide](https://cloud.google.com/apis/design)
