from importlib.metadata import Distribution

from packaging.version import Version
from rich.console import Console
from rich.logging import RichHandler
from rich.traceback import install as rich_install

from rerun_animation.util import Constants, get_package_path

rich_install(show_locals=False, max_frames=0)

import numpy as np

if Version(np.__version__) > Version("1.23.1"):
    np.bool = np.bool_
    np.int = np.int_
    np.float = np.float_
    np.complex = np.complex_
    np.object = np.object_
    np.unicode = np.unicode_
    np.str = np.str_

import argparse
import glob
import logging
import os
import pickle
import platform
import shutil
import stat
import subprocess
import sys
import time

import trimesh

log = logging.getLogger(__name__)

logging.basicConfig(
    format="[rerun-animation-deploy][%(asctime)s]: %(message)s",
    level=os.getenv("RERUN_ANIMATION_LOG_LEVEL", "INFO").upper(),
    handlers=[RichHandler(markup=True, rich_tracebacks=True)],
)


def run():
    parser = argparse.ArgumentParser(
        description="""

    """
    )
    parser.add_argument("--body_data_root", type=str, required=False)
    parser.add_argument("--deploy_path", type=str, default="")
    args = parser.parse_args()
    pkg_path, is_editable, is_windows = get_package_path()
    log.debug(
        f"Setting up the `{'editable' if is_editable else 'installed'}` package @ {pkg_path}"
    )
    binary_path = os.path.join(pkg_path, Constants.BINARY_DIRECTORY_NAME)
    os.makedirs(binary_path, exist_ok=True)

    configs_path = os.path.join(pkg_path, "configs")
    shutil.copy2(
        os.path.join(configs_path, Constants.DEFAULT_CONFIG_FILENAME),
        os.path.join(binary_path, Constants.CURRENT_CONFIG_FILENAME),
    )
    log.info(f":green_circle:\tSetting the default configuration.")

    if uses_external := args.deploy_path:
        out_folder = args.deploy_path
        log.info(f"Creating the output directory @ [italic]{out_folder}[/].")
        os.makedirs(out_folder, exist_ok=True)
    else:
        out_folder = binary_path
    data_root = args.body_data_root or os.devnull
    log.info(
        f":gear:\tPreparing files from [italic]{os.path.abspath(data_root)}[/] to [italic]{os.path.abspath(out_folder)}[/]."
    )

    for gender_in, gender_out in zip(
        ["neutral", "m", "f"], ["NEUTRAL", "MALE", "FEMALE"]
    ):
        # SMPL
        data_files = glob.glob(
            os.path.join(data_root, f"**/basicmodel_{gender_in}*.pkl"), recursive=True
        )
        if not data_files:
            # log.error(f":exclamation_mark:\tCould not locate body model data files @ [italic]{data_root}[/], deployment failed!")
            # sys.exit(-1)
            log.warning(
                f":exclamation_mark:\tCould not locate SMPL {gender_out} body model data files @ [italic]{data_root}[/]!"
            )
        else:
            data_file = data_files[0]

            log.info(f"\t:orange_circle:Processing [italic]{data_file}[/] ...")
            with open(data_file, "rb") as f:
                body_data = pickle.load(f, encoding="latin1")
            shape_blendshapes = np.ascontiguousarray(
                np.array(body_data["shapedirs"]).astype(np.float32)
            )
            pose_blendshapes = np.ascontiguousarray(
                np.array(body_data["posedirs"]).astype(np.float32)
            )
            regressor = np.ascontiguousarray(
                np.array(body_data["J_regressor"].todense()).astype(np.float32)
            )
            template = np.ascontiguousarray(
                np.array(body_data["v_template"]).astype(np.float32)
            )
            weights = np.ascontiguousarray(
                np.array(body_data["weights"]).astype(np.float32)
            )
            faces = np.ascontiguousarray(np.array(body_data["f"]).astype(np.int32))
            parents = np.ascontiguousarray(
                np.array(body_data["kintree_table"]).astype(np.int32)
            )[0]
            mesh = trimesh.Trimesh(
                vertices=template, faces=faces.astype(np.int64), process=False
            )

            output_filename = os.path.join(out_folder, f"SMPL_{gender_out}.npz")
            np.savez_compressed(
                output_filename,
                shape_blendshapes=shape_blendshapes,
                pose_blendshapes=pose_blendshapes,
                regressor=regressor,
                template=template,
                weights=weights,
                faces=faces,
                parents=parents,
                normals=mesh.vertex_normals,
            )
            log.info(f"\t:green_circle:Done.")
            log.debug(f"\tSaved @ [italic]{output_filename}[/] ...")

            if uses_external:
                log.info(
                    f"\t:warning:[bold yellow blink]Creating symlink to[/] [italic]{output_filename}[/] ..."
                )
                local_output_filename = os.path.join(pkg_path, f"SMPL_{gender_out}.npz")
                # NOTE: this is not necessary as we are in control of these files
                #       it will only crash if the file was not symlinked and in use
                if os.path.exists(local_output_filename):
                    os.remove(local_output_filename)
                os.symlink(output_filename, local_output_filename)
                log.info(f"\t:ok_button:[bold green]Success[\]!")

        # SMPL-H
        data_files = glob.glob(
            os.path.join(data_root, f"**/**/{gender_out.lower()}/model.npz"),
            recursive=True,
        )
        if not data_files:
            # log.error(f":exclamation_mark:\tCould not locate body model data files @ [italic]{data_root}[/], deployment failed!")
            # sys.exit(-1)
            log.warning(
                f":exclamation_mark:\tCould not locate SMPL-H {gender_out} body model data files @ [italic]{data_root}[/]!"
            )
        else:
            data_file = data_files[0]

            log.info(f"\t:orange_circle:Processing [italic]{data_file}[/] ...")
            body_data = np.load(data_file)
            shape_blendshapes = np.ascontiguousarray(
                body_data["shapedirs"].astype(np.float32)
            )
            pose_blendshapes = np.ascontiguousarray(
                body_data["posedirs"].astype(np.float32)
            )
            regressor = np.ascontiguousarray(
                body_data["J_regressor"].astype(np.float32)
            )
            template = np.ascontiguousarray(body_data["v_template"].astype(np.float32))
            weights = np.ascontiguousarray(body_data["weights"].astype(np.float32))
            faces = np.ascontiguousarray(body_data["f"].astype(np.int32))
            parents = np.ascontiguousarray(body_data["kintree_table"].astype(np.int32))[
                0
            ]
            mesh = trimesh.Trimesh(
                vertices=template, faces=faces.astype(np.int64), process=False
            )

            output_filename = os.path.join(out_folder, f"SMPLH_{gender_out}.npz")
            np.savez_compressed(
                output_filename,
                shape_blendshapes=shape_blendshapes,
                pose_blendshapes=pose_blendshapes,
                regressor=regressor,
                template=template,
                weights=weights,
                faces=faces,
                parents=parents,
                normals=mesh.vertex_normals,
            )
            log.info(f"\t:green_circle:Done.")
            log.debug(f"\tSaved @ [italic]{output_filename}[/] ...")

            if uses_external:
                log.info(
                    f"\t:warning:Creating symlink to [italic]{output_filename}[/] ..."
                )
                local_output_filename = os.path.join(
                    pkg_path, f"SMPLH_{gender_out}.npz"
                )
                # NOTE: this is not necessary as we are in control of these files
                #       it will only crash if the file was not symlinked and in use
                if os.path.exists(local_output_filename):
                    os.remove(local_output_filename)
                os.symlink(output_filename, local_output_filename)
                log.info(f"\t:ok_button:[bold green]Success[/!")

    plugin_filename = f"{pkg_path}/rerun-loader-animation.py"
    if platform.system() == "Windows":
        log.debug(f"Installation of {plugin_filename} starting @ {pkg_path}")
        log.info(":gear:\tInstalling the rerun-loader-animation plugin [blink]...[/]")
        console = Console()
        # import PyInstaller.__main__
        # PyInstaller.__main__.run([
        #     f'{pkg_path}/rerun_animation/rerun-loader-animation.py',
        #     '--onefile',
        #     '--distpath', f'{pkg_path}',
        #     '--specpath', f'{pkg_path}/build',
        #     '--workpath', f'{pkg_path}/build',
        #     '--clean', '-y',
        # ])
        # log.setLevel(logging.WARNING)

        process = subprocess.Popen(
            [
                "pyinstaller",
                plugin_filename,
                "--onefile",
                "--distpath",
                f"{binary_path}",
                "--specpath",
                f"{pkg_path}/build",
                "--workpath",
                f"{pkg_path}/build",
                "--clean",
                "-y",
            ],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.STDOUT,
        )
        with console.status("[bold green blink]...") as status:
            while process.poll() is None:
                time.sleep(1)
        log.info(
            f":green_circle:\tThe `rerun-loader-animation` plugin has been installed."
        )

        np_pkg = Distribution.from_name("numpy")
        dlls = [str(f.locate()) for f in np_pkg.files if str(f).endswith(".dll")]
        for dll in dlls:
            shutil.copy2(dll, os.path.join(binary_path, os.path.basename(dll)))
    else:  # linux and macos
        executable_filename = shutil.copy2(
            plugin_filename, os.path.join(pkg_path, os.path.basename(plugin_filename))
        )
        st = os.stat(executable_filename)
        os.chmod(
            executable_filename, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH
        )


if __name__ == "__main__":
    run()
