# tests/test_workspace.py
import unittest
from unittest.mock import patch
from typer.testing import CliRunner
from src.jules_cli.cli import app
import os
import yaml

class TestWorkspace(unittest.TestCase):

    @patch('src.jules_cli.commands.workspace.subprocess.run')
    @patch('src.jules_cli.cli.init_db')
    @patch('src.jules_cli.cli.check_env')
    def test_workspace_run(self, mock_check_env, mock_init_db, mock_subprocess_run):
        runner = CliRunner()
        with runner.isolated_filesystem():
            # Create workspace config and repo directories
            repo1_dir = "repo1"
            repo2_dir = "repo2"
            os.makedirs(repo1_dir, exist_ok=True)
            os.makedirs(repo2_dir, exist_ok=True)
            workspace_data = {
                "repos": [
                    {"name": repo1_dir},
                    {"name": repo2_dir},
                ]
            }
            with open("workspace.yaml", "w") as f:
                yaml.dump(workspace_data, f)

            # Invoke the command
            result = runner.invoke(app, ["workspace", "run", "ls -l"])

            # Assertions
            self.assertEqual(result.exit_code, 0, result.output)
            self.assertEqual(mock_subprocess_run.call_count, 2)
            mock_subprocess_run.assert_any_call(['ls', '-l'], cwd=repo1_dir, check=True)
            mock_subprocess_run.assert_any_call(['ls', '-l'], cwd=repo2_dir, check=True)

    @patch('src.jules_cli.cli.init_db')
    @patch('src.jules_cli.cli.check_env')
    def test_missing_workspace_file(self, mock_check_env, mock_init_db):
        runner = CliRunner()
        with runner.isolated_filesystem():
            result = runner.invoke(app, ["workspace", "run", "ls -l"])
            self.assertNotEqual(result.exit_code, 0)
            self.assertIn("Error: workspace.yaml not found.", result.output)

    @patch('src.jules_cli.commands.workspace.subprocess.run')
    @patch('src.jules_cli.cli.init_db')
    @patch('src.jules_cli.cli.check_env')
    def test_missing_repository(self, mock_check_env, mock_init_db, mock_subprocess_run):
        runner = CliRunner()
        with runner.isolated_filesystem():
            # Create workspace config with a missing repo
            workspace_data = {
                "repos": [
                    {"name": "nonexistent_repo"},
                ]
            }
            with open("workspace.yaml", "w") as f:
                yaml.dump(workspace_data, f)

            result = runner.invoke(app, ["workspace", "run", "ls -l"])

            self.assertEqual(result.exit_code, 0)
            self.assertIn("Warning: Repository 'nonexistent_repo' not found. Skipping.", result.output)
            mock_subprocess_run.assert_not_called()

if __name__ == "__main__":
    unittest.main()
