import sys
from pathlib import Path

# hacky hacky dum
sys.path.append(str(Path(__file__).parent.parent))

import subprocess

import click
from api import __version__, base_dir

image = f"api:v{__version__}"
click.secho(f"building {image=}", color="yellow")
subprocess.run(f"docker build -t {image} {base_dir}".split())
