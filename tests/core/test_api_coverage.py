from unittest.mock import patch, MagicMock
import pytest
from jules_cli.core import api
from jules_cli.utils.exceptions import JulesAPIError

# src/jules_cli/core/api.py Coverage Tests

@patch("jules_cli.core.api._http_request")
def test_send_message(mock_req):
    api.send_message("sid", "hello")
    mock_req.assert_called_with("POST", "/sessions/sid:sendMessage", json_data={"prompt": "hello"})

@patch("jules_cli.core.api._http_request")
def test_get_session(mock_req):
    api.get_session("sid")
    mock_req.assert_called_with("GET", "/sessions/sid")

@patch("jules_cli.core.api.list_sources")
def test_pick_source_fallback_repo_short(mock_list):
    # Coverage for:
    # target_short = parsed_repo_short if parsed_repo_short else repo_name
    # ...
    # if source_repo_short == target_short: return s

    mock_list.return_value = [
        {"name": "s1", "githubRepo": {"owner": "o1", "repo": "r1"}}
    ]
    # "r1" should match "r1" short name
    assert api.pick_source_for_repo("r1")["name"] == "s1"

@patch("jules_cli.core.api.list_sources")
def test_pick_source_fallback_substring(mock_list):
    # Coverage for substring match
    mock_list.return_value = [{"name": "long-name-repo-123"}]
    assert api.pick_source_for_repo("repo-123")["name"] == "long-name-repo-123"

def test_poll_for_result_artifacts_patch():
    # Coverage for:
    # if patch: return {"type": "patch", ...}

    with patch("jules_cli.core.api.list_activities") as mock_list:
        with patch("jules_cli.core.api.get_session"):
            with patch("time.sleep"):
                with patch("time.time", side_effect=[0, 0.1]):
                    mock_list.return_value = {"activities": [{
                        "artifacts": [{
                            "changeSet": {"gitPatch": {"unidiffPatch": "diff"}}
                        }]
                    }]}
                    result = api.poll_for_result("sid", timeout=1)
                    assert result["type"] == "patch"
                    assert result["patch"] == "diff"

def test_poll_for_result_artifacts_pr():
    # Coverage for:
    # if pr: return {"type": "pr", ...}

    with patch("jules_cli.core.api.list_activities") as mock_list:
        with patch("jules_cli.core.api.get_session"):
            with patch("time.sleep"):
                with patch("time.time", side_effect=[0, 0.1]):
                    mock_list.return_value = {"activities": [{
                        "artifacts": [{
                            "pullRequest": {"url": "http://pr"}
                        }]
                    }]}
                    result = api.poll_for_result("sid", timeout=1)
                    assert result["type"] == "pr"
                    assert result["pr"]["url"] == "http://pr"

def test_poll_for_result_session_output_pr():
    # Coverage for session outputs check
    with patch("jules_cli.core.api.list_activities") as mock_list:
        mock_list.return_value = {"activities": []}
        with patch("jules_cli.core.api.get_session") as mock_sess:
            mock_sess.return_value = {
                "outputs": [{"pullRequest": {"url": "http://pr"}}]
            }
            with patch("time.sleep"):
                with patch("time.time", side_effect=[0, 0.1]):
                    result = api.poll_for_result("sid", timeout=1)
                    assert result["type"] == "pr"

def test_poll_for_result_session_output_message():
    # Coverage for session outputs message
    with patch("jules_cli.core.api.list_activities") as mock_list:
        mock_list.return_value = {"activities": []}
        with patch("jules_cli.core.api.get_session") as mock_sess:
            mock_sess.return_value = {
                "outputs": [{"agentMessaged": {"agentMessage": "msg"}}]
            }
            with patch("time.sleep"):
                with patch("time.time", side_effect=[0, 0.1]):
                    result = api.poll_for_result("sid", timeout=1)
                    assert result["type"] == "message"
                    assert result["message"] == "msg"

def test_poll_for_result_session_not_found_swallowed():
    # Coverage for:
    # except JulesAPIError as e: if "404" ... pass

    with patch("jules_cli.core.api.list_activities") as mock_list:
        mock_list.return_value = {"activities": []}
        with patch("jules_cli.core.api.get_session") as mock_sess:
            # First call raises 404, second call returns completed
            mock_sess.side_effect = [JulesAPIError("404 NOT_FOUND"), {"state": "COMPLETED"}]
            with patch("time.sleep"):
                with patch("time.time", side_effect=[0, 0.1, 0.2]):
                    result = api.poll_for_result("sid", timeout=1)
                    assert result["type"] == "session_status"

def test_poll_for_result_activities_error_raised():
    # Coverage for:
    # except JulesAPIError as e: else raise e

    with patch("jules_cli.core.api.list_activities") as mock_list:
        mock_list.side_effect = JulesAPIError("500 Internal Error")
        with patch("time.sleep"):
             with pytest.raises(JulesAPIError, match="500"):
                 api.poll_for_result("sid", timeout=1)

def test_poll_for_result_planning_with_message():
    # Coverage for:
    # if sess and sess.get("state") == "PLANNING":
    #   if last_agent_message: return ...

    with patch("jules_cli.core.api.list_activities") as mock_list:
        # Activity has message, but no plan/artifacts yet
        mock_list.return_value = {"activities": [{"agentMessaged": {"agentMessage": "Hold on"}}]}
        with patch("jules_cli.core.api.get_session") as mock_sess:
            mock_sess.return_value = {"state": "PLANNING"}
            with patch("time.sleep"):
                with patch("time.time", side_effect=[0, 0.1]):
                    result = api.poll_for_result("sid", timeout=1)
                    assert result["type"] == "message"
                    assert result["message"] == "Hold on"

def test_poll_for_result_planning_no_message_wait():
    # Coverage for:
    # if sess and sess.get("state") == "PLANNING": pass (and loop)

    with patch("jules_cli.core.api.list_activities") as mock_list:
        mock_list.return_value = {"activities": []}
        with patch("jules_cli.core.api.get_session") as mock_sess:
            # First call PLANNING, second call COMPLETED
            mock_sess.side_effect = [{"state": "PLANNING"}, {"state": "COMPLETED"}]
            with patch("time.sleep"):
                with patch("time.time", side_effect=[0, 0.1, 0.2]):
                    result = api.poll_for_result("sid", timeout=1)
                    assert result["type"] == "session_status"
