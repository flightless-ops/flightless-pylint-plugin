from pylint.lint import PyLinter
from .except_without_log_or_reraise import ExceptWithoutLogOrReraiseChecker
from .no_conditionals_in_test import NoConditionalsInTestChecker
from .no_direct_settings_import import NoDirectSettingsImportChecker
from .no_prints_outside_main import NoPrintOutsideMainChecker
from .no_py_without_init import NoPyWithoutInitChecker
from .no_pytest_skip import NoPytestSkipChecker
from .test_files_start_with_test import TestFilesStartWithTestChecker
from .unused_logger import UnusedLoggerChecker


def register(linter: PyLinter) -> None:
    linter.register_checker(ExceptWithoutLogOrReraiseChecker(linter))
    linter.register_checker(NoConditionalsInTestChecker(linter))
    linter.register_checker(NoDirectSettingsImportChecker(linter))
    linter.register_checker(NoPrintOutsideMainChecker(linter))
    linter.register_checker(NoPyWithoutInitChecker(linter))
    linter.register_checker(NoPytestSkipChecker(linter))
    linter.register_checker(TestFilesStartWithTestChecker(linter))
    linter.register_checker(UnusedLoggerChecker(linter))
