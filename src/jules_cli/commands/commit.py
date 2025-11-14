import time
from ..git.vcs import git_create_branch_and_commit, git_push_branch

def cmd_commit_and_push():
    # create branch with timestamp
    ts = int(time.time())
    branch = f"jules/auto-{ts}"
    try:
        git_create_branch_and_commit(branch, commit_message="chore: automated changes from Jules")
    except Exception as e:
        print("Failed to commit:", e)
        return
    try:
        git_push_branch(branch)
        print(f"Pushed branch {branch}")
    except Exception as e:
        print("Failed to push automatically:", e)
        print(f"Run: git push origin {branch}")
