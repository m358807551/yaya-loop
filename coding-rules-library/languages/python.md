# Python best practices

> **Incomplete stub:** Collaboratively complete each section with the AI before treating this as a field-tested rules source.
> Applies to: Python 3.11 and later

## 1. Static typing and type hints

TODO: Require type hints for every public API; decide whether to use `from __future__ import annotations`; define when to use `TypeVar`, `ParamSpec`, and `Self`.

## 2. Naming conventions

TODO: Define snake_case for functions and variables, PascalCase for classes, CONSTANT_CASE for constants, lowercase module names, `_` for non-public names, and the narrow boundary for `__` name mangling.

## 3. Module organization

TODO: Define the role of `__init__.py` and re-exports; choose between relative and absolute imports; explain regular packages versus namespace packages.

## 4. Control flow and exceptions

TODO: Define the preference for guard clauses; the boundary between EAFP and LBYL; a custom exception hierarchy; `finally` versus context managers; and appropriate use of the `else` clause on `try`.

## 5. Collections and iteration

TODO: Choose among list, tuple, set, and dict; define when a comprehension remains readable and when to expand it into a loop; explain the memory benefit of generators; prohibit unsafe mutation during iteration.

## 6. Asynchronous work and concurrency

TODO: Define the boundaries among asyncio, threading, and multiprocessing; cover `async with` and `async for`; preserve task cancellation through `CancelledError`; account for the GIL when selecting concurrency.

## 7. Data classes and immutability

TODO: Choose among `dataclass`, `pydantic.BaseModel`, and `attrs`; define when to use `frozen=True`; justify uses of `__slots__`.

## 8. Documentation and typing tools

TODO: Select one docstring style from Google, NumPy, or reStructuredText and define a baseline for mypy or pyright and Ruff.

## 9. Linting and formatting

TODO: Prefer Ruff or define a justified flake8, isort, and Black stack; record enabled rule sets and CI integration.

## 10. Anti-pattern checklist

TODO: Cover mutable defaults such as `def f(x=[])`, wildcard imports, bare `except`, list mutation during iteration, dictionaries used as enums, and business logic in `__init__.py`.

## 11. Community references

- [PEP 8](https://peps.python.org/pep-0008/)
- [PEP 484: Type Hints](https://peps.python.org/pep-0484/)
- [Ruff documentation](https://docs.astral.sh/ruff/)
