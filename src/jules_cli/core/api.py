import os
import time
import json
from typing import Optional, Dict, Any, List
import requests

# Configuration
JULES_KEY = os.getenv("JULES_API_KEY")
BASE = "https://jules.googleapis.com/v1alpha"
HEADERS = {"X-Goog-Api-Key": JULES_KEY, "Content-Type": "application/json"}
POLL_INTERVAL = 3
POLL_TIMEOUT = 300

def _http_request(method: str, path: str, json_data: Optional[dict] = None, params: Optional[dict] = None, timeout=60):
    url = f"{BASE}{path}"
    try:
        resp = requests.request(method, url, headers=HEADERS, json=json_data, params=params, timeout=timeout)
    except Exception as e:
        raise RuntimeError(f"HTTP request failed: {e}")
    if resp.status_code == 401:
        raise RuntimeError(f"401 UNAUTHENTICATED from Jules API. Check API key.\nBody: {resp.text}")
    if resp.status_code >= 400:
        raise RuntimeError(f"Jules API returned {resp.status_code}:\n{resp.text}")
    try:
        return resp.json()
    except ValueError:
        raise RuntimeError(f"Invalid JSON response: {resp.text[:2000]}")

def list_sources() -> List[dict]:
    return _http_request("GET", "/sources").get("sources", [])

def pick_source_for_repo(repo_name: str) -> Optional[dict]:
    for s in list_sources():
        gr = s.get("githubRepo") or {}
        if gr.get("repo") == repo_name:
            return s
    for s in list_sources():
        if repo_name in (s.get("name") or ""):
            return s
    return None

def create_session(prompt: str, source_name: str, starting_branch="main", title="Jules CLI session", automation_mode=None) -> dict:
    payload = {
        "prompt": prompt,
        "sourceContext": {"source": source_name, "githubRepoContext": {"startingBranch": starting_branch}},
        "title": title
    }
    if automation_mode:
        payload["automationMode"] = automation_mode
    return _http_request("POST", "/sessions", json_data=payload)

def list_sessions(page_size=20):
    return _http_request("GET", "/sessions", params={"pageSize": page_size})

def get_session(session_id: str):
    return _http_request("GET", f"/sessions/{session_id}")

def list_activities(session_id: str, page_size=50):
    return _http_request("GET", f"/sessions/{session_id}/activities", params={"pageSize": page_size})

def send_message(session_id: str, prompt: str):
    return _http_request("POST", f"/sessions/{session_id}:sendMessage", json_data={"prompt": prompt})

def poll_for_result(session_id: str, timeout=POLL_TIMEOUT):
    t0 = time.time()
    print(f"[+] Polling session {session_id} for up to {timeout}s...")
    while True:
        activities = list_activities(session_id).get("activities", [])
        # newest-first
        for act in reversed(activities):
            for art in act.get("artifacts", []):
                cs = art.get("changeSet")
                if cs:
                    gp = cs.get("gitPatch") or {}
                    patch = gp.get("unidiffPatch")
                    if patch:
                        return {"type": "patch", "patch": patch, "activity": act}
                pr = art.get("pullRequest")
                if pr:
                    return {"type": "pr", "pr": pr, "activity": act}
        # check session outputs
        sess = get_session(session_id)
        if sess.get("outputs"):
            for out in sess["outputs"]:
                if out.get("pullRequest"):
                    return {"type": "pr", "pr": out["pullRequest"], "session": sess}
        if time.time() - t0 > timeout:
            raise TimeoutError("Timed out waiting for Jules outputs.")
        time.sleep(POLL_INTERVAL)
