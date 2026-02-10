import sys
import numpy as np
import cv2
from pathlib import Path
import click
import img_utils.img_utils as iu
from camera_calibration_utils import xc_to_xw, solve_pnp

@click.command
@click.option('-wp', 'world_points_path', required=True, type=str, help='対応点の世界座標系のパス')
@click.option('-in', 'intrinsics_path', required=True, type=str, help='内部パラメータのパス')
@click.option('-im', 'img_path', required=True, type=str, help='入力画像のパス')
@click.option('-o', 'output_path', required=True, type=str, help='推定結果の出力先パス（ファイル名を含む）')
def main(world_points_path, img_path, intrinsics_path, output_path):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    world_points = np.loadtxt(world_points_path, dtype=np.float32)
    intrinsics = np.loadtxt(intrinsics_path, dtype=np.float32)
    # GUIで対応点を取得
    img = iu.load_imgs(img_path) 
    img_points, _ = iu.get_img_points_with_gui(img, 2)

    ret, r_vec, t_vec = solve_pnp(world_points, img_points,  intrinsics)
    r_mat, _ = cv2.Rodrigues(r_vec)
    extrinsics = np.vstack((r_mat, t_vec.T))
    np.savetxt(output_path, extrinsics)

if __name__ == '__main__':
    main()
# print("Return value:", ret)
# print("Rotation Vector:\n", r_vec)
# print("Rotation matrix:\n", R)
# print("Translation Vector:\n", t_vec)

# object_points, img_points, rvec, tvec, camera_matrix, dist_coeffs がある場合
# projected_points, _ = cv2.projectPoints(object_points, r_vec, t_vec, intrinsics, None)
# projected_points は Nx1x2 の形なので、Nx2 に変換
# projected_points = projected_points.reshape(-1, 2)

# reprojected_img = iu.draw_points_on_img(img, projected_points)
# iu.show_imgs(reprojected_img)
# print("Projected Points:\n", projected_points)
# # 再投影誤差
# errors = np.linalg.norm(img_points - projected_points, axis=1)
# mean_error = np.mean(errors)

# print("Reprojection errors per point:", errors)
# print("Mean reprojection error:", mean_error)