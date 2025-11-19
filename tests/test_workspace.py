
import os
from typer.testing import CliRunner
from jules_cli.cli import app
import yaml
from unittest.mock import patch

runner = CliRunner()

@patch('jules_cli.cli.check_env')
@patch('jules_cli.cli.init_db')
def test_workspace_run_command(mock_init_db, mock_check_env):
    # Create dummy repositories and a workspace.yaml file
    os.makedirs("repo1", exist_ok=True)
    os.makedirs("repo2", exist_ok=True)
    with open("workspace.yaml", "w") as f:
        yaml.dump({"repos": [{"name": "repo1"}, {"name": "repo2"}]}, f)

    # Create a dummy file in each repo to check if the command ran
    with open("repo1/test.txt", "w") as f:
        f.write("repo1")
    with open("repo2/test.txt", "w") as f:
        f.write("repo2")

    result = runner.invoke(app, ["workspace", "run", "ls -a"])

    assert result.exit_code == 0
    assert "Running command in 'repo1': ls -a" in result.stdout
    assert "Running command in 'repo2': ls -a" in result.stdout

    # Cleanup
    os.remove("workspace.yaml")
    os.remove("repo1/test.txt")
    os.remove("repo2/test.txt")
    os.rmdir("repo1")
    os.rmdir("repo2")

@patch('jules_cli.cli.check_env')
@patch('jules_cli.cli.init_db')
def test_workspace_run_no_workspace_file(mock_init_db, mock_check_env):
    result = runner.invoke(app, ["workspace", "run", "ls"])
    assert result.exit_code == 1
    assert "Error: workspace.yaml not found." in result.stdout

@patch('jules_cli.cli.check_env')
@patch('jules_cli.cli.init_db')
def test_workspace_run_missing_repos_key(mock_init_db, mock_check_env):
    with open("workspace.yaml", "w") as f:
        yaml.dump({"not_repos": []}, f)

    result = runner.invoke(app, ["workspace", "run", "ls"])
    assert result.exit_code == 1
    assert "Error: workspace.yaml is missing the 'repos' key." in result.stdout

    # Cleanup
    os.remove("workspace.yaml")

@patch('jules_cli.cli.check_env')
@patch('jules_cli.cli.init_db')
def test_workspace_run_repo_not_found(mock_init_db, mock_check_env):
    with open("workspace.yaml", "w") as f:
        yaml.dump({"repos": [{"name": "repo1"}, {"name": "non_existent_repo"}]}, f)

    os.makedirs("repo1", exist_ok=True)

    result = runner.invoke(app, ["workspace", "run", "ls"])
    assert result.exit_code == 0
    assert "Warning: Repository 'non_existent_repo' not found. Skipping." in result.stdout

    # Cleanup
    os.remove("workspace.yaml")
    os.rmdir("repo1")

@patch('jules_cli.cli.check_env')
@patch('jules_cli.cli.init_db')
def test_workspace_run_command_fails(mock_init_db, mock_check_env):
    with open("workspace.yaml", "w") as f:
        yaml.dump({"repos": [{"name": "repo1"}]}, f)

    os.makedirs("repo1", exist_ok=True)

    result = runner.invoke(app, ["workspace", "run", "non_existent_command"])
    assert result.exit_code == 1

    # Cleanup
    os.remove("workspace.yaml")
    os.rmdir("repo1")
