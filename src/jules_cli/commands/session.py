import json
from ..core.api import list_sessions, get_session

def cmd_session_list():
    j = list_sessions()
    print(json.dumps(j, indent=2))

def cmd_session_show(session_id: str):
    s = get_session(session_id)
    print(json.dumps(s, indent=2))
