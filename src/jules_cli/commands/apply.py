# src/jules_cli/commands/apply.py

from ..state import _state
from ..patch.apply import apply_patch_text
from ..utils.logging import logger

def cmd_apply():
    res = _state.get("last_result")
    if not res:
        logger.warning("No last result to apply.")
        return {"status": "error", "message": "No last result to apply."}
    if res["type"] != "patch":
        logger.warning("Last result is not a patch. It may be a PR artifact.")
        return {"status": "error", "message": "Last result is not a patch."}
    patch = res["patch"]
    apply_patch_text(patch)
    return {"status": "success", "message": "Patch applied."}
