# 🧠 ECHO.core Contributor Guidelines

Welcome to ECHO.core — a modular, symbolic cognitive architecture. To ensure coherence, modularity, and minimal error propagation, all contributors must follow these conventions:

---

## 🔁 File Structure & Import Conventions

- All shared logic (like YAML I/O) must live in dedicated utility modules (`yaml_utils.py`, `log_utils.py`, etc.).
- **Do not directly import standard libraries that have been wrapped.**  
  ✅ Use `from yaml_utils import load, dump`  
  ❌ Avoid `import yaml`

- Always reference files using paths relative to project root, or via `os.path.join()` for cross-platform compatibility.

---

## 🧱 Agent Design Rules

- Each agent class (e.g. `CuriosityAgent`, `IntuitionAgent`) must:
  - Have a clearly defined purpose
  - Contain `__init__`, data loading, and output generation methods
  - Use **utility functions** for logging, file I/O, or error handling
  - Include meaningful debug prints (e.g., `[AgentName] Loading goals...`)

---

## 📦 YAML Handling Standard

- Use only `yaml_utils.load()` and `yaml_utils.dump()` for all `.yaml` file access.
- Always supply a fallback in `load(path, fallback={})`
- Do not use `import yaml` in agent or runtime files
- Log meaningful warnings if fallback is used or file is malformed

---

## ✅ Code Hygiene

- Avoid partial edits. Make atomic commits with full, drop-in-safe replacements.
- Purge stale bytecode before testing:  
  ```bash
  find . -name "__pycache__" -type d -exec rm -rf {} +  
  find . -name "*.pyc" -delete
