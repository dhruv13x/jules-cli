# tests/git/test_vcs.py

import pytest
from unittest.mock import patch, MagicMock, ANY
import os
from jules_cli.git.vcs import (
    git_current_branch,
    git_is_clean,
    git_create_branch_and_commit,
    git_push_branch,
    github_create_pr,
    GITHUB_TOKEN,
)
from jules_cli.utils.exceptions import GitError

@pytest.fixture(autouse=True)
def mock_run_cmd():
    with patch("jules_cli.git.vcs.run_cmd") as mock_cmd:
        yield mock_cmd

@pytest.fixture
def mock_requests_post():
    with patch("jules_cli.git.vcs.requests.post") as mock_post:
        yield mock_post

@pytest.fixture
def mock_github_token():
    with patch.dict(os.environ, {"GITHUB_TOKEN": "test_token"}, clear=True):
        yield

def test_git_current_branch_success(mock_run_cmd):
    mock_run_cmd.return_value = (0, "main\n", "")
    assert git_current_branch() == "main"
    mock_run_cmd.assert_called_once_with(["git", "rev-parse", "--abbrev-ref", "HEAD"])

def test_git_current_branch_failure(mock_run_cmd):
    mock_run_cmd.return_value = (1, "", "error")
    with pytest.raises(GitError, match="Failed to get current branch."):
        git_current_branch()
    mock_run_cmd.assert_called_once_with(["git", "rev-parse", "--abbrev-ref", "HEAD"])

def test_git_is_clean_true(mock_run_cmd):
    mock_run_cmd.return_value = (0, "", "")
    assert git_is_clean() is True
    mock_run_cmd.assert_called_once_with(["git", "status", "--porcelain"])

def test_git_is_clean_false(mock_run_cmd):
    mock_run_cmd.return_value = (0, " M file.txt\n", "")
    assert git_is_clean() is False
    mock_run_cmd.assert_called_once_with(["git", "status", "--porcelain"])

def test_git_is_clean_failure(mock_run_cmd):
    mock_run_cmd.return_value = (1, "", "error")
    with pytest.raises(GitError, match="Failed to get git status."):
        git_is_clean()
    mock_run_cmd.assert_called_once_with(["git", "status", "--porcelain"])

def test_git_create_branch_and_commit_success(mock_run_cmd):
    mock_run_cmd.side_effect = [
        (0, "", ""),  # checkout -b
        (0, "", ""),  # add -A
        (0, "", ""),  # commit -m
    ]
    git_create_branch_and_commit(commit_message="feat: new feature", branch_type="feature")
    assert mock_run_cmd.call_count == 3
    mock_run_cmd.assert_any_call(["git", "checkout", "-b", ANY], capture=False)
    mock_run_cmd.assert_any_call(["git", "add", "-A"], capture=False)
    mock_run_cmd.assert_any_call(["git", "commit", "-m", "feat: new feature"], capture=False)

def test_git_create_branch_and_commit_checkout_failure(mock_run_cmd):
    mock_run_cmd.return_value = (1, "", "checkout error")
    with pytest.raises(GitError, match="Failed to create branch: checkout error"):
        git_create_branch_and_commit()
    mock_run_cmd.assert_called_once()
    mock_run_cmd.assert_called_with(["git", "checkout", "-b", ANY], capture=False)

def test_git_create_branch_and_commit_add_failure(mock_run_cmd):
    mock_run_cmd.side_effect = [
        (0, "", ""),  # checkout -b success
        (1, "", "add error"),  # add -A failure
    ]
    with pytest.raises(GitError, match="Failed to add files: add error"):
        git_create_branch_and_commit()
    assert mock_run_cmd.call_count == 2
    mock_run_cmd.assert_any_call(["git", "checkout", "-b", ANY], capture=False)
    mock_run_cmd.assert_any_call(["git", "add", "-A"], capture=False)

def test_git_create_branch_and_commit_commit_failure(mock_run_cmd):
    mock_run_cmd.side_effect = [
        (0, "", ""),  # checkout -b success
        (0, "", ""),  # add -A success
        (1, "", "commit error"),  # commit -m failure
    ]
    with pytest.raises(GitError, match="Failed to commit changes: commit error"):
        git_create_branch_and_commit()
    assert mock_run_cmd.call_count == 3
    mock_run_cmd.assert_any_call(["git", "checkout", "-b", ANY], capture=False)
    mock_run_cmd.assert_any_call(["git", "add", "-A"], capture=False)
    mock_run_cmd.assert_any_call(["git", "commit", "-m", ANY], capture=False)

def test_git_push_branch_success(mock_run_cmd):
    mock_run_cmd.return_value = (0, "", "")
    git_push_branch("test-branch")
    mock_run_cmd.assert_called_once_with(["git", "push", "-u", "origin", "test-branch"], capture=False)

def test_git_push_branch_failure(mock_run_cmd):
    mock_run_cmd.return_value = (1, "", "push error")
    with pytest.raises(GitError, match="Failed to push branch: push error"):
        git_push_branch("test-branch")
    mock_run_cmd.assert_called_once_with(["git", "push", "-u", "origin", "test-branch"], capture=False)

def test_github_create_pr_no_token(mock_run_cmd):
    with patch.dict(os.environ, {"GITHUB_TOKEN": ""}, clear=True):
        with pytest.raises(GitError, match="GITHUB_TOKEN not set; cannot create PR automatically."):
            github_create_pr(owner="owner", repo="repo", head="head")

def test_github_create_pr_success(mock_requests_post, mock_github_token):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"html_url": "http://pr.url"}
    mock_requests_post.return_value = mock_response

    pr_url = github_create_pr(owner="owner", repo="repo", head="head", title="Test PR")
    assert pr_url == {"html_url": "http://pr.url"}
    mock_requests_post.assert_called_once()
    args, kwargs = mock_requests_post.call_args
    assert kwargs["json"]["head"] == "head"
    assert kwargs["json"]["title"] == "Test PR"
    assert kwargs["headers"]["Authorization"] == "token test_token"

def test_github_create_pr_failure(mock_requests_post, mock_github_token):
    mock_response = MagicMock()
    mock_response.status_code = 422
    mock_response.text = "Validation Failed"
    mock_requests_post.return_value = mock_response

    with pytest.raises(GitError, match="GitHub PR creation failed 422: Validation Failed"):
        github_create_pr(owner="owner", repo="repo", head="head")
    mock_requests_post.assert_called_once()

def test_github_create_pr_with_optional_fields(mock_requests_post, mock_github_token):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"html_url": "http://pr.url"}
    mock_requests_post.return_value = mock_response

    labels = ["bug", "enhancement"]
    reviewers = ["user1", "user2"]
    assignees = ["user3"]

    github_create_pr(
        owner="owner",
        repo="repo",
        head="head",
        body="PR body",
        draft=True,
        labels=labels,
        reviewers=reviewers,
        assignees=assignees,
    )
    mock_requests_post.assert_called_once()
    args, kwargs = mock_requests_post.call_args
    assert kwargs["json"]["body"] == "PR body"
    assert kwargs["json"]["draft"] is True
    assert kwargs["json"]["labels"] == labels
    assert kwargs["json"]["reviewers"] == reviewers
    assert kwargs["json"]["assignees"] == assignees
