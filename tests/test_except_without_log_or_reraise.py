from flightless_pylint_plugin.except_without_log_or_reraise import ExceptWithoutLogOrReraiseChecker
from .utilities import run_checker_on_code


def test_except_without_logging_or_raise_triggers() -> None:
    code = """
try:
    risky()
except Exception:
    pass
"""
    messages = run_checker_on_code(code, ExceptWithoutLogOrReraiseChecker)
    assert "except-without-log-or-reraise" in messages


def test_except_with_raise_is_allowed() -> None:
    code = """
try:
    risky()
except Exception:
    raise
"""
    messages = run_checker_on_code(code, ExceptWithoutLogOrReraiseChecker)
    assert not messages


def test_except_with_logging_is_allowed() -> None:
    code = """
import logging
try:
    risky()
except Exception:
    logging.error("failed")
"""
    messages = run_checker_on_code(code, ExceptWithoutLogOrReraiseChecker)
    assert not messages


def test_except_with_logger_var_is_allowed() -> None:
    code = """
def func():
    try:
        do_something()
    except Exception:
        logger.warning("uh-oh")
"""
    messages = run_checker_on_code(code, ExceptWithoutLogOrReraiseChecker)
    assert not messages


def test_except_with_both_is_allowed() -> None:
    code = """
try:
    do()
except Exception:
    log.error("problem")
    raise
"""
    messages = run_checker_on_code(code, ExceptWithoutLogOrReraiseChecker)
    assert not messages


def test_except_on_non_exception_does_not_trigger() -> None:
    code = """
try:
    do()
except ValueError:
    pass
"""
    messages = run_checker_on_code(code, ExceptWithoutLogOrReraiseChecker)
    assert not messages
