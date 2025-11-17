# tests/test_cli_coverage.py


import os
from unittest.mock import patch
from typer.testing import CliRunner
from jules_cli.cli import app

runner = CliRunner()

def setup_function():
    os.environ["JULES_API_KEY"] = "test-key"

def test_json_output():
    result = runner.invoke(app, ["doctor", "--json"])
    assert result.exit_code == 0
    assert '"JULES_API_KEY"' in result.stdout

def test_pretty_json_output():
    result = runner.invoke(app, ["doctor", "--json", "--pretty"])
    assert result.exit_code == 0
    assert '"JULES_API_KEY"' in result.stdout

def test_no_color_output():
    result = runner.invoke(app, ["doctor", "--no-color"])
    assert result.exit_code == 0

def test_push_command():
    with patch("jules_cli.cli.git_push_branch") as mock_push:
        mock_push.return_value = {"status": "success"}
        result = runner.invoke(app, ["push"])
        assert result.exit_code == 0
        mock_push.assert_called_once()
