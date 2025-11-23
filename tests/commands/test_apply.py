# tests/commands/test_apply.py

from unittest.mock import patch
from jules_cli.commands import apply
from jules_cli.state import _state

@patch('jules_cli.commands.apply.apply_patch_text')
def test_cmd_apply_success(mock_apply_patch):
    _state["last_result"] = {"type": "patch", "patch": "fake_patch"}
    apply.cmd_apply()
    mock_apply_patch.assert_called_once_with("fake_patch")

@patch('jules_cli.commands.apply.apply_patch_text')
@patch('jules_cli.commands.apply.poll_for_result', return_value=None)
def test_cmd_apply_no_result(mock_poll_for_result, mock_apply_patch):
    _state["last_result"] = None
    apply.cmd_apply()
    mock_apply_patch.assert_not_called()

@patch('jules_cli.commands.apply.apply_patch_text')
def test_cmd_apply_not_patch(mock_apply_patch):
    _state["last_result"] = {"type": "pr"}
    apply.cmd_apply()
    mock_apply_patch.assert_not_called()
