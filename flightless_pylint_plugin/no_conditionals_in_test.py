from pylint.checkers import BaseChecker
import astroid

RULE_NAME = "no-conditionals-in-test"


class NoConditionalsInTestChecker(BaseChecker):
    name = RULE_NAME
    priority = -1
    msgs = {
        "E9001": (
            "Use of 'if', 'else', or 'elif' in test functions is not allowed",
            RULE_NAME,
            "Avoid conditional logic in test functions.",
        )
    }

    def visit_functiondef(self, node):
        if not node.name.startswith("test"):
            return

        # Catch if/elif/else blocks
        for subnode in node.nodes_of_class(astroid.If):
            self.add_message(RULE_NAME, node=subnode)

        # Catch inline conditional expressions (ternary-esque) (x if y else z)
        for subnode in node.nodes_of_class(astroid.IfExp):
            self.add_message(RULE_NAME, node=subnode)


def register(linter):
    linter.register_checker(NoConditionalsInTestChecker(linter))
