# tests/commands/test_testgen.py

from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from src.jules_cli.cli import app
from src.jules_cli.commands.testgen import run_testgen
import os

runner = CliRunner()

@patch("src.jules_cli.cli.check_env")
@patch("src.jules_cli.cli.init_db")
@patch("src.jules_cli.cli.add_history_record")
@patch("src.jules_cli.cli.run_testgen")
def test_testgen_command(mock_run_testgen, mock_add_history_record, mock_init_db, mock_check_env):
    os.environ["JULES_API_KEY"] = "test_key"
    result = runner.invoke(app, ["testgen", "my_file.py"])
    assert result.exit_code == 0
    mock_run_testgen.assert_called_once_with("my_file.py", test_type="missing")

@patch("src.jules_cli.commands.testgen.config")
@patch("src.jules_cli.commands.testgen.pick_source_for_repo")
@patch("src.jules_cli.commands.testgen.create_session")
@patch("src.jules_cli.commands.testgen.poll_for_result")
def test_run_testgen(mock_poll, mock_create, mock_pick, mock_config):
    mock_config.get_nested.return_value = "test_repo"
    mock_pick.return_value = {"name": "test", "githubRepo": {"owner": "test", "repo": "test"}}
    mock_create.return_value = {"id": "123"}
    mock_poll.return_value = {"type": "patch", "patch": "test"}
    run_testgen("my_file.py")
    mock_create.assert_called_once()
    mock_poll.assert_called_once()

@patch("src.jules_cli.commands.testgen.config")
@patch("src.jules_cli.commands.testgen.pick_source_for_repo", return_value=None)
def test_run_testgen_no_source(mock_pick, mock_config):
    mock_config.get_nested.return_value = "test_repo"
    with patch("src.jules_cli.commands.testgen.list_sources", return_value=[]) as mock_list_sources:
        try:
            run_testgen("my_file.py")
        except RuntimeError:
            pass
        mock_list_sources.assert_called_once()

@patch("src.jules_cli.commands.testgen.config")
@patch("src.jules_cli.commands.testgen.pick_source_for_repo")
@patch("src.jules_cli.commands.testgen.create_session", return_value={})
def test_run_testgen_no_session(mock_create, mock_pick, mock_config):
    mock_config.get_nested.return_value = "test_repo"
    mock_pick.return_value = {"name": "test", "githubRepo": {"owner": "test", "repo": "test"}}
    try:
        run_testgen("my_file.py")
    except RuntimeError:
        pass
    mock_create.assert_called_once()

@patch("src.jules_cli.commands.testgen.config")
@patch("src.jules_cli.commands.testgen.pick_source_for_repo")
@patch("src.jules_cli.commands.testgen.create_session")
@patch("src.jules_cli.commands.testgen.poll_for_result")
def test_run_testgen_pr(mock_poll, mock_create, mock_pick, mock_config):
    mock_config.get_nested.return_value = "test_repo"
    mock_pick.return_value = {"name": "test", "githubRepo": {"owner": "test", "repo": "test"}}
    mock_create.return_value = {"id": "123"}
    mock_poll.return_value = {"type": "pr", "pr": {}}
    run_testgen("my_file.py")
    mock_create.assert_called_once()
    mock_poll.assert_called_once()
