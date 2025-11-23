from unittest.mock import patch, MagicMock
import pytest
from jules_cli.commands import history
from jules_cli.pytest import runner
from jules_cli.utils.exceptions import JulesError, TestRunnerError
import json
import sqlite3

# Coverage for history and runner

def test_history_list_no_sessions():
    with patch("jules_cli.commands.history.get_db_path") as mock_path:
        with patch("sqlite3.connect") as mock_conn:
            mock_conn.return_value.cursor.return_value.fetchall.return_value = []
            result = history.cmd_history_list()
            assert result == []

def test_history_list_with_sessions():
    with patch("jules_cli.commands.history.get_db_path") as mock_path:
        with patch("sqlite3.connect") as mock_conn:
            mock_conn.return_value.cursor.return_value.fetchall.return_value = [
                ("sess1", "time", "prompt", "ok")
            ]
            result = history.cmd_history_list()
            assert len(result) == 1
            assert result[0]["session_id"] == "sess1"

def test_history_list_db_error():
    with patch("jules_cli.commands.history.get_db_path") as mock_path:
        with patch("sqlite3.connect", side_effect=sqlite3.Error("fail")):
            result = history.cmd_history_list()
            assert "error" in result

def test_history_view_success():
    with patch("jules_cli.commands.history.get_db_path") as mock_path:
        with patch("sqlite3.connect") as mock_conn:
            mock_conn.return_value.cursor.return_value.fetchone.return_value = (
                "sess1", "time", "prompt", "patch", "pr", "ok"
            )
            result = history.cmd_history_view("sess1")
            assert result["session_id"] == "sess1"

def test_history_view_not_found():
    with patch("jules_cli.commands.history.get_db_path") as mock_path:
        with patch("sqlite3.connect") as mock_conn:
            mock_conn.return_value.cursor.return_value.fetchone.return_value = None
            result = history.cmd_history_view("sess1")
            assert "error" in result
            assert result["error"] == "Session not found."

def test_history_view_db_error():
    with patch("jules_cli.commands.history.get_db_path") as mock_path:
        with patch("sqlite3.connect", side_effect=sqlite3.Error("fail")):
            result = history.cmd_history_view("sess1")
            assert "error" in result

def test_runner_run_pytest_report_read_error():
    # Test reading report json fails
    with patch("jules_cli.pytest.runner.run_cmd") as mock_run:
        mock_run.return_value = (0, "ok", "")
        # open("report.json") raises FileNotFoundError
        # runner catches it and logs warning
        with patch("builtins.open", side_effect=FileNotFoundError):
             with patch("jules_cli.pytest.runner.logger") as mock_logger:
                 code, out, err = runner.run_pytest()
                 assert code == 0
                 mock_logger.warning.assert_called_with("Could not read pytest report.")

def test_runner_run_pytest_json_decode_error():
    with patch("jules_cli.pytest.runner.run_cmd") as mock_run:
        mock_run.return_value = (0, "ok", "")
        with patch("builtins.open", new_callable=MagicMock): # mock open context manager
             with patch("json.load", side_effect=json.JSONDecodeError("msg", "doc", 0)):
                 with patch("jules_cli.pytest.runner.logger") as mock_logger:
                     code, out, err = runner.run_pytest()
                     mock_logger.warning.assert_called_with("Could not read pytest report.")
