import typing

import numpy as np


def forward_kinematics(
    rotation: np.ndarray,  # [B/T, J, 3, 3]
    position: np.ndarray,  # [B/T, 3]
    offset: np.ndarray,  # [J, 3]
    parents: np.ndarray,  # [B/T, J]
) -> typing.Tuple[np.ndarray, np.ndarray]:  # ( [B/T, J, 3], [B/T, J, 3, 3] )
    joints = np.empty(rotation.shape[:-1])
    joints[..., 0, :] = position.copy()
    # offset = offset[:, ..., np.newaxis]
    global_rotation = rotation.copy()
    if (
        parents.shape[-1] == offset.shape[0]
    ):  # NOTE: to support using the same parents everywhere
        parents = parents[1:]
    for current_idx, parent_idx in enumerate(
        parents, start=1
    ):  # NOTE: assumes parents exclude root
        joints[..., current_idx, :] = np.einsum(
            "brc,c -> br", global_rotation[..., parent_idx, :, :], offset[current_idx]
        )
        global_rotation[..., current_idx, :, :] = np.matmul(
            global_rotation[..., parent_idx, :, :].copy(),
            rotation[..., current_idx, :, :].copy(),
        )
        joints[..., current_idx, :] += joints[..., parent_idx, :]
    return joints, global_rotation
