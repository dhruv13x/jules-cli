# tests/commands/test_doctor.py


import os
import importlib.metadata
from unittest.mock import patch
from jules_cli.commands.doctor import (
    check_jules_api_key,
    check_dependencies,
    run_doctor_command,
    check_configured_repo, # Import the new function
)
from jules_cli.git.vcs import git_get_remote_repo_info # Import for mocking

def test_check_jules_api_key_set():
    with patch.dict(os.environ, {"JULES_API_KEY": "test-key"}):
        assert "is set" in check_jules_api_key()

def test_check_jules_api_key_not_set():
    with patch.dict(os.environ, clear=True):
        assert "is not set" in check_jules_api_key()

def test_check_dependencies_installed():
    with patch("importlib.metadata.version") as mock_version:
        mock_version.return_value = "1.0" # Simulate package being found
        assert "All dependencies are installed" in check_dependencies()

def test_check_dependencies_missing():
    with patch("importlib.metadata.version", side_effect=importlib.metadata.PackageNotFoundError):
        assert "Missing dependencies" in check_dependencies()

@patch('jules_cli.commands.doctor.git_get_remote_repo_info', return_value=("owner", "repo", "github"))
def test_check_configured_repo_found(mock_git_get_remote_repo_info):
    assert "Configured repository: owner/repo" in check_configured_repo()

@patch('jules_cli.commands.doctor.git_get_remote_repo_info', return_value=(None, None, None))
def test_check_configured_repo_not_found(mock_git_get_remote_repo_info):
    assert "No repository configured or detected from git remote." in check_configured_repo()

def test_run_doctor_command():
    with patch("jules_cli.commands.doctor.check_jules_api_key") as mock_api_key, \
         patch("jules_cli.commands.doctor.check_dependencies") as mock_dependencies, \
         patch("jules_cli.commands.doctor.check_configured_repo") as mock_configured_repo: # Mock the new check
        mock_api_key.return_value = "API key set"
        mock_dependencies.return_value = "Dependencies installed"
        mock_configured_repo.return_value = "Configured repository: owner/repo" # Return value for the mock
        result = run_doctor_command()
        assert "JULES_API_KEY" in result
        assert "Dependencies" in result
        assert "Configured Repository" in result # Assert the new check is in the result
        assert result["JULES_API_KEY"] == "API key set"
        assert result["Dependencies"] == "Dependencies installed"
        assert result["Configured Repository"] == "Configured repository: owner/repo" # Assert the value

