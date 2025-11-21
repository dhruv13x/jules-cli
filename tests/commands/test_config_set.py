# tests/commands/test_config_set.py

import os
import pytest
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from jules_cli.cli import app
from jules_cli.utils.config import config
from jules_cli.commands import config_set

runner = CliRunner()

@pytest.fixture(autouse=True)
def clean_config_data():
    """Ensure config.data is clean and has default log_level and core before each test."""
    config.data = {
        "log_level": "INFO",
        "core": {
            "default_repo": "owner/repo" # Default for tests that don't override it
        }
    }

@patch.object(config_set.config, 'save')
@patch.object(config_set.logger, 'info')
def test_set_repo_success(mock_logger_info, mock_save, monkeypatch):
    monkeypatch.setenv("JULES_API_KEY", "dummy_key")
    # Initialize config.data if it's not already, or ensure it has the expected structure
    if "core" not in config.data:
        config.data["core"] = {}
    
    result = runner.invoke(app, ["config", "set-repo", "owner/repo-name"])
    assert result.exit_code == 0 # Command returns gracefully now
    mock_logger_info.assert_called_with("Default repository set to: owner/repo-name")
    assert config.data["core"]["default_repo"] == "owner/repo-name"
    mock_save.assert_called_once()

@patch.object(config_set.config, 'save')
@patch.object(config_set.logger, 'error')
def test_set_repo_invalid_format(mock_logger_error, mock_save, monkeypatch):
    monkeypatch.setenv("JULES_API_KEY", "dummy_key")
    result = runner.invoke(app, ["config", "set-repo", "invalid-repo-name"])
    assert result.exit_code == 1
    # logger.error calls are likely captured by caplog, but runner.invoke might not show them in stderr depending on handler config
    # mock_logger_error ensures we verify the error logging independently of stdout/stderr
    mock_logger_error.assert_called_with("Invalid repository format. Please use 'owner/repo'.")
    mock_save.assert_not_called()

@patch.object(config_set.config, 'save', side_effect=Exception("Save failed"))
@patch.object(config_set.logger, 'error')
def test_set_repo_save_failure(mock_logger_error, mock_save, monkeypatch):
    monkeypatch.setenv("JULES_API_KEY", "dummy_key")
    # Initialize config.data if it's not already, or ensure it has the expected structure
    if "core" not in config.data:
        config.data["core"] = {}
    
    result = runner.invoke(app, ["config", "set-repo", "owner/repo-name"])
    assert result.exit_code == 1 # Command should exit with error code 1 for save failure
    mock_logger_error.assert_called_with("Failed to set default repository: Save failed")
    mock_save.assert_called_once()
