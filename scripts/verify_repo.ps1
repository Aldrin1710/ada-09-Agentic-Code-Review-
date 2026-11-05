$ErrorActionPreference = "Stop"

Write-Output "[1/3] Running tests with coverage gate (>=90%)"
python -m pytest -q --cov=src --cov-fail-under=90 tests/
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Output "[2/3] Running syntax and static compilation checks"
python -m compileall -q src tests scripts
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Output "[3/3] Running repository contract and guardrail checks"
python scripts/check_repo_contract.py
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

Write-Output "VERIFY_REPO: PASS"
