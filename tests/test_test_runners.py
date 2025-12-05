
import pytest
from unittest.mock import patch
from jules_cli.commands.auto import auto_fix_command
from jules_cli.testing.runner import run_tests

def test_auto_fix_command_accepts_runner_unittest():
    """
    Test that auto_fix_command accepts a 'runner' argument and passes it down.
    """
    # We patch run_tests in auto.py
    with patch("jules_cli.commands.auto.run_tests") as mock_run_tests, \
         patch("jules_cli.commands.auto.config.get_nested", return_value="dummy/repo"):

        mock_run_tests.return_value = (0, "ok", "")

        # Now this should pass without TypeError
        auto_fix_command(runner="unittest")

        mock_run_tests.assert_called_with(runner="unittest")

def test_run_tests_dispatch():
    """
    Test that the test runner logic dispatches to the correct command.
    """

    with patch("jules_cli.testing.runner.run_cmd") as mock_run_cmd:
        mock_run_cmd.return_value = (0, "ok", "")

        run_tests(runner="unittest")
        mock_run_cmd.assert_called_with(["python", "-m", "unittest"])

        run_tests(runner="nose2")
        mock_run_cmd.assert_called_with(["python", "-m", "nose2"])

        run_tests(runner="pytest")
        # pytest args might differ, but at least checking it calls pytest
        args, _ = mock_run_cmd.call_args
        assert args[0][0] == "pytest"

def test_run_tests_invalid_runner():
    with pytest.raises(ValueError, match="Unknown runner: invalid"):
        run_tests(runner="invalid")
