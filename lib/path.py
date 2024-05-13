import os
from pathlib import Path

TIMER = str(os.path.expanduser('~/.fango/timer.json'))
CONFIG = str(os.path.expanduser('~/.fango/config.json'))
ROOT_DIR = Path(os.path.realpath(__file__)).parent.parent
ASSETS_DIR = os.path.join(ROOT_DIR, "assets")
USER_DIR = os.path.expanduser("~/.fango")