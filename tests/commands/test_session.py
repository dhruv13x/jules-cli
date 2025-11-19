# tests/commands/test_session.py

from unittest.mock import patch
from jules_cli.commands import session

@patch('jules_cli.core.api._http_request')
@patch('jules_cli.commands.session.load_from_cache', return_value=None)
def test_cmd_session_list(mock_load_from_cache, mock_http_request):
    mock_http_request.return_value = {"sessions": []}
    session.cmd_session_list()
    mock_http_request.assert_called_once_with("GET", "/sessions", params={"pageSize": 20})

@patch('jules_cli.core.api._http_request')
@patch('jules_cli.commands.session.load_from_cache', return_value=None)
def test_cmd_session_show(mock_load_from_cache, mock_http_request):
    mock_http_request.return_value = {"id": "session_id"}
    session.cmd_session_show("session_id")
    mock_http_request.assert_called_once_with("GET", f"/sessions/session_id")
