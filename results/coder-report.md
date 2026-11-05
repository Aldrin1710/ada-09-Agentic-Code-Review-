# Coder Agent Report

## Change
Change ID: CR-03
Branch: ada09/cr-email-domain-filter
Base commit: 801ec04

## Requirements Covered
- FR-02
- FR-03
- FR-04
- FR-05
- FR-07
- AC-07

## Implementation Plan
1. **Service Layer (`src/service.py`)**:
   - Update `search_customers(term: str, domain: str | None = None) -> list[Customer]` with an optional `domain` parameter.
   - Implement `_extract_domain` helper to normalize domain extraction (`email.rsplit('@', 1)[1].strip().lower()` if `@` in email).
   - Normalize target domain (`domain.strip().lower().lstrip('@')`) and filter out customers whose email domain does not match before match evaluation.
   - Maintain 100% backward compatibility when `domain` is omitted or `None`.
   - Preserve exact match priority (ordered by `id` ascending) and partial match ordering (ordered by `last_name` case-insensitive, tie-broken by `id` ascending).
2. **CLI Layer (`src/cli.py`)**:
   - Add argument parsing (`_parse_cli_args`) supporting optional `--domain <domain>`, `-d <domain>`, `--domain=<domain>`, and `-d=<domain>`.
   - Maintain existing validation rules (`VR-01`, `VR-02`) and standardized output formatting (`EH-01`).
   - If `--domain` or `-d` is passed without a value, safely treat the query as invalid, print `"No se encontraron clientes"`, and exit with code `0`.
   - Pass `domain` to `search_customers` when present, or call without `domain` when absent.
3. **Automated Testing (`tests/`)**:
   - Add unit tests in `tests/test_search.py` covering email domain filtering, `@` prefix handling, case insensitivity, no matches, ordering preservation, backward compatibility, and malformed emails.
   - Add unit tests in `tests/test_cli.py` covering `--domain`, `-d`, `@` prefix, uppercase domains, nonexistent domain queries, and missing value handling.
4. **Traceability & Contract Guardrails (`docs/traceability.md`)**:
   - Add FR-07 / AC-07 (CR-03) row to `docs/traceability.md` documenting all test functions in `tests/test_search.py` to maintain repository contract compliance.
5. **Deterministic Verification**:
   - Execute `scripts/verify_repo.sh` to ensure test suite passes with >=90% coverage, static compilation passes, and repository contract passes.

## Files Changed
- `src/service.py`: Added optional `domain: str | None = None` parameter and domain normalization/filtering logic.
- `src/cli.py`: Added argument parsing for `--domain` / `-d` flags while preserving validation, error handling, and formatting.
- `tests/test_search.py`: Added 7 test cases validating domain filtering functionality, ordering, and backward compatibility.
- `tests/test_cli.py`: Added 9 test cases validating CLI domain flags, argument ordering, and error handling.
- `docs/traceability.md`: Registered FR-07 / AC-07 traceability and mapped all test functions.
- `results/coder-report.md`: Documented implementation report.

## Tests Added / Updated
- `tests/test_search.py`:
  - `test_search_with_email_domain_filter`: Validates filtering customers by email domain.
  - `test_search_domain_with_at_prefix`: Validates `@domain.com` syntax normalization.
  - `test_search_domain_case_insensitive`: Validates case-insensitive domain matching.
  - `test_search_domain_no_match`: Validates empty result when domain does not match.
  - `test_search_domain_preserves_ordering`: Validates exact matches first by ID and partial matches by last name / ID.
  - `test_search_domain_none_backward_compatible`: Validates default parameter backward compatibility.
  - `test_search_domain_email_without_at_symbol`: Validates customer email without `@` is excluded safely.
- `tests/test_cli.py`:
  - `test_cli_domain_long_flag`: Validates `--domain` option filtering.
  - `test_cli_domain_short_flag`: Validates `-d` option filtering.
  - `test_cli_domain_with_at_prefix`: Validates `-d @domain` handling in CLI.
  - `test_cli_domain_case_insensitive`: Validates case-insensitive domain handling in CLI.
  - `test_cli_domain_no_match`: Validates standard "No se encontraron clientes" message on domain mismatch.
  - `test_cli_domain_flag_missing_value`: Validates `--domain` without value exits cleanly.
  - `test_cli_domain_flag_before_term`: Validates flag placed before positional search term.
  - `test_cli_domain_equals_syntax`: Validates `--domain=value` and `-d=value` syntax.
  - `test_cli_unexpected_extra_argument`: Validates rejection of extra positional tokens.

## Commands Executed
- `python -m pytest -v tests/`
- `python -m pytest --cov=src --cov-report=term-missing tests/`
- `D:/Git/bin/bash.exe scripts/verify_repo.sh`

## Verification Result
- Test execution: 37 passed in 0.72s.
- Coverage gate: 99.18% overall coverage (required >= 90.00%).
  - `src/service.py`: 100%
  - `src/storage.py`: 100%
  - `src/model.py`: 100%
  - `src/cli.py`: 98%
- Static compilation (`compileall`): PASS.
- Repository contract check (`scripts/check_repo_contract.py`): PASS.
- Script output summary: `REPO_CONTRACT: PASS`, `VERIFY_REPO: PASS`.

## Assumptions
- Domain filtering evaluates the domain portion of an email (the portion following the last `@`).
- Providing a domain with a leading `@` (e.g. `@example.com`) is normalized to match `example.com`.
- Matching is case-insensitive for both the domain query and customer email address.
- When an optional `--domain` or `-d` flag is passed without a parameter value in the CLI, it is handled as invalid input printing `"No se encontraron clientes"` and exiting with code `0`.

## Known Limitations
- Domain filtering operates strictly on exact matching of the domain portion (no globbing, wildcards, or regex domain patterns).
- `data/customers.json` remains read-only as constrained by architecture rules.

## Self-Check
[x] Scope respected
[x] Existing tests not weakened
[x] No undocumented dependency/API introduced
[x] Ready for independent review

This report is NOT an approval.
