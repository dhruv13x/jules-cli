# src/jules_cli/commands/config.py

import typer
import ast
from ..utils.config import config
from ..utils.logging import logger

config_app = typer.Typer(name="config", help="Manage CLI configuration.")

@config_app.command("set-repo")
def set_repo(
    repo_name: str = typer.Argument(..., help="The repository name in 'owner/repo' format."),
):
    """
    Sets the default repository for Jules CLI.
    """
    if "/" not in repo_name:
        logger.error("Invalid repository format. Please use 'owner/repo'.")
        raise typer.Exit(code=1)

    try:
        if "core" not in config.data:
            config.data["core"] = {}
        config.data["core"]["default_repo"] = repo_name
        config.save()
        logger.info(f"Default repository set to: {repo_name}")
    except Exception as e:
        logger.error(f"Failed to set default repository: {e}")
        raise typer.Exit(code=1)

@config_app.command("get")
def get_config(
    key: str = typer.Argument(..., help="The configuration key (e.g. core.api_timeout)."),
):
    """
    Get a configuration value.
    """
    try:
        parts = key.split(".")
        value = config.data
        for part in parts:
            if isinstance(value, dict) and part in value:
                value = value[part]
            else:
                logger.error(f"Key '{key}' not found.")
                raise typer.Exit(code=1)

        typer.echo(value)
    except Exception as e:
        logger.error(f"Failed to get config key: {e}")
        raise typer.Exit(code=1)

@config_app.command("set")
def set_config(
    key: str = typer.Argument(..., help="The configuration key (e.g. core.api_timeout)."),
    value: str = typer.Argument(..., help="The value to set."),
):
    """
    Set a configuration value. Types (int, bool) are inferred.
    """
    try:
        # Infer type
        real_value = value
        # Try evaluating literal for bool/int/float/list/dict
        try:
             # ast.literal_eval is safe for simple types
             real_value = ast.literal_eval(value)
        except (ValueError, SyntaxError):
             # Keep as string if it fails (e.g. "some_string")
             pass

        parts = key.split(".")
        target = config.data

        # Navigate to the parent dict
        for i, part in enumerate(parts[:-1]):
            if part not in target:
                target[part] = {}
            target = target[part]
            if not isinstance(target, dict):
                 # If we encounter a non-dict where we expect a dict (e.g. overwriting a scalar)
                 logger.error(f"Cannot set nested key '{key}' because '{parts[i]}' is not a dictionary.")
                 raise typer.Exit(code=1)

        last_key = parts[-1]
        target[last_key] = real_value
        config.save()
        logger.info(f"Set '{key}' to {real_value!r}")

    except Exception as e:
        logger.error(f"Failed to set config key: {e}")
        raise typer.Exit(code=1)
