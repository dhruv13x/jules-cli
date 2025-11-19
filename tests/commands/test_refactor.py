# tests/commands/test_refactor.py

from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from src.jules_cli.cli import app
from src.jules_cli.commands.refactor import run_refactor
import os

runner = CliRunner()

@patch("src.jules_cli.cli.check_env")
@patch("src.jules_cli.cli.init_db")
@patch("src.jules_cli.cli.add_history_record")
@patch("src.jules_cli.cli.run_refactor")
def test_refactor_command(mock_run_refactor, mock_add_history_record, mock_init_db, mock_check_env):
    os.environ["JULES_API_KEY"] = "test_key"
    result = runner.invoke(app, ["refactor", "my instruction"])
    assert result.exit_code == 0
    mock_run_refactor.assert_called_once_with("my instruction")

@patch("src.jules_cli.commands.refactor.config")
@patch("src.jules_cli.commands.refactor.pick_source_for_repo")
@patch("src.jules_cli.commands.refactor.create_session")
@patch("src.jules_cli.commands.refactor.poll_for_result")
@patch("src.jules_cli.commands.refactor.send_message")
def test_run_refactor(mock_send, mock_poll, mock_create, mock_pick, mock_config):
    mock_config.get_nested.return_value = "test_repo"
    mock_pick.return_value = {"name": "test", "githubRepo": {"owner": "test", "repo": "test"}}
    mock_create.return_value = {"id": "123"}
    mock_poll.side_effect = [{"plan": ["step 1", "step 2"]}, {"type": "patch", "patch": "test"}, {"type": "patch", "patch": "test"}]
    run_refactor("my instruction")
    mock_create.assert_called_once()
    assert mock_poll.call_count == 3
    assert mock_send.call_count == 3

@patch("src.jules_cli.commands.refactor.config")
@patch("src.jules_cli.commands.refactor.pick_source_for_repo", return_value=None)
def test_run_refactor_no_source(mock_pick, mock_config):
    mock_config.get_nested.return_value = "test_repo"
    with patch("src.jules_cli.commands.refactor.list_sources", return_value=[]) as mock_list_sources:
        try:
            run_refactor("my instruction")
        except RuntimeError:
            pass
        mock_list_sources.assert_called_once()

@patch("src.jules_cli.commands.refactor.config")
@patch("src.jules_cli.commands.refactor.pick_source_for_repo")
@patch("src.jules_cli.commands.refactor.create_session", return_value={})
def test_run_refactor_no_session(mock_create, mock_pick, mock_config):
    mock_config.get_nested.return_value = "test_repo"
    mock_pick.return_value = {"name": "test", "githubRepo": {"owner": "test", "repo": "test"}}
    try:
        run_refactor("my instruction")
    except RuntimeError:
        pass
    mock_create.assert_called_once()

@patch("src.jules_cli.commands.refactor.config")
@patch("src.jules_cli.commands.refactor.pick_source_for_repo")
@patch("src.jules_cli.commands.refactor.create_session")
@patch("src.jules_cli.commands.refactor.poll_for_result")
@patch("src.jules_cli.commands.refactor.send_message")
def test_run_refactor_pr(mock_send, mock_poll, mock_create, mock_pick, mock_config):
    mock_config.get_nested.return_value = "test_repo"
    mock_pick.return_value = {"name": "test", "githubRepo": {"owner": "test", "repo": "test"}}
    mock_create.return_value = {"id": "123"}
    mock_poll.side_effect = [{"plan": ["step 1"]}, {"type": "pr", "pr": {}}]
    run_refactor("my instruction")
    mock_create.assert_called_once()
    assert mock_poll.call_count == 2
    assert mock_send.call_count == 2
