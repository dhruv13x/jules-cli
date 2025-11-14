from unittest.mock import patch
from src.jules_cli.commands import commit

@patch('src.jules_cli.git.vcs.git_create_branch_and_commit')
@patch('src.jules_cli.git.vcs.git_push_branch')
def test_cmd_commit_and_push_success(mock_push, mock_commit):
    with patch('time.time', return_value=12345):
        commit.cmd_commit_and_push()
        mock_commit.assert_called_once()
        mock_push.assert_called_once()
