from pylint.checkers import BaseChecker
import astroid

RULE_NAME = "except-without-log-or-reraise"


class ExceptWithoutLogOrReraiseChecker(BaseChecker):

    name = RULE_NAME
    priority = -1
    msgs = {
        "W9002": (
            "except block without logging or re-raise",
            RULE_NAME,
            "Do not swallow exceptions. Use logging and/or re-raise.",
        ),
    }

    def visit_excepthandler(self, node: astroid.ExceptHandler) -> None:
        if not node.type:
            return  # bare `except:` not this rule's concern

        # Only flag generic Exception types
        if isinstance(node.type, astroid.Name) and node.type.name != "Exception":
            return

        has_logging = False
        has_reraise = False

        for stmt in node.body:
            if isinstance(stmt, astroid.Raise):
                has_reraise = True
            elif self._is_logging_call(stmt):
                has_logging = True

        if not (has_logging or has_reraise):
            self.add_message(RULE_NAME, node=node)

    def _is_logging_call(self, node: astroid.NodeNG) -> bool:
        if not isinstance(node, astroid.Expr):
            return False
        if not isinstance(node.value, astroid.Call):
            return False
        func = node.value.func
        if isinstance(func, astroid.Attribute):
            if isinstance(func.expr, astroid.Name) and func.expr.name in {"log", "logger", "logging"}:
                return True
        return False
