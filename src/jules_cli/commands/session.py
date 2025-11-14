import json
from ..core.api import list_sessions, get_session
from ..utils.logging import logger

def cmd_session_list():
    j = list_sessions()
    logger.info(json.dumps(j, indent=2))

def cmd_session_show(session_id: str):
    s = get_session(session_id)
    logger.info(json.dumps(s, indent=2))
