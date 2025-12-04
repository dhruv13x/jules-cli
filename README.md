<div align="center">
  <img src="https://raw.githubusercontent.com/dhruv13x/jules-cli/main/jules-cli_logo.png" alt="jules-cli logo" width="200"/>
</div>

<div align="center">

<!-- Package Info -->
[![PyPI version](https://img.shields.io/pypi/v/jules-cli.svg)](https://pypi.org/project/jules-cli/)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://www.python.org/)
![Wheel](https://img.shields.io/pypi/wheel/jules-cli.svg)
[![Release](https://img.shields.io/badge/release-PyPI-blue)](https://pypi.org/project/jules-cli/)

<!-- Build & Quality -->
[![Build status](https://github.com/dhruv13x/jules-cli/actions/workflows/publish.yml/badge.svg)](https://github.com/dhruv13x/jules-cli/actions/workflows/publish.yml)
[![Codecov](https://codecov.io/gh/dhruv13x/jules-cli/graph/badge.svg)](https://codecov.io/gh/dhruv13x/jules-cli)
[![Test Coverage](https://img.shields.io/badge/coverage-90%25%2B-brightgreen.svg)](https://github.com/dhruv13x/jules-cli/actions/workflows/test.yml)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Ruff](https://img.shields.io/badge/linting-ruff-yellow.svg)](https://github.com/astral-sh/ruff)
![Security](https://img.shields.io/badge/security-CodeQL-blue.svg)

<!-- Usage -->
![Downloads](https://img.shields.io/pypi/dm/jules-cli.svg)
[![PyPI Downloads](https://img.shields.io/pypi/dm/jules-cli.svg)](https://pypistats.org/packages/jules-cli)
![OS](https://img.shields.io/badge/os-Linux%20%7C%20macOS%20%7C%20Windows-blue.svg)
[![Python Versions](https://img.shields.io/pypi/pyversions/jules-cli.svg)](https://pypi.org/project/jules-cli/)

<!-- License -->
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

# jules-cli

A fully automated **developer assistant CLI** built on the **Jules API** (Google’s experimental code automation system).  
`jules-cli` lets you run tests, fix bugs, apply patches, refactor code, and even create GitHub pull requests — all from your terminal.

Designed for real-world workflows, CI pipelines, and local debugging sessions.

---

## 🚀 Quick Start (User View)

### Prerequisites
- Python 3.8+
- `pip`

### One-command installation
```bash
pip install jules-cli
```

### Usage Example
```bash
# Initialize and setup API keys
jules init

# Fix tests automatically
jules auto
```

---

## ✨ Key Features

- **God Level: Proactive Suggestions**: `jules suggest` scans your codebase to identify security holes, missing tests, and technical debt before they become problems.
- **God Level: Automated Test Fixer**: `jules auto` runs pytest, sends failures to the API, and autonomously applies fixes.
- **AI-Powered Development Assistant**: Issue natural-language commands to refactor code, add test coverage, or fix bugs (`jules task`).
- **Stateful Interactive REPL**: Chat with your codebase in real-time (`jules interact`).
- **Workspace Automation**: Manage multi-repo workflows with `jules workspace run`.
- **GitHub Integration**: Automatically create branches, commits, and pull requests (`jules pr create`).
- **Secure Credential Storage**: Safely stores API keys in your system keyring (`jules auth login`) instead of plain text files.
- **Self-Update Mechanism**: Keep your CLI up-to-date with `jules upgrade`.
- **Context Management**: Use `.julesignore` to filter out sensitive files (like `.env`, `node_modules/`) from being sent to the AI.

---

## ⚙️ Configuration & Advanced Usage (Dev View)

### Environment Variables
- `JULES_API_KEY`: Your Jules API key.
- `GITHUB_TOKEN`: Your GitHub token for PR creation.

### CLI/API Table

| Command | Description | Arguments | Options |
| --- | --- | --- | --- |
| `init` | Interactive setup wizard. | | |
| `auth login` | Interactively set API keys securely. | | |
| `config get/set`| Manage configuration values. | `key`, `value` | |
| `config list` | List all configuration. | | |
| `auto` | Run pytest and auto-fix failures. | | |
| `testgen` | Generate tests for a given file. | `file_path` | `--type, -t` |
| `refactor` | Run a repository-wide refactor. | `instruction` | |
| `task` | Ask Jules to perform an arbitrary dev task. | `prompt` | |
| `suggest` | Proactively scan and suggest improvements. | | `--focus, -f`, `--security`, `--tests`, `--chore` |
| `interact` | Start an interactive chat session. | `prompt` | |
| `workspace run` | Run command across multiple repos. | `command` | |
| `approve` | Approve the plan for the current session. | `session_id` | |
| `reject` | Reject the plan for the current session. | `session_id` | |
| `session list` | List sessions. | | |
| `session show` | Show session details. | `session_id` | |
| `history list` | List all sessions. | | |
| `history view` | Show session details by id. | `session_id` | |
| `apply` | Apply last patch received. | | |
| `commit` | Commit & create branch after apply. | | `--message, -m`, `--type, -t` |
| `push` | Push branch to origin. | | |
| `pr create` | Create a GitHub PR from last branch. | | `--title`, `--body`, `--draft`, `--labels`, `--reviewers` |
| `stage` | Interactively stage changes. | | |
| `doctor` | Run environment validation checks. | | |
| `upgrade` | Self-update the Jules CLI. | | |

---

## 🏗️ Architecture

```
jules-cli/
│
├── src/
│   └── jules_cli/
│       ├── commands/
│       │   ├── auto.py
│       │   ├── task.py
│       │   ├── suggest.py
│       │   ├── interact.py
│       │   ├── workspace.py
│       │   └── ...
│       ├── core/          # Jules API interaction
│       ├── git/           # Git utilities
│       ├── patch/         # Patch application logic
│       ├── pytest/        # Test integration
│       ├── utils/         # Shared helpers (logging, config)
│       ├── cli.py         # Main entry point (Typer app)
│       └── __init__.py
│
├── tests/
├── pyproject.toml
└── README.md
```

The `jules-cli` is a Python-based command-line interface powered by the `typer` library. The core logic is organized into several modules within the `src/jules_cli` directory. `cli.py` serves as the main entry point, aggregating sub-commands from the `commands/` directory. The application uses a global state (`_state`) to manage session data across commands and secure storage (`keyring`) for credentials.

---

## 🗺️ Roadmap

### Upcoming
- **Multi-repo workspace automation**: Enhanced support for managing dependencies across multiple repositories.
- **AI-powered merge conflict resolver**: Intelligent conflict resolution strategies.
- **Spec-First Mode**: Generate specs, then code, then tests.

### Completed
- **Automated test fixer**: `jules auto`
- **Proactive Suggestions**: `jules suggest`
- **Interactive REPL**: `jules interact`
- **GitHub Integration**: `jules pr create`
- **Secure Auth**: Keyring integration.
- **Self-Updates**: `jules upgrade`

---

## 🤝 Contributing & License

Contributions, bug reports, and feature requests are welcome. Please refer to the `FEATURE_PROPOSAL_TEMPLATE` for more information.

This project is licensed under the MIT License. See `LICENSE` for details.
