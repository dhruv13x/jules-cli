# tests/commands/test_auto.py

from unittest.mock import patch
from jules_cli.commands import auto
from jules_cli.utils import environment
from jules_cli.utils.config import config

@patch('jules_cli.commands.auto.run_tests', return_value=(0, "", ""))
@patch('jules_cli.commands.auto.run_task')
@patch.object(environment, 'check_env')
@patch.object(config, 'get_nested', return_value="owner/repo")
def test_auto_fix_command_success(mock_get_nested, mock_check_env, mock_run_task, mock_run_tests):
    auto.auto_fix_command()
    mock_run_task.assert_not_called()

@patch('jules_cli.commands.auto.run_tests', return_value=(1, "out", "err"))
@patch('jules_cli.commands.auto.run_task')
@patch.object(environment, 'check_env')
@patch.object(config, 'get_nested', return_value="bot_platform")
def test_auto_fix_command_failure(mock_get_nested, mock_check_env, mock_run_task, mock_run_tests):
    with patch('jules_cli.commands.auto.prompt_from_failure', return_value="prompt"):
        auto.auto_fix_command()
        mock_run_task.assert_called_once_with("prompt", repo_dir_name="bot_platform", auto=True)
