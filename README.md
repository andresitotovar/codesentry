# CodeSentry
AI-Assisted Static Analysis and Code Review Pipeline for Python Codebases

---

## Overview
CodeSentry is a developer-facing CLI tool that orchestrates multiple static analysis utilities, aggregates their outputs, and generates a structured AI-based code review using the OpenAI Responses API. The tool models an end-to-end evaluation loop commonly used in AI-augmented engineering environments: run analyzers, collect signals, generate structured output, and compute an overall pipeline status.

The name “CodeSentry” is an arbitrary term chosen to convey the idea of a guard or watcher over code quality. It is not tied to any external product or company.

The system is built with reliability in mind. Static analysis results are always produced deterministically, and if the AI review step fails (such as from a missing API key, timeout, or model error), the report clearly indicates the failure rather than generating placeholder content.

---

## Features

### Static Analysis Layer
- flake8 for formatting, style, and lint violations  
- bandit for security scanning  
- pytest or pylint depending on test detection  
- Automatic detection of test directories and naming conventions

### Evaluation Layer
- Captures exit codes, durations, and tool versions  
- Normalizes analyzer outputs into a unified structure  
- Computes an overall `pipeline_status` (`PASSED` or `FAILED`)  
- Produces consistent JSON for downstream automation

### AI Review Layer
- Integrates with OpenAI's Responses API to generate a structured review containing:
  - Critical Risks  
  - High-Value Fixes  
  - Lint/Style Themes  
  - Recommended Next Steps  
- Uses trimmed analyzer output to build a structured context window  
- If the AI step fails, a clear error message is included and the pipeline remains stable

### Output Artifacts
- `codesentry_report.md` (human-readable)  
- `codesentry_report.json` (machine-readable)

---

## Example Repositories

### bad_code_example/
A minimal example containing:
- unused imports  
- missing docstrings  
- simple logic issues  

### bad_code_complex/
A multi-file example illustrating:
- unsafe `eval` usage  
- insecure subprocess calls  
- SQL injection risks  
- hardcoded secrets  
- global mutable state  
- broad exception handling  
- missing documentation  
- relative import errors  

These examples demonstrate how CodeSentry surfaces issues through analyzers and AI review.

---

## Installation

```bash
pip install -r requirements.txt
```

---

## Usage

Run CodeSentry against any Python project:

```bash
python -m codesentry.cli <path-to-python-project>
```

Command-line options:

```
--strict          Return a non-zero exit status if any analyzer fails
--max-chars N     Maximum characters of analyzer output included in the AI prompt
--timeout N       Timeout in seconds per analyzer
--out DIR         Directory to store generated reports
```

Example:

```bash
python -m codesentry.cli codesentry/example/bad_code_complex --strict
```

Generated outputs:

- `codesentry_report.md`  
- `codesentry_report.json`  

---

## Technical Architecture

CodeSentry is organized as a three-layer pipeline.  
The name “Sentry” is simply a conceptual reference to a guard or watchman over code quality; it has no external association.

### 1. Collection Layer
Executes static analyzers (`flake8`, `bandit`, `pytest` or `pylint`) through subprocess calls, capturing:

- standard output and error streams  
- exit codes  
- tool versions  
- runtime durations  

This layer provides deterministic signals describing the state of the codebase.

### 2. Evaluation Layer
Normalizes analyzer outputs into a consistent structure and computes:

```
pipeline_status = PASSED | FAILED
```

based solely on deterministic analyzer results.  
This isolates CI-style evaluation logic from any nondeterministic AI behavior.

### 3. AI Review Layer
Builds a structured prompt using trimmed analyzer outputs and repository metadata, then submits it to OpenAI’s Responses API.

If the AI review step fails for any reason, the system produces a clear message such as:

```
AI summary could not be generated.
Reason: <error message>
```

No fabricated or placeholder summaries are produced.

---

## Repository Structure

```
codesentry/
├── README.md
├── requirements.txt
└── codesentry/
    ├── __init__.py
    ├── cli.py
    ├── analyzers.py
    ├── reporter.py
    ├── ai_review.py
    ├── constants.py
    ├── repo_utils.py
    ├── timers.py
    └── example/
        ├── bad_code_example/
        └── bad_code_complex/
```

---

## Relevance to AI-Driven Engineering

CodeSentry demonstrates hands-on experience with:

- building compile/test/evaluate pipelines  
- integrating deterministic tooling with nondeterministic AI models  
- generating both human- and machine-readable artifacts  
- constructing structured AI prompts from real analyzer signals  
- handling AI failure cases cleanly and explicitly  
- designing developer-facing automation tools  
- modeling real-world evaluation loops used in AI-augmented development workflows  

These capabilities align directly with engineering roles that integrate AI into production developer workflows.

---

## Roadmap

Future enhancements may include:

- Automatic patch suggestion generation  
- Embedding-based context retrieval for large codebases  
- Optional MCP server integration  
- Pull request comment automation  
- Web-based dashboards for browsing results  
- Support for additional programming languages  

---

## License
MIT
