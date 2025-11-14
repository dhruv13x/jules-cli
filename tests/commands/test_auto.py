from unittest.mock import patch
from src.jules_cli.commands import auto

@patch('src.jules_cli.commands.auto.run_pytest', return_value=(0, "", ""))
@patch('src.jules_cli.commands.auto.run_task')
def test_auto_fix_command_success(mock_run_task, mock_run_pytest):
    auto.auto_fix_command()
    mock_run_task.assert_not_called()

@patch('src.jules_cli.commands.auto.run_pytest', return_value=(1, "out", "err"))
@patch('src.jules_cli.commands.auto.run_task')
def test_auto_fix_command_failure(mock_run_task, mock_run_pytest):
    with patch('src.jules_cli.commands.auto.prompt_from_failure', return_value="prompt"):
        auto.auto_fix_command()
        mock_run_task.assert_called_once_with("prompt", repo_dir_name="bot_platform", auto=True)
