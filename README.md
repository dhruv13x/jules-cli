# jules-cli

[![PyPI Version](https://img.shields.io/pypi/v/jules-cli.svg)](https://pypi.org/project/jules-cli/)
![Python Versions](https://img.shields.io/pypi/pyversions/jules-cli)
[![License](https://img.shields.io/github/license/dhruv13x/jules-cli)](LICENSE)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/dhruv13x/jules-cli/publish.yml?label=PyPI%20Publish)](https://github.com/dhruv13x/jules-cli/actions)

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
jules auto
```
---

## ✨ Key Features

- **Automated Test Fixer**: Runs pytest, sends failures to the Jules API, receives automated patches, applies them locally, and re-runs tests.
- **AI-Powered Development Assistant**: Issue natural-language commands to refactor code, add test coverage, or fix bugs.
- **Stateful Interactive REPL**: Access a full command shell for an immersive development experience.
- **GitHub Integration**: Automatically create branches, commits, and pull requests.
- **Trusted Auth**: Uses Google's Jules API with the `X-Goog-Api-Key` header for secure and isolated sessions.

---

## ⚙️ Configuration & Advanced Usage (Dev View)

### Environment Variables
- `JULES_API_KEY`: Your Jules API key.
- `GITHUB_TOKEN`: Your GitHub token for PR creation.

### CLI/API Table

| Command | Description | Arguments | Options |
| --- | --- | --- | --- |
| `auto` | Run pytest and auto-fix failures. | | |
| `testgen` | Generate tests for a given file. | `file_path` | `--type, -t` |
| `refactor` | Run a repository-wide refactor. | `instruction` | |
| `task` | Ask Jules to perform an arbitrary dev task. | `prompt` | |
| `approve` | Approve the plan for the current or specified session. | `session_id` | |
| `reject` | Reject the plan for the current or specified session. | `session_id` | |
| `session list` | List sessions. | | |
| `session show` | Show session details. | `session_id` | |
| `history list` | List all sessions. | | |
| `history view` | Show session details by id. | `session_id` | |
| `apply` | Apply last patch received. | | |
| `commit` | Commit & create branch after apply. | | `--message, -m`, `--type, -t` |
| `push` | Push branch to origin. | | |
| `pr create` | Create a GitHub PR from last branch. | | `--title, -t`, `--body, -b`, `--draft`, `--labels, -l`, `--reviewers, -r`, `--assignees, -a`, `--issue, -i` |
| `stage` | Interactively stage changes. | | |
| `doctor` | Run environment validation checks. | | |
| `suggest` | Proactively scan the codebase and suggest improvements. | | `--focus, -f`, `--security`, `--tests`, `--chore` |
| `interact` | Start an interactive chat session with Jules. | `prompt` | |

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
│       │   └── ...
│       ├── core/
│       ├── git/
│       ├── patch/
│       ├── pytest/
│       ├── utils/
│       ├── cli.py
│       ├── __init__.py
│       └── ...
│
├── tests/
├── pyproject.toml
└── README.md
```

The `jules-cli` is a Python-based command-line interface powered by the `typer` library. The core logic is organized into several modules within the `src/jules_cli` directory, including `commands` for CLI command definitions, `core` for Jules API interaction, `git` for Git utilities, `patch` for patch management, `pytest` for test integration, and `utils` for shared helpers. The main entry point of the application is `cli.py`, which defines the CLI commands and their arguments.

---

## 🗺️ Roadmap

### Upcoming
- Multi-repo workspace automation
- AI-powered merge conflict resolver

### Completed
- Automated test fixer
- AI-powered development assistant
- Stateful interactive REPL
- GitHub integration

---

## 🤝 Contributing & License

Contributions, bug reports, and feature requests are welcome. Please refer to the `FEATURE_PROPOSAL_TEMPLATE` for more information.

This project is licensed under the MIT License. See `LICENSE` for details.
