import logging
from src.jules_cli.utils.logging import setup_logging, logger

def test_setup_logging():
    setup_logging(level="DEBUG", color=False)
    assert logger.level == logging.DEBUG
    assert len(logger.handlers) > 0
    assert not isinstance(logger.handlers[0].formatter, type(logging.Formatter))
