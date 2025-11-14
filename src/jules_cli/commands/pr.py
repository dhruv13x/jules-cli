from ..state import _state
from ..git.vcs import git_current_branch, github_create_pr
import os
from ..utils.logging import logger

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def cmd_create_pr():
    if not GITHUB_TOKEN:
        logger.error("GITHUB_TOKEN not set; cannot create PR.")
        return {"status": "error", "message": "GITHUB_TOKEN not set."}
    owner = _state.get("repo_owner"); repo = _state.get("repo_name")
    if not owner or not repo:
        logger.warning("No repo detected in state. Run a task first.")
        return {"status": "error", "message": "No repo detected in state."}
    # determine current branch to use as head
    head = git_current_branch()
    try:
        pr = github_create_pr(owner, repo, head=head, base="main", title="Automated fix from Jules CLI", body="Auto PR")
        logger.info("Created PR: %s", pr.get("html_url"))
        return pr
    except Exception as e:
        logger.error("Failed to create PR: %s", e)
        return {"status": "error", "message": f"Failed to create PR: {e}"}
