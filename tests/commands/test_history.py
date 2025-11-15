
from unittest.mock import patch
from jules_cli.commands.history import cmd_history_list, cmd_history_view

@patch("jules_cli.commands.history.sqlite3.connect")
def test_cmd_history_list_empty(mock_connect):
    mock_connect.return_value.cursor.return_value.fetchall.return_value = []
    result = cmd_history_list()
    assert result == []

@patch("jules_cli.commands.history.sqlite3.connect")
def test_cmd_history_view_not_found(mock_connect):
    mock_connect.return_value.cursor.return_value.fetchone.return_value = None
    result = cmd_history_view("non-existent-session")
    assert result["error"] == "Session not found."

@patch("jules_cli.commands.history.sqlite3.connect")
def test_cmd_history_view_not_found(mock_connect):
    mock_connect.return_value.cursor.return_value.fetchone.return_value = None
    result = cmd_history_view("non-existent-session")
    assert result["error"] == "Session not found."

@patch("jules_cli.commands.history.sqlite3.connect")
def test_cmd_history_view_not_found(mock_connect):
    mock_connect.return_value.cursor.return_value.fetchone.return_value = None
    result = cmd_history_view("non-existent-session")
    assert result["error"] == "Session not found."

@patch("jules_cli.commands.history.sqlite3.connect")
def test_cmd_history_view_not_found(mock_connect):
    mock_connect.return_value.cursor.return_value.fetchone.return_value = None
    result = cmd_history_view("non-existent-session")
    assert result["error"] == "Session not found."

@patch("jules_cli.commands.history.sqlite3.connect")
def test_cmd_history_view_not_found(mock_connect):
    mock_connect.return_value.cursor.return_value.fetchone.return_value = None
    result = cmd_history_view("non-existent-session")
    assert result["error"] == "Session not found."

@patch("jules_cli.commands.history.sqlite3.connect")
def test_cmd_history_view_not_found(mock_connect):
    mock_connect.return_value.cursor.return_value.fetchone.return_value = None
    result = cmd_history_view("non-existent-session")
    assert result["error"] == "Session not found."

@patch("jules_cli.commands.history.sqlite3.connect")
def test_cmd_history_view_not_found(mock_connect):
    mock_connect.return_value.cursor.return_value.fetchone.return_value = None
    result = cmd_history_view("non-existent-session")
    assert result["error"] == "Session not found."

@patch("jules_cli.commands.history.sqlite3.connect")
def test_cmd_history_view_not_found(mock_connect):
    mock_connect.return_value.cursor.return_value.fetchone.return_value = None
    result = cmd_history_view("non-existent-session")
    assert result["error"] == "Session not found."
