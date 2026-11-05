# Change Request

Change ID: CR-03

## Goal
Add optional email domain filtering to customer search in `search_customers` and the CLI interface, enabling users to narrow search results by a specific email domain (e.g., `example.com` or `@example.com`) evaluated case-insensitively, while preserving existing search semantics, input validation, and result ordering when domain filtering is not used.

## Requirements Covered
- FR-02 (Search evaluation against customer fields including email)
- FR-03 (Substring and partial matching behavior)
- FR-04 (Case-insensitive matching)
- FR-05 (Deterministic result ordering by exact match then partial match, tie-broken by ID)
- FR-07 (Bounded extension: optional email domain filter parameter in service and `--domain` option in CLI)
- AC-07 (Acceptance criteria: when domain filter is specified, results contain only customers whose email domain matches the specified domain, case-insensitively)

## Constraints
- Follow AGENTS.md.
- Use REQUIREMENTS.md and SPEC.md as the source of truth.
- Preserve architecture boundaries (CLI handles parsing/formatting, Service implements filtering logic, Storage and Model contracts remain unmodified).
- Do not weaken existing tests; ensure 100% backward compatibility for calls to `search_customers(term)` without domain.
- Do not invent external dependencies or rewrite unrelated layers.

## Verification
- Deterministic verification via `./scripts/verify_repo.sh` passing all unit tests, contract checks, and coverage targets.
- Targeted unit tests in `tests/test_search.py` verifying domain matching, case insensitivity, combined term + domain filtering, and empty results.
- Targeted CLI tests in `tests/test_cli.py` verifying `--domain` flag handling and output.

## Human Approval
Approved to implement: YES
Approved by: Aldrin (User)
Date: 2026-11-05
