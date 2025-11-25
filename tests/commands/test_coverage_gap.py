# tests/commands/test_coverage_gap.py

from unittest.mock import patch, MagicMock
import pytest
from jules_cli.commands import auto, task, apply, pr, refactor
from jules_cli.pytest import runner as test_runner
from jules_cli.utils.exceptions import JulesError, GitError
import subprocess
import os

# Coverage for commands modules

def test_auto_fix_command_success():
    with patch("jules_cli.commands.auto.run_pytest") as mock_test:
        with patch("jules_cli.commands.auto.run_task") as mock_task:
            with patch("jules_cli.commands.auto.config.get_nested") as mock_config:
                mock_config.return_value = "o/r"
                mock_test.return_value = (1, "fail", "")
                mock_task.return_value = {"status": "running"}

                result = auto.auto_fix_command()
                assert result["status"] == "running"
                mock_task.assert_called()

def test_auto_fix_command_no_repo():
    with patch("jules_cli.commands.auto.config.get_nested") as mock_config:
        mock_config.return_value = None
        with pytest.raises(RuntimeError, match="No repository specified"):
            auto.auto_fix_command()

def test_auto_fix_command_no_failures():
    with patch("jules_cli.commands.auto.run_pytest") as mock_test:
        with patch("jules_cli.commands.auto.config.get_nested") as mock_config:
            mock_config.return_value = "o/r"
            mock_test.return_value = (0, "ok", "")

            result = auto.auto_fix_command()
            assert result["status"] == "success"

def test_task_run_task_success():
    with patch("jules_cli.commands.task.create_session") as mock_sess:
        with patch("jules_cli.commands.task.poll_for_result") as mock_poll:
            with patch("jules_cli.commands.task.pick_source_for_repo") as mock_pick:
                with patch("jules_cli.commands.task.config") as mock_config:
                    with patch("jules_cli.commands.task._state", new_callable=dict) as mock_state:
                        # Setup
                        mock_pick.return_value = {"name": "source", "githubRepo": {"owner": "o", "repo": "r"}}
                        mock_sess.return_value = {"name": "sessions/123", "id": "123"}
                        mock_poll.return_value = {"type": "patch", "patch": "diff"}

                        result = task.run_task("do it", repo_dir_name="o/r")
                        assert result["type"] == "patch"
                        # The test failure earlier was KeyError. The code in `run_task`:
                        # sess = create_session(...)
                        # _state["current_session"] = sess
                        # if not sid: ...
                        # ... poll_for_result
                        # ... _state["last_result"] = result
                        # ... return result
                        pass

def test_task_run_task_no_repo():
    with patch("jules_cli.commands.task.config.get_nested") as mock_config:
        mock_config.return_value = None
        with pytest.raises(RuntimeError, match="No repository specified"):
            task.run_task("do it")

def test_task_run_task_no_source_match():
    with patch("jules_cli.commands.task.pick_source_for_repo") as mock_pick:
        with patch("jules_cli.commands.task.list_sources") as mock_list:
            mock_pick.return_value = None
            mock_list.return_value = [{"name": "other"}]
            with pytest.raises(RuntimeError, match="No source matched"):
                task.run_task("do it", repo_dir_name="o/r")

def test_task_run_task_pr_result():
    with patch("jules_cli.commands.task.create_session") as mock_sess:
        with patch("jules_cli.commands.task.poll_for_result") as mock_poll:
            with patch("jules_cli.commands.task.pick_source_for_repo") as mock_pick:
                 with patch("jules_cli.commands.task.config"):
                    with patch("jules_cli.commands.task._state", new_callable=dict):
                        mock_pick.return_value = {"name": "source", "githubRepo": {"owner": "o", "repo": "r"}}
                        mock_sess.return_value = {"id": "123"}
                        mock_poll.return_value = {"type": "pr", "pr": {"url": "url"}}

                        result = task.run_task("do it", repo_dir_name="o/r")
                        assert result["type"] == "pr"

def test_task_run_task_plan_result():
    with patch("jules_cli.commands.task.create_session") as mock_sess:
        with patch("jules_cli.commands.task.poll_for_result") as mock_poll:
            with patch("jules_cli.commands.task.pick_source_for_repo") as mock_pick:
                 with patch("jules_cli.commands.task.config"):
                    with patch("jules_cli.commands.task._state", new_callable=dict):
                        mock_pick.return_value = {"name": "source", "githubRepo": {"owner": "o", "repo": "r"}}
                        mock_sess.return_value = {"id": "123"}
                        mock_poll.return_value = {
                            "type": "plan",
                            "plan": {"steps": [{"title": "s1", "description": "d1"}]}
                        }

                        result = task.run_task("do it", repo_dir_name="o/r")
                        assert result["type"] == "plan"

def test_task_run_task_status_result():
    with patch("jules_cli.commands.task.create_session") as mock_sess:
        with patch("jules_cli.commands.task.poll_for_result") as mock_poll:
            with patch("jules_cli.commands.task.pick_source_for_repo") as mock_pick:
                 with patch("jules_cli.commands.task.config"):
                    with patch("jules_cli.commands.task._state", new_callable=dict):
                        mock_pick.return_value = {"name": "source", "githubRepo": {"owner": "o", "repo": "r"}}
                        mock_sess.return_value = {"id": "123"}
                        mock_poll.return_value = {
                            "type": "session_status",
                            "status": "COMPLETED",
                            "session": {"id": "123"}
                        }

                        result = task.run_task("do it", repo_dir_name="o/r")
                        assert result["type"] == "session_status"

