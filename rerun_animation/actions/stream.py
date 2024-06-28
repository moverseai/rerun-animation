import sys
import os
import importlib
from rerun_animation.util import (
    get_package_path
)

module_name = importlib.import_module('rerun_animation.rerun-loader-animation')

def run() -> None:
    # ensure input filepaths are absolute as we will be changing the cwd
    sys.argv[1:] = [os.path.abspath(f) for f in sys.argv[1:]]
    os.chdir(get_package_path())
    module_name.main()

if __name__ == "__main__":
    run()