from pylint.checkers import BaseChecker
from pylint.lint import PyLinter
from astroid import NodeNG

RULE_NAME = "no-direct-settings-import"


class NoDirectSettingsImportChecker(BaseChecker):
    name = RULE_NAME
    priority = -1
    msgs = {
        "E9003": (
            'Do not import settings directly (e.g., from myapp.settings); use "from django.conf import settings"',
            RULE_NAME,
            "Direct settings module import detected. Use django.conf.settings instead.",
        )
    }

    def visit_importfrom(self, node: NodeNG) -> None:
        if node.modname and node.modname.endswith(".settings") or node.modname == "settings":
            self.add_message(RULE_NAME, node=node)

    def visit_import(self, node: NodeNG) -> None:
        for name, _alias in node.names:
            if name.endswith(".settings") or name == "settings":
                self.add_message(RULE_NAME, node=node)


def register(linter: PyLinter) -> None:
    linter.register_checker(NoDirectSettingsImportChecker(linter))
