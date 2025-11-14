from unittest.mock import patch
from src.jules_cli.commands import doctor

@patch('src.jules_cli.commands.doctor.check_jules_api_key', return_value="OK")
@patch('src.jules_cli.commands.doctor.check_git_installed', return_value="OK")
@patch('src.jules_cli.commands.doctor.check_patch_installed', return_value="OK")
@patch('src.jules_cli.commands.doctor.check_repo_is_clean', return_value="OK")
@patch('src.jules_cli.commands.doctor.check_internet_connectivity', return_value="OK")
@patch('src.jules_cli.commands.doctor.check_github_token', return_value="OK")
@patch('src.jules_cli.commands.doctor.check_config_file', return_value="OK")
def test_run_doctor_command(mock_config, mock_token, mock_internet, mock_repo, mock_patch, mock_git, mock_api):
    doctor.run_doctor_command()
    assert mock_api.called
    assert mock_git.called
    assert mock_patch.called
    assert mock_repo.called
    assert mock_internet.called
    assert mock_token.called
    assert mock_config.called
