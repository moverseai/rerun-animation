# NOTE this code is mostly a numpy adaptation of the corresponding code in the smplx package https://github.com/vchoutas/smplx

import typing

import numpy as np

__all__ = [
    "calc_shaped_vertices",
    "calc_landmarks",
    "calc_pose_offsets",
    "traverse_kinematic_chain",
    "skinning",
    "rodrigues",
    "SMPL_JOINT_NAMES",
    "append_missing_rotations",
]

SMPL_JOINT_NAMES = [
    "pelvis",
    "left_hip",
    "right_hip",
    "spine1",
    "left_knee",
    "right_knee",
    "spine2",
    "left_ankle",
    "right_ankle",
    "spine3",
    "left_foot",
    "right_foot",
    "neck",
    "left_collar",
    "right_collar",
    "head",
    "left_shoulder",
    "right_shoulder",
    "left_elbow",
    "right_elbow",
    "left_wrist",
    "right_wrist",
    "left_hand",
    "right_hand",
]


def calc_shaped_vertices(
    betas: np.ndarray,
    shape_blendshapes: np.ndarray,
) -> np.ndarray:
    shape_blendshapes = shape_blendshapes[..., : betas.shape[-1]]
    shape_offets = np.einsum("vcb,b->vc", shape_blendshapes, betas)
    return shape_offets


def calc_landmarks(
    regressor: np.ndarray,
    vertices: np.ndarray,
) -> np.ndarray:
    return np.einsum("jv,vc->jc", regressor, vertices)


def calc_pose_offsets(
    blendshapes: np.ndarray,
    rotations: np.ndarray,  # includes global root which is skipped
) -> np.ndarray:
    identity = np.eye(3, dtype=blendshapes.dtype)
    features = rotations[1:] - identity
    offsets = np.einsum("vcp,p->vc", blendshapes, features.ravel())
    return offsets


def rodrigues(axisangle: np.ndarray) -> np.ndarray:
    T = axisangle.shape[0]
    angle = np.linalg.norm(axisangle.reshape(-1, 3), ord=2, axis=-1) + 1e-8
    rot_dir = axisangle.reshape(-1, 3) / angle[:, np.newaxis]

    cos = np.cos(angle)[:, np.newaxis, np.newaxis]
    sin = np.sin(angle)[:, np.newaxis, np.newaxis]

    rx, ry, rz = np.split(rot_dir, 3, axis=1)
    K = np.zeros((3, 3), dtype=np.float32)

    zeros = np.zeros_like(rx)
    K = np.concatenate(
        [zeros, -rz, ry, rz, zeros, -rx, -ry, rx, zeros], axis=1
    ).reshape((-1, 3, 3))

    ident = np.eye(3, dtype=np.float32)[np.newaxis]
    rot_mat = ident + sin * K + (1 - cos) * (K @ K)
    return rot_mat.reshape(T, -1, 3, 3)


def traverse_kinematic_chain(
    rotations: np.ndarray,
    joints: np.ndarray,
    parents: np.ndarray,
) -> np.ndarray:
    J = joints.shape[0]
    joints = joints[..., np.newaxis]

    rel_joints = joints.copy()
    rel_joints[1:] -= joints[parents[1:]]

    transforms_mat = np.tile(np.eye(4, dtype=np.float32), (J, 1, 1))
    transforms_mat[:, :3, :3] = rotations
    transforms_mat[:, :3, 3:4] = rel_joints

    transform_chain = [transforms_mat[0]]
    for c, p in enumerate(parents[1:], start=1):
        curr_res = transform_chain[p] @ transforms_mat[c]
        transform_chain.append(curr_res)
    transforms = np.stack(transform_chain, axis=0)

    posed_joints = transforms[:, :3, 3]

    transformed_joints = transforms[:, :3, :3] @ joints  # + transforms[..., :3, 3:4]
    relative_transforms = transforms.copy()
    relative_transforms[..., :3, 3] -= transformed_joints[..., 0]

    return posed_joints, relative_transforms


def skinning(
    weights: np.ndarray,
    vertices: np.ndarray,
    relative_transforms: np.ndarray,
    normals: np.ndarray,
) -> np.ndarray:
    blended_transforms = weights @ relative_transforms.reshape(-1, 16)
    blended_transforms = blended_transforms.reshape(-1, 4, 4)
    posed_vertices = (blended_transforms[:, :3, :3] @ vertices[..., np.newaxis])[
        ..., 0
    ] + blended_transforms[:, :3, 3]
    posed_normals = blended_transforms[:, :3, :3] @ normals[..., np.newaxis]
    return posed_vertices, posed_normals


def append_missing_rotations(rotations: np.ndarray, max_joints: int = 24) -> np.ndarray:
    T, J, _, __ = rotations.shape
    if J < max_joints:
        remainder = max_joints - J
        identities = np.tile(np.eye(3, dtype=np.float32), (T, remainder, 1, 1))
        rotations = np.concatenate([rotations, identities], axis=1)
    return rotations


def ensure_pose_shape(pose: np.ndarray, type: str) -> np.ndarray:
    T = pose.shape[0]
    match type:
        case "axisangle":
            pose = pose.reshape(T, -1, 3)
        case "rotmat":
            pose = pose.reshape(T, -1, 3, 3)
        case _:
            raise ValueError(f"Pose representation {type} not supported.")
    return pose


def ensure_rotmat(pose: np.ndarray, type: str) -> np.ndarray:
    if type == "axisangle":
        return rodrigues(pose)
    else:
        return pose
