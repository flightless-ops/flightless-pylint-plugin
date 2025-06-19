from pylint.checkers import BaseChecker
import astroid

RULE_NAME = "unused-logger"


class UnusedLoggerChecker(BaseChecker):
    name = RULE_NAME
    priority = -1
    msgs = {
        "W9004": (
            "Logger assigned to '%s' but never used",
            RULE_NAME,
            "Detects logger variables that are never referenced after assignment.",
        ),
    }

    def __init__(self, linter=None):
        super().__init__(linter)
        self.logger_assignments = {}

    def visit_assign(self, node: astroid.Assign) -> None:
        if not isinstance(node.value, astroid.Call):
            return

        func = node.value.func
        if isinstance(func, astroid.Attribute):
            if isinstance(func.expr, astroid.Name) and func.expr.name == "logging" and func.attrname == "getLogger":
                for target in node.targets:
                    if isinstance(target, astroid.AssignName) or isinstance(target, astroid.AssignAttr):
                        # Accept both variable and attribute assignments (e.g. class attr)
                        self.logger_assignments[target.name] = node

    def visit_name(self, node: astroid.Name) -> None:
        if node.name in self.logger_assignments:
            if not self._is_store_context(node):
                self.logger_assignments.pop(node.name, None)

    def visit_attribute(self, node: astroid.Attribute) -> None:
        # Detect self.logger usage
        if isinstance(node.expr, astroid.Name) and node.expr.name == "self" and node.attrname in self.logger_assignments:
            self.logger_assignments.pop(node.attrname, None)

    def leave_module(self, node):
        for name, assign_node in self.logger_assignments.items():
            self.add_message(RULE_NAME, node=assign_node, args=(name,))
        self.logger_assignments.clear()

    def _is_store_context(self, node: astroid.Name) -> bool:
        parent = node.parent
        if parent is None:
            return False

        if isinstance(parent, astroid.Assign):
            if hasattr(parent.targets, "__iter__"):
                return any(node is target for target in parent.targets)
            else:
                return node is parent.targets

        if isinstance(parent, astroid.AugAssign):
            return node is parent.target

        if isinstance(parent, astroid.AnnAssign):
            return node is parent.target

        if isinstance(parent, astroid.For):
            if hasattr(parent.target, "elts"):
                return any(node is elt for elt in parent.target.elts)
            else:
                return node is parent.target

        return False
