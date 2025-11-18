# tests/commands/test_doctor_extra.py

from unittest.mock import patch
from jules_cli.commands import doctor

@patch('os.getenv', return_value=None)
def test_check_jules_api_key_not_set(mock_getenv):
    assert "not set" in doctor.check_jules_api_key()

@patch('shutil.which', return_value=None)
def test_check_git_installed_not_installed(mock_which):
    assert "not installed" in doctor.check_git_installed()

@patch('shutil.which', return_value=None)
def test_check_patch_installed_not_installed(mock_which):
    assert "not installed" in doctor.check_patch_installed()

@patch('jules_cli.commands.doctor.run_cmd', return_value=(0, "changes", ""))
def test_check_repo_is_clean_dirty(mock_run_cmd):
    assert "uncommitted changes" in doctor.check_repo_is_clean()

@patch('socket.create_connection', side_effect=OSError)
def test_check_internet_connectivity_no_connectivity(mock_create_connection):
    assert "No internet connectivity" in doctor.check_internet_connectivity()

@patch('os.getenv', return_value=None)
def test_check_github_token_not_set(mock_getenv):
    assert "not set" in doctor.check_github_token()

@patch('os.path.exists', return_value=False)
def test_check_config_file_not_found(mock_exists):
    assert "not found" in doctor.check_config_file()

@patch('jules_cli.commands.doctor.logger')
def test_run_doctor_command_json(mock_logger):
    with patch('jules_cli.commands.doctor.check_jules_api_key', return_value='ok'), \
         patch('jules_cli.commands.doctor.check_git_installed', return_value='ok'), \
         patch('jules_cli.commands.doctor.check_patch_installed', return_value='ok'), \
         patch('jules_cli.commands.doctor.check_repo_is_clean', return_value='ok'), \
         patch('jules_cli.commands.doctor.check_internet_connectivity', return_value='ok'), \
         patch('jules_cli.commands.doctor.check_github_token', return_value='ok'), \
         patch('jules_cli.commands.doctor.check_config_file', return_value='ok'):
        doctor.run_doctor_command()
        assert mock_logger.info.call_count > 1
