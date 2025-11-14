#!/usr/bin/env python3
"""
Jules Interactive CLI (Option C - immersive assistant)
"""

import os
import shlex
import json
import argparse

from .commands.auto import auto_fix_command
from .commands.task import run_task
from .commands.session import cmd_session_list, cmd_session_show
from .commands.apply import cmd_apply
from .commands.commit import cmd_commit_and_push
from .commands.pr import cmd_create_pr
from .commands.doctor import run_doctor_command
from .git.vcs import git_push_branch, git_current_branch
from .state import _state
from .utils.environment import check_env
from .utils.logging import logger, setup_logging
from .utils.exceptions import JulesError
from .utils.config import config

WELCOME = """
Jules Interactive CLI — fully immersive developer assistant.

Commands:
  auto                      Run pytest and auto-fix failures
  task "your instruction"    Ask Jules to perform arbitrary dev task (bugfix/refactor/tests/docs)
  session list              List sessions
  session show <SESSION_ID> Show session details
  apply                     Apply last patch received
  commit                    Commit & create branch after apply (if patch applied locally)
  push                      Push branch to origin
  pr create                 Create a GitHub PR from last branch (requires GITHUB_TOKEN)
  doctor                    Run environment validation checks
  last                      Show last result/session
  help                      Show this help
  exit                      Quit
"""

def repl():
    logger.info(WELCOME)
    while True:
        try:
            raw = input("jules> ").strip()
        except (EOFError, KeyboardInterrupt):
            logger.info("\nExiting.")
            break
        if not raw:
            continue
        parts = shlex.split(raw)
        cmd = parts[0].lower()
        args = parts[1:]
        try:
            if cmd in ("exit", "quit"):
                break
            elif cmd == "help":
                logger.info(WELCOME)
            elif cmd == "auto":
                auto_fix_command()
            elif cmd == "task":
                # join remainder as the prompt
                prompt = raw[len("task"):].strip()
                if not prompt:
                    logger.warning("Usage: task \"Your description here\"")
                    continue
                # if user wraps with quotes, strip them
                if (prompt.startswith('"') and prompt.endswith('"')) or (prompt.startswith("'") and prompt.endswith("'")):
                    prompt = prompt[1:-1]
                run_task(prompt)
            elif cmd == "session" and args and args[0] == "list":
                cmd_session_list()
            elif cmd == "session" and args and args[0] == "show" and len(args) > 1:
                cmd_session_show(args[1])
            elif cmd == "apply":
                cmd_apply()
            elif cmd == "commit":
                cmd_commit_and_push()
            elif cmd == "push":
                # assume last created branch is current; push current branch
                branch = git_current_branch()
                git_push_branch(branch)
            elif cmd == "pr" and args and args[0] == "create":
                cmd_create_pr()
            elif cmd == "doctor":
                json_output = "--json" in args
                run_doctor_command(json_output=json_output)
            elif cmd == "last":
                logger.info("current_session: %s", json.dumps(_state.get("current_session"), indent=2))
                logger.info("last_result: %s", json.dumps(_state.get("last_result"), indent=2))
            else:
                logger.warning("Unknown command. Type 'help' for commands.")
        except JulesError as e:
            logger.error(e)
        except Exception as e:
            logger.error("An unexpected error occurred: %s", e)


def main():
    parser = argparse.ArgumentParser(description="Jules Interactive CLI")
    parser.add_argument("--debug", action="store_true", help="Enable debug logging.")
    parser.add_argument("--no-color", action="store_true", help="Disable colored output.")
    args = parser.parse_args()

    log_level = config.get("log_level", "INFO").upper()
    if args.debug:
        log_level = "DEBUG"

    color_mode = config.get("color_mode", "auto")
    use_color = not args.no_color and color_mode != "off"

    setup_logging(level=log_level, color=use_color)

    try:
        check_env()
    except JulesError as e:
        logger.error(e)
        return

    logger.info("Jules CLI starting. JULES_API_KEY detected.")
    repl()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical("Fatal error: %s", e)
        raise
