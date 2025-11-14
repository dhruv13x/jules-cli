from ..state import _state
from ..git.vcs import git_current_branch, github_create_pr
import os

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def cmd_create_pr():
    if not GITHUB_TOKEN:
        print("GITHUB_TOKEN not set; cannot create PR.")
        return
    owner = _state.get("repo_owner"); repo = _state.get("repo_name")
    if not owner or not repo:
        print("No repo detected in state. Run a task first.")
        return
    # determine current branch to use as head
    head = git_current_branch()
    try:
        pr = github_create_pr(owner, repo, head=head, base="main", title="Automated fix from Jules CLI", body="Auto PR")
        print("Created PR:", pr.get("html_url"))
    except Exception as e:
        print("Failed to create PR:", e)
