# tests/commands/test_stage.py


from unittest.mock import patch
from jules_cli.commands.stage import cmd_stage

@patch("jules_cli.commands.stage.git_is_clean", return_value=False)
@patch("jules_cli.commands.stage.run_cmd_interactive")
def test_cmd_stage(mock_run_cmd_interactive, mock_git_is_clean):
    mock_run_cmd_interactive.return_value = 0
    result = cmd_stage()
    assert result["status"] == "success"
    mock_run_cmd_interactive.assert_called_once_with(["git", "add", "-p"])

@patch("jules_cli.commands.stage.git_is_clean", return_value=False)
@patch("jules_cli.commands.stage.run_cmd_interactive", side_effect=Exception("Staging failed"))
def test_cmd_stage_fails(mock_run_cmd_interactive, mock_git_is_clean):
    result = cmd_stage()
    assert result["status"] == "error"
    assert "Staging failed" in result["message"]

@patch("jules_cli.commands.stage.git_is_clean", return_value=True)
def test_cmd_stage_clean(mock_git_is_clean):
    result = cmd_stage()
    assert result["status"] == "success"
    assert result["message"] == "No changes."
