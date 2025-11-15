
import pytest
from unittest.mock import patch

@pytest.fixture(autouse=True)
def mock_os_system():
    with patch("os.system", return_value=0) as mock_system:
        yield mock_system
