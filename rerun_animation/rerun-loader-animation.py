#!/usr/bin/env python3

import argparse
import configparser
import os
import sys
from collections import defaultdict
from enum import Enum

import colour  # pip install colour
import numpy as np
import rerun as rr  # pip install rerun-sdk

from rerun_animation.bvh import euler_angles_to_matrix
from rerun_animation.bvh import load as load_bvh
from rerun_animation.kinematics import forward_kinematics
from rerun_animation.smpl import (
    SMPL_JOINT_NAMES,
    append_missing_rotations,
    calc_landmarks,
    calc_pose_offsets,
    calc_shaped_vertices,
    ensure_pose_shape,
    ensure_rotmat,
    skinning,
    traverse_kinematic_chain,
)
from rerun_animation.util import (
    Constants,
    flatten_globs,
    set_time_from_args,
    setup_rerun_logging,
)


class Mode(Enum):
    BVH = 1
    BODY = 2


def log_bvh(filename: str, entity_path: str, config) -> None:
    root_position, euler, offsets, parents, joint_names, order, timestep = load_bvh(
        filename
    )
    # TODO: add config scale param?
    T, J, C = euler.shape
    local_rotations = euler_angles_to_matrix(np.deg2rad(euler), order.upper())
    joint_positions, global_rotations = forward_kinematics(
        local_rotations, root_position, offsets, parents
    )

    color_key = config.get("rerun", "color", fallback="magenta")
    color = colour.Color(color_key).get_rgb() + (0.5,)

    rr.log(
        "/",
        rr.AnnotationContext(
            rr.ClassDescription(
                # NOTE: until the issue w/ the labels taking up all space is resolved, we will not be logging them
                # info=rr.AnnotationInfo(id=0, label=entity_path, color=color),
                # keypoint_annotations=[rr.AnnotationInfo(id=id, label=j) for id, j in enumerate(joint_names)],
                info=rr.AnnotationInfo(id=0, label=None, color=color),
                keypoint_annotations=[
                    rr.AnnotationInfo(id=id, label=None)
                    for id, j in enumerate(joint_names)
                ],
                keypoint_connections=list(
                    filter(lambda t: t[1] > 0, enumerate(parents))
                ),
            )
        ),
        static=True,
    )

    if show_rotations := config.getboolean(
        "bvh.options", "show_rotations", fallback=False
    ):
        axii_colors = np.array([[255, 0, 0], [0, 255, 0], [0, 0, 255]])

    joint_radius = config.getfloat("bvh.options", "joint_radius", fallback=0.2)
    for i, t in enumerate(joint_positions):
        rr.set_time_seconds("time", i * timestep)
        rr.log(
            f"{entity_path}/joints/positions",
            rr.Points3D(
                t, class_ids=0, keypoint_ids=range(t.shape[0]), radii=joint_radius
            ),
        )
        if show_rotations:
            rr.log(
                f"{entity_path}/joints/rotations",
                rr.Arrows3D(
                    origins=np.tile(t, (1, 3)).reshape(-1, 3),
                    vectors=global_rotations[i].transpose(0, 2, 1).reshape(-1, 3),
                    colors=np.tile(axii_colors, (J, 1)),
                ),
            )


