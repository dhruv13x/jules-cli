# tests/utils/test_environment.py

from unittest.mock import patch
import pytest
from jules_cli.utils import environment
from jules_cli.utils.exceptions import JulesError

@patch.dict(environment.os.environ, {"JULES_API_KEY": "test_key"})
def test_check_env_success():
    environment.check_env()

@patch.dict(environment.os.environ, {}, clear=True)
def test_check_env_failure():
    try:
        environment.check_env()
    except JulesError as e:
        assert "JULES_API_KEY not set" in str(e)

@patch.dict(environment.os.environ, {"JULES_API_KEY": "test_key"})
@patch('jules_cli.utils.environment.os.system', return_value=1)  # Simulate git not found
def test_check_env_git_not_found(mock_os_system):
    with pytest.raises(JulesError) as excinfo:
        environment.check_env()

    assert "git command not found. Make sure git is installed and in your PATH." in str(excinfo.value)
    mock_os_system.assert_called_once_with("git --version > /dev/null 2>&1")
