# tests/commands/test_suggest.py

from unittest.mock import patch
from jules_cli.commands import suggest

@patch("jules_cli.commands.suggest.run_task")
def test_cmd_suggest_default(mock_run_task):
    mock_run_task.return_value = {"status": "success"}

    result = suggest.cmd_suggest()

    assert result["status"] == "success"
    mock_run_task.assert_called_once()
    args, kwargs = mock_run_task.call_args
    assert suggest.MASTER_SUGGEST_PROMPT in args[0]
    assert kwargs["timeout"] == 600

@patch("jules_cli.commands.suggest.run_task")
def test_cmd_suggest_security(mock_run_task):
    mock_run_task.return_value = {"status": "success"}

    suggest.cmd_suggest(security=True)

    args, _ = mock_run_task.call_args
    assert suggest.SECURITY_PROMPT in args[0]

@patch("jules_cli.commands.suggest.run_task")
def test_cmd_suggest_tests(mock_run_task):
    mock_run_task.return_value = {"status": "success"}

    suggest.cmd_suggest(tests=True)

    args, _ = mock_run_task.call_args
    assert suggest.TESTS_PROMPT in args[0]

@patch("jules_cli.commands.suggest.run_task")
def test_cmd_suggest_chore(mock_run_task):
    mock_run_task.return_value = {"status": "success"}

    suggest.cmd_suggest(chore=True)

    args, _ = mock_run_task.call_args
    assert suggest.CHORE_PROMPT in args[0]

@patch("jules_cli.commands.suggest.run_task")
def test_cmd_suggest_with_focus(mock_run_task):
    mock_run_task.return_value = {"status": "success"}

    suggest.cmd_suggest(focus="auth module")

    args, _ = mock_run_task.call_args
    assert suggest.MASTER_SUGGEST_PROMPT in args[0]
    assert "AUTH MODULE" in args[0]

@patch("jules_cli.commands.suggest.run_task")
def test_cmd_suggest_security_with_focus(mock_run_task):
    suggest.cmd_suggest(security=True, focus="api keys")

    args, _ = mock_run_task.call_args
    assert suggest.SECURITY_PROMPT in args[0]
    assert "API KEYS" in args[0]
