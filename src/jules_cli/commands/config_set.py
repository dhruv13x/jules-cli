# src/jules_cli/commands/config_set.py

import typer
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
    try:
        if "/" not in repo_name:
            logger.error("Invalid repository format. Please use 'owner/repo'.")
            raise typer.Exit(code=1)

        config.data["core"]["default_repo"] = repo_name
        config.save()
        logger.info(f"Default repository set to: {repo_name}")
    except Exception as e:
        logger.error(f"Failed to set default repository: {e}")
        raise typer.Exit(code=1)
