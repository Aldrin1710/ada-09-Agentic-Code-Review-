# AGENTS.md

## Read First
1. `TASK_UNDER_TEST.md` (when implementing a bounded change)
2. `docs/REPO_MAP.md` (fast navigation, entry points, and change guide)
3. `REQUIREMENTS.md`
4. `SPEC.md`
5. `ARCHITECTURE.md`
6. `TASKS.md`

## Sources of Truth
- Functional and non-functional requirements live only in `REQUIREMENTS.md`.
- Verifiable behavior, validation rules, and acceptance criteria live in `SPEC.md`.
- Requirement-to-test traceability lives in `docs/traceability.md`.
- Do not change `REQUIREMENTS.md` or `SPEC.md` merely to make tests pass.

## Repository Map
- `src/` — CLI (`cli.py`), domain search (`service.py`), model (`model.py`), JSON storage (`storage.py`)
- `tests/` — Automated `pytest` suite (`test_search.py`, `test_cli.py`, `test_storage.py`, `test_environment.py`)
- `data/` — Protected seed dataset (`data/customers.json` — read-only)
- `docs/` — `REPO_MAP.md` (navigation & change guide) and `traceability.md` (requirement-to-test matrix)
- `scripts/` — Deterministic verification (`verify_repo.sh`, `verify_repo.ps1`, `check_repo_contract.py`)
- `results/` — Agent execution and readiness audit reports

## Standard Commands
- **Install**: `pip install -r requirements.txt`
- **Run CLI**: `python src/cli.py "ale"`
- **Test (with coverage gate >= 90%)**: `pytest -v --cov=src --cov-fail-under=90 tests/`
- **Lint / Syntax & Static Check**: `python -m compileall -q src tests scripts`
- **Repo Contract & Guardrails**: `python scripts/check_repo_contract.py`
- **Verify (Single Verification Contract)**:
  - Unix / CI / Git Bash: `D:\Git\bin\bash.exe scripts/verify_repo.sh` (or `./scripts/verify_repo.sh`)
  - Windows PowerShell: `pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/verify_repo.ps1`

## Change Rules
- Keep changes strictly scoped to the requested task (`TASK_UNDER_TEST.md`).
- Whenever you add or rename a test function in `tests/test_search.py`, you **must** also add its function name to the corresponding row in `docs/traceability.md` (`scripts/check_repo_contract.py` enforces this deterministically).
- Do not weaken or delete existing tests.
- Do not introduce new runtime dependencies outside the Python standard library (`C-01`).
- Do not modify `data/customers.json`, `.env` files, or commit generated artifacts (`__pycache__/`, `*.pyc`, `.coverage`).

## Stop Conditions
Stop and ask for human input when:
- `REQUIREMENTS.md` and `SPEC.md` conflict on the requested behavior,
- a destructive action or modification of `data/customers.json` is required,
- an architecture boundary defined in `ARCHITECTURE.md` must change,
- a required external system or tool is unavailable.

## Definition of Done
A task is DONE only when all of the following hold:
1. Requested code changes and unit tests are implemented within scope.
2. `docs/traceability.md` lists all test functions in `tests/test_search.py`.
3. The unified verification script (`D:\Git\bin\bash.exe scripts/verify_repo.sh` or `pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/verify_repo.ps1`) completes with `REPO_CONTRACT: PASS` and `VERIFY_REPO: PASS`.
4. `git status -s` shows only the files intentionally modified for the task (no untracked or binary cache files).
