# tests/commands/test_commit.py

from unittest.mock import patch
from src.jules_cli.commands import commit

@patch('src.jules_cli.commands.commit.git_create_branch_and_commit')
@patch('src.jules_cli.commands.commit.git_push_branch')
def test_cmd_commit_and_push_success(mock_push, mock_commit):
    with patch('time.time', return_value=12345):
        commit.cmd_commit_and_push()
        mock_commit.assert_called_once()
        mock_push.assert_called_once()

@patch('src.jules_cli.commands.commit.git_create_branch_and_commit', side_effect=Exception("Commit failed"))
def test_cmd_commit_and_push_commit_fails(mock_commit):
    result = commit.cmd_commit_and_push()
    assert result["status"] == "error"
    assert "Commit failed" in result["message"]

@patch('src.jules_cli.commands.commit.git_create_branch_and_commit')
@patch('src.jules_cli.commands.commit.git_push_branch', side_effect=Exception("Push failed"))
def test_cmd_commit_and_push_push_fails(mock_push, mock_commit):
    result = commit.cmd_commit_and_push()
    assert result["status"] == "error"
    assert "Push failed" in result["message"]
