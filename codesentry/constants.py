DEFAULT_MODEL = "gpt-4o-mini" 
DEFAULT_MAX_CHARS = 6000
DEFAULT_TIMEOUT_SEC = 300

SYSTEM_PROMPT = """You are a senior AI code reviewer focused on Python repositories. \
You are concise, accurate, and action-oriented. You prioritize security > correctness \
> maintainability > style. You reference files/lines if present in tool outputs.
"""

USER_PROMPT_TEMPLATE = """You are given outputs from automatic code checks on a Python repo.
Provide four sections with markdown headers and bullet points:
1) Critical Risks (security, failing tests, crashes)
2) High-Value Fixes (highest ROI refactors)
3) Lint/Style Themes (recurring issues)
4) Recommended Next Steps (concrete actions)

Context:
- Repo path: {repo_path}
- Chosen analyzers: {chosen}
- flake8 (trimmed):
{flake8}
- bandit (trimmed):
{bandit}
- tests_or_pylint (trimmed):
{pytest_or_pylint}

Rules:
- Keep total under 250 words.
- Use bullets, no long paragraphs.
- If no tests detected, propose a minimal test plan.
"""
