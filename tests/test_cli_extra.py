from unittest.mock import patch
from src.jules_cli import cli
from src.jules_cli.utils.exceptions import JulesError

@patch('builtins.input', side_effect=['help', 'exit'])
@patch('src.jules_cli.cli.logger')
def test_repl_help_command(mock_logger, mock_input):
    cli.repl()
    mock_logger.info.assert_called_with(cli.WELCOME)

@patch('builtins.input', side_effect=['auto', 'exit'])
@patch('src.jules_cli.cli.auto_fix_command')
def test_repl_auto_command(mock_auto_fix_command, mock_input):
    cli.repl()
    mock_auto_fix_command.assert_called_once()

@patch('builtins.input', side_effect=['session list', 'exit'])
@patch('src.jules_cli.cli.cmd_session_list')
def test_repl_session_list_command(mock_cmd_session_list, mock_input):
    cli.repl()
    mock_cmd_session_list.assert_called_once()

@patch('builtins.input', side_effect=['session show 123', 'exit'])
@patch('src.jules_cli.cli.cmd_session_show')
def test_repl_session_show_command(mock_cmd_session_show, mock_input):
    cli.repl()
    mock_cmd_session_show.assert_called_once_with('123')

@patch('builtins.input', side_effect=['apply', 'exit'])
@patch('src.jules_cli.cli.cmd_apply')
def test_repl_apply_command(mock_cmd_apply, mock_input):
    cli.repl()
    mock_cmd_apply.assert_called_once()

@patch('builtins.input', side_effect=['commit', 'exit'])
@patch('src.jules_cli.cli.cmd_commit_and_push')
def test_repl_commit_command(mock_cmd_commit_and_push, mock_input):
    cli.repl()
    mock_cmd_commit_and_push.assert_called_once()

@patch('builtins.input', side_effect=['push', 'exit'])
@patch('src.jules_cli.cli.git_current_branch', return_value='my-branch')
@patch('src.jules_cli.cli.git_push_branch')
def test_repl_push_command(mock_git_push_branch, mock_git_current_branch, mock_input):
    cli.repl()
    mock_git_current_branch.assert_called_once()
    mock_git_push_branch.assert_called_once_with('my-branch')

@patch('builtins.input', side_effect=['pr create', 'exit'])
@patch('src.jules_cli.cli.cmd_create_pr')
def test_repl_pr_create_command(mock_cmd_create_pr, mock_input):
    cli.repl()
    mock_cmd_create_pr.assert_called_once()

@patch('builtins.input', side_effect=['doctor', 'exit'])
@patch('src.jules_cli.cli.run_doctor_command')
def test_repl_doctor_command(mock_run_doctor_command, mock_input):
    cli.repl()
    mock_run_doctor_command.assert_called_once_with(json_output=False)

@patch('builtins.input', side_effect=['last', 'exit'])
@patch('src.jules_cli.cli.logger')
def test_repl_last_command(mock_logger, mock_input):
    cli.repl()
    mock_logger.info.assert_called()

@patch('builtins.input', side_effect=['unknown', 'exit'])
@patch('src.jules_cli.cli.logger')
def test_repl_unknown_command(mock_logger, mock_input):
    cli.repl()
    mock_logger.warning.assert_called_with("Unknown command. Type 'help' for commands.")

@patch('src.jules_cli.cli.main')
def test_main_entry_point(mock_main):
    with patch.object(cli, "__name__", "__main__"):
        with patch.object(cli, "main", mock_main):
            # ToDo: Find a way to test the __main__ block
            pass

@patch('argparse.ArgumentParser.parse_args')
@patch('src.jules_cli.cli.check_env', side_effect=JulesError("test error"))
@patch('src.jules_cli.cli.logger')
def test_main_jules_error(mock_logger, mock_check_env, mock_parse_args):
    cli.main()
    mock_logger.error.assert_called_once()
    assert "test error" in str(mock_logger.error.call_args)
