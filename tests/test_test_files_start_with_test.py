from flightless_pylint_plugin.test_files_start_with_test import TestFilesStartWithTestChecker
from .utilities import run_checker_on_file


def test_test_file_without_test_prefix_triggers(tmp_path) -> None:
    file = tmp_path / "some_tests.py"
    file.write_text("def test_ok(): pass")
    messages = run_checker_on_file(str(file), TestFilesStartWithTestChecker)
    assert "test-files-start-with-test" in messages


def test_non_test_file_does_not_trigger(tmp_path) -> None:
    file = tmp_path / "utils.py"
    file.write_text("def helper(): pass")
    messages = run_checker_on_file(str(file), TestFilesStartWithTestChecker)
    assert not messages


def test_correctly_named_test_file_does_not_trigger(tmp_path) -> None:
    file = tmp_path / "test_example.py"
    file.write_text("def test_stuff(): pass")
    messages = run_checker_on_file(str(file), TestFilesStartWithTestChecker)
    assert not messages


def test_init_file_does_not_trigger(tmp_path) -> None:
    file = tmp_path / "__init__.py"
    file.write_text("# init")
    messages = run_checker_on_file(str(file), TestFilesStartWithTestChecker)
    assert not messages
