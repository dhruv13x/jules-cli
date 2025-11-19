# tests/core/test_api.py

from unittest.mock import patch, MagicMock
from jules_cli.core import api
from jules_cli.utils.exceptions import JulesAPIError

@patch('requests.request')
def test_http_request_success(mock_request):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {"data": "success"}
    mock_request.return_value = mock_response

    response = api._http_request("GET", "/test")
    assert response == {"data": "success"}

@patch('requests.request')
def test_http_request_401(mock_request):
    mock_response = MagicMock()
    mock_response.status_code = 401
    mock_request.return_value = mock_response

    try:
        api._http_request("GET", "/test")
    except JulesAPIError as e:
        assert "401 UNAUTHENTICATED" in str(e)

@patch('requests.request')
def test_http_request_400(mock_request):
    mock_response = MagicMock()
    mock_response.status_code = 400
    mock_request.return_value = mock_response

    try:
        api._http_request("GET", "/test")
    except JulesAPIError as e:
        assert "Jules API returned 400" in str(e)

@patch('requests.request', side_effect=Exception("Request failed"))
def test_http_request_exception(mock_request):
    try:
        api._http_request("GET", "/test")
    except JulesAPIError as e:
        assert "HTTP request failed" in str(e)

@patch('requests.request')
def test_http_request_json_error(mock_request):
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.side_effect = ValueError("Invalid JSON")
    mock_request.return_value = mock_response

    try:
        api._http_request("GET", "/test")
    except JulesAPIError as e:
        assert "Invalid JSON response" in str(e)

@patch('jules_cli.core.api.get_session')
@patch('jules_cli.core.api.list_activities')
@patch('time.sleep', return_value=None) # Mock time.sleep to avoid actual delays
def test_poll_for_result_patch(mock_sleep, mock_list_activities, mock_get_session):
    mock_list_activities.return_value = {
        "activities": [
            {
                "artifacts": [
                    {
                        "changeSet": {
                            "gitPatch": {
                                "unidiffPatch": "fake_patch"
                            }
                        }
                    }
                ]
            }
        ]
    }
    mock_get_session.return_value = {"id": "fake_session_id", "state": "PLANNING", "outputs": []} # Return a basic session state
    result = api.poll_for_result("fake_session_id", timeout=10) # Increased timeout
    assert result["type"] == "patch"
    assert result["patch"] == "fake_patch"

@patch('jules_cli.core.api.list_activities')
@patch('jules_cli.core.api.get_session')
def test_poll_for_result_pr(mock_get_session, mock_list_activities):
    mock_list_activities.return_value = {"activities": []}
    mock_get_session.return_value = {
        "outputs": [
            {
                "pullRequest": {
                    "url": "fake_pr_url"
                }
            }
        ]
    }
    result = api.poll_for_result("fake_session_id", timeout=1)
    assert result["type"] == "pr"
    assert result["pr"]["url"] == "fake_pr_url"

@patch('jules_cli.core.api.list_activities')
@patch('jules_cli.core.api.get_session')
def test_poll_for_result_timeout(mock_get_session, mock_list_activities):
    mock_list_activities.return_value = {"activities": []}
    mock_get_session.return_value = {"outputs": []}
    try:
        api.poll_for_result("fake_session_id", timeout=0.1)
    except JulesAPIError as e:
        assert "Timed out" in str(e)

@patch('jules_cli.core.api._http_request')
def test_list_sources(mock_http_request):
    mock_http_request.return_value = {"sources": [{"name": "source1"}, {"name": "source2"}]}
    sources = api.list_sources()
    assert sources == [{"name": "source1"}, {"name": "source2"}]
    mock_http_request.assert_called_once_with("GET", "/sources")

@patch('jules_cli.core.api.list_sources')
def test_pick_source_for_repo_github_match(mock_list_sources):
    mock_list_sources.return_value = [
        {"githubRepo": {"repo": "my-repo"}, "name": "source-my-repo"},
        {"githubRepo": {"repo": "other-repo"}, "name": "source-other-repo"},
    ]
    source = api.pick_source_for_repo("my-repo")
    assert source == {"githubRepo": {"repo": "my-repo"}, "name": "source-my-repo"}

