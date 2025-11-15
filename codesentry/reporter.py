import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional


def _safe_text(d: Dict[str, Any], key: str) -> str:
    """Get a string value from a dict without crashing on missing keys."""
    v = d.get(key)
    return "" if v is None else str(v)


def write_reports(
    repo_path: Path,
    results: Dict[str, Dict[str, Any]],
    ai_summary_markdown: str,
    versions: Dict[str, str],
    pipeline_status: str,
    out_dir: Optional[Path] = None,
) -> Dict[str, Path]:
    """
    Write the JSON and Markdown reports.

    Returns:
        {"json": <json_path>, "markdown": <md_path>}
    """
    out_dir = out_dir or repo_path
    out_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).isoformat()
    repo_str = str(repo_path)

    # JSON report
    json_data: Dict[str, Any] = {
        "generated_at_utc": timestamp,
        "repo_path": repo_str,
        "pipeline_status": pipeline_status,
        "versions": versions,
        "tools": results,
        "ai_summary_markdown": ai_summary_markdown,
    }

    json_path = out_dir / "codesentry_report.json"
    with json_path.open("w", encoding="utf-8") as f:
        json.dump(json_data, f, indent=2)

    # Markdown report
    md_parts = [
        "# CodeSentry Report",
        f"_Status: {pipeline_status} | Generated: {timestamp} | Repo: {repo_str}_",
        "",
        "## AI Summary",
        ai_summary_markdown.strip(),
        "",
        "## Tool Results",
    ]

    for name, res in results.items():
        md_parts.append(f"### {name}")
        md_parts.append("```")
        md_parts.append(_safe_text(res, "output"))
        md_parts.append("```")
        md_parts.append("")

    md_text = "\n".join(md_parts)
    md_path = out_dir / "codesentry_report.md"
    with md_path.open("w", encoding="utf-8") as f:
        f.write(md_text)

    return {"json": json_path, "markdown": md_path}
