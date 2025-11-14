from src.jules_cli.utils.exceptions import JulesError, JulesAPIError, GitError, PatchError, TestRunnerError, ConfigError

def test_jules_error():
    try:
        raise JulesError("Test message")
    except JulesError as e:
        assert str(e) == "Test message"

def test_jules_api_error():
    try:
        raise JulesAPIError("API error")
    except JulesAPIError as e:
        assert str(e) == "API error"

def test_git_error():
    try:
        raise GitError("Git error")
    except GitError as e:
        assert str(e) == "Git error"

def test_patch_error():
    try:
        raise PatchError("Patch error")
    except PatchError as e:
        assert str(e) == "Patch error"

def test_test_runner_error():
    try:
        raise TestRunnerError("Test runner error")
    except TestRunnerError as e:
        assert str(e) == "Test runner error"

def test_config_error():
    try:
        raise ConfigError("Config error")
    except ConfigError as e:
        assert str(e) == "Config error"
