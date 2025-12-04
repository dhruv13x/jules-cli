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

def test_config_set_list():
    # Setup
    key = "core.test_list"
    value = "[1, 2, 3]"

    # Execute
    result = runner.invoke(app, ["config", "set", key, value])

    # Verify
    assert result.exit_code == 0

    # Check if it was stored as a list
    stored_value = config.get_from_path(key)

    assert isinstance(stored_value, list), f"Expected list, got {type(stored_value)}: {stored_value}"
    assert stored_value == [1, 2, 3]

def test_config_set_dict():
    # Setup
    key = "core.test_dict"
    value = "{'a': 1, 'b': 2}"

    # Execute
    result = runner.invoke(app, ["config", "set", key, value])

    # Verify
    assert result.exit_code == 0

    # Check if it was stored as a dict
    stored_value = config.get_from_path(key)
    assert isinstance(stored_value, dict), f"Expected dict, got {type(stored_value)}: {stored_value}"
    assert stored_value == {'a': 1, 'b': 2}
