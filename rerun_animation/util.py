import glob
import logging
import os
import platform
import typing
from importlib.metadata import Distribution

import rerun as rr

__all__ = [
    "setup_rerun_logging",
    "set_time_from_args",
    "flatten_globs",
    "get_package_path",
    "Constants",
]

if platform.system() == "Windows":
    _BIN_PATH_: str = "bin"
else:
    _BIN_PATH_: str = ""


class Constants:
    BINARY_DIRECTORY_NAME: str = _BIN_PATH_
    CURRENT_CONFIG_FILENAME: str = "rerun-animation.ini"
    DEFAULT_CONFIG_FILENAME: str = "default.ini"
    TEMPLATE_CONFIG_FILENAME: str = "template.ini"
    CONFIGURATION_DEFAULTS: typing.Dict[str, str] = {
        # viewer
        "up_axis": "y",
        "show_rotations": "no",
        "color": "magenta",
        "joint_radius": "0.25",
        "fps": "30",
        # body
        "type": "smpl",
        "use_pose_blendshapes": "no",
        "pose_type": "axisangle",
        "gender": "neutral",
        # file keys
        "shape": "betas",
        "pose": "pose_body",
        "translation": "trans",
        "rotation": "",
        "fps": "mocap_frame_rate",
        "hands": "pose_hand",
    }


def setup_rerun_logging() -> None:
    handler = rr.LoggingHandler("rerun-animation")
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(os.getenv("RERUN_ANIMATION_LOG_LEVEL", "INFO").upper())
    return logging.getLogger()


def set_time_from_args(args: typing.Mapping[str, typing.Any]) -> None:
    if not args.timeless and args.time is not None:
        for time_str in args.time:
            parts = time_str.split("=")
            if len(parts) != 2:
                continue
            timeline_name, time = parts
            rr.set_time_nanos(timeline_name, int(time))

        for time_str in args.sequence:
            parts = time_str.split("=")
            if len(parts) != 2:
                continue
            timeline_name, time = parts
            rr.set_time_sequence(timeline_name, int(time))


def flatten_globs(filepaths: typing.Sequence[str]) -> typing.List[str]:
    all_filepaths = []
    for filepath in filepaths:
        all_filepaths.extend(glob.glob(filepath))
    return all_filepaths


def get_package_path() -> typing.Tuple[str, bool]:
    pkg = Distribution.from_name("rerun_animation")
    is_windows = False
    if platform.system() == "Windows":
        main_filename = "rerun-loader-animation.py"  # "rerun-loader-animation.exe"
        is_windows = True
    else:
        main_filename = "rerun-loader-animation.py"
    main_abspath = None
    is_editable = True
    for pkg_file in pkg.files:
        abspath = str(pkg_file.locate())
        if abspath.endswith(main_filename):
            main_abspath = abspath
            # break
        if abspath.endswith("RECORD"):
            is_editable = False
    if not main_filename:
        raise RuntimeError(
            "The rerun-animation installation is corrupt, please re-install."
        )
    pkg_path = os.path.dirname(main_abspath)
    if not is_editable:
        pkg_path = os.path.join(os.path.dirname(pkg_path), "rerun_animation")
    return pkg_path, is_editable, is_windows
