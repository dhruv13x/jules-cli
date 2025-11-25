# tests/commands/test_task_unit.py

from unittest.mock import patch, MagicMock
import pytest
from jules_cli.commands import task
from jules_cli.state import _state
from jules_cli.utils.config import config

@pytest.fixture
def mock_config():
    with patch.object(config, 'get_nested') as mock_get:
        yield mock_get

@patch("jules_cli.commands.task.pick_source_for_repo")
@patch("jules_cli.commands.task.create_session")
@patch("jules_cli.commands.task.poll_for_result")
@patch("jules_cli.commands.task.generate_branch_name")
@patch("jules_cli.commands.task.list_sources")
def test_run_task_success(mock_list, mock_gen_branch, mock_poll, mock_create, mock_pick, mock_config):
    # Setup mocks
    mock_config.return_value = "default-repo"
    mock_pick.return_value = {"name": "source1", "githubRepo": {"owner": "owner", "repo": "repo"}}
    mock_gen_branch.return_value = "branch-123"
    mock_create.return_value = {"id": "session-123"}
    mock_poll.return_value = {"type": "message", "message": "Done"}

    result = task.run_task("Do something")

    assert result["type"] == "message"
    assert _state["repo_source"] == "source1"
    assert _state["repo_owner"] == "owner"
    assert _state["repo_name"] == "repo"

@patch("jules_cli.commands.task.pick_source_for_repo")
def test_run_task_no_repo(mock_pick, mock_config):
    mock_config.return_value = None # simulate no default repo

    with pytest.raises(RuntimeError, match="No repository specified"):
        task.run_task("Do something")

@patch("jules_cli.commands.task.pick_source_for_repo")
@patch("jules_cli.commands.task.list_sources")
def test_run_task_no_source_matched(mock_list, mock_pick, mock_config):
    mock_config.return_value = "owner/repo"
    mock_pick.return_value = None
    mock_list.return_value = [{"name": "other_source"}]

    with pytest.raises(RuntimeError, match="No source matched repo"):
        task.run_task("Do something")

@patch("jules_cli.commands.task.pick_source_for_repo")
@patch("jules_cli.commands.task.create_session")
@patch("jules_cli.commands.task.generate_branch_name")
def test_run_task_session_creation_failed(mock_gen, mock_create, mock_pick, mock_config):
    mock_config.return_value = "owner/repo"
    mock_pick.return_value = {"name": "source1", "githubRepo": {"owner": "owner", "repo": "repo"}}
    mock_create.return_value = {"error": "failed"} # No ID

    with pytest.raises(RuntimeError, match="Failed to create session"):
        task.run_task("Do something")

@patch("jules_cli.commands.task.pick_source_for_repo")
@patch("jules_cli.commands.task.create_session")
@patch("jules_cli.commands.task.poll_for_result")
@patch("jules_cli.commands.task.generate_branch_name")
def test_run_task_patch_result(mock_gen, mock_poll, mock_create, mock_pick, mock_config):
    mock_config.side_effect = lambda section, key, default=None: "owner/repo" if key == "default_repo" else default
    mock_pick.return_value = {"name": "source1", "githubRepo": {"owner": "owner", "repo": "repo"}}
    mock_create.return_value = {"id": "session-123"}
    mock_poll.return_value = {"type": "patch", "patch": "diff content"}

    result = task.run_task("Do something")
    assert result["type"] == "patch"

@patch("jules_cli.commands.task.pick_source_for_repo")
@patch("jules_cli.commands.task.create_session")
@patch("jules_cli.commands.task.poll_for_result")
@patch("jules_cli.commands.task.generate_branch_name")
def test_run_task_pr_result(mock_gen, mock_poll, mock_create, mock_pick, mock_config):
    mock_config.side_effect = lambda section, key, default=None: "owner/repo" if key == "default_repo" else default
    mock_pick.return_value = {"name": "source1", "githubRepo": {"owner": "owner", "repo": "repo"}}
    mock_create.return_value = {"id": "session-123"}
    mock_poll.return_value = {"type": "pr", "pr": {"url": "http://github.com/pr/1"}}

    result = task.run_task("Do something")
    assert result["type"] == "pr"

@patch("jules_cli.commands.task.pick_source_for_repo")
@patch("jules_cli.commands.task.create_session")
@patch("jules_cli.commands.task.poll_for_result")
@patch("jules_cli.commands.task.generate_branch_name")
def test_run_task_plan_result(mock_gen, mock_poll, mock_create, mock_pick, mock_config):
    mock_config.side_effect = lambda section, key, default=None: "owner/repo" if key == "default_repo" else default
    mock_pick.return_value = {"name": "source1", "githubRepo": {"owner": "owner", "repo": "repo"}}
    mock_create.return_value = {"id": "session-123"}
    mock_poll.return_value = {"type": "plan", "plan": {"steps": [{"title": "Step 1", "description": "Desc"}]}}

    result = task.run_task("Do something")
    assert result["type"] == "plan"

@patch("jules_cli.commands.task.pick_source_for_repo")
@patch("jules_cli.commands.task.create_session")
@patch("jules_cli.commands.task.poll_for_result")
@patch("jules_cli.commands.task.generate_branch_name")
def test_run_task_session_status_result(mock_gen, mock_poll, mock_create, mock_pick, mock_config):
    mock_config.side_effect = lambda section, key, default=None: "owner/repo" if key == "default_repo" else default
    mock_pick.return_value = {"name": "source1", "githubRepo": {"owner": "owner", "repo": "repo"}}
    mock_create.return_value = {"id": "session-123"}
    mock_poll.return_value = {"type": "session_status", "status": "COMPLETED", "session": {"id": "session-123"}}

    result = task.run_task("Do something")
    assert result["type"] == "session_status"
    assert result["status"] == "COMPLETED"

@patch("jules_cli.commands.task.pick_source_for_repo")
@patch("jules_cli.commands.task.create_session")
@patch("jules_cli.commands.task.poll_for_result")
@patch("jules_cli.commands.task.generate_branch_name")
def test_run_task_with_explicit_repo(mock_gen, mock_poll, mock_create, mock_pick, mock_config):
    mock_pick.return_value = {"name": "source1", "githubRepo": {"owner": "owner", "repo": "repo"}}
    mock_create.return_value = {"id": "session-123"}
    mock_poll.return_value = {"type": "message", "message": "Done"}

    task.run_task("Do something", repo_dir_name="explicit/repo")

    mock_pick.assert_called_with("explicit/repo")
