---
type: "always_apply"
---

05-testing

Purpose
Guarantee reliability and facilitate safe refactors assisted by the coding agent.

Rules
	1.	Framework – Use pytest 9.x with --strict-config --strict-markers.
	2.	Structure – Mirror package layout under tests/; name files test_*.py.
	3.	Coverage – Achieve ≥ 90 % statement + branch coverage; enforced in CI via pytest‑cov.
	4.	Property‑based – Use hypothesis for critical logic; target edge cases.
	5.	Mocks – Prefer pytest-mock; avoid over‑mocking – favour real behaviour or fakes.
	6.	Filesystem – Use pyfakefs for file IO tests.
	7.	DB/API – Spin up containers via testcontainers‑python; no live prod services.
	8.	Performance – Mark long tests with @pytest.mark.slow; run on nightly CI.
	9.	Reproducers – Capture failing seeds from Hypothesis in hypothesis.json.
	10.	Test data – Keep small fixtures in tests/fixtures; large (>100 KB) in remote storage.
