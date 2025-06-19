from flightless_pylint_plugin.no_conditionals_in_test import NoConditionalsInTestChecker
from .utilities import run_checker_on_code


def test_if_statement_triggers_error() -> None:
    code = """
def test_example():
    if True:
        pass
"""
    messages = run_checker_on_code(code, NoConditionalsInTestChecker)
    assert "no-conditionals-in-test" in messages


def test_if_expression_triggers_error() -> None:
    code = """
def test_example():
    x = 1 if True else 0
"""
    messages = run_checker_on_code(code, NoConditionalsInTestChecker)
    assert "no-conditionals-in-test" in messages


def test_non_test_function_does_not_trigger() -> None:
    code = """
def helper_function():
    if True:
        pass
"""
    messages = run_checker_on_code(code, NoConditionalsInTestChecker)
    assert "no-conditionals-in-test" not in messages


def test_clean_test_function_does_not_trigger() -> None:
    code = """
def test_clean():
    x = 42
    print(x)
"""
    messages = run_checker_on_code(code, NoConditionalsInTestChecker)
    assert not messages
