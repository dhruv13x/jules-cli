# tests/commands/test_config.py

import pytest
import logging
from unittest.mock import patch, MagicMock
from typer.testing import CliRunner
from jules_cli.cli import app
from jules_cli.utils.config import config
from jules_cli.commands import config as config_cmd

runner = CliRunner()

@pytest.fixture(autouse=True)
def clean_config_data():
    """Ensure config.data is clean before each test."""
    config.data = {
        "log_level": "INFO",
        "core": {
            "default_repo": "owner/repo" 
        }
    }

@pytest.fixture(autouse=True)
def mock_logging_setup():
    """Prevent setup_logging from interfering with CliRunner streams."""
    # Clear existing handlers to avoid I/O errors on closed streams
    logging.getLogger("jules").handlers = []
    
    with patch("jules_cli.utils.logging.setup_logging"):
        yield

@pytest.fixture(autouse=True)
def mock_env_check():
    """Mock check_env to avoid CLI errors."""
    with patch("jules_cli.cli.check_env"):
        yield

@pytest.fixture(autouse=True)
def mock_command_logger():
    """Mock the logger used in the command to avoid I/O errors on closed streams."""
    with patch("jules_cli.commands.config.logger") as mock:
        yield mock

@pytest.fixture(autouse=True)
def mock_ui():
    """Mock UI elements like logo to keep stdout clean."""
    with patch("jules_cli.cli.print_logo"):
        yield

@patch.object(config_cmd.config, 'save')
def test_set_config_success(mock_save):
    result = runner.invoke(app, ["config", "set", "core.api_timeout", "120"])
    assert result.exit_code == 0
    assert config.data["core"]["api_timeout"] == 120
    mock_save.assert_called_once()

@patch.object(config_cmd.config, 'save')
def test_set_config_bool(mock_save):
    result = runner.invoke(app, ["config", "set", "new.flag", "true"])
    assert result.exit_code == 0
    assert config.data["new"]["flag"] is True
    mock_save.assert_called_once()

def test_get_config_success():
    config.data["core"]["foo"] = "bar"
    result = runner.invoke(app, ["config", "get", "core.foo"])
    assert result.exit_code == 0
    assert "bar" in result.stdout

def test_get_config_not_found():
    result = runner.invoke(app, ["config", "get", "nonexistent.key"])
    assert result.exit_code == 0
    # Should log warning (mocked) and output nothing to stdout?
    # The command does: logger.warning(...); else: typer.echo(...)
    assert result.stdout.strip() == ""

@patch.object(config_cmd.config, 'save')
def test_set_repo_legacy(mock_save):
    result = runner.invoke(app, ["config", "set-repo", "user/repo"])
    assert result.exit_code == 0
    assert config.data["core"]["default_repo"] == "user/repo"
    mock_save.assert_called_once()

def test_list_config():
    result = runner.invoke(app, ["config", "list"])
    assert result.exit_code == 0
    assert "default_repo" in result.stdout
