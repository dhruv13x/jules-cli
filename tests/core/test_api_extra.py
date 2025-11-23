from unittest.mock import patch, MagicMock
import pytest
from jules_cli.core import api
from jules_cli.utils.exceptions import JulesAPIError
import os
import logging

@patch("requests.request")
def test_http_request_no_api_key(mock_request, monkeypatch):
    monkeypatch.delenv("JULES_API_KEY", raising=False)
    with pytest.raises(JulesAPIError, match="JULES_API_KEY is not set"):
        api._http_request("GET", "/test")

@patch("requests.request")
def test_http_request_401(mock_request, monkeypatch):
    monkeypatch.setenv("JULES_API_KEY", "key")
    mock_request.return_value.status_code = 401
    mock_request.return_value.text = "Unauthenticated"
    with pytest.raises(JulesAPIError, match="401 UNAUTHENTICATED"):
        api._http_request("GET", "/test")

@patch("requests.request")
def test_http_request_400(mock_request, monkeypatch):
    monkeypatch.setenv("JULES_API_KEY", "key")
    mock_request.return_value.status_code = 400
    mock_request.return_value.text = "Bad Request"
    with pytest.raises(JulesAPIError, match="Jules API returned 400"):
        api._http_request("GET", "/test")

@patch("requests.request")
def test_http_request_invalid_json(mock_request, monkeypatch):
    monkeypatch.setenv("JULES_API_KEY", "key")
    mock_request.return_value.status_code = 200
    mock_request.return_value.json.side_effect = ValueError
    mock_request.return_value.text = "invalid"
    with pytest.raises(JulesAPIError, match="Invalid JSON response"):
        api._http_request("GET", "/test")

@patch("requests.request")
def test_http_request_connection_error(mock_request, monkeypatch):
    monkeypatch.setenv("JULES_API_KEY", "key")
    mock_request.side_effect = Exception("Connection Error")
    with pytest.raises(JulesAPIError, match="HTTP request failed"):
        api._http_request("GET", "/test")

@patch("jules_cli.core.api.list_sources")
def test_pick_source_for_repo_owner_repo(mock_list):
    mock_list.return_value = [
        {"name": "s1", "githubRepo": {"owner": "o1", "repo": "r1"}},
        {"name": "s2", "githubRepo": {"owner": "o2", "repo": "r2"}}
    ]
    assert api.pick_source_for_repo("o2/r2")["name"] == "s2"

@patch("jules_cli.core.api.list_sources")
def test_pick_source_for_repo_name(mock_list):
    mock_list.return_value = [
        {"name": "s1", "githubRepo": {"owner": "o1", "repo": "r1"}},
        {"name": "sources/123", "githubRepo": {"owner": "o2", "repo": "r2"}}
    ]
    assert api.pick_source_for_repo("sources/123")["name"] == "sources/123"

@patch("jules_cli.core.api.list_sources")
def test_pick_source_for_repo_short_name(mock_list):
    mock_list.return_value = [
        {"name": "s1", "githubRepo": {"owner": "o1", "repo": "r1"}},
    ]
    assert api.pick_source_for_repo("r1")["name"] == "s1"

@patch("jules_cli.core.api.list_sources")
def test_pick_source_for_repo_substring(mock_list):
    mock_list.return_value = [
        {"name": "projects/p1/locations/l1/sources/my-repo"},
    ]
    assert api.pick_source_for_repo("my-repo")["name"] == "projects/p1/locations/l1/sources/my-repo"

@patch("jules_cli.core.api.list_sources")
def test_pick_source_for_repo_none(mock_list):
    mock_list.return_value = []
    assert api.pick_source_for_repo("unknown") is None

@patch("jules_cli.core.api._http_request")
def test_create_session_with_automation_mode(mock_req):
    api.create_session("prompt", "source", automation_mode="MODE")
    args, kwargs = mock_req.call_args
    assert kwargs["json_data"]["automationMode"] == "MODE"

@patch("jules_cli.core.api._http_request")
def test_list_sessions(mock_req):
    api.list_sessions(page_size=10)
    mock_req.assert_called_with("GET", "/sessions", params={"pageSize": 10})

@patch("jules_cli.core.api._http_request")
def test_approve_plan(mock_req):
    api.approve_plan("sid")
    mock_req.assert_called_with("POST", "/sessions/sid:approvePlan")

