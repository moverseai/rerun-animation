import logging
from importlib.metadata import Distribution

from rich.logging import RichHandler
from rich.pretty import pprint
from rich.traceback import install as rich_install

from rerun_animation.util import Constants, get_package_path

rich_install(show_locals=False, max_frames=0)

log = logging.getLogger(__name__)

logging.basicConfig(
    format="%(message)s", level=logging.INFO, handlers=[RichHandler(markup=True)]
)

import argparse
import configparser
import glob
import os
import platform
import shutil

_ACTIONS_ = [
    "list",
    "install",
    "reset",
    "print",
    "select",
    "create",
]


def run():
    parser = argparse.ArgumentParser(
        description="""

    """
    )
    parser.add_argument("action", type=str)
    parser.add_argument("file_or_name", type=str, nargs="?", default="")
    args = parser.parse_args()

    pkg_path, is_editable, is_windows = get_package_path()
    configs_path = os.path.join(pkg_path, "configs")
    binary_path = os.path.join(pkg_path, Constants.BINARY_DIRECTORY_NAME)
    match args.action:
        case "list":
            installed = glob.glob(
                os.path.join(configs_path, "**", "*.ini"), recursive=True
            )
            current = glob.glob(os.path.join(os.path.curdir, "*.ini"))
            all_configs = set(installed) | set(current)
            log.info(f"{len(all_configs)} configurations available:")
            for config in all_configs:
                name = os.path.splitext(os.path.basename(config))[0].removeprefix(
                    "rerun-animation-"
                )
                log.info(f"\t[bold yellow]{name}[/]")
        case "install":
            filepath = os.path.abspath(args.file_or_name)
            filename = os.path.basename(filepath)
            name = os.path.splitext(filename)[0]
            log.info(f":gear:\tInstalling configuration [bold yellow]{name}[/]")
            if filename == Constants.DEFAULT_CONFIG_FILENAME:
                log.error(
                    f':exclamation:\tCannot overwrite "{Constants.DEFAULT_CONFIG_FILENAME}", please rename the configuration.'
                )
                exit(-1)
            else:
                dst = shutil.copy2(
                    f"{name}.ini", os.path.join(configs_path, f"{name}.ini")
                )
                shutil.copy2(dst, os.path.join(binary_path, "rerun-animation.ini"))
                log.info(
                    f":green_circle:\tCompleted, the new ([bold italic cyan]{name}[/]) configuration was installed and also selected as the current configuration."
                )
        case "reset":
            shutil.copy2(
                os.path.join(configs_path, Constants.DEFAULT_CONFIG_FILENAME),
                os.path.join(binary_path, Constants.CURRENT_CONFIG_FILENAME),
            )
            log.info(f":orange_circle:\tSwitched back to the default configuration.")
        case "print":
            config = configparser.ConfigParser(
                inline_comment_prefixes=("#",),
                empty_lines_in_values=False,
                # defaults=Constants.CONFIGURATION_DEFAULTS,
                interpolation=configparser.ExtendedInterpolation(),
            )
            if args.file_or_name:
                log.info(args.file_or_name)
                name, ext = os.path.splitext(args.file_or_name)
                if ext == ".ini":
                    filepath = os.path.abspath(args.file_or_name)
                    log.info(filepath)
                    if os.path.exists(filepath):
                        config.read(filepath)
                else:
                    installed = glob.glob(
                        os.path.join(configs_path, "**", "*.ini"), recursive=True
                    )
                    all_names = []
                    for installed_config in installed:
                        all_names.append(
                            os.path.splitext(os.path.basename(installed_config))[0]
                        )
                    log.info(all_names)
                    if name in set(all_names):
                        log.info(name)
                        config.read(
                            os.path.join(
                                configs_path, name.replace(".ini", "") + ".ini"
                            )
                        )
            else:
                log.info(Constants.CURRENT_CONFIG_FILENAME)
                config.read(
                    os.path.join(binary_path, Constants.CURRENT_CONFIG_FILENAME)
                )
            pprint(
                {
                    section: dict(config[section])
                    for section in config
                    if section != "DEFAULT"
                },
                expand_all=True,
            )
        case "select":
            names = [
                os.path.splitext(os.path.basename(fp))[0]
                for fp in glob.glob(os.path.join(configs_path, "*.ini"))
            ]
            name = args.file_or_name
            if name not in names:
                log.warning(
                    f"[bold yellow]:warning:[/]\tConfiguration [bold yellow]{name}[/] not found. The list of available configurations are: [bold]{names}[/]"
                )
            else:
                shutil.copy2(
                    os.path.join(configs_path, f"{name}.ini"),
                    os.path.join(binary_path, Constants.CURRENT_CONFIG_FILENAME),
                )
                log.info(
                    f":green_circle:\tSwitched to the [bold cyan italic]{name}[/] configuration."
                )
        case "create":
            filepath = args.file_or_name or Constants.TEMPLATE_CONFIG_FILENAME
            filepath = os.path.abspath(filepath)
            filedir = os.path.dirname(filepath)
            name, ext = os.path.splitext(os.path.basename(filepath))
            os.chdir(pkg_path)
            config = configparser.ConfigParser(
                inline_comment_prefixes=("#",),
                empty_lines_in_values=False,
                interpolation=configparser.ExtendedInterpolation(),
            )
            config.read(
                os.path.join(pkg_path, "configs", Constants.DEFAULT_CONFIG_FILENAME)
            )
            new_filepath = os.path.join(filedir, f"{name}.ini")
            with open(new_filepath, "w") as f:
                config.write(f)
            log.info(
                f"A configuration file was created @ [italic cyan]{new_filepath}[/]."
            )
        case _:
            log.error(
                f"Unsupported [cyan italic]rerun-animation-config[/] action:exclamation:\nThe following actions are supported: {_ACTIONS_}"
            )


if __name__ == "__main__":
    run()
