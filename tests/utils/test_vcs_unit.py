import pytest
from unittest.mock import patch, MagicMock
from jules_cli.git import vcs
from jules_cli.utils.exceptions import GitError

@patch("jules_cli.git.vcs.run_cmd")
def test_git_current_branch_success(mock_run):
    mock_run.return_value = (0, "main\n", "")
    assert vcs.git_current_branch() == "main"

@patch("jules_cli.git.vcs.run_cmd")
def test_git_current_branch_failure(mock_run):
    mock_run.return_value = (1, "", "error")
    with pytest.raises(GitError):
        vcs.git_current_branch()

@patch("jules_cli.git.vcs.run_cmd")
def test_git_is_clean_true(mock_run):
    mock_run.return_value = (0, "", "")
    assert vcs.git_is_clean()

@patch("jules_cli.git.vcs.run_cmd")
def test_git_is_clean_false(mock_run):
    mock_run.return_value = (0, "M file.txt", "")
    assert not vcs.git_is_clean()

@patch("jules_cli.git.vcs.run_cmd")
def test_git_is_clean_failure(mock_run):
    mock_run.return_value = (1, "", "error")
    with pytest.raises(GitError):
        vcs.git_is_clean()

@patch("jules_cli.git.vcs.run_cmd")
def test_git_get_remote_repo_info_ssh(mock_run):
    mock_run.return_value = (0, "git@github.com:owner/repo.git\n", "")
    assert vcs.git_get_remote_repo_info() == ("owner", "repo")

@patch("jules_cli.git.vcs.run_cmd")
def test_git_get_remote_repo_info_https(mock_run):
    mock_run.return_value = (0, "https://github.com/owner/repo.git\n", "")
    assert vcs.git_get_remote_repo_info() == ("owner", "repo")

@patch("jules_cli.git.vcs.run_cmd")
def test_git_get_remote_repo_info_failure(mock_run):
    mock_run.return_value = (1, "", "error")
    assert vcs.git_get_remote_repo_info() == (None, None)

@patch("jules_cli.git.vcs.run_cmd")
def test_git_get_remote_repo_info_invalid(mock_run):
    mock_run.return_value = (0, "invalid_url", "")
    assert vcs.git_get_remote_repo_info() == (None, None)

@patch("jules_cli.git.vcs.run_cmd")
def test_git_create_branch_and_commit_success(mock_run):
    mock_run.return_value = (0, "", "")
    vcs.git_create_branch_and_commit("fix: bug", "fix")
    assert mock_run.call_count == 3 # checkout, add, commit

@patch("jules_cli.git.vcs.run_cmd")
def test_git_create_branch_and_commit_checkout_fail(mock_run):
    mock_run.side_effect = [(1, "", "error"), (0, "", ""), (0, "", "")]
    with pytest.raises(GitError):
        vcs.git_create_branch_and_commit()

@patch("jules_cli.git.vcs.run_cmd")
def test_git_create_branch_and_commit_add_fail(mock_run):
    mock_run.side_effect = [(0, "", ""), (1, "", "error"), (0, "", "")]
    with pytest.raises(GitError):
        vcs.git_create_branch_and_commit()

@patch("jules_cli.git.vcs.run_cmd")
def test_git_create_branch_and_commit_commit_fail(mock_run):
    mock_run.side_effect = [(0, "", ""), (0, "", ""), (1, "", "error")]
    with pytest.raises(GitError):
        vcs.git_create_branch_and_commit()

@patch("jules_cli.git.vcs.run_cmd")
def test_git_push_branch_success(mock_run):
    mock_run.return_value = (0, "", "")
    vcs.git_push_branch("branch")
    mock_run.assert_called_once()

@patch("jules_cli.git.vcs.run_cmd")
def test_git_push_branch_failure(mock_run):
    mock_run.return_value = (1, "", "error")
    with pytest.raises(GitError):
        vcs.git_push_branch("branch")

@patch("requests.post")
def test_github_create_pr_success(mock_post, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "token")
    mock_post.return_value.status_code = 201
    mock_post.return_value.json.return_value = {"url": "pr_url"}

    result = vcs.github_create_pr("owner", "repo", "head")
    assert result["url"] == "pr_url"

@patch("requests.post")
def test_github_create_pr_failure(mock_post, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "token")
    mock_post.return_value.status_code = 400
    mock_post.return_value.text = "error"

    with pytest.raises(GitError):
        vcs.github_create_pr("owner", "repo", "head")

def test_github_create_pr_no_token(monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    with pytest.raises(GitError):
        vcs.github_create_pr("owner", "repo", "head")

@patch("requests.post")
def test_github_create_pr_with_extras(mock_post, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "token")
    mock_post.return_value.status_code = 201

    vcs.github_create_pr("owner", "repo", "head", labels=["bug"], reviewers=["user"], assignees=["user"])

    kwargs = mock_post.call_args[1]
    data = kwargs["json"]
    assert data["labels"] == ["bug"]
    assert data["reviewers"] == ["user"]
    assert data["assignees"] == ["user"]
