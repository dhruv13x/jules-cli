import os
from ..utils.commands import run_cmd

def apply_patch_text(patch_text: str):
    tmp = "tmp_patch.diff"
    with open(tmp, "w", encoding="utf-8") as f:
        f.write(patch_text)
    print("[+] Applying patch via 'patch -p1 -i tmp_patch.diff' ...")
    code, out, err = run_cmd(["patch", "-p1", "-i", tmp])
    os.remove(tmp)
    if code != 0:
        print("[!] Patch failed; stdout/stderr:")
        print(out)
        print(err)
        raise RuntimeError("patch failed")
    print("[+] Patch applied successfully.")
