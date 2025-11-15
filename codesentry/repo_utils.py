import sys
from pathlib import Path
from typing import Tuple


def validate_repo_path(path_str: str) -> Path:
    """
    Validate that the given path exists, is a directory, and has at least one .py file.
    If not valid, print a message and exit the program.
    """
    path = Path(path_str).expanduser().resolve()

    if not path.exists():
        print(f"[codesentry] ERROR: Path does not exist: {path}", file=sys.stderr)
        sys.exit(1)

    if not path.is_dir():
        print(f"[codesentry] ERROR: Path is not a directory: {path}", file=sys.stderr)
        sys.exit(1)

    py_files = list(path.rglob("*.py"))
    if not py_files:
        print(f"[codesentry] WARNING: No Python files found in {path}. Nothing to analyze.")
        sys.exit(0)

    return path


def detect_tests(repo_path: Path) -> Tuple[bool, str]:
    """
    Detect whether the repo has tests.

    Returns:
        (has_tests, reason)
    """
    tests_dir = repo_path / "tests"
    if tests_dir.exists() and tests_dir.is_dir():
        return True, "Found tests/ directory"

    # Look for test_*.py or *_test.py anywhere in the repo
    for p in repo_path.rglob("*.py"):
        name = p.name
        if name.startswith("test_") or name.endswith("_test.py"):
            return True, f"Found test file: {name}"

    return False, "No tests/ directory or test_*.py / *_test.py files detected"
