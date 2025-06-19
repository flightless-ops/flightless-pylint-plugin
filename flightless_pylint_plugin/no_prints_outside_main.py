from pylint.checkers import BaseChecker
import astroid

RULE_NAME = "no-prints-outside-main"


class NoPrintOutsideMainChecker(BaseChecker):
    name = RULE_NAME
    priority = -1
    msgs = {
        "W9001": (
            "print() call found outside of __main__. Use logging instead.",
            RULE_NAME,
            "Discourage use of print() outside of if __name__ == '__main__'.",
        ),
    }

    def __init__(self, linter=None):
        super().__init__(linter)
        self._main_stack = []

    def visit_if(self, node):
        test = node.test
        if (
            isinstance(test, astroid.Compare)
            and isinstance(test.left, astroid.Name)
            and test.left.name == "__name__"
            and len(test.ops) == 1
            and test.ops[0][0] == "=="
            and isinstance(test.ops[0][1], astroid.Const)
            and test.ops[0][1].value == "__main__"
        ):
            self._main_stack.append(True)
        else:
            self._main_stack.append(False)

    def leave_if(self, node):
        self._main_stack.pop()

    def visit_call(self, node):
        if isinstance(node.func, astroid.Name) and node.func.name == "print" and not any(self._main_stack):
            self.add_message(RULE_NAME, node=node)
