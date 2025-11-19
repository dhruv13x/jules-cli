# tests/utils/test_commands.py

from unittest.mock import patch
import subprocess
from jules_cli.utils import commands

@patch('subprocess.run')
def test_run_cmd_capture(mock_subprocess):
    commands.run_cmd(["ls", "-l"])
    mock_subprocess.assert_called_once_with(["ls", "-l"], capture_output=True, text=True)

@patch('subprocess.run')
def test_run_cmd_no_capture(mock_subprocess):
    commands.run_cmd(["ls", "-l"], capture=False)
    mock_subprocess.assert_called_once_with(["ls", "-l"], capture_output=False, text=True)

@patch('subprocess.run')
@patch('jules_cli.utils.commands.logger')
def test_run_cmd_failure(mock_logger, mock_subprocess):
    mock_subprocess.return_value.returncode = 1
    mock_subprocess.return_value.stderr = "Error message"
    mock_subprocess.return_value.stdout = ""

    return_code, stdout, stderr = commands.run_cmd(["bad_command"])

    mock_subprocess.assert_called_once_with(["bad_command"], capture_output=True, text=True)
    mock_logger.error.assert_called_once_with("Command failed with code 1: Error message")
    assert return_code == 1
    assert stdout == ""
    assert stderr == "Error message"

@patch('subprocess.Popen')
def test_run_cmd_interactive_success(mock_subprocess_popen):
    mock_process = mock_subprocess_popen.return_value
    mock_process.returncode = 0

    commands.run_cmd_interactive(["git", "add", "-p"])

    mock_subprocess_popen.assert_called_once_with(["git", "add", "-p"], stdin=subprocess.PIPE)
    mock_process.communicate.assert_called_once()

@patch('subprocess.Popen')
@patch('jules_cli.utils.commands.logger')
def test_run_cmd_interactive_failure(mock_logger, mock_subprocess_popen):
    mock_process = mock_subprocess_popen.return_value
    mock_process.returncode = 1

    commands.run_cmd_interactive(["bad_interactive_command"])

    mock_subprocess_popen.assert_called_once_with(["bad_interactive_command"], stdin=subprocess.PIPE)
    mock_process.communicate.assert_called_once()
    mock_logger.error.assert_called_once_with("Command failed with code 1")
