import pytest
from unittest.mock import patch, MagicMock
from jules_cli.commands.apply import cmd_apply
from jules_cli.utils.logging import logger

@patch("jules_cli.commands.apply._state", {})
@patch("jules_cli.commands.apply.get_latest_session_id", return_value="sess_123")
@patch("jules_cli.commands.apply.poll_for_result")
@patch("jules_cli.commands.apply.logger")
def test_apply_swallows_exception(mock_logger, mock_poll, mock_get_latest_session):
    # Setup: poll_for_result raises an exception
    mock_poll.side_effect = Exception("API Error")

    # Execute
    cmd_apply()

    # Verify:
    # Current behavior: The exception is swallowed (pass), and then it logs "No last result to apply."
    # We want to ensure that the exception is LOGGED properly before swallowing/ignoring.

    # Check if logger.debug or logger.error was called with the exception info
    # currently it is NOT logged. So this test expects failure if we assert it was logged.

    # Let's see if we can catch the lack of logging
    found_log = False
    for call in mock_logger.method_calls:
        # We look for something that logs the exception
        if "API Error" in str(call):
            found_log = True
            break

    assert found_log, "Exception from poll_for_result was not logged!"