def log_smpl_body(data_root: str, filepath: str, entity_path: str, config) -> None:
    animation_data = np.load(filepath)

    if body_key := config.get("smpl.file.keys", "body", fallback=None):
        body_type = str(animation_data[body_key]).lower()
    else:
        body_type = config.get("body", "type", fallback="smpl").lower()

    if gender_key := config.get(f"{body_type}.file.keys", "gender", fallback=None):
        gender = str(animation_data[gender_key])
    else:
        gender = config.get(f"{body_type}.options", "gender", fallback=None)
    if not gender:
        gender = "neutral"

    body_data = np.load(
        os.path.join(data_root, f"{body_type.upper()}_{gender.upper()}.npz")
    )
    shape_blendshapes = body_data["shape_blendshapes"]
    template = body_data["template"]
    regressor = body_data["regressor"]

    betas_key = config.get(f"{body_type}.file.keys", "shape", fallback="betas")
    if betas_key in animation_data:
        betas = animation_data[betas_key].astype(np.float32)
    else:
        betas = np.zeros(shape_blendshapes.shape[-1], dtype=np.float32)

    shaped_vertices = template + calc_shaped_vertices(betas, shape_blendshapes)
    shaped_joints = calc_landmarks(regressor, shaped_vertices)
    pose_key = config.get(f"{body_type}.file.keys", "pose", fallback="pose")
    pose = animation_data[pose_key].astype(np.float32)
    pose_type = config.get(
        f"{body_type}.options",
        "pose_type",
        fallback=config.get("body", "pose_type", fallback="axisangle"),
    )
    pose = ensure_pose_shape(pose, pose_type)

    if orientation_key := config.get(
        f"{body_type}.file.keys", "rotation", fallback=None
    ):
        orientation = animation_data[orientation_key].astype(np.float32)
        orientation = ensure_pose_shape(orientation, pose_type)
        pose = np.concatenate([orientation, pose], axis=1)

    if body_type == "smplh" and (
        hands_key := config.get(f"{body_type}.file.keys", "hands", fallback=None)
    ):
        hands_pose = animation_data[hands_key].astype(np.float32)
        hands_pose = ensure_pose_shape(hands_pose, pose_type)
        pose = np.concatenate([pose, hands_pose], axis=1)

    translation_key = config.get(
        f"{body_type}.file.keys", "translation", fallback="trans"
    )
    translation = animation_data[translation_key].astype(np.float32)

    rotations = ensure_rotmat(pose, pose_type)
    rotations = append_missing_rotations(rotations, max_joints=len(SMPL_JOINT_NAMES))

    if use_pose_blendshapes := config.getboolean(
        f"{body_type}.options", "use_pose_blendshapes", fallback=False
    ):
        pose_blendshapes = body_data["pose_blendshapes"]

    parents = body_data["parents"].astype(np.int32)
    weights = body_data["weights"].astype(np.float32)
    faces = body_data["faces"].astype(np.int32)
    normals = body_data["normals"].astype(np.float32)

    skeleton_color_key = config.get("rerun", "color", fallback="magenta")
    skeleton_color = colour.Color(skeleton_color_key).get_rgb() + (0.5,)

    rr.log(
        "/",
        rr.AnnotationContext(
            rr.ClassDescription(
                # NOTE: until the issue w/ the labels taking up all space is resolved, we will not be logging them
                # info=rr.AnnotationInfo(id=0, label=entity_path, color=skeleton_color),
                # keypoint_annotations=[rr.AnnotationInfo(id=id, label=j) for id, j in enumerate(SMPL_JOINT_NAMES)],
                info=rr.AnnotationInfo(id=0, label=None, color=skeleton_color),
                keypoint_annotations=[
                    rr.AnnotationInfo(id=id, label=None)
                    for id, j in enumerate(SMPL_JOINT_NAMES)
                ],
                keypoint_connections=list(
                    filter(lambda t: t[1] > 0, enumerate(parents))
                ),
            )
        ),
        static=True,
    )

    if mesh_color_key := config.get(f"{body_type}.options", "color", fallback=None):
        mesh_color = colour.Color(mesh_color_key).get_rgb() + (0.5,)
    else:
        mesh_color = skeleton_color

    if (
        fps_key := config.get(f"{body_type}.file.keys", "fps", fallback=None)
    ) and fps_key in animation_data:
        fps = int(animation_data[fps_key])
    else:
        fps = config.getfloat(f"rerun", "fps", fallback=30.0)
    delta_time_secs = 1.0 / fps

    for i, rotation in enumerate(rotations):
        vertices = shaped_vertices.copy()
        if use_pose_blendshapes:
            vertices += calc_pose_offsets(pose_blendshapes, rotations[0])
        posed_joints, joint_transforms = traverse_kinematic_chain(
            rotation, shaped_joints, parents
        )
        posed_vertices, posed_normals = skinning(
            weights, vertices, joint_transforms, normals
        )

        rr.set_time_seconds("time", i * delta_time_secs)
        rr.log(
            f"/{entity_path}/joints",
            rr.Points3D(
                posed_joints + translation[i],
                class_ids=0,
                keypoint_ids=range(max(posed_joints.shape)),
            ),
        )
        rr.log(
            f"/{entity_path}/mesh",
            rr.Mesh3D(
                vertex_positions=posed_vertices + translation[i],
                triangle_indices=faces,
                vertex_normals=posed_normals,
                albedo_factor=rr.AlbedoFactor(mesh_color),
            ),
        )


