# tests/utils/test_branch.py

from unittest.mock import patch
from src.jules_cli.utils.branch import generate_branch_name

@patch("src.jules_cli.utils.branch.config")
def test_generate_branch_name(mock_config):
    mock_config.get_nested.return_value = "{type}/{description}"
    branch_name = generate_branch_name("My Test PR", "feature")
    assert branch_name == "feature/my-test-pr"

    mock_config.get_nested.return_value = "custom/{description}"
    branch_name = generate_branch_name("Another Test")
    assert branch_name == "custom/another-test"
