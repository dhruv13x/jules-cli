# tests/utils/test_logging.py


import logging
from jules_cli.utils.logging import setup_logging, VERBOSE

def test_setup_logging_verbose():
    setup_logging(level="VERBOSE")
    logger = logging.getLogger("jules")
    assert logger.level == VERBOSE
