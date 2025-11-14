from unittest.mock import patch, mock_open
from src.jules_cli.utils.config import Config, ConfigError

def test_config_from_file_success():
    mock_toml_data = 'default_repo = "my-repo"'
    with patch("builtins.open", mock_open(read_data=mock_toml_data)):
        with patch("toml.load") as mock_toml_load:
            mock_toml_load.return_value = {"default_repo": "my-repo"}
            config = Config.from_file("dummy_path")
            assert config.get("default_repo") == "my-repo"

def test_config_from_file_not_found():
    with patch("builtins.open", side_effect=FileNotFoundError):
        config = Config.from_file("non_existent_path")
        assert config.data == {}

def test_config_from_file_error():
    with patch("builtins.open", mock_open(read_data="invalid toml")):
        with patch("toml.load", side_effect=Exception("TOML parse error")):
            try:
                Config.from_file("dummy_path")
            except ConfigError as e:
                assert "Failed to load config file" in str(e)

def test_config_get():
    config = Config({"key": "value"})
    assert config.get("key") == "value"
    assert config.get("non_existent_key", "default") == "default"

def test_config_get_nested():
    config = Config({"section": {"key": "value"}})
    assert config.get_nested("section", "key") == "value"
    assert config.get_nested("section", "non_existent_key", "default") == "default"
    assert config.get_nested("non_existent_section", "key", "default") == "default"
