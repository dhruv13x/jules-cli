from unittest.mock import patch
from src.jules_cli.commands import apply
from src.jules_cli.state import _state

@patch('src.jules_cli.patch.apply.apply_patch_text')
def test_cmd_apply_success(mock_apply_patch):
    _state["last_result"] = {"type": "patch", "patch": "fake_patch"}
    apply.cmd_apply()
    mock_apply_patch.assert_called_once_with("fake_patch")

@patch('src.jules_cli.patch.apply.apply_patch_text')
def test_cmd_apply_no_result(mock_apply_patch):
    _state["last_result"] = None
    apply.cmd_apply()
    mock_apply_patch.assert_not_called()

@patch('src.jules_cli.patch.apply.apply_patch_text')
def test_cmd_apply_not_patch(mock_apply_patch):
    _state["last_result"] = {"type": "pr"}
    apply.cmd_apply()
    mock_apply_patch.assert_not_called()
