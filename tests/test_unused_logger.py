from flightless_pylint_plugin.unused_logger import UnusedLoggerChecker
from .utilities import run_checker_on_code


def test_unused_logger_triggers() -> None:
    code = """
import logging
logger = logging.getLogger(__name__)
def do_nothing():
    pass
"""
    messages = run_checker_on_code(code, UnusedLoggerChecker)
    assert "unused-logger" in messages


def test_used_logger_does_not_trigger() -> None:
    code = """
import logging
logger = logging.getLogger(__name__)
def something():
    logger.info("used")
"""
    messages = run_checker_on_code(code, UnusedLoggerChecker)
    assert not messages


def test_multiple_loggers_only_unused_triggers() -> None:
    code = """
import logging
logger1 = logging.getLogger("used")
logger2 = logging.getLogger("not_used")

def func():
    logger1.debug("doing something")
"""
    messages = run_checker_on_code(code, UnusedLoggerChecker)
    assert "unused-logger" in messages


def test_logger_in_class_context_usage() -> None:
    code = """
import logging
class Foo:
    logger = logging.getLogger(__name__)
    def run(self):
        self.logger.warning("running")
"""
    messages = run_checker_on_code(code, UnusedLoggerChecker)
    assert not messages