def test_poll_for_result_plan(monkeypatch):
    mock_list_activities = MagicMock(return_value={"activities": [{"planGenerated": {"plan": {"id": "p1"}}}]})
    mock_get_session = MagicMock(return_value={"state": "PLANNING"})

    monkeypatch.setattr("jules_cli.core.api.list_activities", mock_list_activities)
    monkeypatch.setattr("jules_cli.core.api.get_session", mock_get_session)

    monkeypatch.setattr("time.sleep", MagicMock())
    monkeypatch.setattr("jules_cli.core.api.logger", MagicMock())

    # Ensure other logging calls don't interfere
    monkeypatch.setattr(logging.getLogger("jules"), "handlers", [])
    monkeypatch.setattr(logging, 'disable', MagicMock())
    monkeypatch.setattr(logging, 'info', MagicMock())

    # Use a side effect for time.time so that it doesn't timeout
    # But enough for it to enter the loop and exit

    # NOTE: The failure previously was "Timed out waiting for Jules outputs." which means it hit the timeout check.
    # The timeout check is `if time.time() - t0 > timeout: raise`
    # If `time.time()` increments too fast, it will trigger timeout.
    # If it returns constant, it loops forever (if condition not met) -> Test Timeout.
    # But here condition IS met: `planGenerated` is in activities.
    # Why did it not return?
    # Maybe `reversed(activities)` logic?
    # activities = [{"planGenerated": {"plan": {}}}]
    # reversed(...) -> yields the item.
    # item has `planGenerated` -> `plan` -> return.

    # Maybe the issue is with `mock_list_activities` being called multiple times if it doesn't break?
    # Or maybe `t0 = time.time()` is 0, and then `time.time()` inside loop is > timeout.

    def time_generator():
        # First call (t0)
        yield 0.0
        # Loop calls
        t = 0.0
        while True:
            yield t
            t += 0.1 # Increment slowly to stay within timeout

    monkeypatch.setattr("time.time", MagicMock(side_effect=time_generator()))

    result = api.poll_for_result("sid", timeout=10)
    assert result["type"] == "plan"
    # verify it was called at least once
    assert mock_list_activities.called
    assert mock_get_session.called

@patch("jules_cli.core.api.list_activities")
@patch("jules_cli.core.api.get_session")
def test_poll_for_result_message_in_output(mock_get, mock_list):
    mock_list.return_value = {"activities": []}
    mock_get.return_value = {
        "state": "RUNNING",
        "outputs": [{"agentMessaged": {"agentMessage": "Hello"}}]
    }

    def time_generator():
        t = 0.0
        while True:
            yield t
            t += 0.1

    with patch("time.sleep"), patch("time.time", side_effect=time_generator()):
        result = api.poll_for_result("sid", timeout=1)
    assert result["type"] == "message"
    assert result["message"] == "Hello"

@patch("jules_cli.core.api.list_activities")
@patch("jules_cli.core.api.get_session")
def test_poll_for_result_pr_in_output(mock_get, mock_list):
    mock_list.return_value = {"activities": []}
    mock_get.return_value = {
        "state": "RUNNING",
        "outputs": [{"pullRequest": {"url": "url"}}]
    }

    def time_generator():
        t = 0.0
        while True:
            yield t
            t += 0.1

    with patch("time.sleep"), patch("time.time", side_effect=time_generator()):
        result = api.poll_for_result("sid", timeout=1)
    assert result["type"] == "pr"

@patch("jules_cli.core.api.list_activities")
@patch("jules_cli.core.api.get_session")
def test_poll_for_result_completed_status(mock_get, mock_list):
    mock_list.return_value = {"activities": []}
    mock_get.return_value = {"state": "COMPLETED", "id": "sid"}

    def time_generator():
        t = 0.0
        while True:
            yield t
            t += 0.1

    with patch("time.sleep"), patch("time.time", side_effect=time_generator()):
        result = api.poll_for_result("sid", timeout=1)
    assert result["type"] == "session_status"
    assert result["status"] == "COMPLETED"

@patch("jules_cli.core.api.list_activities")
@patch("jules_cli.core.api.get_session")
def test_poll_for_result_timeout(mock_get, mock_list):
    mock_list.return_value = {"activities": []}
    mock_get.return_value = {"state": "RUNNING"}

    # Mock time.time to simulate time passing
    with patch("time.time", side_effect=[0, 10, 20, 30]):
        # Also mock time.sleep to avoid waiting
        with patch("time.sleep"):
            with pytest.raises(JulesAPIError, match="Timed out"):
                api.poll_for_result("sid", timeout=5)

@patch("jules_cli.core.api.list_activities")
@patch("jules_cli.core.api.get_session")
def test_poll_for_result_404_retry(mock_get, mock_list):
    # First call raises 404, second call returns success
    mock_list.side_effect = [JulesAPIError("404 Not Found"), {"activities": []}]
    mock_get.return_value = {"state": "COMPLETED", "id": "sid"}

    with patch("time.sleep"), patch("time.time", side_effect=[0, 0.1, 0.2, 0.3, 0.4, 0.5]):
        result = api.poll_for_result("sid", timeout=5)
        assert result["type"] == "session_status"
