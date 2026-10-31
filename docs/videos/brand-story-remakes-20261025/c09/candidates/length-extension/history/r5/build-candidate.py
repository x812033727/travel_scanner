"""Rebuild the current r5 author candidate; all earlier builders remain in history."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().with_name('build-r5.py')), run_name='__main__')
