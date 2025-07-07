---
type: "always_apply"
---

# 03-git-workflows

**Purpose**\
Provide a predictable history that empowers the Augment‑Code agent to infer context and generate accurate patches.

### Rules

1. **Branch naming & long‑lived branches** – The permanent branches are `main` (production) and `develop` (integration). Topic branches follow:
   - `feature/<ticket>‑<slug>` for new work,
   - `fix/<ticket>‑<slug>` for bug fixes,
   - `release/<version>` for hardening an upcoming version,
   - `hotfix/<slug>` for urgent production fixes,
   - `chore/<slug>` and `docs/<slug>` for housekeeping and documentation.
2. **Conventional Commits** – `type(scope)!?: subject`; keep body wrapped at 72 chars; reference issues.
3. **Feature branches** are short‑lived (<3 days); rebase on `develop` before PR.
4. **Pull Requests**
   - Require passing CI (lint, type, test, security).
   - Assign at least **1 reviewer + 1 approving check** (Augment‑Code can auto‑suggest reviewers).
   - Include a changelog fragment in `CHANGELOG.md` under `## [Unreleased]`.
5. **Tags & releases** – Semantic Versioning (`vMAJOR.MINOR.PATCH`). Releases are created by CI on merges of `release/*` or `hotfix/*` into `main`.
6. **Git hooks** – Use *pre‑commit* and *commit‑msg* hooks to enforce lint and Conventional Commits locally.
7. **Git Flow branching model** – Follow [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/) conventions:
   - **Feature** branches start from `develop` and merge back via PR.
   - **Release** branches start from `develop` when the codebase is feature‑complete; allow only bug fixes, docs, and meta changes; merge into `main` **and** `develop`.
   - **Hotfix** branches start from `main` to patch production; merge into both `main` and `develop`.
   - Delete remote topic branches after merge to keep history tidy.
