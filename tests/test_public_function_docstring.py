import textwrap
from flightless_pylint_plugin.public_function_docstring import PublicFunctionDocstringChecker
from .utilities import run_checker_on_code


def test_public_function_without_docstring_triggers() -> None:
    code = """
def public_func():
    pass
"""
    messages = run_checker_on_code(code, PublicFunctionDocstringChecker)
    assert "public-function-missing-docstring" in messages


def test_public_function_with_docstring_does_not_trigger() -> None:
    code = textwrap.dedent(
        '''
        def public_func():
            """Docstring present."""
            pass
    '''
    )
    messages = run_checker_on_code(code, PublicFunctionDocstringChecker)
    assert not messages


def test_private_function_without_docstring_does_not_trigger() -> None:
    code = """
def _private_func():
    pass
"""
    messages = run_checker_on_code(code, PublicFunctionDocstringChecker)
    assert not messages


def test_special_method_without_docstring_does_not_trigger() -> None:
    code = """
class C:
    def __init__(self):
        pass
"""
    messages = run_checker_on_code(code, PublicFunctionDocstringChecker)
    assert not messages


def test_async_public_function_without_docstring_triggers() -> None:
    code = """
async def public_async_func():
    pass
"""
    messages = run_checker_on_code(code, PublicFunctionDocstringChecker)
    assert "public-function-missing-docstring" in messages
