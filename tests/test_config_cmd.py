import os
from unittest.mock import patch
from typer.testing import CliRunner
from jules_cli.cli import app

runner = CliRunner()

def test_config_set_get_flow(tmp_path):
    config_path = tmp_path / "config.toml"

    with patch("jules_cli.utils.config.DEFAULT_CONFIG_PATH", str(config_path)), \
         patch("jules_cli.utils.config.config.path", str(config_path)), \
         patch("jules_cli.commands.config.logger") as mock_logger, \
         patch("jules_cli.cli.check_env"), \
         patch("jules_cli.cli.init_db"), \
         patch("jules_cli.cli.print_logo"), \
         patch("jules_cli.utils.logging.setup_logging"): # Prevent real setup_logging

         # 1. Set a value
         result = runner.invoke(app, ["config", "set", "core.test_val", "123"])
         assert result.exit_code == 0
         mock_logger.info.assert_called_with("Set 'core.test_val' to 123")

         # 2. Get the value
         result = runner.invoke(app, ["config", "get", "core.test_val"])
         assert result.exit_code == 0
         assert "123" in result.stdout

         # 3. Set a nested bool
         result = runner.invoke(app, ["config", "set", "feature.enabled", "True"])
         assert result.exit_code == 0
         mock_logger.info.assert_called_with("Set 'feature.enabled' to True")

         # 4. Get nested bool
         result = runner.invoke(app, ["config", "get", "feature.enabled"])
         assert result.exit_code == 0
         assert "True" in result.stdout

def test_config_get_missing_key(tmp_path):
    config_path = tmp_path / "config.toml"

    with patch("jules_cli.utils.config.DEFAULT_CONFIG_PATH", str(config_path)), \
         patch("jules_cli.utils.config.config.path", str(config_path)), \
         patch("jules_cli.commands.config.logger") as mock_logger, \
         patch("jules_cli.cli.check_env"), \
         patch("jules_cli.cli.init_db"), \
         patch("jules_cli.cli.print_logo"), \
         patch("jules_cli.utils.logging.setup_logging"):

         result = runner.invoke(app, ["config", "get", "non.existent"])
         assert result.exit_code == 1
         mock_logger.error.assert_called_with("Key 'non.existent' not found.")

def test_config_set_type_inference(tmp_path):
    config_path = tmp_path / "config.toml"

    with patch("jules_cli.utils.config.DEFAULT_CONFIG_PATH", str(config_path)), \
         patch("jules_cli.utils.config.config.path", str(config_path)), \
         patch("jules_cli.commands.config.logger") as mock_logger, \
         patch("jules_cli.cli.check_env"), \
         patch("jules_cli.cli.init_db"), \
         patch("jules_cli.cli.print_logo"), \
         patch("jules_cli.utils.logging.setup_logging"):

         # List
         result = runner.invoke(app, ["config", "set", "my.list", "[1, 2, 3]"])
         assert result.exit_code == 0
         mock_logger.info.assert_called_with("Set 'my.list' to [1, 2, 3]")

         # String (that looks like int but quoted?)
         result = runner.invoke(app, ["config", "set", "my.str", "'123'"])
         assert result.exit_code == 0
         mock_logger.info.assert_called_with("Set 'my.str' to '123'")
