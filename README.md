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

- ** automated Test Fixer**: Automatically runs `pytest`, sends failures to the Jules API, applies the returned patch, and re-runs tests to verify the fix.
- ** natural-language tasks**: Issue plain-English commands to refactor code, add test coverage, or fix complex bugs.
- ** Interactive REPL**: An immersive shell with command history, stateful sessions, and a streamlined workflow.
- ** full Git Integration**: Automatically creates branches, commits, and pushes patches.
- ** GitHub Workflow**: Creates and manages GitHub Pull Requests with a single command.
- ** secure and simple Auth**: Uses Google's `X-Goog-Api-Key` for trusted, hassle-free authentication.
- ** local and CI/CD**: Built for both local debugging and fully automated CI/CD pipelines.

---

## 📦 Installation & Setup

**1. Install via PyPI**
```bash
pip install jules-cli
```
*Or install from source (for development):*
```bash
git clone https://github.com/dhruv13x/jules-cli
cd jules-cli
pip install -e .
```
**2. Set your API Key**
```bash
export JULES_API_KEY="your_api_key_here"
```
**3. Set your GitHub Token** (Optional, for creating PRs)
```bash
export GITHUB_TOKEN="ghp_xxx"
```
**4. Configure Git** (Optional, for local commits)
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

---
## 🧪 Usage
**1. Open the REPL**
```bash
jules
```
This launches the interactive shell.
**2. Run a command**
```bash
jules> auto
```
Jules will automatically run `pytest`, fix failures, and apply patches.
## 📘 Command Guide
| Command | Description |
|---|---|
| `auto` | **fully automated test fixer**. Runs `pytest`, sends failures to Jules, and applies patches. |
| `task "<instruction>"` | **send any instruction to jules**. |
| `apply` | **apply the last patch** returned by the API. |
| `commit` | **create a new branch** and commit the current patch. |
| `push` | **push the branch** to the remote repository. |
| `pr create` | **create a pull request** on GitHub. |
| `session list` | **list all sessions** in the current context. |
| `session show <id>` | **show session details** including logs and patches. |
| `last` | **show the last session** and its result. |
| `exit` | **exit the REPL**. |

---

## 💡 Example Workflow

A common workflow for fixing a test failure:
```bash
# 1. Start the interactive REPL
jules

# 2. Run the automated test-fixer
jules> auto

# 3. Apply the patch returned by Jules
jules> apply

# 4. Create a new branch and commit the changes
jules> commit

# 5. Push the branch and create a PR
jules> push
jules> pr create
```

---

## 🏗️ Project Structure
```
jules-cli/
├── src/
│   └── jules_cli/
│       ├── commands/     # Command handlers
│       ├── core/         # Core API client and services
│       ├── git/          # Git and GitHub utilities
│       ├── patch/        # Patch management
│       ├── pytest/       # Pytest integration
│       ├── utils/        # Shared helpers
│       ├── cli.py        # Main Typer app
│       ├── cache.py      # Caching logic
│       ├── db.py         # Database interaction
│       └── state.py      # Global state management
├── tests/                # Unit and integration tests
├── .github/              # GitHub Actions workflows
├── pyproject.toml        # Project metadata and dependencies
└── README.md
```

---

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 🛡️ License

This project is licensed under the **MIT License**. See the [LICENSE](LICENSE) file for details.

## 💬 Get Help

- **Open an Issue**: If you find a bug or have a feature request, please [open an issue](https://github.com/dhruv13x/jules-cli/issues).
- **Community**: Join our community channel (link pending) for discussions.

## 🔭 Vision

Our vision is to make `jules-cli` the go-to developer assistant for automating tedious and time-consuming tasks. We believe that by integrating powerful AI into the command line, we can help developers focus on what matters most: building great software.

---
