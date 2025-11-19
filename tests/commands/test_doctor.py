# tests/commands/test_doctor.py


import os
import importlib.metadata # Added this line
from unittest.mock import patch
from jules_cli.commands.doctor import (
    check_jules_api_key,
    check_dependencies,
    run_doctor_command,
)

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

def test_run_doctor_command():
    with patch("jules_cli.commands.doctor.check_jules_api_key") as mock_api_key, \
         patch("jules_cli.commands.doctor.check_dependencies") as mock_dependencies:
        mock_api_key.return_value = "API key set"
        mock_dependencies.return_value = "Dependencies installed"
        result = run_doctor_command()
        assert "JULES_API_KEY" in result
        assert "Dependencies" in result
        assert result["JULES_API_KEY"] == "API key set"
        assert result["Dependencies"] == "Dependencies installed"
