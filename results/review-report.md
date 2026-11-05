# Independent Review Report

## Review Context
Change ID: CR-03
Branch / PR: ada09/cr-email-domain-filter
Commit reviewed: c291a00
Reviewer agent: Reviewer Agent (Independent Session)
Model: Gemini 2.5 Pro (inherited)
Tools / permissions: Read-only codebase access, artifact write for review report

## Requirements Reviewed
- FR-02
- FR-03
- FR-04
- FR-05
- FR-07
- AC-07

## Verification Evidence Reviewed
- **Verification Harness**: Executed `bash scripts/verify_repo.sh` (and `pwsh scripts/verify_repo.ps1`) cleanly against commit `c291a00`.
- **Unit Test Execution**: 37 tests collected and passed in 0.65s (0 failures, 0 errors).
- **Code Coverage**: Achieved 99.18% overall line coverage against the required threshold of >= 90.00%:
  - `src/service.py`: 100% (31/31 statements)
  - `src/storage.py`: 100% (31/31 statements)
  - `src/model.py`: 100% (7/7 statements)
  - `src/cli.py`: 98% (52/53 statements; line 83 `if __name__ == '__main__':` excluded during test imports)
- **Static Compilation**: `python -m compileall -q src tests scripts` passed without syntax errors or warnings.
- **Repository Contract Guardrails**: `python scripts/check_repo_contract.py` reported `REPO_CONTRACT: PASS` across all 7 checks (required paths, AGENTS sections, SPEC requirement IDs, traceability synchronization, untracked forbidden files, data integrity of `data/customers.json`, and static type annotations on public service/storage functions).
- **Coverage Quality Note**: While nominal line coverage is 99.18%, the tests exercise only standard inputs and omit critical edge cases around empty, whitespace, and malformed domain inputs, giving a false sense of comprehensive security.

## Findings

### RF-01 — [Severity: MUST FIX]
Category: Correctness / Functional Defect
Requirement / AC: AC-07, FR-07
File / Line: `src/service.py:5-9, 20-30`
Evidence:
In `src/service.py`, `_extract_domain` returns an empty string `""` when the customer's email lacks an `@` symbol:
```python
def _extract_domain(email: str) -> str:
    """Extrae el dominio de una dirección de correo en minúsculas."""
    if "@" in email:
        return email.rsplit("@", 1)[1].strip().lower()
    return ""
```
In `search_customers`, the `domain` parameter is normalized as follows:
```python
target_domain: str | None = None
if domain is not None:
    target_domain = domain.strip().lower().lstrip('@')
```
If a caller supplies `domain=""`, `domain="   "`, or `domain="@"`, `target_domain` evaluates to `""` (which is not `None`).
During customer iteration:
```python
if target_domain is not None:
    cust_domain = _extract_domain(customer.email)
    if cust_domain != target_domain:
        continue
```
When a customer has a malformed email without an `@` (e.g., `email="carlos_sin_arroba"`), `_extract_domain` returns `""`. The condition `cust_domain != target_domain` evaluates to `"" != ""` (False), meaning the customer is NOT filtered out and is returned as a valid match.
Conversely, all legitimate customers with valid email domains (e.g., `carlos@example.com`) produce `cust_domain == "example.com" != ""`, so they are all excluded.
Problem:
Passing an empty string, whitespace string, or lone `@` as `domain` inverts the filtering logic: customers with invalid email addresses lacking `@` are treated as valid matches for the domain filter, while all legitimate customers with valid domains are discarded. AC-07 mandates that "results must include only customers whose email domain matches the given domain"; an empty string or lone `@` is not a domain, and malformed emails do not have a matching domain.
Risk:
Data integrity risk and unexpected query behavior: API callers or CLI invocations passing empty or whitespace domain strings unintentionally retrieve records with corrupted or non-standard email data, while all legitimate customer records are suppressed.
Recommended next step:
1. Normalize domain extraction so that emails without an `@` or without a valid post-`@` domain return `None` (or a distinct non-matching sentinel) rather than `""`.
2. Treat `domain` input that normalizes to an empty string (`domain.strip().lstrip('@') == ""`) as either:
   - Invalid input (returning an empty list or raising a validation error), or
   - An omitted filter (`target_domain = None`), matching the behavior of `domain=None`.
3. Add targeted unit tests verifying that `domain=""`, `domain="   "`, and `domain="@"` never match customers without `@` in their email address.

