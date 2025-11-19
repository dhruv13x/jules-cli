# jules-cli

[![PyPI Version](https://img.shields.io/pypi/v/jules-cli.svg)](https://pypi.org/project/jules-cli/)
![Python Versions](https://img.shields.io/pypi/pyversions/jules-cli)
[![License](https://img.shields.io/github/license/dhruv13x/jules-cli)](LICENSE)
[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/dhruv13x/jules-cli/publish.yml?label=PyPI%20Publish)](https://github.com/dhruv13x/jules-cli/actions)

A fully automated **developer assistant CLI** built on the **Jules API** (Google’s experimental code automation system).
`jules-cli` lets you run tests, fix bugs, apply patches, refactor code, and even create GitHub pull requests — all from your terminal.

Designed for real-world workflows, CI pipelines, and local debugging sessions.

---

## 🚀 Features

### 🔧 Automated Test Fixer
- Runs pytest and sends failures to the Jules API for automated patch generation.
- Applies patches, re-runs tests, and creates GitHub PRs automatically.

### ✨ AI-Powered Code Generation & Refactoring
- **`task`**: Give Jules natural-language instructions to perform any development task.
  `jules task "add a --verbose flag"`
- **`refactor`**: Perform repository-wide code improvements.
  `jules refactor "simplify the error handling in lib/utils.py"`
- **`testgen`**: Generate unit tests for your code.
  `jules testgen src/auth.py --type missing`

### 🔁 Stateful Interactive REPL
- Run `jules` to enter an interactive shell with command history and stateful operations.
- Chain commands like `auto`, `apply`, `commit`, and `pr create` in a seamless workflow.

### 🛠️ Full Git & GitHub Integration
- **`stage`**: Interactively stage file changes.
- **`commit`**: Automatically create branches and commit applied patches.
- **`pr create`**: Create detailed GitHub pull requests with labels, reviewers, and assignees.
- **`workspace`**: Manage multi-repository projects (coming soon).

### 📖 Session & History Management
- **`session`**: List and inspect active Jules sessions.
- **`history`**: Review past activity, including prompts, patches, and PRs.


### 🔐 Trusted Auth
Uses Google's **Jules API** with the `X-Goog-Api-Key` header.  
Secure, isolated, and simple.

---

## 📦 Installation

### From PyPI (recommended)

pip install jules-cli

### From source (editable)

git clone https://github.com/dhruv13x/jules-cli cd jules-cli pip install -e .

---

## ⚙️ Environment Setup

Before using the CLI, set:

### **1. Jules API Key**

export JULES_API_KEY="your_key_here"

### **2. GitHub Token (optional, for PR creation)**

export GITHUB_TOKEN="ghp_xxx..."

(Optional) Set your Git identity:

git config --global user.name "Your Name" git config --global user.email "you@example.com"

---

## 🧪 Usage

### Open the REPL

jules

You’ll see:

Jules Interactive CLI — fully immersive developer assistant.

Commands: auto task "instruction" apply commit push pr create session list ...

---

## 📘 Command Guide

### 🔥 `auto` – Automatic pytest debugging
Runs `pytest`, detects failures, sends them to Jules, and applies the returned patch.

`jules> auto`

### 📝 `task "<instruction>"` – Run any development task
Instruct Jules to perform a bug fix, refactor, or add new functionality.

`jules> task "refactor utils.py to remove duplicated logic"`
`jules> task "add unit tests for the create_dump function"`

### 🔬 `testgen "<file_path>"` – Generate unit tests
Create new tests for a specific file.

`jules> testgen src/api/handlers.py --type missing`

### 🏗️ `refactor "<instruction>"` – Refactor code
Perform a repository-wide refactor.

`jules> refactor "simplify error handling throughout the codebase"`

### 🩹 `apply` – Apply the last patch
Applies the most recent patch returned by Jules.

`jules> apply`

### 🌿 `commit` – Create a branch and commit changes
Commits the applied patch to a new branch.

`jules> commit -m "feat: implement user authentication" -t feature`

### 🚀 `push` – Push the current branch
Pushes the current branch to the remote repository.

`jules> push`

### 🔗 `pr create` – Create a GitHub pull request
Creates a GitHub PR from the current branch. Requires a `GITHUB_TOKEN`.

`jules> pr create --title "feat: new login flow" --labels bug,frontend`

### 📖 `history list` – View command history
Lists all past sessions from the local database.

`jules> history list`

### 📜 `history view <session_id>` – Inspect a session
Shows detailed information for a specific session.

`jules> history view 1234567890`

### 📦 `stage` – Interactively stage changes
Allows you to interactively select and stage file changes before committing.

`jules> stage`

### 🩺 `doctor` – Run environment checks
Validates your environment to ensure all dependencies and configurations are correct.

`jules> doctor`

---

## 🧩 Example Workflow

### Fix test failure automatically
```bash
jules
jules> auto
jules> apply
jules> commit
jules> push
jules> pr create

Request refactor

jules> task "Refactor bot_platform/init_manager for clarity"
jules> apply

Add tests

jules> task "Add pytest tests for projectclone cli"


---

🏗 Project Structure

jules-cli/
├── src/
│   └── jules_cli/
│       ├── cli.py          # Main CLI entrypoint
│       ├── commands/       # Subcommand logic
│       ├── core/           # Jules API client
│       ├── git/            # Git and VCS utilities
│       ├── patch/          # Patch application logic
│       ├── pytest/         # Pytest integration
│       ├── utils/          # Shared helpers
│       ├── db.py           # Database management
│       ├── state.py        # Global state
│       └── __init__.py
│
├── tests/                  # Test suite
├── pyproject.toml
├── README.md
└── .github/workflows/publish.yml


---

🔄 Release Workflow (PyPI Trusted Publisher)

To publish a new version:

1. Update version in pyproject.toml

version = "1.1.0"

2. Commit and push

git add .
git commit -m "Release 1.1.0"
git push

3. Create tag

git tag v1.1.0
git push origin v1.1.0

GitHub Actions will automatically build & publish to PyPI.


---

🛡 License

This project is licensed under the MIT License.
See LICENSE for details.


---

🤝 Contributing

Contributions, bug reports, and feature requests are welcome.

1. Fork the repo


2. Create a feature branch


3. Add your changes


4. Submit a PR




---

⭐ Support the Project

If you like this tool:

⭐ Star the repo

🗣 Share ideas

🧪 Open issues and feature requests



---

💬 Feedback Welcome

Feel free to open an issue or reach out anytime — the goal is to make jules-cli the most powerful local automation assistant for developers.

---
