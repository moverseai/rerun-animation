import numpy as np
from packaging.version import Version

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
import os
import pickle

import trimesh

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="""

    """
    )
    parser.add_argument("--data_root", type=str, required=True)
    parser.add_argument("--output_folder", type=str, default=".")
    args = parser.parse_args()

    out_folder = args.output_folder
    if not os.path.exists(out_folder):
        os.makedirs(out_folder)

    data_root = args.data_root
    for gender_in, gender_out in zip(
        ["neutral", "m", "f"], ["NEUTRAL", "MALE", "FEMALE"]
    ):
        # SMPL
        data_files = glob.glob(
            os.path.join(data_root, f"**/basicmodel_{gender_in}*.pkl"), recursive=True
        )
        data_file = data_files[0]
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

        np.savez_compressed(
            os.path.join(out_folder, f"SMPL_{gender_out}.npz"),
            shape_blendshapes=shape_blendshapes,
            pose_blendshapes=pose_blendshapes,
            regressor=regressor,
            template=template,
            weights=weights,
            faces=faces,
            parents=parents,
            normals=mesh.vertex_normals,
        )
        # SMPL-H
        data_files = glob.glob(
            os.path.join(data_root, f"**/**/{gender_out.lower()}/model.npz"),
            recursive=True,
        )
        data_file = data_files[0]
        body_data = np.load(data_file)
        shape_blendshapes = np.ascontiguousarray(
            body_data["shapedirs"].astype(np.float32)
        )
        pose_blendshapes = np.ascontiguousarray(
            body_data["posedirs"].astype(np.float32)
        )
        regressor = np.ascontiguousarray(body_data["J_regressor"].astype(np.float32))
        template = np.ascontiguousarray(body_data["v_template"].astype(np.float32))
        weights = np.ascontiguousarray(body_data["weights"].astype(np.float32))
        faces = np.ascontiguousarray(body_data["f"].astype(np.int32))
        parents = np.ascontiguousarray(body_data["kintree_table"].astype(np.int32))[0]
        mesh = trimesh.Trimesh(
            vertices=template, faces=faces.astype(np.int64), process=False
        )

        np.savez_compressed(
            os.path.join(out_folder, f"SMPLH_{gender_out}.npz"),
            shape_blendshapes=shape_blendshapes,
            pose_blendshapes=pose_blendshapes,
            regressor=regressor,
            template=template,
            weights=weights,
            faces=faces,
            parents=parents,
            normals=mesh.vertex_normals,
        )
