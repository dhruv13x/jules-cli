from unittest.mock import patch, MagicMock
from src.jules_cli import cli

@patch('src.jules_cli.cli.repl')
def test_main(mock_repl):
    with patch('argparse.ArgumentParser.parse_args', return_value=MagicMock(debug=False, no_color=False)):
        with patch('src.jules_cli.cli.check_env'):
            cli.main()
            mock_repl.assert_called_once()

@patch('builtins.input', side_effect=['task "my task"', 'exit'])
@patch('src.jules_cli.cli.run_task')
def test_repl_task_command(mock_run_task, mock_input):
    cli.repl()
    mock_run_task.assert_called_once_with("my task")

@patch('builtins.input', side_effect=['apply', 'pr create', 'exit'])
@patch('src.jules_cli.cli.cmd_apply')
@patch('src.jules_cli.cli.cmd_create_pr')
def test_repl_apply_and_pr_before_task(mock_cmd_create_pr, mock_cmd_apply, mock_input):
    cli.repl()
    mock_cmd_apply.assert_called_once()
    mock_cmd_create_pr.assert_called_once()