### RF-02 — [Severity: SHOULD FIX]
Category: Input Validation / CLI Robustness
Requirement / AC: FR-07, AC-07, EH-01
File / Line: `src/cli.py:26-31, 42-46, 60-63`
Evidence:
In `src/cli.py`, `_parse_cli_args` handles `--domain` / `-d` without a trailing value by detecting `i + 1 >= len(argv_list)` and returning `is_valid = False` (line 25), which correctly causes `main()` to print `"No se encontraron clientes"` and exit with code `0`.
However, when the equals syntax is used with an empty string:
```python
elif arg.startswith("--domain="):
    domain = arg.split("=", 1)[1]
    i += 1
elif arg.startswith("-d="):
    domain = arg.split("=", 1)[1]
    i += 1
```
Or when `--domain ""` is explicitly passed, `domain` is assigned `""` and `is_valid` remains `True`.
In `main()`:
`term` is rigorously validated against `VR-01` (`not term.strip() or not any(c.isalnum()...)`) and `VR-02` (`len(term) < 3`), but `domain` undergoes zero validation.
The CLI proceeds to call `search_customers(term, domain="")`.
Problem:
Inconsistent validation: `python src/cli.py "ana" --domain` is cleanly rejected as invalid input, whereas `python src/cli.py "ana" --domain=` or `python src/cli.py "ana" --domain ""` bypasses validation and invokes `search_customers` with an empty domain string, triggering the flawed matching behavior reported in RF-01.
Risk:
User experience inconsistency and fragile command-line interface behavior depending on whether flags use space or equals syntax.
Recommended next step:
Validate `domain` in `src/cli.py` (or within `_parse_cli_args`): if `domain` is passed but consists only of whitespace or `@` characters (`not domain.strip().lstrip('@')`), treat the input as invalid (`is_valid = False`), consistent with missing flag arguments.

### RF-03 — [Severity: SHOULD FIX]
Category: Testing Veracity / Boundary Coverage
Requirement / AC: NFR-03, AC-07
File / Line: `tests/test_search.py:90-177`, `tests/test_cli.py:57-117`
Evidence:
The test suite reports 99.18% overall code coverage and passes all 37 tests.
However, inspection of `tests/test_search.py` reveals that existing tests only exercise well-formed domains (`"example.com"`, `"@example.com"`, `"EXAMPLE.COM"`, `"nonexistent.com"`).
Not a single unit test tests:
- `search_customers("Carlos", domain="")`
- `search_customers("Carlos", domain="   ")`
- `search_customers("Carlos", domain="@")`
- `search_customers("Carlos", domain="@@example.com")`
In `tests/test_cli.py`, `test_cli_domain_flag_missing_value` only exercises `run_cli_internal(capsys, "ana", "--domain")`.
No CLI tests verify `--domain=""`, `-d=""`, or `--domain " "`.
Problem:
False sense of security created by nominal 99.18% line coverage. The test suite does not exercise boundary values for the new `domain` parameter, allowing the flawed matching in RF-01 and the CLI inconsistency in RF-02 to remain undetected.
Risk:
Regressions or unhandled exceptions under edge-case inputs will bypass CI/CD guardrails despite a high line coverage score.
Recommended next step:
Add parameterized unit tests in `tests/test_search.py` and CLI tests in `tests/test_cli.py` covering empty string, whitespace-only, lone `@`, and equals-syntax empty arguments (`--domain=`).

### RF-04 — [Severity: OPTIONAL]
Category: Code Quality / Maintainability
Requirement / AC: FR-07
File / Line: `src/cli.py:60-63`
Evidence:
```python
if domain is not None:
    results = search_customers(term, domain=domain)
else:
    results = search_customers(term)
```
Problem:
In `src/service.py`, `search_customers` has the signature `search_customers(term: str, domain: str | None = None)`.
Calling `search_customers(term, domain=domain)` with `domain=None` yields identical behavior to calling `search_customers(term)`.
The `if/else` branching in `src/cli.py` is entirely redundant.
Risk:
Unnecessary code complexity and maintenance burden without functional benefit.
Recommended next step:
Simplify lines 60-63 to a single call: `results = search_customers(term, domain=domain)`.

