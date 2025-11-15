# CodeSentry  
**AI-Assisted Static Analysis & Code Review Pipeline for Python Repositories**

---

## 🚀 Overview  
CodeSentry is a developer-facing CLI tool designed to mirror the workflows of modern developer productivity platforms—especially those described in IMC’s *Software Engineer – AI Powered Engineering* role.  
It runs static analysis (flake8, bandit, pytest/pylint), captures version metadata, and feeds results into an LLM that outputs a structured Markdown + JSON report.

---

## ✅ Key Features  
- Runs **static analysis & security checks**:  
  - `flake8` – style and lint issues  
  - `bandit` – security scanning  
  - `pytest` or `pylint` – depending on test detection  
- Captures **tool metadata & timings** (versions, exit codes, durations)  
- Generates an **LLM-based code review** with 4 sections:  
  1. Critical Risks  
  2. High-Value Fixes  
  3. Lint/Style Themes  
  4. Recommended Next Steps  
- Produces output artifacts:  
  - `codesentry_report.md` – human-readable review  
  - `codesentry_report.json` – machine-readable data  
- Computes **pipeline_status** (`PASSED` or `FAILED`) to reflect code health like a real CI tool  
- Example projects included (simple + complex) to demonstrate real usage  

---

## 🧪 Example: Complex “Bad Codebase” Review  
A sample multi-file repo (`example/bad_code_complex/`) includes:  
- Hardcoded secrets  
- SQL injection via f-strings  
- `eval()` usage  
- `shell=True` in subprocess calls  
- Global mutable state  
- Missing docstrings and unused imports  

Running CodeSentry on this codebase demonstrates how the tool surfaces real-world risks and suggests concrete improvements.  

---

## ▶️ Installation & Usage  
```bash
pip install -r requirements.txt
