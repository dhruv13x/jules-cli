# tests/commands/test_pr_extra.py

from unittest.mock import patch
from jules_cli.commands import pr
from jules_cli.state import _state

@patch('jules_cli.commands.pr.logger')
def test_cmd_create_pr_no_token(mock_logger):
    with patch('jules_cli.commands.pr.GITHUB_TOKEN', None):
        pr.cmd_create_pr()
        mock_logger.error.assert_called_with("GITHUB_TOKEN not set; cannot create PR.")

@patch('jules_cli.commands.pr.logger')
@patch('jules_cli.commands.pr.git_get_remote_repo_info', return_value=(None, None))
def test_cmd_create_pr_no_repo(mock_git_get_remote_repo_info, mock_logger):
    with patch('jules_cli.commands.pr.GITHUB_TOKEN', 'test_token'):
        _state["repo_owner"] = None
        pr.cmd_create_pr()
        mock_logger.warning.assert_called_with("No repo detected in state or git remote. Run a task first.")

@patch('jules_cli.commands.pr.git_current_branch', return_value="my-branch")
@patch('jules_cli.commands.pr.github_create_pr', side_effect=Exception("API error"))
@patch('jules_cli.commands.pr.logger')
def test_cmd_create_pr_api_error(mock_logger, mock_github_create_pr, mock_git_current_branch):
    with patch('jules_cli.commands.pr.GITHUB_TOKEN', 'test_token'):
        _state["repo_owner"] = "owner"
        _state["repo_name"] = "repo"
        pr.cmd_create_pr()
        mock_logger.error.assert_called_once()
        assert "Failed to create PR" in mock_logger.error.call_args[0][0]
