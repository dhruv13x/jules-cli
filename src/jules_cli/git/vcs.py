import os
import requests
from ..utils.commands import run_cmd

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def git_current_branch() -> str:
    code, out, _ = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    return out.strip() if code == 0 else "main"

def git_create_branch_and_commit(branch_name: str, commit_message: str = "jules: automated fix"):
    run_cmd(["git", "checkout", "-b", branch_name], capture=False)
    run_cmd(["git", "add", "-A"], capture=False)
    run_cmd(["git", "commit", "-m", commit_message], capture=False)

def git_push_branch(branch_name: str):
    run_cmd(["git", "push", "-u", "origin", branch_name], capture=False)

def github_create_pr(owner: str, repo: str, head: str, base: str = "main", title: str = None, body: str = None):
    if not GITHUB_TOKEN:
        raise RuntimeError("GITHUB_TOKEN not set; cannot create PR automatically.")
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    data = {"head": head, "base": base, "title": title or "Automated fix from Jules CLI", "body": body or ""}
    resp = requests.post(url, headers=headers, json=data, timeout=30)
    if resp.status_code >= 400:
        raise RuntimeError(f"GitHub PR creation failed {resp.status_code}: {resp.text}")
    return resp.json()
