# Traceability Matrix

| Requirement | SPEC / AC | Task | Files | Test Functions | Status |
| :--- | :--- | :--- | :--- | :--- | :--- |
| FR-01 | AC-01, VR-01, VR-02 (TS-01, TS-04, TS-05) | T-04 | `src/cli.py` | `test_cli_empty_term`, `test_cli_short_term`, `test_cli_non_alphanumeric` | Completed |
| FR-02 | AC-02 (TS-02) | T-03 | `src/service.py` | `test_search_unallowed_fields` | Completed |
| FR-03, FR-04 | AC-03 (TS-03) | T-03 | `src/service.py` | `test_search_case_insensitive` | Completed |
| FR-05 | AC-04 (TS-03, TS-04) | T-03 | `src/service.py` | `test_search_exact_and_partial_order`, `test_search_exact_match_last_name`, `test_search_deterministic_tie_breaking_by_id` | Completed |
| FR-06 | AC-05, EH-01 (TS-06) | T-04 | `src/cli.py`, `src/service.py` | `test_cli_no_match`, `test_search_no_results` | Completed |
| NFR-02 | EH-02 (TS-07) | T-02 | `src/storage.py` | `test_load_customers_file_not_found`, `test_load_customers_invalid_json`, `test_load_customers_invalid_data_types` | Completed |
| NFR-01 | Performance (<= 150ms) | T-03 | `src/service.py` | In-memory linear scan architecture | Completed |
| NFR-03 | Quality (>= 90% coverage & static check) | T-05, T-06 | `src/`, `tests/` | Verified via `pytest --cov=src --cov-fail-under=90` and `scripts/check_repo_contract.py` | Completed |
