import os

JULES_KEY = os.getenv("JULES_API_KEY")

def check_env():
    if not JULES_KEY:
        raise RuntimeError("JULES_API_KEY not set in environment. Set it before running.")
