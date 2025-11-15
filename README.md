# CodeSentry
AI-Assisted Static Analysis and Code Review Pipeline for Python Codebases

---

## Overview
CodeSentry is a developer-facing CLI tool that orchestrates multiple static analysis utilities, aggregates their outputs, and generates a structured AI-based review using the OpenAI Responses API. It is designed to resemble production-grade evaluation loops such as those described in IMC Trading’s *AI Powered Engineering* role: measure, validate, and summarize code quality signals across a repository in a reliable and repeatable way.

The pipeline executes deterministic analyzers (flake8, bandit, pytest or pylint), collects tool metadata and runtime metrics, computes an overall pipeline status, and produces two artifacts per run:

- `codesentry_report.md` — high-level, human-readable findings  
- `codesentry_report.json` — machine-readable analysis data

This approach models an end-to-end AI-assisted compile/test/evaluate workflow.

---

## Key Features

### Static Analysis Layer
- **flake8** for formatting, style, and lint violations  
- **bandit** for security scanning  
- **pytest or pylint** depending on test detection  
- Automatic detection of `tests/` directory or test files

### Metadata and Evaluation Layer
- Tool version capture  
- Exit code tracking  
- Duration per analyzer  
- Pipeline status classification: `PASSED` or `FAILED`  
- Consistent output structures for downstream consumers (e.g., agents, dashboards, CI systems)

### AI Review Layer
- Structured LLM-generated summary incorporating analyzer outputs:
  - Critical Risks  
  - High-Value Fixes  
  - Lint/Style Themes  
  - Recommended Next Steps  
- Honest failure-handling: if the AI call fails, the report explicitly states that no AI summary was generated

### Output Artifacts
- Markdown report for human review  
- JSON report for programmatic use or ingestion into automated systems  

---

## Example Codebases
Two example repositories are included under `codesentry/example/`:

- **bad_code_example** — simple single-file issues (missing docstrings, unused imports)  
- **bad_code_complex** — multi-file example including:  
  - insecure `eval` usage  
  - improper subprocess calls  
  - SQL injection via f-strings  
  - global mutable state  
  - hardcoded credentials  
  - broad exception handling  
  - relative import errors  
  - missing documentation across modules

Running CodeSentry on these repos demonstrates the pipeline’s ability to surface meaningful issues and generate structured analysis artifacts.

---

## Installation

```bash
pip install -r requirements.txt
