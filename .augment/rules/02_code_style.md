---
type: "always_apply"
---

02-code-style

Purpose
Ensure a consistent, modern Python 3.13 codebase that leverages new language features while remaining readable.

Rules
	1.	PEP 8 baseline + line length 100; let Black enforce.
	2.	Docstrings – Follow PEP 257; functions/classes/modules must include purpose, args, returns, raises, and examples.
	3.	Typing – Use PEP 695 type parameter syntax and typing.TypeAlias for readability; prefer collections.abc over builtin generics.
	4.	Pattern matching – Prefer match/case for simple value dispatch; limit to ≤5 cases or refactor to polymorphism.
	5.	f‑strings everywhere – Use formatted and debug (f'{x=}') f‑strings instead of % or format.
	6.	Avoid mutable defaults, shadowed names, and bare excepts.
	7.	Logging – Use the stdlib logging module with [structlog] adapters; never print in library code.
	8.	Return early to reduce indentation; guard clauses are preferred.
	9.	Functional helpers – Use comprehensions/generator expressions before map/filter; be explicit with lambdas.
	10.	Data classes – Use @dataclasses.dataclass(slots=True, frozen=True) for simple data containers.
	11.	File size – Source files must not exceed 1000 logical lines of code (excluding comments and blank lines); split oversized modules into packages.
