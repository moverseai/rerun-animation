# NOTE: parts of this code are adapted from GANimator https://github.com/PeizhuoLi/ganimator
#   based on Holden's https://theorangeduck.com/media/uploads/other_stuff/motionsynth_code.zip
#   and from PyTorch 3D's transforms https://github.com/facebookresearch/pytorch3d/blob/main/pytorch3d/transforms/rotation_conversions.py

import re
import typing

import numpy as np

__all__ = [
    "load",
    "euler_angles_to_matrix",
]

_ROTATION_TO_ID__ = {"Xrotation": "x", "Yrotation": "y", "Zrotation": "z"}


def load(filename: str) -> typing.Tuple[
    np.ndarray,  # root position
    np.ndarray,  # joint rotations
    np.ndarray,  # joint offsets
    np.ndarray,  # joint parents
    typing.List[str],  # joint names
    str,  # rotation order
    float,  # timestep
]:
    with open(filename, "r") as f:
        i = 0
        active = -1
        end_site = False
        names = []
        orders = []
        offsets = np.array([]).reshape((0, 3))
        parents = np.array([], dtype=int)
        for line in f:
            if "HIERARCHY" in line:
                continue
            if "MOTION" in line:
                continue
            rmatch = re.match(r"ROOT (\w+:?\w+)", line)  # mixamo mod
            if rmatch:
                names.append(rmatch.group(1))
                offsets = np.append(offsets, np.array([[0, 0, 0]]), axis=0)
                parents = np.append(parents, active)
                active = len(parents) - 1
                continue
            if "{" in line:
                continue
            if "}" in line:
                if end_site:
                    end_site = False
                else:
                    active = parents[active]
                continue
            offmatch = re.match(
                r"\s*OFFSET\s+([\-\d\.e]+)\s+([\-\d\.e]+)\s+([\-\d\.e]+)", line
            )
            if offmatch:
                if not end_site:
                    offsets[active] = np.array([list(map(float, offmatch.groups()))])
                continue
            chanmatch = re.match(r"\s*CHANNELS\s+(\d+)", line)
            if chanmatch:
                channels = int(chanmatch.group(1))
                channelis = 0 if channels == 3 else 3
                channelie = 3 if channels == 3 else 6
                parts = line.split()[2 + channelis : 2 + channelie]
                if any([p not in _ROTATION_TO_ID__ for p in parts]):
                    continue
                order = "".join([_ROTATION_TO_ID__[p] for p in parts])
                orders.append(order)
                continue
            jmatch = re.match("\s*JOINT\s+(\w+:?\w+)", line)  # mixamo mod
            if jmatch:
                names.append(jmatch.group(1))
                offsets = np.append(offsets, np.array([[0, 0, 0]]), axis=0)
                parents = np.append(parents, active)
                active = len(parents) - 1
                continue
            if "End Site" in line:
                end_site = True
                continue
            fmatch = re.match("\s*Frames:\s+(\d+)", line)
            if fmatch:
                fnum = int(fmatch.group(1))
                positions = np.zeros((fnum, 3))
                rotations = np.zeros((fnum, len(names), 3))
                continue
            fmatch = re.match("\s*Frame Time:\s+([\d\.]+)", line)
            if fmatch:
                frametime = float(fmatch.group(1))
                continue
            dmatch = line.strip().split()
            if dmatch:
                data_block = np.array(list(map(float, dmatch)))
                N = len(parents)
                if channels == 3:
                    # positions[i, 0:1] = data_block[0:3]
                    positions[i] = data_block[0:3]
                    rotations[i, :] = data_block[3:].reshape(N, 3)
                elif channels == 6:
                    positions[i] = data_block[0:3]
                    rotations[i, :] = data_block.reshape(N, 6)[:, 3:6]
                elif channels == 9:
                    # positions[i, 0] = data_block[0:3]
                    positions[i] = data_block[0:3]
                    data_block = data_block[3:].reshape(N - 1, 9)
                    rotations[i, 1:] = data_block[:, 3:6]
                    # positions[i, 1:] += data_block[:, 0:3] * data_block[:, 6:9]
                else:
                    raise Exception("Too many channels! %i" % channels)
                i += 1
    order = orders[0]  # NOTE: assumes all in same order
    return positions, rotations, offsets, parents, names, order, frametime


def _axis_angle_rotation(axis: str, angle: np.ndarray) -> np.ndarray:
    """
    Return the rotation matrices for one of the rotations about an axis
    of which Euler angles describe, for each value of the angle given.

    Args:
        axis: Axis label "X" or "Y or "Z".
        angle: any shape tensor of Euler angles in radians

    Returns:
        Rotation matrices as tensor of shape (..., 3, 3).
    """

    cos = np.cos(angle)
    sin = np.sin(angle)
    one = np.ones_like(angle)
    zero = np.zeros_like(angle)

    if axis == "X":
        R_flat = (one, zero, zero, zero, cos, -sin, zero, sin, cos)
    elif axis == "Y":
        R_flat = (cos, zero, sin, zero, one, zero, -sin, zero, cos)
    elif axis == "Z":
        R_flat = (cos, -sin, zero, sin, cos, zero, zero, zero, one)
    else:
        raise ValueError("letter must be either X, Y or Z.")

    return np.stack(R_flat, -1).reshape(angle.shape + (3, 3))


def euler_angles_to_matrix(euler_angles: np.ndarray, convention: str) -> np.ndarray:
    """
    Convert rotations given as Euler angles in radians to rotation matrices.

    Args:
        euler_angles: Euler angles in radians as tensor of shape (..., 3).
        convention: Convention string of three uppercase letters from
            {"X", "Y", and "Z"}.

    Returns:
        Rotation matrices as tensor of shape (..., 3, 3).
    """
    if len(euler_angles.shape) == 0 or euler_angles.shape[-1] != 3:
        raise ValueError("Invalid input euler angles.")
    if len(convention) != 3:
        raise ValueError("Convention must have 3 letters.")
    if convention[1] in (convention[0], convention[2]):
        raise ValueError(f"Invalid convention {convention}.")
    for letter in convention:
        if letter not in ("X", "Y", "Z"):
            raise ValueError(f"Invalid letter {letter} in convention string.")
    matrices = [
        _axis_angle_rotation(c, e.squeeze())
        for c, e in zip(convention, np.dsplit(euler_angles, 3))
    ]
    return np.matmul(np.matmul(matrices[0], matrices[1]), matrices[2])
