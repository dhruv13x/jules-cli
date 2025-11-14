from ..state import _state
from ..patch.apply import apply_patch_text

def cmd_apply():
    res = _state.get("last_result")
    if not res:
        print("No last result to apply.")
        return
    if res["type"] != "patch":
        print("Last result is not a patch. It may be a PR artifact.")
        return
    patch = res["patch"]
    apply_patch_text(patch)
