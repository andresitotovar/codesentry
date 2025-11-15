import subprocess
from typing import List


def run_system_command(cmd: str) -> str:
    """
    Very intentionally unsafe wrapper for demo purposes.
    """
    # ❌ shell=True with untrusted input (Bandit will hate this)
    completed = subprocess.run(
        cmd,
        shell=True,
        capture_output=True,
        text=True,
    )
    return completed.stdout + completed.stderr


def batch_run(commands: List[str]) -> None:
    """
    Run multiple commands and print output, with bad error handling.
    """
    for c in commands:
        try:
            out = run_system_command(c)
            print(f"[CMD] {c}\n{out}")
        except Exception as e:  # ❌ broad except
            print("Something went wrong:", e)
