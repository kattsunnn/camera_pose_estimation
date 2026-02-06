import numpy as np
import cv2
import img_utils.img_utils as iu

def xc_to_xw(xc:np.ndarray, R:np.ndarray, t:np.ndarray):
    return R.T @ ( xc - t )

def xw_to_xc(xw:np.ndarray, R:np.ndarray, t:np.ndarray):
    return R @ xw + t

def solve_pnp(object_points, img_points, intrinsics, dist_coeffs=None):
    if dist_coeffs is None:
        dist_coeffs = np.zeros((5,1))

    ret, r_vec, t_vec = cv2.solvePnP(object_points, img_points, intrinsics, dist_coeffs)
    return ret, r_vec, t_vec

def reproject_points(world_points, r_vec, t_vec, intrinsics, img):
    img_points, _ = cv2.projectPoints(world_points, r_vec, t_vec, intrinsics, None)
    img_points = img_points.reshape(-1,2).astype(int)
    reprojected_img = iu.draw_points_on_img(img, img_points)
    return reprojected_img    