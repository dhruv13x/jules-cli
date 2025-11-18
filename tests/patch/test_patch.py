# tests/patch/test_patch.py

from unittest.mock import patch
from jules_cli.patch import apply
from jules_cli.utils.exceptions import PatchError
import os

@patch('jules_cli.patch.apply.run_cmd', return_value=(0, "", ""))
def test_apply_patch_text_success(mock_run_cmd):
    with open("file_to_patch.txt", "w") as f:
        f.write("hello")

    patch_text = f"--- a/file_to_patch.txt\n+++ b/file_to_patch.txt\n@@ -1 +1 @@\n-hello\n+world\n"
    apply.apply_patch_text(patch_text)
    mock_run_cmd.assert_called_once()
    assert os.path.exists("tmp_patch.diff") is False
    os.remove("file_to_patch.txt")

@patch('jules_cli.patch.apply.run_cmd', return_value=(1, "out", "err"))
def test_apply_patch_text_error(mock_run_cmd):
    try:
        apply.apply_patch_text("fake_patch_text")
    except PatchError as e:
        assert "patch failed" in str(e)
    assert os.path.exists("tmp_patch.diff") is False
