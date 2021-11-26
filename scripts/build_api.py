import sys
from pathlib import Path

# hacky hacky dum
sys.path.append(str(Path(__file__).parent.parent))

import subprocess

from api import __version__, base_dir

subprocess.run(f"docker build -t api:v{__version__} {base_dir}".split())
