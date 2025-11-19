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
- Runs pytest  
- Sends failures to the Jules API  
- Receives automated patches or PRs  
- Applies patches locally  
- Re-runs tests  
- Optional auto-push + auto-PR via GitHub

### 🤖 AI-Powered Development Assistant
Issue natural-language commands:

jules task "refactor the user login service" jules task "add test coverage for payment workflows" jules task "fix NullPointer bug in auth module"

Jules performs the work in a dedicated session and returns patches or PRs.

### 🔁 Stateful Interactive REPL
Run:

jules

And access a full command shell:

auto task "..." apply commit push pr create session list session show <id> last exit

### 🛠 GitHub Integration
- Auto-creates branches  
- Auto-commits and auto-pushes  
- Automatically creates PRs using `GITHUB_TOKEN`

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

## 💻 Development

### Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/dhruv13x/jules-cli
    cd jules-cli
    ```

2.  **Install dependencies:**
    It's recommended to use a virtual environment.
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    pip install -e .
    ```

### Running Tests
To run the test suite, use `pytest`:
```bash
python -m pytest
```

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
Runs pytest → detects failures → sends to Jules → applies patch or PR.

jules> auto

### 📝 `task "<instruction>"` – Tell Jules anything
Examples:

jules> task "refactor utils.py to remove duplicated logic" jules> task "add unit tests for create_dump function" jules> task "fix failing integration test for redis manager"

### 🩹 `apply` – Apply the last patch Jules returned

jules> apply

### 🌿 `commit` – Auto-create branch & commit patch

jules> commit

### 🚀 `push` – Push current branch

jules> push

### 🔗 `pr create` – Create GitHub pull request
Requires `GITHUB_TOKEN`.

jules> pr create

### 🔍 `session list` – View recent Jules sessions

jules> session list

### 📖 `session show <id>` – Inspect a session

jules> session show 1234567890

### 📦 `last` – Show last session + result

jules> last

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
│
├── src/
│   └── jules_cli/
│       ├── cli.py
│       └── __init__.py
│
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
