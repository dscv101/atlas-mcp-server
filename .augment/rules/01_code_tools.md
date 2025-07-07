---
type: "always_apply"
---

# 01-code-tools

**Purpose**\
Define the standard toolchain and automation hooks that the Augment‑Code agent relies on when generating or modifying Python 3.13 projects.

### Rules

1. **Formatter** – Use **Black** (`black --preview --line-length 100`) as the single‑source‑of‑truth formatter. Never hand‑edit style that Black can format.
2. **Linter & Import sorter** – Run **Ruff** (`ruff check` + `ruff format`) on every save; fail CI on any `E`, `F`, or `I` codes.
3. **Static typing** – Use **Pyright** (`pyright --pythonversion 3.13 --strict`) with the `strict` preset; zero type errors in CI. Optionally run **mypy** in `--strict` mode for cross‑validation.
4. **Pre‑commit** – Install a *pre‑commit* config that runs Black, Ruff, Pyright, Commitlint, and Reuse on staged files.
5. **Task runner** – Use **Hatch** tasks (`hatch run <task>`) for linting, test, docs, and release.
6. **Packaging & Environment** – Manage dependencies and virtual environments with **uv**:
   - Create isolated envs via `uv venv .venv`.
   - Add/upgrade packages with `uv pip install --no-index <pkg>`; always commit the generated **`uv.lock`** file for reproducible builds.
   - Sync CI/CD and production with `uv pip sync`.
   - Keep project metadata in `pyproject.toml` (PEP 621) and build wheels with **hatchling**.
7. **Doc generation** – Generate developer docs with **MkDocs‑Material**; auto‑publish on every **main** or **develop** branch push.
8. **IDE integration** – The VSCode Augment‑Code extension should surface tool diagnostics inline and on pull requests.
