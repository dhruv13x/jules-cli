import os
import pytest
from src.jules_cli.commands import task
from tests.fixtures.fake_api import start_fake_api

@pytest.fixture(scope="module")
def fake_api():
    api = start_fake_api()
    os.environ["JULES_API_URL"] = "http://localhost:8000/v1alpha"
    yield api
    api.stop()

def test_run_task_integration(fake_api):
    # This is a very basic integration test. A more complete test
    # would involve a more sophisticated fake API.
    with pytest.raises(Exception):
        task.run_task("my prompt")
