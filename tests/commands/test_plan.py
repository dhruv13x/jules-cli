# tests/commands/test_plan.py

from unittest.mock import patch, MagicMock
from jules_cli.commands import plan
from jules_cli.state import _state

@patch("jules_cli.commands.plan.get_latest_session_id")
@patch("jules_cli.commands.plan.approve_plan")
@patch("jules_cli.commands.plan.poll_for_result")
def test_cmd_approve_success(mock_poll, mock_approve, mock_get_latest):
    mock_get_latest.return_value = "session-123"
    mock_poll.return_value = {"type": "message", "message": "Done"}
    _state.pop("current_session", None)

    result = plan.cmd_approve()

    assert result["status"] == "success"
    mock_approve.assert_called_with("session-123")
    mock_poll.assert_called_with("session-123")

@patch("jules_cli.commands.plan.get_latest_session_id")
def test_cmd_approve_no_session(mock_get_latest):
    mock_get_latest.return_value = None
    _state.pop("current_session", None)

    result = plan.cmd_approve()

    assert result["status"] == "error"
    assert result["message"] == "No session found."

@patch("jules_cli.commands.plan.approve_plan")
def test_cmd_approve_with_arg(mock_approve):
    with patch("jules_cli.commands.plan.poll_for_result") as mock_poll:
        mock_poll.return_value = {"type": "patch", "patch": "diff"}

        result = plan.cmd_approve(session_id="arg-session")

        assert result["status"] == "success"
        mock_approve.assert_called_with("arg-session")

@patch("jules_cli.commands.plan.get_latest_session_id")
@patch("jules_cli.commands.plan.approve_plan")
def test_cmd_approve_exception(mock_approve, mock_get_latest):
    mock_get_latest.return_value = "session-123"
    mock_approve.side_effect = Exception("API Error")

    result = plan.cmd_approve()

    assert result["status"] == "error"
    assert "API Error" in result["message"]

@patch("jules_cli.commands.plan.get_latest_session_id")
@patch("jules_cli.commands.plan.send_message")
def test_cmd_reject_success(mock_send, mock_get_latest):
    mock_get_latest.return_value = "session-123"

    result = plan.cmd_reject()

    assert result["status"] == "success"
    mock_send.assert_called_with("session-123", "I reject this plan. Please stop or propose a different approach.")

@patch("jules_cli.commands.plan.get_latest_session_id")
def test_cmd_reject_no_session(mock_get_latest):
    mock_get_latest.return_value = None
    _state.pop("current_session", None)

    result = plan.cmd_reject()

    assert result["status"] == "error"

@patch("jules_cli.commands.plan.get_latest_session_id")
@patch("jules_cli.commands.plan.send_message")
def test_cmd_reject_exception(mock_send, mock_get_latest):
    mock_get_latest.return_value = "session-123"
    mock_send.side_effect = Exception("API Error")

    result = plan.cmd_reject()

    assert result["status"] == "error"
    assert "API Error" in result["message"]

@patch("jules_cli.commands.plan.get_latest_session_id")
@patch("jules_cli.commands.plan.approve_plan")
@patch("jules_cli.commands.plan.poll_for_result")
def test_cmd_approve_pr_result(mock_poll, mock_approve, mock_get_latest):
    mock_get_latest.return_value = "session-123"
    mock_poll.return_value = {"type": "pr", "pr": {"url": "http://github.com/pr/1"}}

    result = plan.cmd_approve()

    assert result["status"] == "success"

@patch("jules_cli.commands.plan.approve_plan")
@patch("jules_cli.commands.plan.poll_for_result")
def test_cmd_approve_state_session(mock_poll, mock_approve):
    _state["current_session"] = {"id": "state-session"}
    mock_poll.return_value = {"type": "message", "message": "Done"}

    result = plan.cmd_approve()

    assert result["status"] == "success"
    mock_approve.assert_called_with("state-session")
    _state.pop("current_session", None)
