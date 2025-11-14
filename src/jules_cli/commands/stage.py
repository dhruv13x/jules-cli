from ..utils.commands import run_cmd_interactive
from ..utils.logging import logger

def cmd_stage():
    """
    Run git add -p to interactively stage changes.
    """
    logger.info("Starting interactive staging session...")
    try:
        run_cmd_interactive(["git", "add", "-p"])
        logger.info("Interactive staging session finished.")
        return {"status": "success"}
    except Exception as e:
        logger.error("Failed to run interactive staging: %s", e)
        return {"status": "error", "message": str(e)}
