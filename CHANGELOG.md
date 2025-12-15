# Changelog

## [17.0.1] - 2025-12-15
### Documentation
- update README.md to V3 gold standard (#50)

## [17.0.0] - 2025-12-07
### Other Changes
- update

---

📄 CHANGELOG.md

# Changelog

All notable changes to this project will be documented in this file.

This project adheres to:
- **Semantic Versioning** (https://semver.org/)
- **Keep a Changelog** format (https://keepachangelog.com/)

---

## 🔔 Policy Notice

**Every major change must be recorded here.**  
This includes:

### ✔ Human-based manual refactoring  
### ✔ AI-automated code changes  
### ✔ Patch-based fixes from Jules sessions  
### ✔ Structural redesigns  
### ✔ CLI behavior updates  
### ✔ Git / API / plugin / architecture changes  

No exceptions.  
If it changes how users or developers interact with the codebase, it *must be logged*.

---

# [Unreleased]

### Added
- Placeholder for new features not yet published.
- Add upcoming CLI expansion (`jules tui`, `jules doctor`, plugin architecture).
- Introduce upcoming Git conflict resolution engine.

### Changed
- Internal adjustments for future patch-resolver.
- Refactoring planned for session polling & caching layer.

### Fixed
- General placeholders for future bug fixes.

### Deprecated
- None yet.

### Removed
- None yet.

### Security
- None yet.

---

# [1.0.0] – 2025-11-14  
### 🎉 Initial PyPI Release

### Added
- Fully working **interactive Jules CLI REPL**:
  - `auto` — run pytest + auto-fix  
  - `task` — natural language tasks for refactoring, debugging, test creation  
  - `apply` — apply unidiff patches  
  - `commit` — auto-create branch and commit  
  - `push` — push current branch  
  - `pr create` — GitHub PR automation  
  - `session list` & `session show` — inspect Jules sessions  
  - `last` — show last session & result  

- Jules API integration using:
  - `/sources`, `/sessions`, `/activities`  
  - `AUTO_CREATE_PR` automation mode  
  - Real-time polling for patches and PRs

- GitHub integration:
  - Auto-branch creation  
  - Auto-commit  
  - Auto-push  
  - Auto-PR (with `GITHUB_TOKEN`)  

- Full local test runner (pytest)  
- Patch application with GNU `patch`  
- Full error-handling layer for:
  - Git  
  - Jules API  
  - Patch failures  
  - Connectivity

- Modern Python packaging:
  - `pyproject.toml`  
  - Editable installs  
  - setuptools backend  

- Fully configured PyPI Trusted Publisher (GitHub Actions workflow)  
- First-class Termux & Linux support  

### Changed
- N/A — first release.

### Fixed
- N/A — first release.

### Deprecated
- None.

### Removed
- None.

### Security
- API key validation checks (`JULES_API_KEY`)
- Warning on missing permissions (GitHub token)

---

# Future Versions (Planning)

## [1.1.0] – Planned
### Added
- Config file: `~/.config/jules/config.toml`
- Colorized terminal output  
- `--json` and `--debug` flags  
- Plugin loading system (alpha)

### Changed
- Improve patch recovery when conflicts occur  
- Faster API polling

### Fixed
- Placeholder

---

## [2.0.0] – Planned
### Added
- Local state database (SQLite) for caching:
  - session history  
  - patches  
  - logs  
- Multi-session management:

jules sessions jules resume <id>

- Structured logging across all CLI commands  
- Parallel task execution

### Changed
- REPL rewrite for performance  
- Git operations rewritten with async support

### Deprecated
- Older single-session architecture

---

## [3.0.0] – Planned
### Added
- AI-driven git merge conflict resolver  
- Local multi-agent backend (Gemini + Jules + third-party LLMs)  
- Deep repo reasoning mode (indexing & embedding)  
- Pull request stack creation

### Changed
- Full internal architecture redesign for plugin workflows

---

## [4.0.0] – Long-term Vision
### Added
- Autonomous engineering agent  
- Multi-repo orchestration  
- Full CI/CD agent capable of:
- test fixing  
- pipeline repair  
- release automation  

### Changed
- OS-native daemon: `julesd`  
- GUI interface (Electron/Tauri)  

---

# Versioning Notes

- Versions use **MAJOR.MINOR.PATCH**.  
- MAJOR increases for breaking changes.  
- MINOR for new features.  
- PATCH for fixes.

Every version increment requires:
- Git tag (`vX.Y.Z`)
- GitHub Action publish
- Entry added to this CHANGELOG  

---

# End of Changelog
