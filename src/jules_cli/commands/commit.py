import time
from ..git.vcs import git_create_branch_and_commit, git_push_branch
from ..utils.logging import logger

def cmd_commit_and_push():
    # create branch with timestamp
    ts = int(time.time())
    branch = f"jules/auto-{ts}"
    try:
        git_create_branch_and_commit(branch, commit_message="chore: automated changes from Jules")
    except Exception as e:
        logger.error("Failed to commit: %s", e)
        return
    try:
        git_push_branch(branch)
        logger.info(f"Pushed branch {branch}")
    except Exception as e:
        logger.error("Failed to push automatically: %s", e)
        logger.info(f"Run: git push origin {branch}")
