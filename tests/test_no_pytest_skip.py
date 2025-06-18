from pylint_plugins.no_pytest_skip import NoPytestSkipChecker
from .utilities import run_checker_on_code


def test_pytest_skip_triggers_error():
    code = """
import pytest
def test_example():
    pytest.skip("Not ready")
"""
    messages = run_checker_on_code(code, NoPytestSkipChecker)
    assert "no-pytest-skip" in messages


def test_direct_skip_call_triggers_error():
    code = """
from pytest import skip
def test_example():
    skip("Skipping!")
"""
    messages = run_checker_on_code(code, NoPytestSkipChecker)
    assert "no-pytest-skip" in messages


def test_skip_in_non_test_function_still_triggers():
    code = """
def helper():
    import pytest
    pytest.skip("nope")
"""
    messages = run_checker_on_code(code, NoPytestSkipChecker)
    assert "no-pytest-skip" in messages


def test_unrelated_function_call_does_not_trigger():
    code = """
def test_ok():
    print("Hello")
"""
    messages = run_checker_on_code(code, NoPytestSkipChecker)
    assert not messages
