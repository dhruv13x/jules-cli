# src/jules_cli/utils/config.py

import os
import toml
from .exceptions import ConfigError

class Config:
    def __init__(self, data):
        self.data = data

    @classmethod
    def from_file(cls, path):
        try:
            with open(path, "r") as f:
                data = toml.load(f)
                return cls(data)
        except FileNotFoundError:
            return cls({})
        except Exception as e:
            raise ConfigError(f"Failed to load config file: {e}")

    def get(self, key, default=None):
        return self.data.get(key, default)

    def get_nested(self, section, key, default=None):
        return self.data.get(section, {}).get(key, default)

DEFAULT_CONFIG_PATH = os.path.expanduser("~/.config/jules/config.toml")
config = Config.from_file(DEFAULT_CONFIG_PATH)
