# tests/commands/test_session.py

import json
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

@patch('jules_cli.commands.session.load_from_cache')
@patch('jules_cli.commands.session.list_sessions')
@patch('jules_cli.commands.session.logger')
def test_cmd_session_list_cached(mock_logger, mock_list_sessions, mock_load_from_cache):
    cached_data = {"sessions": [{"id": "cached_session_id"}]}
    mock_load_from_cache.return_value = cached_data

    result = session.cmd_session_list()

    mock_load_from_cache.assert_called_once_with("session_list")
    mock_list_sessions.assert_not_called()
    mock_logger.info.assert_any_call("Loaded session list from cache.")
    mock_logger.info.assert_any_call(json.dumps(cached_data, indent=2))
    assert result == cached_data

@patch('jules_cli.commands.session.load_from_cache')
@patch('jules_cli.commands.session.get_session')
@patch('jules_cli.commands.session.logger')
def test_cmd_session_show_cached(mock_logger, mock_get_session, mock_load_from_cache):
    cached_data = {"id": "cached_session_id", "status": "completed"}
    mock_load_from_cache.return_value = cached_data

    result = session.cmd_session_show("cached_session_id")

    mock_load_from_cache.assert_called_once_with("session_cached_session_id")
    mock_get_session.assert_not_called()
    mock_logger.info.assert_any_call("Loaded session cached_session_id from cache.")
    mock_logger.info.assert_any_call(json.dumps(cached_data, indent=2))
    assert result == cached_data
