# src/jules_cli/utils/config.py

import os
import toml
from .exceptions import ConfigError
from .logging import logger

class Config:
    """A class to manage the CLI configuration."""

    def __init__(self, data: dict, path: str):
        """
        Initializes the Config object.

        Args:
            data: The configuration data.
            path: The path to the configuration file.
        """
        self.data = data
        self.path = path

    @classmethod
    def from_file(cls, path: str) -> "Config":
        """
        Loads the configuration from a file.

        Args:
            path: The path to the configuration file.

        Returns:
            A Config object.
        """
        if not os.path.exists(path):
            cls.create_default_config(path)

        try:
            with open(path, "r") as f:
                data = toml.load(f)
                return cls(data, path)
        except Exception as e:
            raise ConfigError(f"Failed to load config file: {e}")

    @classmethod
    def create_default_config(cls, path: str) -> None:
        """
        Creates a default configuration file.

        Args:
            path: The path to the configuration file.
        """
        default_config = {
            "core": {
                "default_repo": "",
                "default_branch": "main",
                "api_timeout": 60,
                "logging_level": "INFO",
            },
            "git": {
                "name": "Jules CLI User",
                "email": "jules-cli@example.com",
            },
            "branch": {
                "pattern": "{type}/{slug}/{timestamp}",
            },
        }
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            toml.dump(default_config, f)

    def get(self, key: str, default: any = None) -> any:
        """
        Gets a value from the configuration.

        Args:
            key: The key to get.
            default: The default value to return if the key is not found.

        Returns:
            The value of the key.
        """
        return self.data.get(key, default)

    def get_nested(self, section: str, key: str, default: any = None) -> any:
        """
        Gets a nested value from the configuration.

        Args:
            section: The section to get the key from.
            key: The key to get.
            default: The default value to return if the key is not found.

        Returns:
            The value of the key.
        """
        return self.data.get(section, {}).get(key, default)

    def save(self) -> None:
        """Saves the configuration to the file."""
        try:
            logger.debug(f"Saving config data: {self.data!r} to path: {self.path!r}")
            with open(self.path, "w") as f:
                toml.dump(self.data, f)
        except Exception as e:
            raise ConfigError(f"Failed to save config file: {e}")

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/jules/config.toml")
config = Config.from_file(DEFAULT_CONFIG_PATH)
