from flightless_pylint_plugin.no_prints_outside_main import NoPrintOutsideMainChecker
from .utilities import run_checker_on_code


def test_print_outside_main_triggers_error() -> None:
    code = """
def foo():
    print("hello")
"""
    messages = run_checker_on_code(code, NoPrintOutsideMainChecker)
    assert "no-prints-outside-main" in messages


def test_top_level_print_triggers_error() -> None:
    code = """
print("this should fail")
"""
    messages = run_checker_on_code(code, NoPrintOutsideMainChecker)
    assert "no-prints-outside-main" in messages


def test_print_inside_main_does_not_trigger() -> None:
    code = """
if __name__ == "__main__":
    print("this is okay")
"""
    messages = run_checker_on_code(code, NoPrintOutsideMainChecker)
    assert not messages


def test_logging_call_does_not_trigger() -> None:
    code = """
import logging
def foo():
    logging.info("This is fine")
"""
    messages = run_checker_on_code(code, NoPrintOutsideMainChecker)
    assert not messages


def test_nested_main_blocks_only_allow_inside() -> None:
    code = """
if __name__ == "__main__":
    def inner():
        print("still okay")
"""
    messages = run_checker_on_code(code, NoPrintOutsideMainChecker)
    assert not messages


def test_multiple_if_blocks_only_allow_main() -> None:
    code = """
if something:
    print("bad")
if __name__ == "__main__":
    print("good")
"""
    messages = run_checker_on_code(code, NoPrintOutsideMainChecker)
    assert "no-prints-outside-main" in messages
