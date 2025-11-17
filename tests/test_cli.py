# tests/test_cli.py

from unittest.mock import patch
from typer.testing import CliRunner
from src.jules_cli.cli import app

runner = CliRunner()

def test_main_callback():
    with patch('src.jules_cli.cli.check_env') as mock_check_env, \
         patch('src.jules_cli.cli.init_db') as mock_init_db, \
         patch('src.jules_cli.cli.run_doctor_command'):
        result = runner.invoke(app, ["doctor"])
        assert result.exit_code == 0
        mock_check_env.assert_called_once()
        mock_init_db.assert_called_once()

def test_task_command():
    with patch('src.jules_cli.cli.run_task') as mock_run_task, \
         patch('src.jules_cli.cli.add_history_record') as mock_add_history, \
         patch('src.jules_cli.cli.check_env'), \
         patch('src.jules_cli.cli.init_db'):
        result = runner.invoke(app, ["task", "my task"])
        assert result.exit_code == 0
        mock_run_task.assert_called_once_with("my task")
        mock_add_history.assert_called_once()

def test_apply_command():
    with patch('src.jules_cli.cli.cmd_apply') as mock_cmd_apply, \
         patch('src.jules_cli.cli.add_history_record'), \
         patch('src.jules_cli.cli.check_env'), \
         patch('src.jules_cli.cli.init_db'):
        result = runner.invoke(app, ["apply"])
        assert result.exit_code == 0
        mock_cmd_apply.assert_called_once()

def test_pr_create_command():
    with patch('src.jules_cli.cli.cmd_create_pr') as mock_cmd_create_pr, \
         patch('src.jules_cli.cli.add_history_record'), \
         patch('src.jules_cli.cli.check_env'), \
         patch('src.jules_cli.cli.init_db'):
        result = runner.invoke(app, ["pr", "create"])
        assert result.exit_code == 0
        mock_cmd_create_pr.assert_called_once()
