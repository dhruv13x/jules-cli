from unittest.mock import patch
from src.jules_cli.utils import environment
from src.jules_cli.utils.exceptions import JulesError

@patch.dict(environment.os.environ, {"JULES_API_KEY": "test_key"})
def test_check_env_success():
    environment.check_env()

@patch.dict(environment.os.environ, {}, clear=True)
def test_check_env_failure():
    try:
        environment.check_env()
    except JulesError as e:
        assert "JULES_API_KEY not set" in str(e)
