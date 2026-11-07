"""Rebuild the current R7 author delta from the frozen R6 archive."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().with_name('build-r7.py')), run_name='__main__')
