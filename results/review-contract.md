# Review Contract

## Change
CR-03

## Requirements / Acceptance Criteria
- FR-02: Search term evaluation across allowed customer fields (`name`, `last_name`, and `email`).
- FR-03: Substring / partial match identification across allowed customer fields.
- FR-04: Case-insensitive matching.
- FR-05: Ordering results by exact match first (by ID ascending), then partial match (by last name ascending, tie-broken by ID ascending).
- FR-07: Optional email domain filter parameter (`domain: str | None = None`) in `search_customers` and CLI `--domain` / `-d` flag.
- AC-07: When a domain filter is provided, results must include only customers whose email domain matches the given domain (case-insensitively, handling optional '@' prefix gracefully). When omitted or None, existing search behavior and results must remain identical.

## Architecture Constraints
- Expected dependency flow: CLI (`src/cli.py`) -> Service (`src/service.py`) -> Storage (`src/storage.py`) -> Model (`src/model.py`). CLI cannot bypass Service or directly access Storage.
- Business-rule location: Domain filtering and search matching must reside in `src/service.py`. CLI is restricted to command-line argument parsing, terminal output formatting, and top-level error trapping.
- Protected boundaries: `src/storage.py` and `src/model.py` contracts must remain untouched. `data/customers.json` is read-only seed data.

## Review Rules
- Verify requirement coverage against CR-03, SPEC.md, and REQUIREMENTS.md.
- Verify every called API / dependency exists in Python standard library and project codebase.
- Check architecture boundaries: ensure no layer leaks or direct storage operations in the CLI.
- Inspect tests for masking, over-mocking, or false confidence (verify that tests assert on filtered output rather than mock pass-throughs).
- Check regression behavior and backward compatibility for existing callers.
- Identify unnecessary technical debt or code smells introduced by the change.
- Cite concrete file and line evidence for every finding.

## Severity
- **MUST FIX**: Requirement violation, regression, security/integrity risk, hallucinated API/dependency, broken architecture constraint, or defect that makes the change unsafe to approve.
- **SHOULD FIX**: Significant maintainability, coverage, design, or clarity issue that does not block the requested behavior.
- **OPTIONAL**: Non-blocking improvement outside the minimum acceptance threshold.
