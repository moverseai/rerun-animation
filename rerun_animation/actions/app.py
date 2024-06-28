from subprocess import call
from rich.logging import RichHandler
from rerun_animation.util import (
    get_package_path
)
import os
import logging

log = logging.getLogger(__name__)

logging.basicConfig(
    format='[rerun-animation-deploy][%(asctime)s]: %(message)s',
    level=logging.INFO,
    handlers=[RichHandler()]
)

def run():
    #TODO: check for installation if platform == Windows
    pkg_path = get_package_path()
    env_vars = os.environ.copy()
    env_vars["PATH"] = f"{os.getcwd()}{os.pathsep}{pkg_path}{os.pathsep}{env_vars['PATH']}"
    log.debug(env_vars["PATH"])
    call(["rerun"], env=env_vars)

if __name__ == "__main__":
    run()