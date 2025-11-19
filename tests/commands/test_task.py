# tests/commands/test_task.py

import json
from unittest.mock import patch, MagicMock
import pytest
from jules_cli.commands import task
from jules_cli.core import api

@patch('jules_cli.commands.task.pick_source_for_repo')
@patch('jules_cli.commands.task.create_session')
@patch('jules_cli.commands.task.poll_for_result')
def test_run_task_success(mock_poll, mock_create, mock_pick):
    mock_pick.return_value = {"name": "source", "githubRepo": {"owner": "owner", "repo": "repo"}}
    mock_create.return_value = {"id": "session_id"}
    mock_poll.return_value = {"type": "patch", "patch": "fake_patch"}
    with patch.object(api, 'list_sources', return_value=[{"name": "source", "githubRepo": {"owner": "owner", "repo": "repo"}}]):
        task.run_task("my prompt", repo_dir_name="repo")
        mock_pick.assert_called_once()
        mock_create.assert_called_once()
        mock_poll.assert_called_once()

@patch('jules_cli.commands.task.config')
def test_run_task_no_repo_name_or_default_repo(mock_config):
    mock_config.get_nested.return_value = None  # Simulate no default_repo

    with pytest.raises(RuntimeError) as excinfo:
        task.run_task("my prompt")

    assert "No repository specified. Use --repo or set default_repo in your config." in str(excinfo.value)
    mock_config.get_nested.assert_called_once_with("core", "default_repo")

@patch('jules_cli.commands.task.pick_source_for_repo', return_value=None)
@patch('jules_cli.commands.task.list_sources', return_value=[{"name": "source1"}, {"name": "source2"}])
def test_run_task_no_source_matched(mock_list_sources, mock_pick_source_for_repo):
    with pytest.raises(RuntimeError) as excinfo:
        task.run_task("my prompt", repo_dir_name="non_existent_repo")

    assert "No source matched repo 'non_existent_repo'. Available: ['source1', 'source2']" in str(excinfo.value)
    mock_pick_source_for_repo.assert_called_once_with("non_existent_repo")
    mock_list_sources.assert_called_once()

@patch('jules_cli.commands.task.pick_source_for_repo', return_value={"name": "source", "githubRepo": {"owner": "owner", "repo": "repo"}})
@patch('jules_cli.commands.task.create_session', return_value={})  # Simulate failed session creation
def test_run_task_create_session_fails(mock_create_session, mock_pick_source_for_repo):
    with pytest.raises(RuntimeError) as excinfo:
        task.run_task("my prompt", repo_dir_name="repo")

    assert "Failed to create session: {}" in str(excinfo.value)
    mock_pick_source_for_repo.assert_called_once_with("repo")
    mock_create_session.assert_called_once()

@patch('jules_cli.commands.task.pick_source_for_repo')
@patch('jules_cli.commands.task.create_session')
@patch('jules_cli.commands.task.poll_for_result')
@patch('jules_cli.commands.task.logger')
def test_run_task_pr_result(mock_logger, mock_poll, mock_create, mock_pick):
    mock_pick.return_value = {"name": "source", "githubRepo": {"owner": "owner", "repo": "repo"}}
    mock_create.return_value = {"id": "session_id"}
    mock_pr_data = {"url": "http://example.com/pr/1"}
    mock_poll.return_value = {"type": "pr", "pr": mock_pr_data}
    with patch.object(api, 'list_sources', return_value=[{"name": "source", "githubRepo": {"owner": "owner", "repo": "repo"}}]):
        task.run_task("my prompt", repo_dir_name="repo")
        mock_pick.assert_called_once()
        mock_create.assert_called_once()
        mock_poll.assert_called_once()
        mock_logger.info.assert_any_call("PR artifact: %s", json.dumps(mock_pr_data, indent=2))
