"""Current deterministic C09 revision builder; previous generators stay in history folders."""
from pathlib import Path
import runpy
runpy.run_path(str(Path(__file__).resolve().with_name('build-r8.py')),run_name='__main__')
