import os
from pylint.checkers import BaseChecker


RULE_NAME = "missing-init-py"


class NoPyWithoutInitChecker(BaseChecker):
    name = RULE_NAME
    priority = -1
    msgs = {
        "W9006": (
            "Directory '%s' contains Python files but is missing __init__.py",
            RULE_NAME,
            "Python packages require __init__.py in directories containing Python files.",
        ),
    }

    def process_module(self, node):
        # Get directory of current module file
        filename = getattr(node, "file", None)
        if not filename:
            return
        directory = os.path.dirname(os.path.abspath(filename))

        # Check if __init__.py exists in directory
        init_py = os.path.join(directory, "__init__.py")
        if os.path.exists(init_py):
            return  # all good

        # Check if directory contains any other .py files besides __init__.py
        py_files = [f for f in os.listdir(directory) if f.endswith(".py") and f != "__init__.py"]
        if py_files:
            # Emit message on first line of file
            self.add_message(RULE_NAME, node=node, line=1, args=(directory,))
