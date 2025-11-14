from ..utils.commands import run_cmd
from ..utils.logging import logger
from ..utils.exceptions import TestRunnerError

def run_pytest() -> (int, str, str):
    logger.info("Running pytest...")
    code, out, err = run_cmd(["pytest", "-q", "--maxfail=1"])
    if code != 0:
        # It's not always an error, but we'll wrap it for now
        # and let the caller decide.
        pass
    return code, out, err
