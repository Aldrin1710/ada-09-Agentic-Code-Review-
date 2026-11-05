# Repository Map

## Entry Points
- `src/cli.py` — CLI bootstrap and argument validation (`main()`). Run via `python src/cli.py "<term>"`.
- `src/service.py` — Domain search and sorting logic (`search_customers(term: str) -> list[Customer]`).
- `src/storage.py` — JSON file loading and schema/type validation (`load_customers(file_path: str) -> list[Customer]`).
- `src/model.py` — `Customer` dataclass (`id: int`, `name: str`, `last_name: str`, `email: str`).

## Tests
- `tests/test_search.py` — Unit tests for `src/service.py` (`search_customers`), mocking `src.service.load_customers`.
- `tests/test_cli.py` — End-to-end CLI argument and validation tests for `src/cli.py`.
- `tests/test_storage.py` — JSON persistence and schema error tests for `src/storage.py`.
- `tests/test_environment.py` — Test environment smoke check.

## Change Guide
### If changing search, matching, or ordering behavior (`FR-02`..`FR-05`, `AC-02`..`AC-04`):
1. Check `TASK_UNDER_TEST.md`, `REQUIREMENTS.md`, and `SPEC.md` (`Search Rules`).
2. Update `search_customers` in `src/service.py` (do **not** need to inspect or edit `src/storage.py` or `src/cli.py` unless CLI validation/I/O is part of the task).
3. Add or update unit tests in `tests/test_search.py` using `@patch('src.service.load_customers')`.
4. Register any new test function names from `tests/test_search.py` in `docs/traceability.md` under the corresponding requirement row (`FR-05` / `AC-04`, etc.).
5. Run the unified verification command:
   - `D:\Git\bin\bash.exe scripts/verify_repo.sh` (or `pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/verify_repo.ps1`).

### If changing CLI validation or output formatting (`FR-01`, `FR-06`, `VR-01`, `VR-02`, `EH-01`):
1. Check `REQUIREMENTS.md` and `SPEC.md`.
2. Update `src/cli.py` and `tests/test_cli.py`.
3. Update `docs/traceability.md` and run `scripts/verify_repo.sh`.

### If changing JSON schema validation (`NFR-02`, `EH-02`):
1. Check `REQUIREMENTS.md` and `SPEC.md`.
2. Update `src/storage.py` and `tests/test_storage.py`.
3. Update `docs/traceability.md` and run `scripts/verify_repo.sh`.

## Do Not Edit Directly
- `data/customers.json` — Canonical seed dataset protected by `scripts/check_repo_contract.py` (use mocks or temp files in tests).
- `.env` / secrets — Never commit credentials or environment files.
- `__pycache__/` and `.coverage` — Generated artifacts blocked by `.gitignore` and `scripts/check_repo_contract.py`.
- `REQUIREMENTS.md` and `SPEC.md` — Normative sources of truth; do not alter them during feature implementation tasks.
