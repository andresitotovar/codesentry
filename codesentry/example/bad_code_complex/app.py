import json
from typing import Dict

from . import db
from . import services
from .settings import DEBUG, DEFAULT_ADMIN_USER, DEFAULT_ADMIN_PASSWORD


# Global mutable state
CACHE: Dict[str, str] = {}


def create_default_admin() -> None:
    # Pretend to insert a user; not even using the DB properly.
    users = db.get_users_by_role("admin")
    if not users:
        print(f"[INIT] Creating default admin user={DEFAULT_ADMIN_USER}")
        # In a real app we'd INSERT here; we leave it as a no-op on purpose.


def unsafe_math_eval(expression: str) -> float:
    """
    Intentionally unsafe: evaluates arbitrary input.
    """
    # ❌ eval on untrusted input (Bandit will flag this)
    return eval(expression)  # nosec


def handle_request(raw_body: str) -> str:
    """
    Simulate a very bad HTTP handler.
    """
    if DEBUG:
        print("[DEBUG] Raw body:", raw_body)

    try:
        data = json.loads(raw_body)
    except Exception:
        # Swallowing all exceptions, returning vague error
        return json.dumps({"status": "error", "message": "invalid"})

    cmd = data.get("cmd", "")
    expr = data.get("expr", "1+1")

    if cmd:
        # Unsafe command execution
        output = services.run_system_command(cmd)
    else:
        output = ""

    try:
        result = unsafe_math_eval(expr)
    except Exception as e:
        result = str(e)

    CACHE["last_result"] = str(result)

    return json.dumps(
        {
            "status": "ok",
            "result": result,
            "cmd_output": output,
        }
    )


if __name__ == "__main__":
    create_default_admin()

    example_body = json.dumps(
        {
            "cmd": "echo hello && dir",  # this will be executed by shell
            "expr": "10 / 2",
        }
    )
    print(handle_request(example_body))
