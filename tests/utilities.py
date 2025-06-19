from collections.abc import Callable
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
        # Manually call visit_* if it exists for the node type
        method_name = f"visit_{node.__class__.__name__.lower()}"
        visit_method = getattr(checker, method_name, None)
        if visit_method:
            visit_method(node)

        for child in node.get_children():
            visit_recursively(child)

    for node in tree.body:
        node.parent = tree
        node.root = lambda: tree
        visit_recursively(node)

    return messages
