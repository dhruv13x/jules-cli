#!/usr/bin/env python3
"""
Jules Interactive CLI (Option C - immersive assistant)
"""

import os
import shlex
import json

from .commands.auto import auto_fix_command
from .commands.task import run_task
from .commands.session import cmd_session_list, cmd_session_show
from .commands.apply import cmd_apply
from .commands.commit import cmd_commit_and_push
from .commands.pr import cmd_create_pr
from .git.vcs import git_push_branch, git_current_branch
from .state import _state
from .utils.environment import check_env

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
  last                      Show last result/session
  help                      Show this help
  exit                      Quit
"""

def repl():
    print(WELCOME)
    while True:
        try:
            raw = input("jules> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
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
                print(WELCOME)
            elif cmd == "auto":
                auto_fix_command()
            elif cmd == "task":
                # join remainder as the prompt
                prompt = raw[len("task"):].strip()
                if not prompt:
                    print("Usage: task \"Your description here\"")
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
                try:
                    git_push_branch(branch)
                except Exception as e:
                    print("Push failed:", e)
            elif cmd == "pr" and args and args[0] == "create":
                cmd_create_pr()
            elif cmd == "last":
                print("current_session:", json.dumps(_state.get("current_session"), indent=2))
                print("last_result:", json.dumps(_state.get("last_result"), indent=2))
            else:
                print("Unknown command. Type 'help' for commands.")
        except Exception as e:
            print("[!] Error during command:", e)

def main():
    check_env()
    print("Jules CLI starting. JULES_API_KEY detected.")
    repl()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("Fatal error:", e)
        raise
