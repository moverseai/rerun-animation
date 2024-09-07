import logging
import os
from subprocess import call

from rich.logging import RichHandler

from rerun_animation.util import Constants, get_package_path

log = logging.getLogger(__name__)

logging.basicConfig(
    format="[rerun-animation-deploy][%(asctime)s]: %(message)s",
    level=os.getenv("RERUN_ANIMATION_LOG_LEVEL", "INFO").upper(),
    handlers=[RichHandler()],
)


def run():
    pkg_path, is_editable, is_windows = get_package_path()
    env_vars = os.environ.copy()
    binary_path = os.path.join(pkg_path, Constants.BINARY_DIRECTORY_NAME)
    env_vars["RERUN_ANIMATION_PLUGIN_DATA"] = binary_path
    if is_windows:  # windows uses the standalone .exe and .ini at bin path
        env_vars["PATH"] = f"{binary_path}{os.pathsep}{env_vars['PATH']}"
    else:  # non-windows uses the bin/bash exec .py file located at the pkg root, and needs the .ini located at bin path
        env_vars["PATH"] = (
            f"{binary_path}{os.pathsep}{pkg_path}{os.pathsep}{env_vars['PATH']}"
        )
    log.debug(env_vars["PATH"])
    call(["rerun"], env=env_vars)


if __name__ == "__main__":
    run()
