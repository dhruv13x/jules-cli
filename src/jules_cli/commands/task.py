from typing import Optional
from ..core.api import pick_source_for_repo, create_session, poll_for_result, list_sources
from ..state import _state

def run_task(user_prompt: str, repo_dir_name: str = "bot_platform", automation_mode: Optional[str] = "AUTO_CREATE_PR"):
    # pick source
    source_obj = pick_source_for_repo(repo_dir_name)
    if not source_obj:
        available = [s.get("name") for s in list_sources()]
        raise RuntimeError(f"No source matched repo '{repo_dir_name}'. Available: {available}")
    source_name = source_obj["name"]
    owner = source_obj["githubRepo"]["owner"]
    repo = source_obj["githubRepo"]["repo"]
    print(f"[+] Using Jules source: {source_name} (repo {owner}/{repo})")

    # create session
    print("[+] Creating Jules session...")
    sess = create_session(prompt=user_prompt, source_name=source_name, starting_branch="main",
                          title="Jules CLI interactive", automation_mode=automation_mode)
    _state["current_session"] = sess
    sid = sess.get("id")
    if not sid:
        raise RuntimeError(f"Failed to create session: {sess}")
    print(f"[+] Session created: {sid}. Polling for result...")
    result = poll_for_result(sid)
    _state["last_result"] = result
    _state["repo_source"] = source_name
    _state["repo_owner"] = owner
    _state["repo_name"] = repo
    print("[+] Result received:", result["type"])
    if result["type"] == "patch":
        print("[+] Patch available in last_result['patch']. Use `apply` to apply locally.")
    elif result["type"] == "pr":
        pr = result.get("pr")
        print("[+] PR artifact:", json.dumps(pr, indent=2))
    return result
