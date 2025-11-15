
import json
from unittest.mock import patch, mock_open
from jules_cli.pytest.runner import run_pytest

@patch("jules_cli.pytest.runner.run_cmd")
def test_run_pytest_summary(mock_run_cmd):
    mock_run_cmd.return_value = (0, "", "")

    report_data = {
        "summary": {
            "passed": 5,
            "failed": 2,
            "skipped": 1,
        }
    }

    with patch("builtins.open", mock_open(read_data=json.dumps(report_data))):
        with patch("jules_cli.pytest.runner.logger") as mock_logger:
            run_pytest()
            mock_logger.info.assert_any_call("Test run summary: 5 passed, 2 failed, 1 skipped.")
