"""Rebuild the current R6 author delta from the frozen R5 archive."""
from pathlib import Path
import runpy

runpy.run_path(str(Path(__file__).resolve().with_name('build-r6.py')), run_name='__main__')
