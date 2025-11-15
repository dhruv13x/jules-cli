
import os
import pytest
from unittest.mock import patch

# We need to patch the GITHUB_TOKEN before importing the vcs module
with patch.dict(os.environ, {"GITHUB_TOKEN": "test-token"}):
    from jules_cli.git.vcs import git_create_branch_and_commit, git_current_branch, github_create_pr

@patch("jules_cli.git.vcs.run_cmd")
def test_git_create_branch_and_commit_semantic_branch(mock_run_cmd):
    mock_run_cmd.return_value = (0, "", "")

    with patch("time.time", return_value=12345):
        git_create_branch_and_commit(
            commit_message="fix: resolve critical bug in auth module",
            branch_type="fix",
        )

    # Corrected assertion: Check the actual call to git checkout
    branch_name_arg = mock_run_cmd.call_args_list[0][0][0][3]
    assert branch_name_arg.startswith("fix/fix-resolve-critical-bug-in-auth-module-")

    # Also check the commit message
    commit_message_arg = mock_run_cmd.call_args_list[2][0][0][3]
    assert commit_message_arg == "fix: resolve critical bug in auth module"

@patch("jules_cli.git.vcs.run_cmd")
def test_git_current_branch(mock_run_cmd):
    mock_run_cmd.return_value = (0, "my-branch", "")
    branch = git_current_branch()
    assert branch == "my-branch"

@patch("jules_cli.git.vcs.requests.post")
def test_github_create_pr(mock_post):
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {"html_url": "http://pr.url"}
    pr = github_create_pr(
        owner="test-owner",
        repo="test-repo",
        head="my-branch",
    )
    assert pr["html_url"] == "http://pr.url"

@patch("jules_cli.git.vcs.requests.post")
def test_github_create_pr_fails(mock_post):
    mock_post.return_value.status_code = 400
    with pytest.raises(Exception):
        github_create_pr(
            owner="test-owner",
            repo="test-repo",
            head="my-branch",
        )
