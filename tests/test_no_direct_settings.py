from flightless_pylint_plugin.no_direct_settings_import import NoDirectSettingsImportChecker
from .utilities import run_checker_on_code


def test_from_settings_import_triggers_error():
    code = "from myapp.settings import DEBUG"
    messages = run_checker_on_code(code, NoDirectSettingsImportChecker)
    assert "no-direct-settings-import" in messages


def test_from_settings_only_import_triggers_error():
    code = "from settings import DEBUG"
    messages = run_checker_on_code(code, NoDirectSettingsImportChecker)
    assert "no-direct-settings-import" in messages


def test_plain_settings_import_triggers_error():
    code = "import settings"
    messages = run_checker_on_code(code, NoDirectSettingsImportChecker)
    assert "no-direct-settings-import" in messages


def test_import_dotted_settings_triggers_error():
    code = "import myapp.settings"
    messages = run_checker_on_code(code, NoDirectSettingsImportChecker)
    assert "no-direct-settings-import" in messages


def test_django_conf_settings_does_not_trigger():
    code = "from django.conf import settings"
    messages = run_checker_on_code(code, NoDirectSettingsImportChecker)
    assert not messages


def test_unrelated_import_does_not_trigger():
    code = "import os"
    messages = run_checker_on_code(code, NoDirectSettingsImportChecker)
    assert not messages
