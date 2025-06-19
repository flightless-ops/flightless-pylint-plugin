from pylint.checkers import BaseChecker
import os

RULE_NAME = "test-files-start-with-test"


class TestFilesStartWithTestChecker(BaseChecker):
    name = RULE_NAME
    msgs = {
        "W9003": (
            "Test files must start with 'test_'",
            RULE_NAME,
            "All test files must be named with a 'test_' prefix for pytest discovery.",
        ),
    }

    def process_module(self, node):
        filename = node.file
        basename = os.path.basename(filename)

        if basename.endswith(".py") and "test" in basename and not basename.startswith("test_"):
            self.add_message(RULE_NAME, line=1, node=None)
