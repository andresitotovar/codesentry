import argparse
from pathlib import Path
from typing import Dict, Any, List, Optional

from . import repo_utils
from . import analyzers
from . import ai_review
from . import reporter
from .constants import DEFAULT_MAX_CHARS, DEFAULT_TIMEOUT_SEC


def run_pipeline(
    path: str,
    max_chars: int = DEFAULT_MAX_CHARS,
    timeout_sec: int = DEFAULT_TIMEOUT_SEC,
    strict: bool = False,
    out_dir: Optional[str] = None,
) -> int:
    repo_path = repo_utils.validate_repo_path(path)
    has_tests, reason = repo_utils.detect_tests(repo_path)
    print(f"[codesentry] Analyzing repo: {repo_path}")
    print(f"[codesentry] Test detection: {reason}")

    # Collect tool versions up front (for JSON metadata)
    print("[codesentry] Collecting tool versions...")
    versions: Dict[str, str] = analyzers.get_tool_versions()

    results: Dict[str, Dict[str, Any]] = {}

    print("[codesentry] Running flake8...")
    results["flake8"] = analyzers.run_flake8(repo_path, timeout_sec)

    print("[codesentry] Running bandit...")
    results["bandit"] = analyzers.run_bandit(repo_path, timeout_sec)

    if has_tests:
        print("[codesentry] Running pytest (tests detected)...")
        results["pytest"] = analyzers.run_pytest(repo_path, timeout_sec)
    else:
        print("[codesentry] Running pylint (no tests detected)...")
        results["pylint"] = analyzers.run_pylint(repo_path, timeout_sec)

    # Compute overall pipeline status
    failed = any((res.get("exit_code", 0) != 0) for res in results.values())
    pipeline_status = "FAILED" if failed else "PASSED"
    print(f"[codesentry] Pipeline status: {pipeline_status}")

    print("[codesentry] Generating AI summary...")
    ai_md = ai_review.generate_ai_summary(
        repo_path=str(repo_path),
        results=results,
        max_chars=max_chars,
    )

    out_dir_path: Optional[Path] = Path(out_dir).resolve() if out_dir else None
    paths = reporter.write_reports(
        repo_path,
        results,
        ai_md,
        versions=versions,
        pipeline_status=pipeline_status,
        out_dir=out_dir_path,
    )

    print("[codesentry] Done.")
    print(f"[codesentry] Markdown report: {paths['markdown']}")
    print(f"[codesentry] JSON report: {paths['json']}")

    # Strict mode: exit non-zero if the pipeline failed
    if strict and pipeline_status == "FAILED":
        return 1

    return 0


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="codesentry",
        description="AI-assisted static analysis and code review for Python repos.",
    )
    parser.add_argument("path", help="Path to the Python code project.")
    parser.add_argument(
        "--max-chars",
        type=int,
        default=DEFAULT_MAX_CHARS,
        help="Max characters per tool output for AI input.",
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT_SEC,
        help="Timeout (seconds) per analyzer.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit non-zero if any analyzer fails.",
    )
    parser.add_argument(
        "--out",
        type=str,
        default=None,
        help="Optional output directory (default: repo root).",
    )
    return parser


def main(argv: Optional[List[str]] = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    return run_pipeline(
        path=args.path,
        max_chars=args.max_chars,
        timeout_sec=args.timeout,
        strict=bool(args.strict),
        out_dir=args.out,
    )


if __name__ == "__main__":
    raise SystemExit(main())
