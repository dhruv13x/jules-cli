from unittest.mock import patch, MagicMock, call
from src.jules_cli.git import vcs
from src.jules_cli.utils.exceptions import GitError

@patch('src.jules_cli.git.vcs.run_cmd')
def test_git_current_branch_success(mock_run_cmd):
    mock_run_cmd.return_value = (0, "my-branch", "")
    branch = vcs.git_current_branch()
    assert branch == "my-branch"
    mock_run_cmd.assert_called_once_with(["git", "rev-parse", "--abbrev-ref", "HEAD"])

@patch('src.jules_cli.git.vcs.run_cmd', return_value=(1, "", "error"))
def test_git_current_branch_error(mock_run_cmd):
    with patch.object(vcs, 'run_cmd', return_value=(1, "", "error")):
        try:
            vcs.git_current_branch()
        except GitError as e:
            assert "Failed to get current branch" in str(e)

@patch('src.jules_cli.git.vcs.run_cmd')
@patch('time.time', return_value=12345)
def test_git_create_branch_and_commit_success(mock_time, mock_run_cmd):
    mock_run_cmd.return_value = (0, "", "")
    vcs.git_create_branch_and_commit("new-branch")
    expected_calls = [
        call(['git', 'checkout', '-b', 'jules/auto-12345'], capture=False),
        call(['git', 'add', '-A'], capture=False),
        call(['git', 'commit', '-m', 'jules: automated fix'], capture=False)
    ]
    mock_run_cmd.assert_has_calls(expected_calls)

@patch('src.jules_cli.git.vcs.run_cmd', return_value=(1, "", "error"))
def test_git_create_branch_and_commit_error(mock_run_cmd):
    with patch.object(vcs, 'run_cmd', return_value=(1, "", "error")):
        with patch('time.time', return_value=12345):
            try:
                vcs.git_create_branch_and_commit("new-branch")
            except GitError as e:
                assert "Failed to create branch" in str(e)

@patch('src.jules_cli.git.vcs.run_cmd')
def test_git_push_branch_success(mock_run_cmd):
    mock_run_cmd.return_value = (0, "", "")
    vcs.git_push_branch("my-branch")
    mock_run_cmd.assert_called_with(["git", "push", "-u", "origin", "my-branch"], capture=False)

@patch('src.jules_cli.git.vcs.run_cmd', return_value=(1, "", "error"))
def test_git_push_branch_error(mock_run_cmd):
    with patch.object(vcs, 'run_cmd', return_value=(1, "", "error")):
        try:
            vcs.git_push_branch("my-branch")
        except GitError as e:
            assert "Failed to push branch" in str(e)

@patch('src.jules_cli.git.vcs.GITHUB_TOKEN', "test_token")
@patch('requests.post')
def test_github_create_pr_success(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 201
    mock_response.json.return_value = {"html_url": "pr_url"}
    mock_post.return_value = mock_response

    pr = vcs.github_create_pr("owner", "repo", "head")
    assert pr["html_url"] == "pr_url"

@patch('src.jules_cli.git.vcs.GITHUB_TOKEN', "test_token")
@patch('requests.post')
def test_github_create_pr_error(mock_post):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_post.return_value = mock_response

    try:
        vcs.github_create_pr("owner", "repo", "head")
    except GitError as e:
        assert "GitHub PR creation failed" in str(e)
