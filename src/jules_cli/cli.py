#!/usr/bin/env python3
"""
Jules Interactive CLI
"""
import os
import typer
from typing_extensions import Annotated

from .commands.auto import auto_fix_command
from .commands.task import run_task
from .commands.session import cmd_session_list, cmd_session_show
from .commands.history import cmd_history_list, cmd_history_view
from .commands.apply import cmd_apply
from .commands.commit import cmd_commit_and_push
from .commands.pr import cmd_create_pr
from .commands.doctor import run_doctor_command
from .db import init_db, add_history_record
from .git.vcs import git_push_branch, git_current_branch
from .state import _state
from .utils.environment import check_env
from .utils.logging import logger, setup_logging
from .utils.exceptions import JulesError
from .utils.config import config
from .utils.output import print_json

app = typer.Typer(
    help="Jules Interactive CLI — fully immersive developer assistant.",
    add_completion=False,
    no_args_is_help=True,
    rich_markup_mode="markdown",
)

session_app = typer.Typer(name="session", help="Manage sessions.")
history_app = typer.Typer(name="history", help="View session history.")
pr_app = typer.Typer(name="pr", help="Manage pull requests.")

app.add_typer(session_app)
app.add_typer(history_app)
app.add_typer(pr_app)

@app.callback()
def main(
    debug: bool = typer.Option(False, "--debug", help="Enable debug logging."),
    no_color: bool = typer.Option(False, "--no-color", help="Disable colored output."),
    json_output: bool = typer.Option(False, "--json", help="Output in JSON format."),
    pretty: bool = typer.Option(False, "--pretty", help="Pretty-print JSON output."),
):
    _state["json_output"] = json_output
    _state["pretty"] = pretty
    """
    Jules CLI
    """
    log_level = config.get("log_level", "INFO").upper()
    if debug:
        log_level = "DEBUG"

    color_mode = config.get("color_mode", "auto")
    use_color = not no_color and color_mode != "off"

    setup_logging(level=log_level, color=use_color)

    try:
        check_env()
    except JulesError as e:
        logger.error(e)
        raise typer.Exit(code=1)

    logger.info("Jules CLI starting. JULES_API_KEY detected.")

    try:
        init_db()
    except JulesError as e:
        logger.error("Failed to initialize database: %s", e)
        raise typer.Exit(code=1)


@app.command()
def auto():
    """
    Run pytest and auto-fix failures.
    """
    result = auto_fix_command()
    if _state.get("json_output"):
        print_json(result, pretty=_state.get("pretty"))

@app.command()
def task(prompt: str):
    """
    Ask Jules to perform an arbitrary dev task (bugfix/refactor/tests/docs).
    """
    _state["session_id"] = os.urandom(8).hex()
    result = run_task(prompt)
    add_history_record(session_id=_state["session_id"], prompt=prompt, status="task_run")
    if _state.get("json_output"):
        print_json(result, pretty=_state.get("pretty"))

@session_app.command("list")
def session_list():
    """
    List sessions.
    """
    result = cmd_session_list()
    if _state.get("json_output"):
        print_json(result, pretty=_state.get("pretty"))

@session_app.command("show")
def session_show(session_id: str):
    """
    Show session details.
    """
    result = cmd_session_show(session_id)
    if _state.get("json_output"):
        print_json(result, pretty=_state.get("pretty"))

@history_app.command("list")
def history_list():
    """
    List all sessions.
    """
    result = cmd_history_list()
    if _state.get("json_output"):
        print_json(result, pretty=_state.get("pretty"))

@history_app.command("view")
def history_view(session_id: str):
    """
    Show session details by id.
    """
    result = cmd_history_view(session_id)
    if _state.get("json_output"):
        print_json(result, pretty=_state.get("pretty"))

@app.command()
def apply():
    """
    Apply last patch received.
    """
    result = cmd_apply()
    if _state.get("session_id"):
        add_history_record(session_id=_state.get("session_id"), patch=_state.get("last_patch"), status="patched")
    if _state.get("json_output"):
        print_json(result, pretty=_state.get("pretty"))

@app.command()
def commit():
    """
    Commit & create branch after apply (if patch applied locally).
    """
    result = cmd_commit_and_push()
    if _state.get("json_output"):
        print_json(result, pretty=_state.get("pretty"))

@app.command()
def push():
    """
    Push branch to origin.
    """
    branch = git_current_branch()
    result = git_push_branch(branch)
    if _state.get("json_output"):
        print_json(result, pretty=_state.get("pretty"))

@pr_app.command("create")
def pr_create():
    """
    Create a GitHub PR from last branch (requires GITHUB_TOKEN).
    """
    pr_url = cmd_create_pr()
    if _state.get("session_id"):
        add_history_record(session_id=_state.get("session_id"), pr_url=pr_url, status="pr_created")
    if _state.get("json_output"):
        print_json({"pr_url": pr_url}, pretty=_state.get("pretty"))

@app.command()
def doctor():
    """
    Run environment validation checks.
    """
    result = run_doctor_command()
    if _state.get("json_output"):
        print_json(result, pretty=_state.get("pretty"))


if __name__ == "__main__":
    try:
        app()
    except JulesError as e:
        logger.error(e)
        raise typer.Exit(code=1)
    except Exception as e:
        logger.critical("Fatal error: %s", e)
        raise typer.Exit(code=1)
