---
type: "always_apply"
---

04-security

Purpose
Minimise vulnerabilities and ensure compliance with OWASP Top 10 for Python.

Rules
	1.	Dependency scanning – Run Safety and pip‑audit weekly in CI; fail on high severity CVEs.
	2.	Static analysis – Enable Ruff‑bandit and bandit rules; zero high/medium findings.
	3.	Secrets – Enforce GitGuardian scan on every push; block committed secrets.
	4.	Least privilege – Store credentials in env vars or HashiCorp Vault; never in code.
	5.	Sandboxing – For dynamic eval/exec, use ast.literal_eval or a restricted execution environment.
	6.	HTTPS everywhere – Use requests with verify=True; pin certs where possible.
	7.	Deserialization safety – Disallow pickle for untrusted input; prefer json or orjson.
	8.	Runtime hardening – Use python -X frozen_modules=on -X warn_default_encoding in production.
