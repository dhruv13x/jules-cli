from unittest.mock import patch, MagicMock
from src.jules_cli.commands import task
from src.jules_cli.core import api

@patch('src.jules_cli.commands.task.pick_source_for_repo')
@patch('src.jules_cli.commands.task.create_session')
@patch('src.jules_cli.commands.task.poll_for_result')
def test_run_task_success(mock_poll, mock_create, mock_pick):
    mock_pick.return_value = {"name": "source", "githubRepo": {"owner": "owner", "repo": "repo"}}
    mock_create.return_value = {"id": "session_id"}
    mock_poll.return_value = {"type": "patch", "patch": "fake_patch"}
    with patch.object(api, 'list_sources', return_value=[{"name": "source", "githubRepo": {"owner": "owner", "repo": "repo"}}]):
        task.run_task("my prompt", repo_dir_name="repo")
        mock_pick.assert_called_once()
        mock_create.assert_called_once()
        mock_poll.assert_called_once()
