import cv2
import numpy as np

def solve_pnp(object_points, img_points, camera_matrix, dist_coeffs=None):
    if dist_coeffs is None:
        dist_coeffs = np.zeros((5,1))

    ret, rvec, tvec = cv2.solvePnP(object_points, img_points, camera_matrix, dist_coeffs)
    return ret, rvec, tvec

if __name__ == "__main__":

    import sys
    # import img_utils.img_utils as iu

    object_points = np.array(   [[-4.115, 11.86, 0],
                                [-4.115, 6.375, 0],
                                [0, 6.375, 0],
                                [4.115, 6.375, 0],], dtype=np.float32)

    img_points = np.array([ [8, 191],
                            [627, 272],
                            [640, 150],
                            [644, 113],], dtype=np.float32)

    camera_matrix = np.array([  [611, 0, 352.5],
                                [0, 610, 163.5],
                                [0, 0, 1]]
                                , dtype=np.float32)

    ret, rvec, tvec = solve_pnp(object_points, img_points, camera_matrix)
    R, _ = cv2.Rodrigues(rvec)

    print("Return value:", ret)
    print("Rotation Vector:\n", rvec)
    print("Rotation matrix:\n", R)
    print("Translation Vector:\n", tvec)

    # object_points, img_points, rvec, tvec, camera_matrix, dist_coeffs がある場合
    projected_points, _ = cv2.projectPoints(object_points, rvec, tvec, camera_matrix, None)

    # projected_points は Nx1x2 の形なので、Nx2 に変換
    projected_points = projected_points.reshape(-1, 2)
    print("Projected Points:\n", projected_points)
    # 再投影誤差
    errors = np.linalg.norm(img_points - projected_points, axis=1)
    mean_error = np.mean(errors)

    print("Reprojection errors per point:", errors)
    print("Mean reprojection error:", mean_error)

    print(3840/(2*np.pi))
    print(705/(2*np.tan(np.deg2rad(30))))
    print(327/(2*np.tan(np.deg2rad(15))))
    print("\n")
    print(1058/(2*np.tan(np.deg2rad(30))))
    print(491/(2*np.tan(np.deg2rad(15))))
    print(5760/(2*np.pi))
