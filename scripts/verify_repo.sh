#!/usr/bin/env bash
set -euo pipefail

echo "[1/3] Running tests with coverage gate (>=90%)"
python -m pytest -q --cov=src --cov-fail-under=90 tests/

echo "[2/3] Running syntax and static compilation checks"
python -m compileall -q src tests scripts

echo "[3/3] Running repository contract and guardrail checks"
python scripts/check_repo_contract.py

echo "VERIFY_REPO: PASS"