def test_apply_cmd_apply_no_patch_memory_or_db():
    with patch("jules_cli.commands.apply._state", new_callable=dict) as mock_state:
        mock_state.update({})
        with patch("jules_cli.commands.apply.get_latest_session_id") as mock_db:
            mock_db.return_value = None
            result = apply.cmd_apply()
            assert result["status"] == "error"
            assert "No last result" in result["message"]

def test_apply_cmd_apply_fetch_from_db_success():
    with patch("jules_cli.commands.apply._state", new_callable=dict) as mock_state:
        mock_state.update({})
        with patch("jules_cli.commands.apply.get_latest_session_id") as mock_db:
            mock_db.return_value = "sess1"
            with patch("jules_cli.commands.apply.poll_for_result") as mock_poll:
                mock_poll.return_value = {"type": "patch", "patch": "diff"}
                with patch("jules_cli.commands.apply.apply_patch_text") as mock_apply_func:
                    result = apply.cmd_apply()
                    assert result["status"] == "success"

def test_apply_cmd_apply_not_patch_type():
    with patch("jules_cli.commands.apply._state", new_callable=dict) as mock_state:
        mock_state.update({"last_result": {"type": "pr"}})
        result = apply.cmd_apply()
        assert result["status"] == "error"
        assert "not a patch" in result["message"]

def test_apply_cmd_apply_success_memory():
    with patch("jules_cli.commands.apply._state", new_callable=dict) as mock_state:
        mock_state.update({"last_result": {"type": "patch", "patch": "diff"}})
        with patch("jules_cli.commands.apply.apply_patch_text") as mock_apply_func:
            with patch("jules_cli.commands.apply.save_to_cache"):
                result = apply.cmd_apply()
                assert result["status"] == "success"
                mock_apply_func.assert_called_with("diff")

def test_pr_create_pr_success():
    # pr.py: from ..git.vcs import ... github_create_pr
    with patch("jules_cli.commands.pr.github_create_pr") as mock_gh:
        mock_gh.return_value = {"html_url": "http://pr", "number": 123}
        # Patch GITHUB_TOKEN in the module
        with patch("jules_cli.commands.pr.GITHUB_TOKEN", "token"):
             with patch("jules_cli.commands.pr._state", new_callable=dict) as mock_state:
                 mock_state.update({"repo_owner": "o", "repo_name": "r"})
                 with patch("jules_cli.commands.pr.git_current_branch", return_value="feature"):
                     with patch("jules_cli.commands.pr.save_to_cache"):
                        pr_dict = pr.cmd_create_pr(title="t", body="b")
                        assert pr_dict["html_url"] == "http://pr"

def test_refactor_run_refactor_success():
    # refactor.py calls pick_source_for_repo, create_session, poll_for_result, send_message
    # it does NOT use run_task, it implements its own loop.
    with patch("jules_cli.commands.refactor.pick_source_for_repo") as mock_pick:
        with patch("jules_cli.commands.refactor.create_session") as mock_sess:
            with patch("jules_cli.commands.refactor.poll_for_result") as mock_poll:
                 with patch("jules_cli.commands.refactor.send_message") as mock_send:
                      with patch("jules_cli.commands.refactor.config"):
                        mock_pick.return_value = {"name": "src", "githubRepo": {"owner": "o", "repo": "r"}}
                        mock_sess.return_value = {"id": "123"}

                        # Sequence: poll for plan, then loop through steps
                        # mock_poll side_effect:
                        # 1. returns plan
                        # 2. returns result for step 1
                        mock_poll.side_effect = [
                            {"plan": ["step1"]}, # plan result
                            {"type": "patch", "patch": "diff"} # step result
                        ]

                        result = refactor.run_refactor("instr", repo_dir_name="o/r")
                        assert result["type"] == "patch"

def test_runner_run_pytest_timeout():
    # runner.py: run_cmd from ..utils.commands
    # patch jules_cli.pytest.runner.run_cmd
    with patch("jules_cli.pytest.runner.run_cmd") as mock_run:
        # run_cmd in utils/commands.py wraps subprocess.run
        # runner.py calls run_cmd. If run_cmd raises TimeoutExpired (it propagates it), runner doesn't catch it.
        # Wait, run_cmd implementation in utils/commands.py:
        # def run_cmd(...): result = subprocess.run(...); return ...
        # If subprocess.run raises TimeoutExpired, run_cmd propagates it.
        # runner.py calls run_cmd.
        # If I want to test runner.py behavior when timeout happens, I should check if it handles it or propagates it.
        # Looking at runner.py (I read it earlier):
        # try: ... except (FileNotFoundError, json.JSONDecodeError): ...
        # It does NOT catch TimeoutExpired. So it should propagate.
        mock_run.side_effect = subprocess.TimeoutExpired(cmd="pytest", timeout=10)
        with pytest.raises(subprocess.TimeoutExpired):
             test_runner.run_pytest()

def test_runner_run_pytest_error():
    # It catches FileNotFoundError/JSONDecodeError for report reading, but not general run errors.
    with patch("jules_cli.pytest.runner.run_cmd") as mock_run:
        mock_run.side_effect = Exception("Boom")
        with pytest.raises(Exception, match="Boom"):
             test_runner.run_pytest()
