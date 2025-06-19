from io import StringIO
from collections.abc import Callable
from unittest.mock import MagicMock
from typing import Any
import astroid
from astroid import NodeNG
from pylint.lint import PyLinter


def run_checker_on_code(
    code: str,
    checker_class: Callable,
    filename: str = "tests/test_example.py",
) -> list:
    tree = astroid.parse(code)
    tree.file = filename

    linter = PyLinter()
    checker = checker_class(linter)
    checker.open()
    linter.register_checker(checker)

    messages = []

    def capture(msg_id: str, **__kwargs: Any) -> None:
        messages.append(msg_id)

    checker.add_message = capture

    def visit_recursively(node: NodeNG) -> None:
        method_name = f"visit_{node.__class__.__name__.lower()}"
        visit_method = getattr(checker, method_name, None)
        if visit_method:
            visit_method(node)

        for child in node.get_children():
            visit_recursively(child)

        # Call leave_* after children are visited
        leave_method_name = f"leave_{node.__class__.__name__.lower()}"
        leave_method = getattr(checker, leave_method_name, None)
        if leave_method:
            leave_method(node)

    # Call visit_module hook before traversal
    visit_module = getattr(checker, "visit_module", None)
    if visit_module:
        visit_module(tree)

    for node in tree.body:
        node.parent = tree
        node.root = lambda: tree
        visit_recursively(node)

    # Call leave_module hook after traversal
    leave_module = getattr(checker, "leave_module", None)
    if leave_module:
        leave_module(tree)

    return messages


def run_checker_on_file(filepath: str, checker_class) -> list[str]:
    with open(filepath, encoding="utf-8") as f:
        code = f.read()

    # Parse module with fake filename
    module = astroid.parse(code)
    module.file = filepath

    # Setup linter and checker
    linter = PyLinter()
    checker = checker_class(linter)
    checker.add_message = MagicMock()
    linter.register_checker(checker)

    # Run file-level and module-level checks
    checker.process_module(module)

    # Extract message IDs from calls to add_message
    return [args[0] for args, kwargs in checker.add_message.call_args_list]
