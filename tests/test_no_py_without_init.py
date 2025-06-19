import tempfile
import shutil
from pathlib import Path
from flightless_pylint_plugin.no_py_without_init import NoPyWithoutInitChecker
from .utilities import run_checker_on_file


def test_triggers_when_no_init_py():
    tmp_dir = tempfile.mkdtemp()
    try:
        (Path(tmp_dir) / "main.py").write_text("print('hello')")
        (Path(tmp_dir) / "helper.py").write_text("print('helper')")
        filename = str(Path(tmp_dir) / "main.py")

        messages = run_checker_on_file(filename, NoPyWithoutInitChecker)
        assert "missing-init-py" in messages
    finally:
        shutil.rmtree(tmp_dir)


def test_no_trigger_when_init_py_exists():
    tmp_dir = tempfile.mkdtemp()
    try:
        (Path(tmp_dir) / "main.py").write_text("print('hello')")
        (Path(tmp_dir) / "__init__.py").write_text("")
        filename = str(Path(tmp_dir) / "main.py")

        messages = run_checker_on_file(filename, NoPyWithoutInitChecker)
        assert "missing-init-py" not in messages
    finally:
        shutil.rmtree(tmp_dir)
