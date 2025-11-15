
import json
from unittest.mock import patch
from jules_cli.utils.output import print_json

@patch("builtins.print")
def test_print_json(mock_print):
    data = {"key": "value"}
    print_json(data)
    mock_print.assert_called_once_with(json.dumps(data))

@patch("builtins.print")
def test_print_json_pretty(mock_print):
    data = {"key": "value"}
    print_json(data, pretty=True)
    mock_print.assert_called_once_with(json.dumps(data, indent=2))