def get_args() -> None:
    # The Rerun Viewer will always pass these two pieces of information:
    # 1. The path to be loaded, as a positional arg.
    # 2. A shared recording ID, via the `--recording-id` flag.
    #
    # It is up to you whether you make use of that shared recording ID or not.
    # If you use it, the data will end up in the same recording as all other plugins interested in
    # that file, otherwise you can just create a dedicated recording for it. Or both.
    #
    # Check out `re_data_source::DataLoaderSettings` documentation for an exhaustive listing of
    # the available CLI parameters.
    parser = argparse.ArgumentParser(
        description="""
    This is an animation data loader plugin for the Rerun Viewer.
    """
    )
    parser.add_argument("filepaths", type=str, nargs="+")
    parser.add_argument(
        "--application-id", type=str, help="optional recommended ID for the application"
    )
    parser.add_argument(
        "--recording-id", type=str, help="optional recommended ID for the recording"
    )
    parser.add_argument(
        "--entity-path-prefix", type=str, help="optional prefix for all entity paths"
    )
    parser.add_argument(
        "--timeless",
        action="store_true",
        default=False,
        help="deprecated: alias for `--static`",
    )
    parser.add_argument(
        "--static",
        action="store_true",
        default=False,
        help="optionally mark data to be logged as static",
    )
    parser.add_argument(
        "--time",
        type=str,
        action="append",
        help="optional timestamps to log at (e.g. `--time sim_time=1709203426`)",
    )
    parser.add_argument(
        "--sequence",
        type=str,
        action="append",
        help="optional sequences to log at (e.g. `--sequence sim_frame=42`)",
    )
    args = parser.parse_args()
    return args


def main() -> None:
    args = get_args()
    filepaths = flatten_globs(args.filepaths)
    valid_extensions = set([".bvh", ".npz"])
    valid_filepaths = defaultdict(list)
    for filepath in filepaths:
        if os.path.isfile(filepath):
            extension = os.path.splitext(filepath)[1].lower()
            if extension in valid_extensions:
                valid_filepaths[extension].append(filepath)
    if not all(valid_filepaths.values()):
        sys.exit(rr.EXTERNAL_DATA_LOADER_INCOMPATIBLE_EXIT_CODE)

    log = setup_rerun_logging()

    data_root = os.environ.get("RERUN_ANIMATION_PLUGIN_DATA", "./bin")
    config_filename = os.path.join(data_root, Constants.CURRENT_CONFIG_FILENAME)

    if not os.path.exists(config_filename):
        log.error(f"Could not find current config: {config_filename}.")
        sys.exit(-1)

    config = configparser.ConfigParser(
        inline_comment_prefixes=("#",),
        empty_lines_in_values=False,
        defaults=Constants.CONFIGURATION_DEFAULTS,
        interpolation=configparser.ExtendedInterpolation(),
    )
    config.read(config_filename)

    for extension in valid_filepaths:
        match extension:
            case ".bvh":
                app_id = "biovision_hierarchy_data"
                mode = Mode.BVH
            case ".npz":
                app_id = "body_model_data"
                mode = Mode.BODY
            case _:  # NOTE: should not get here
                sys.exit(rr.EXTERNAL_DATA_LOADER_INCOMPATIBLE_EXIT_CODE)
        if args.application_id is not None:
            app_id = args.application_id
        rr.init(app_id, recording_id=args.recording_id)
        if args.application_id is not None:
            rr.stdout()
        else:
            rr.connect()
        set_time_from_args(args)

        for filepath in valid_filepaths[extension]:
            filename = os.path.basename(filepath)
            if args.entity_path_prefix:
                entity_path = f"{args.entity_path_prefix}/{filename}"
            else:
                entity_path = filename

            match up_axis := config.get("rerun", "up_axis", fallback="y"):
                case "y":
                    coord_system = rr.ViewCoordinates.RIGHT_HAND_Y_UP
                case "z":
                    coord_system = rr.ViewCoordinates.RIGHT_HAND_Z_UP
            rr.log("/", coord_system, static=True)

            match mode:
                case Mode.BVH:
                    log_bvh(filepath, entity_path, config)
                case Mode.BODY:
                    log_smpl_body(data_root, filepath, entity_path, config)


if __name__ == "__main__":
    main()
