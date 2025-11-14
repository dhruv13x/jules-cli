import os
from ..utils.commands import run_cmd
from ..utils.logging import logger
from ..utils.exceptions import PatchError

def apply_patch_text(patch_text: str):
    tmp = "tmp_patch.diff"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(patch_text)
    logger.info("Applying patch via 'patch -p1 -i tmp_patch.diff' ...")
    code, out, err = run_cmd(["patch", "-p1", "-i", tmp])
    os.remove(tmp)
    if code != 0:
        logger.error("Patch failed; stdout/stderr:")
        logger.error(out)
        logger.error(err)
        raise PatchError("patch failed")
    logger.info("Patch applied successfully.")
