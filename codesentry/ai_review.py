import os
from typing import Dict, Any

from openai import OpenAI, OpenAIError  # type: ignore

from .constants import SYSTEM_PROMPT, USER_PROMPT_TEMPLATE, DEFAULT_MODEL


def _trim_output(text: str | None, max_chars: int) -> str:
    if not text:
        return ""
    if len(text) <= max_chars:
        return text
    return text[:max_chars] + "\n... [truncated]"


def _build_user_prompt(
    repo_path: str,
    chosen: str,
    flake8_out: str,
    bandit_out: str,
    tests_or_pylint_out: str,
) -> str:
    return USER_PROMPT_TEMPLATE.format(
        repo_path=repo_path,
        chosen=chosen,
        flake8=flake8_out,
        bandit=bandit_out,
        pytest_or_pylint=tests_or_pylint_out,
    )


def _prepare_prompt_inputs(
    repo_path: str,
    results: Dict[str, Dict[str, Any]],
    max_chars: int,
) -> str:
    chosen = ", ".join(results.keys())
    flake8_out = _trim_output(results.get("flake8", {}).get("output", ""), max_chars)
    bandit_out = _trim_output(results.get("bandit", {}).get("output", ""), max_chars)

    tests_or_pylint_key = "pytest" if "pytest" in results else "pylint"
    tests_or_pylint_out = _trim_output(
        results.get(tests_or_pylint_key, {}).get("output", ""),
        max_chars,
    )

    return _build_user_prompt(
        repo_path=repo_path,
        chosen=chosen,
        flake8_out=flake8_out,
        bandit_out=bandit_out,
        tests_or_pylint_out=tests_or_pylint_out,
    )


def generate_ai_summary(
    repo_path: str,
    results: Dict[str, Dict[str, Any]],
    max_chars: int,
) -> str:
    """
    Generate a markdown summary using OpenAI.
    If the API key is not configured or the call fails, return a short
    explanation instead of a fabricated summary.
    """
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return (
            "AI summary is not available.\n\n"
            "OpenAI API key is not configured in this environment.\n"
        )

    user_prompt = _prepare_prompt_inputs(repo_path, results, max_chars)
    client = OpenAI(api_key=api_key)

    try:
        response = client.responses.create(
            model=DEFAULT_MODEL,
            instructions=SYSTEM_PROMPT,
            input=user_prompt,
        )
        return response.output_text
    except OpenAIError as e:
        return (
            "AI summary could not be generated.\n\n"
            f"OpenAI error: {e}\n"
        )
    except Exception as e:  # safety net
        return (
            "AI summary could not be generated due to an unexpected error.\n\n"
            f"Error: {e}\n"
        )
