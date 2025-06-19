from pylint.checkers import BaseChecker
from pylint.lint import PyLinter
import astroid

RULE_NAME = "no-pytest-skip"


class NoPytestSkipChecker(BaseChecker):
    name = RULE_NAME
    priority = -1
    msgs = {
        "E9002": (
            "Usage of 'pytest.skip()' is not allowed",
            RULE_NAME,
            "Do not skip tests with pytest.skip().",
        )
    }

    def visit_call(self, node: astroid.NodeNG) -> None:
        func = node.func
        # Match pytest.skip or from pytest import skip.
        if isinstance(func, astroid.Attribute):
            if func.attrname == "skip" and func.expr.as_string() == "pytest":
                self.add_message(RULE_NAME, node=node)
        elif isinstance(func, astroid.Name) and func.name == "skip":
            self.add_message(RULE_NAME, node=node)


def register(linter: PyLinter) -> None:
    linter.register_checker(NoPytestSkipChecker(linter))
