from .no_pytest_skip import NoPytestSkipChecker
from .no_direct_settings_import import NoDirectSettingsImportChecker
from .no_conditionals_in_test import NoConditionalsInTestChecker


def register(linter):
    linter.register_checker(NoPytestSkipChecker(linter))
    linter.register_checker(NoDirectSettingsImportChecker(linter))
    linter.register_checker(NoConditionalsInTestChecker(linter))
