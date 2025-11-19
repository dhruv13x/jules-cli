# src/jules_cli/commands/pr.py

from typing import List
from ..state import _state
from ..git.vcs import git_current_branch, github_create_pr
import os
from ..utils.logging import logger
from ..cache import save_to_cache

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

def cmd_create_pr(
    title: str = "Automated fix from Jules CLI",
    body: str = "Auto PR",
    draft: bool = False,
    labels: List[str] = None,
    reviewers: List[str] = None,
    assignees: List[str] = None,
    issue: int = None,
):
    if not GITHUB_TOKEN:
        logger.error("GITHUB_TOKEN not set; cannot create PR.")
        return {"status": "error", "message": "GITHUB_TOKEN not set."}
    owner = _state.get("repo_owner"); repo = _state.get("repo_name")
    if not owner or not repo:
        logger.warning("No repo detected in state. Run a task first.")
        return {"status": "error", "message": "No repo detected in state."}
    # determine current branch to use as head
    head = git_current_branch()

    if issue:
        body += f"\n\nCloses #{issue}"

    try:
        pr = github_create_pr(
            owner,
            repo,
            head=head,
            base="main",
            title=title,
            body=body,
            draft=draft,
            labels=labels,
            reviewers=reviewers,
            assignees=assignees,
        )
        logger.info("Created PR: %s", pr.get("html_url"))

        # Cache the PR metadata
        cache_key = f"pr_{pr['number']}"
        save_to_cache(cache_key, pr)

        return pr
    except Exception as e:
        logger.error("Failed to create PR: %s", e)
        return {"status": "error", "message": f"Failed to create PR: {e}"}
