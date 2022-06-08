import _version
import os
from pathlib import Path

from Updater import Updater

INSTALL_PATH = Path(__file__).resolve().parent.parent.parent
DIR_FULL_PATH = Path(__file__).resolve().parent.parent
THE_LINK = INSTALL_PATH / 'latest'
CURRENT_VERSION = _version.__version__

if __name__ == '__main__':
    print(CURRENT_VERSION)
    print(INSTALL_PATH)
    print(DIR_FULL_PATH)
    print(THE_LINK)
    r = Updater()
    r.updateCheck()
    # os.system('pause')
