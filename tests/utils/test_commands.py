from unittest.mock import patch
from src.jules_cli.utils import commands

@patch('subprocess.run')
def test_run_cmd_capture(mock_subprocess):
    commands.run_cmd(["ls", "-l"])
    mock_subprocess.assert_called_once_with(["ls", "-l"], capture_output=True, text=True)

@patch('subprocess.run')
def test_run_cmd_no_capture(mock_subprocess):
    commands.run_cmd(["ls", "-l"], capture=False)
    mock_subprocess.assert_called_once_with(["ls", "-l"], capture_output=False, text=True)
