import os
import time
import requests
from slugify import slugify
from ..utils.commands import run_cmd
from ..utils.exceptions import GitError
from ..utils.config import config

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def git_current_branch() -> str:
    code, out, _ = run_cmd(["git", "rev-parse", "--abbrev-ref", "HEAD"])
    if code != 0:
        raise GitError("Failed to get current branch.")
    return out.strip()

def git_create_branch_and_commit(
    commit_message: str = "jules: automated fix",
    branch_type: str = "feature",
):

    slug = slugify(commit_message)
    ts = int(time.time())
    branch_name = f"{branch_type}/{slug}-{ts}"

    code, _, err = run_cmd(["git", "checkout", "-b", branch_name], capture=False)
    if code != 0:
        raise GitError(f"Failed to create branch: {err}")
    code, _, err = run_cmd(["git", "add", "-A"], capture=False)
    if code != 0:
        raise GitError(f"Failed to add files: {err}")
    code, _, err = run_cmd(["git", "commit", "-m", commit_message], capture=False)
    if code != 0:
        raise GitError(f"Failed to commit changes: {err}")


def git_push_branch(branch_name: str):
    code, _, err = run_cmd(["git", "push", "-u", "origin", branch_name], capture=False)
    if code != 0:
        raise GitError(f"Failed to push branch: {err}")

def github_create_pr(
    owner: str,
    repo: str,
    head: str,
    base: str = "main",
    title: str = None,
    body: str = None,
    draft: bool = False,
    labels: list = None,
    reviewers: list = None,
    assignees: list = None,
):
    if not GITHUB_TOKEN:
        raise GitError("GITHUB_TOKEN not set; cannot create PR automatically.")
    url = f"https://api.github.com/repos/{owner}/{repo}/pulls"
    headers = {"Authorization": f"token {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    data = {
        "head": head,
        "base": base,
        "title": title or "Automated fix from Jules CLI",
        "body": body or "",
        "draft": draft,
    }

    if labels:
        data["labels"] = labels
    if reviewers:
        data["reviewers"] = reviewers
    if assignees:
        data["assignees"] = assignees

    resp = requests.post(url, headers=headers, json=data, timeout=30)
    if resp.status_code >= 400:
        raise GitError(f"GitHub PR creation failed {resp.status_code}: {resp.text}")
    return resp.json()
