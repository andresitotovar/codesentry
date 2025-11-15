import subprocess
import sys
from pathlib import Path
from typing import Dict, Any, List

from .timers import timed


def _run_tool(
    cmd: List[str],
    cwd: Path,
    timeout_sec: int,
    tool_name: str,
) -> Dict[str, Any]:
    """
    Run a command-line tool and capture exit code, duration, and combined stdout/stderr.
    Handles missing tools and timeouts gracefully.
    """
    with timed() as t:
        try:
            proc = subprocess.run(
                cmd,
                cwd=str(cwd),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=timeout_sec,
            )
            output = proc.stdout or ""
            exit_code = proc.returncode
        except FileNotFoundError:
            output = f"{tool_name} is not installed or not on PATH."
            exit_code = -127
        except subprocess.TimeoutExpired as e:
            partial = e.stdout or ""
            output = (
                f"{tool_name} timed out after {timeout_sec} seconds.\n\n"
                f"Partial output:\n{partial}"
            )
            exit_code = -1
        except Exception as e:
            output = f"Unexpected error running {tool_name}: {e}"
            exit_code = -1

    duration = t.get("duration")
    duration_sec = float(duration) if duration is not None else 0.0

    return {
        "tool": tool_name,
        "exit_code": exit_code,
        "duration_sec": round(duration_sec, 3),
        "output": output,
    }


# Individual Tool Runners


def run_flake8(repo_path: Path, timeout_sec: int) -> Dict[str, Any]:
    cmd = ["flake8", "."]
    return _run_tool(cmd, repo_path, timeout_sec, "flake8")


def run_bandit(repo_path: Path, timeout_sec: int) -> Dict[str, Any]:
    cmd = ["bandit", "-r", "."]
    return _run_tool(cmd, repo_path, timeout_sec, "bandit")


def run_pytest(repo_path: Path, timeout_sec: int) -> Dict[str, Any]:
    cmd = ["pytest"]
    return _run_tool(cmd, repo_path, timeout_sec, "pytest")


def run_pylint(repo_path: Path, timeout_sec: int) -> Dict[str, Any]:
    """
    Fallback when no tests are detected.
    For simplicity, we run pylint on the entire repo ('.').
    """
    cmd = ["pylint", "."]
    return _run_tool(cmd, repo_path, timeout_sec, "pylint")


# Tool Version Collector



def get_tool_versions() -> Dict[str, str]:
    """
    Return a best-effort mapping of tool -> version string.
    If a tool is missing or fails, record a readable message instead of crashing.
    """
    tools = {
        "python": [sys.executable, "--version"],
        "flake8": ["flake8", "--version"],
        "bandit": ["bandit", "--version"],
        "pytest": ["pytest", "--version"],
        "pylint": ["pylint", "--version"],
    }

    versions: Dict[str, str] = {}

    for name, cmd in tools.items():
        try:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                timeout=10,
            )
            output = (proc.stdout or "").strip()
            if not output:
                output = f"{name} version unknown (empty output)"
            versions[name] = output.splitlines()[0]
        except FileNotFoundError:
            versions[name] = f"{name} not installed or not on PATH"
        except subprocess.TimeoutExpired:
            versions[name] = f"{name} version check timed out"
        except Exception as e:
            versions[name] = f"{name} version check error: {e}"

    return versions
