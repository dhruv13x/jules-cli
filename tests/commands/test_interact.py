# tests/commands/test_interact.py

import pytest
from typer.testing import CliRunner
from unittest.mock import patch, MagicMock

from jules_cli.cli import app
from jules_cli.utils.exceptions import JulesAPIError
from jules_cli.core.api import create_session, send_message, poll_for_result, pick_source_for_repo, list_sources
from jules_cli.utils.config import config
from jules_cli.commands import interact # Import the interact module to patch its imports

runner = CliRunner()

@pytest.fixture
def mock_config():
    # Patch interact.config instead of utils.config.config
    with patch("jules_cli.commands.interact.config") as mock_config_obj:
        mock_config_obj.get_nested.return_value = "owner/repo" # Default configured repo
        yield mock_config_obj

@patch('jules_cli.commands.interact.pick_source_for_repo')
@patch('jules_cli.commands.interact.list_sources')
@patch('jules_cli.commands.interact.create_session')
@patch('jules_cli.commands.interact.poll_for_result')
@patch('jules_cli.commands.interact.send_message')
@patch('jules_cli.commands.interact.logger')
def test_interact_no_default_repo(mock_logger, mock_send_message, mock_poll_for_result, mock_create_session, mock_list_sources, mock_pick_source_for_repo, mock_config, monkeypatch):
    monkeypatch.setenv("JULES_API_KEY", "dummy_key")
    mock_config.get_nested.return_value = None # Explicitly simulate no default repo
    # Mock builtins.input to prevent EOFError if it's unexpectedly called
    with patch("builtins.input", side_effect=["exit"]):
        result = runner.invoke(app, ["interact", "initial prompt"])
    assert result.exit_code == 0 # Command returns gracefully even on error, logs it
    mock_logger.error.assert_called_with("No default repository configured. Please set it using 'jules config set default_repo <owner/repo>'.")

@patch('jules_cli.commands.interact.pick_source_for_repo')
@patch('jules_cli.commands.interact.list_sources')
@patch('jules_cli.commands.interact.create_session')
@patch('jules_cli.commands.interact.poll_for_result')
@patch('jules_cli.commands.interact.send_message')
@patch('jules_cli.commands.interact.logger')
def test_interact_no_api_source_found(mock_logger, mock_send_message, mock_poll_for_result, mock_create_session, mock_list_sources, mock_pick_source_for_repo, mock_config, monkeypatch):
    monkeypatch.setenv("JULES_API_KEY", "dummy_key")
    mock_pick_source_for_repo.return_value = None
    mock_list_sources.return_value = []
    # Mock builtins.input to prevent EOFError if it's unexpectedly called
    with patch("builtins.input", side_effect=["exit"]):
        result = runner.invoke(app, ["interact", "initial prompt"])
    assert result.exit_code == 0 # Command returns gracefully even on error, logs it
    # Corrected assertion to match default repo_name from mock_config fixture
    mock_logger.error.assert_called_with("No Jules API source found for repository 'owner/repo'. Available sources: []")

@patch('jules_cli.commands.interact.pick_source_for_repo')
@patch('jules_cli.commands.interact.list_sources')
@patch('jules_cli.commands.interact.create_session')
@patch('jules_cli.commands.interact.poll_for_result')
@patch('jules_cli.commands.interact.send_message')
@patch('jules_cli.commands.interact.logger')
def test_interact_basic_flow_with_plan(mock_logger, mock_send_message, mock_poll_for_result, mock_create_session, mock_list_sources, mock_pick_source_for_repo, mock_config, monkeypatch):
    monkeypatch.setenv("JULES_API_KEY", "dummy_key")
    mock_pick_source_for_repo.return_value = {"name": "sources/github/owner/repo"}
    mock_create_session.return_value = {"name": "sessions/test-session-id"}
    
    mock_poll_for_result.side_effect = [
        {"type": "message", "message": "How can I help you further?"},
        {"type": "plan", "plan": {"steps": [{"title": "Step 1", "description": "Do something"}]}}
    ]

    user_inputs = ["My reply to Jules", "exit"]
    with patch("builtins.input", side_effect=user_inputs):
        result = runner.invoke(app, ["interact", "initial prompt"])
    
    assert result.exit_code == 0
    mock_logger.info.assert_any_call("Starting interactive session with Jules...")
    mock_logger.info.assert_any_call("Session 'test-session-id' created for source 'sources/github/owner/repo'. Waiting for Jules's response...")
    mock_logger.info.assert_any_call("\nJules: How can I help you further?")
    # The "You: " prefix is handled by builtins.input, not the logger.
    mock_logger.info.assert_any_call(f"\nJules has proposed a plan:\n{{'steps': [{{'title': 'Step 1', 'description': 'Do something'}}]}}\n")
    mock_logger.info.assert_any_call("You can now `jules approve` or `jules reject` this plan.")

    mock_create_session.assert_called_once_with(
        prompt="initial prompt", source_name="sources/github/owner/repo"
    )
    mock_send_message.assert_called_once_with(
        "test-session-id", "My reply to Jules"
    )

@patch('jules_cli.commands.interact.pick_source_for_repo')
@patch('jules_cli.commands.interact.list_sources')
@patch('jules_cli.commands.interact.create_session')
@patch('jules_cli.commands.interact.poll_for_result')
@patch('jules_cli.commands.interact.send_message')
@patch('jules_cli.commands.interact.logger')
def test_interact_user_exits(mock_logger, mock_send_message, mock_poll_for_result, mock_create_session, mock_list_sources, mock_pick_source_for_repo, mock_config, monkeypatch):
    monkeypatch.setenv("JULES_API_KEY", "dummy_key")
    mock_pick_source_for_repo.return_value = {"name": "sources/github/owner/repo"}
    mock_create_session.return_value = {"name": "sessions/test-session-id"}
    
    mock_poll_for_result.return_value = {"type": "message", "message": "How can I help you?"}

    user_inputs = ["exit"]
    with patch("builtins.input", side_effect=user_inputs):
        result = runner.invoke(app, ["interact", "initial prompt"])
    
    assert result.exit_code == 0
    mock_logger.info.assert_any_call("\nJules: How can I help you?")
    mock_logger.info.assert_any_call("Exiting interactive session.")
    mock_send_message.assert_not_called()

@patch('jules_cli.commands.interact.pick_source_for_repo')
@patch('jules_cli.commands.interact.list_sources')
@patch('jules_cli.commands.interact.create_session')
@patch('jules_cli.commands.interact.poll_for_result')
@patch('jules_cli.commands.interact.send_message')
@patch('jules_cli.commands.interact.logger')
def test_interact_api_error_during_poll(mock_logger, mock_send_message, mock_poll_for_result, mock_create_session, mock_list_sources, mock_pick_source_for_repo, mock_config, monkeypatch):
    monkeypatch.setenv("JULES_API_KEY", "dummy_key")
    mock_pick_source_for_repo.return_value = {"name": "sources/github/owner/repo"}
    mock_create_session.return_value = {"name": "sessions/test-session-id"}
    
    mock_poll_for_result.side_effect = JulesAPIError("Test API error")

    user_inputs = ["exit"]
    with patch("builtins.input", side_effect=user_inputs):
        result = runner.invoke(app, ["interact", "initial prompt"])
    
    assert result.exit_code == 0 # The interact command itself catches the API error and logs it, returning 0
    mock_logger.error.assert_called_with("Error polling for result: Test API error")
