from pathlib import Path
import ast
import re
import subprocess
import sys


REPO_ROOT = Path(__file__).resolve().parent.parent

REQUIRED_PATHS = [
    "AGENTS.md",
    "README.md",
    "REQUIREMENTS.md",
    "SPEC.md",
    "ARCHITECTURE.md",
    "TASKS.md",
    "TASK_UNDER_TEST.md",
    "docs/REPO_MAP.md",
    "docs/traceability.md",
    "scripts/verify_repo.sh",
    "scripts/check_repo_contract.py",
    ".github/workflows/verify.yml",
    "results",
]

REQUIRED_AGENTS_SECTIONS = [
    "## Read First",
    "## Sources of Truth",
    "## Repository Map",
    "## Standard Commands",
    "## Change Rules",
    "## Stop Conditions",
    "## Definition of Done",
]

REQUIRED_SPEC_IDS = [
    "FR-01",
    "FR-02",
    "FR-03",
    "FR-04",
    "FR-05",
    "FR-06",
    "AC-01",
    "AC-02",
    "AC-03",
    "AC-04",
    "AC-05",
]


def main() -> int:
    errors: list[str] = []

    # 1. Verify required files and directories exist
    for rel_path in REQUIRED_PATHS:
        if not (REPO_ROOT / rel_path).exists():
            errors.append(f"Missing required path: {rel_path}")

    if errors:
        return _report(errors)

    # 2. Verify AGENTS.md contract sections
    agents_text = (REPO_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    for section in REQUIRED_AGENTS_SECTIONS:
        if section not in agents_text:
            errors.append(f"AGENTS.md missing required section: '{section}'")

    # 3. Verify SPEC.md references requirement and acceptance criteria IDs
    spec_text = (REPO_ROOT / "SPEC.md").read_text(encoding="utf-8")
    for req_id in REQUIRED_SPEC_IDS:
        if req_id not in spec_text:
            errors.append(f"SPEC.md missing reference to ID: {req_id}")

    # 4. Verify docs/traceability.md includes all test functions in tests/test_search.py
    traceability_text = (REPO_ROOT / "docs/traceability.md").read_text(encoding="utf-8")
    test_search_text = (REPO_ROOT / "tests/test_search.py").read_text(encoding="utf-8")
    test_funcs = re.findall(r"^def\s+(test_[a-zA-Z0-9_]+)\s*\(", test_search_text, flags=re.MULTILINE)
    for fn_name in test_funcs:
        if fn_name not in traceability_text:
            errors.append(
                f"Traceability gap: '{fn_name}' in tests/test_search.py is not documented in docs/traceability.md"
            )

    # 5. Verify no forbidden artifacts (.pyc, __pycache__, .coverage, .env) are tracked in Git
    git_ls = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "ls-files"],
        capture_output=True,
        text=True,
        check=False,
    )
    if git_ls.returncode == 0:
        for tracked in git_ls.stdout.splitlines():
            if (
                tracked.endswith(".pyc")
                or "__pycache__" in tracked
                or tracked == ".coverage"
                or tracked == ".env"
                or tracked.startswith(".env.")
            ):
                errors.append(f"Forbidden generated/sensitive file tracked in Git: {tracked}")

    # 6. Verify protected path data/customers.json has not been modified
    git_diff = subprocess.run(
        ["git", "-C", str(REPO_ROOT), "diff", "--name-only", "HEAD", "--", "data/customers.json"],
        capture_output=True,
        text=True,
        check=False,
    )
    if git_diff.returncode == 0 and git_diff.stdout.strip():
        errors.append("Protected path violation: data/customers.json was modified")

    # 7. Static type-annotation check on public functions in src/service.py and src/storage.py (NFR-03)
    for rel_src in ("src/service.py", "src/storage.py"):
        tree = ast.parse((REPO_ROOT / rel_src).read_text(encoding="utf-8"), filename=rel_src)
        for node in tree.body:
            if isinstance(node, ast.FunctionDef) and not node.name.startswith("_"):
                if node.returns is None:
                    errors.append(f"Static typing check (NFR-03): '{node.name}' in {rel_src} lacks return type annotation")
                for arg in node.args.args:
                    if arg.annotation is None:
                        errors.append(
                            f"Static typing check (NFR-03): argument '{arg.arg}' of '{node.name}' in {rel_src} lacks type annotation"
                        )

    return _report(errors)


def _report(errors: list[str]) -> int:
    if errors:
        print("REPO_CONTRACT: FAIL")
        for err in errors:
            print(f" - {err}")
        return 1
    print("REPO_CONTRACT: PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
