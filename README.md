# Customer Search CLI (`ada-08-agent-ready-repository`)

Command-line application in Python 3.11+ for searching customer records in a local JSON database (`data/customers.json`), designed with **Spec-Driven Development (SDD)** and **Agent-Ready Repository** guardrails.

## Quick Navigation for Humans & Coding Agents
- **Operational Contract**: [`AGENTS.md`](AGENTS.md)
- **Repository Map & Change Guide**: [`docs/REPO_MAP.md`](docs/REPO_MAP.md)
- **Normative Sources of Truth**: [`REQUIREMENTS.md`](REQUIREMENTS.md) · [`SPEC.md`](SPEC.md) · [`ARCHITECTURE.md`](ARCHITECTURE.md) · [`TASKS.md`](TASKS.md) · [`docs/traceability.md`](docs/traceability.md)
- **Controlled Task Under Test**: [`TASK_UNDER_TEST.md`](TASK_UNDER_TEST.md)

## Requirements & Setup
- Python 3.11+
- Install test dependencies:
  ```bash
  pip install -r requirements.txt
  ```

## Running the CLI
```bash
python src/cli.py "ale"
```
Or on Windows CMD:
```cmd
search "ale"
```

## Unified Verification Contract (Tests + Lint/Compile + Guardrails)
Run the single verification contract shared by human developers, coding agents, and CI:
```bash
# Unix / CI / Git Bash on Windows:
./scripts/verify_repo.sh
# Or explicitly with Git Bash on Windows PowerShell:
D:\Git\bin\bash.exe scripts/verify_repo.sh

# Windows PowerShell equivalent wrapper:
pwsh -NoProfile -ExecutionPolicy Bypass -File scripts/verify_repo.ps1
```