@patch('jules_cli.core.api.list_sources')
def test_pick_source_for_repo_name_match(mock_list_sources):
    mock_list_sources.return_value = [
        {"githubRepo": {"repo": "other-repo"}, "name": "source-other-repo"},
        {"name": "my-repo-source"},
    ]
    source = api.pick_source_for_repo("my-repo-source")
    assert source == {"name": "my-repo-source"}

@patch('jules_cli.core.api.list_sources')
def test_pick_source_for_repo_no_match(mock_list_sources):
    mock_list_sources.return_value = [
        {"githubRepo": {"repo": "other-repo"}, "name": "source-other-repo"},
    ]
    source = api.pick_source_for_repo("non-existent-repo")
    assert source is None

@patch('jules_cli.core.api._http_request')
def test_create_session_with_automation_mode(mock_http_request):
    mock_http_request.return_value = {"session_id": "new_session"}
    session = api.create_session(
        prompt="test prompt",
        source_name="test_source",
        automation_mode="AUTO_CREATE_PR"
    )
    assert session == {"session_id": "new_session"}
    mock_http_request.assert_called_once_with(
        "POST",
        "/sessions",
        json_data={
            "prompt": "test prompt",
            "sourceContext": {"source": "test_source", "githubRepoContext": {"startingBranch": "main"}},
            "title": "Jules CLI session",
            "automationMode": "AUTO_CREATE_PR"
        }
    )

@patch('jules_cli.core.api._http_request')
def test_create_session_without_automation_mode(mock_http_request):
    mock_http_request.return_value = {"session_id": "new_session"}
    session = api.create_session(
        prompt="test prompt",
        source_name="test_source"
    )
    assert session == {"session_id": "new_session"}
    mock_http_request.assert_called_once_with(
        "POST",
        "/sessions",
        json_data={
            "prompt": "test prompt",
            "sourceContext": {"source": "test_source", "githubRepoContext": {"startingBranch": "main"}},
            "title": "Jules CLI session"
        }
    )

@patch('jules_cli.core.api.list_activities')
@patch('jules_cli.core.api.get_session')
@patch('time.sleep', return_value=None)
def test_poll_for_result_multiple_iterations(mock_sleep, mock_get_session, mock_list_activities):
    # Simulate no result on first call, then a patch on second call
    mock_list_activities.side_effect = [
        {"activities": []},
        {"activities": [{"artifacts": [{"changeSet": {"gitPatch": {"unidiffPatch": "fake_patch"}}}]}]},
    ]
    mock_get_session.return_value = {"outputs": []} # No session outputs

    result = api.poll_for_result("fake_session_id", timeout=1)
    assert result["type"] == "patch"
    assert mock_list_activities.call_count == 2
    assert mock_sleep.call_count == 1

@patch('jules_cli.core.api._http_request')
def test_list_sessions(mock_http_request):
    mock_http_request.return_value = {"sessions": [{"id": "session1"}]}
    sessions = api.list_sessions()
    assert sessions == {"sessions": [{"id": "session1"}]}
    mock_http_request.assert_called_once_with("GET", "/sessions", params={"pageSize": 20})

@patch('jules_cli.core.api._http_request')
def test_get_session(mock_http_request):
    mock_http_request.return_value = {"id": "session1"}
    session = api.get_session("session1")
    assert session == {"id": "session1"}
    mock_http_request.assert_called_once_with("GET", "/sessions/session1")

@patch('jules_cli.core.api._http_request')
def test_list_activities(mock_http_request):
    mock_http_request.return_value = {"activities": [{"id": "activity1"}]}
    activities = api.list_activities("session1")
    assert activities == {"activities": [{"id": "activity1"}]}
    mock_http_request.assert_called_once_with("GET", "/sessions/session1/activities", params={"pageSize": 50})

@patch('jules_cli.core.api._http_request')
def test_send_message(mock_http_request):
    mock_http_request.return_value = {"status": "sent"}
    response = api.send_message("session1", "hello")
    assert response == {"status": "sent"}
    mock_http_request.assert_called_once_with("POST", "/sessions/session1:sendMessage", json_data={"prompt": "hello"})
