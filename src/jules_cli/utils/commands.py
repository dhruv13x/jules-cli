import subprocess
from typing import List

def run_cmd(cmd: List[str], capture=True):
    try:
        if capture:
            p = subprocess.run(cmd, capture_output=True, text=True, check=False)
            return p.returncode, p.stdout, p.stderr
        else:
            p = subprocess.run(cmd, check=True)
            return p.returncode, "", ""
    except Exception as e:
        return 1, "", str(e)