### RF-05 — [Severity: OPTIONAL]
Category: CLI Architecture / Design Robustness
Requirement / AC: FR-07
File / Line: `src/cli.py:10-38`
Evidence:
`_parse_cli_args` implements a custom while-loop over `argv_list` instead of utilizing Python standard library `argparse`.
Under the current loop:
1. Duplicate flags: `python src/cli.py "ana" --domain a.com --domain b.com` silently overwrites `domain` with `"b.com"` without error or warning, whereas multiple positional arguments cause rejection (line 36).
2. Flag-like argument consumption: `python src/cli.py --domain -d "ana"` assigns `"-d"` to `domain` and `"ana"` to `term` because `argv_list[i + 1]` is not checked for leading dashes.
Problem:
Handcrafted argument parsing introduces subtle inconsistencies in flag handling compared to standard CLI conventions.
Risk:
User typos or scripting mistakes (such as unintentionally duplicated flags or missing argument values before another flag) may execute unintended queries without informative feedback.
Recommended next step:
Refactor CLI argument parsing to use `argparse.ArgumentParser` (standard library, compliant with C-01) configured with `exit_on_error=False` or explicit error handling, or enhance `_parse_cli_args` to reject duplicate flags and flag-like option arguments.

### RF-06 — [Severity: OPTIONAL]
Category: Repository Hygiene / Scope Discipline
Requirement / AC: AGENTS.md Change Rules
File / Line: Commit `c291a00` (`results/`, `AI_USAGE_LOG.md`)
Evidence:
In commit `c291a00`, four report files from ADA-08 (`results/after-agent-run.md`, `results/before-agent-run.md`, `results/implicit-knowledge.md`, and `results/readiness-improvement-report.md`) were deleted, and `AI_USAGE_LOG.md` had all prior entries (Entries 01-05) removed and replaced with a single entry.
Problem:
AGENTS.md dictates: "Keep changes strictly scoped to the requested task (`TASK_UNDER_TEST.md`)."
While preparing deliverables for ADA-09, deleting prior assignment artifacts and clearing audit logs within the same commit as feature implementation introduces unnecessary commit churn and breaks audit continuity.
Risk:
Loss of historical traceability across milestone transitions and risk of merge conflicts when merging into branches that retain ADA-08 documentation.
Recommended next step:
Keep feature implementation commits isolated to code and tests relevant to CR-03. File cleanups and log updates should be handled in separate chore/documentation commits, or prior logs should be appended rather than overwritten.

## Missing Evidence / Open Questions
- **Missing Evidence**:
  1. Boundary condition tests: No automated tests currently verify behavior when `domain` is passed as `""`, `"   "`, `"@"`, or `"@@"`.
  2. Equals-syntax CLI tests: No automated tests verify CLI behavior when `--domain=""` or `-d=""` is passed with an explicit empty value.
  3. Subdomain matching: No test or specification clarifies whether `--domain example.com` should match subdomains like `user@sub.example.com`. Currently, the implementation requires an exact domain string match following the last `@`.
  4. Duplicate flag tests: No tests verify behavior when multiple domain flags are provided.
- **Open Questions for Human Reviewer**:
  1. *Empty Domain Semantics*: Should `search_customers(term, domain="")` and `python src/cli.py "<term>" --domain=""` treat an empty domain string as "no filter" (fallback to default all-domains search), return zero results (`[]` / `"No se encontraron clientes"`), or raise an error?
  2. *Subdomain Scope*: Is exact domain matching (e.g. `example.com` matching only `@example.com` and not `@sub.example.com`) acceptable for CR-03, or should hierarchical subdomain matching be supported?
  3. *CLI Flag Validation*: Should duplicate `--domain` flags be rejected as invalid input rather than silently taking the last value?
  4. *Audit History Retention*: Should the deleted ADA-08 audit reports (`results/before-agent-run.md`, etc.) be restored in a separate cleanup commit to preserve milestone traceability?

## Summary
The PR candidate `c291a00` successfully implements the core requirements of CR-03 (`FR-02`, `FR-03`, `FR-04`, `FR-05`, `FR-07`, and `AC-07`). It preserves 100% backward compatibility for existing callers of `search_customers(term)`, strictly respects architectural boundaries (CLI handles parsing/formatting, Service handles matching/ordering, Storage/Model contracts remain untouched), introduces no non-standard dependencies, and passes the repository verification harness with 99.18% coverage.

However, the PR should **NOT** be merged in its current state until the **MUST FIX** defect (RF-01: empty/lone-`@` domain matching malformed emails) and **SHOULD FIX** improvements (RF-02: CLI validation of empty domain flags; RF-03: edge-case tests) are addressed. The high test coverage masks an edge case where invalid emails without `@` are falsely returned and valid emails are filtered out.

**Overall Gate Recommendation**: **CHANGES REQUESTED (NEEDS REVISION)** pending resolution of RF-01, RF-02, and RF-03.
