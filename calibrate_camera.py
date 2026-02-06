import sys
import numpy as np
import cv2
from pathlib import Path
import img_utils.img_utils as iu
from camera_calibration_utils import xc_to_xw, solve_pnp

world_points_path = sys.argv[1]
img_path = sys.argv[2]
intrinsics_path = sys.argv[3]
output_path = sys.argv[4]

output_path = Path(output_path)
output_path.parent.mkdir(parents=True, exist_ok=True)

world_points = np.loadtxt(world_points_path, dtype=np.float32)
intrinsics = np.loadtxt(intrinsics_path, dtype=np.float32)
# GUIで対応点を取得
img = iu.load_imgs(img_path) 
img_points, _ = iu.get_img_points_with_gui(img, 2)

ret, r_vec, t_vec = solve_pnp(world_points, img_points,  intrinsics)
r_mat, _ = cv2.Rodrigues(r_vec)
# 世界座標におけるカメラの位置を計算・保存
xc_origin_in_xw = xc_to_xw(np.zeros((3, 1)), r_mat, t_vec)
np.savetxt(output_path, xc_origin_in_xw)
print(xc_origin_in_xw)


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