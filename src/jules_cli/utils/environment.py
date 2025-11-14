import os
from .exceptions import JulesError

def check_env():
    JULES_KEY = os.getenv("JULES_API_KEY")
    if not JULES_KEY:
        raise JulesError("JULES_API_KEY not set in environment. Set it before running.")
