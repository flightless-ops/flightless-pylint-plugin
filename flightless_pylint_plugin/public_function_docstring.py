from pylint.checkers import BaseChecker
import astroid


class PublicFunctionDocstringChecker(BaseChecker):
    name = "public-function-docstring"
    priority = -1
    msgs = {
        "W9005": (
            "Public function '%s' missing docstring",
            "public-function-missing-docstring",
            "All public functions must have a docstring.",
        ),
    }

    def visit_functiondef(self, node: astroid.FunctionDef) -> None:
        if node.name.startswith("_"):
            return  # private or special method, ignore

        docstring = self._get_docstring(node)
        if not docstring.strip():
            self.add_message("public-function-missing-docstring", node=node, args=(node.name,))

    def visit_asyncfunctiondef(self, node: astroid.AsyncFunctionDef) -> None:
        self.visit_functiondef(node)

    def _get_docstring(self, node):
        """
        Get docstring by checking if the first statement in the
        function body is a string literal expression.
        """
        if not node.body:
            return ""

        first_stmt = node.body[0]
        if isinstance(first_stmt, astroid.Expr) and isinstance(first_stmt.value, astroid.Const) and isinstance(first_stmt.value.value, str):
            return first_stmt.value.value
        return ""
