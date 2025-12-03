# tests/commands/test_pr.py

from unittest.mock import patch
from jules_cli.commands import pr
from jules_cli.state import _state

@patch('jules_cli.commands.pr.git_current_branch', return_value="my-branch")
@patch('jules_cli.commands.pr.github_create_pr', return_value={"html_url": "pr_url"})
def test_cmd_create_pr_success(mock_create_pr, mock_current_branch):
    _state["repo_owner"] = "owner"
    _state["repo_name"] = "repo"
    with patch('os.getenv', return_value='test_token'):
        pr.cmd_create_pr()
        mock_create_pr.assert_called_once_with(
            "owner",
            "repo",
            head="my-branch",
            base="main",
            title="Automated fix from Jules CLI",
            body="Auto PR",
            draft=False,
            labels=None,
            reviewers=None,
            assignees=None,
        )

@patch('jules_cli.commands.pr.git_current_branch', return_value="my-branch")
@patch('jules_cli.commands.pr.github_create_pr', return_value={"html_url": "pr_url"})
def test_cmd_create_pr_with_issue_success(mock_create_pr, mock_current_branch):
    _state["repo_owner"] = "owner"
    _state["repo_name"] = "repo"
    with patch('os.getenv', return_value='test_token'):
        pr.cmd_create_pr(issue=123)
        mock_create_pr.assert_called_once_with(
            "owner",
            "repo",
            head="my-branch",
            base="main",
            title="Automated fix from Jules CLI",
            body="Auto PR\n\nCloses #123",
            draft=False,
            labels=None,
            reviewers=None,
            assignees=None,
        )
