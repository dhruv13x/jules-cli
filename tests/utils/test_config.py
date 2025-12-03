# tests/utils/test_config.py

import os
import toml
from unittest.mock import patch, mock_open
from jules_cli.utils.config import Config, DEFAULT_CONFIG_PATH

def test_config_from_file_creates_default_config():
    with patch("os.path.exists", return_value=False), \
         patch("builtins.open", new_callable=mock_open) as m, \
         patch("toml.dump") as dump_mock, \
         patch("os.makedirs") as makedirs_mock:

        config = Config.from_file("/tmp/dummy_path")

        makedirs_mock.assert_called_once_with("/tmp", exist_ok=True)
        m.assert_any_call("/tmp/dummy_path", "w")
        dump_mock.assert_called_once()
        assert config.data is not None

def test_config_get_nested():
    config = Config({"core": {"default_repo": "test"}}, "/tmp/dummy_path")
    assert config.get_nested("core", "default_repo") == "test"
    assert config.get_nested("core", "non_existent") is None

def test_config_save():
    with patch("builtins.open", new_callable=mock_open) as m, \
         patch("toml.dump") as dump_mock, \
         patch("jules_cli.utils.config.logger") as mock_logger:

        config = Config({"core": {"default_repo": "test"}}, "/tmp/dummy_path")
        config.save()

        m.assert_called_once_with("/tmp/dummy_path", "w")
        dump_mock.assert_called_once_with({"core": {"default_repo": "test"}}, m())
        # Verify logger.debug was called instead of print
        mock_logger.debug.assert_called()

@patch("jules_cli.utils.config.Config.create_default_config")
def test_config_from_file_raises_error(mock_create_default):
    with patch("builtins.open", side_effect=Exception("test error")):
        try:
            Config.from_file("/tmp/dummy_path")
        except Exception as e:
            assert "Failed to load config file" in str(e)

def test_config_save_raises_error():
    with patch("builtins.open", side_effect=Exception("test error")):
        try:
            config = Config({}, "/tmp/dummy_path")
            config.save()
        except Exception as e:
            assert "Failed to save config file" in str(e)
