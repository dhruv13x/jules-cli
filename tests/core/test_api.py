from unittest.mock import patch, MagicMock
from src.jules_cli.core import api
from src.jules_cli.utils.exceptions import JulesAPIError

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

@patch('src.jules_cli.core.api.list_activities')
def test_poll_for_result_patch(mock_list_activities):
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
    result = api.poll_for_result("fake_session_id", timeout=1)
    assert result["type"] == "patch"
    assert result["patch"] == "fake_patch"

@patch('src.jules_cli.core.api.list_activities')
@patch('src.jules_cli.core.api.get_session')
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

@patch('src.jules_cli.core.api.list_activities')
@patch('src.jules_cli.core.api.get_session')
def test_poll_for_result_timeout(mock_get_session, mock_list_activities):
    mock_list_activities.return_value = {"activities": []}
    mock_get_session.return_value = {"outputs": []}
    try:
        api.poll_for_result("fake_session_id", timeout=0.1)
    except JulesAPIError as e:
        assert "Timed out" in str(e)
