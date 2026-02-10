import cv2
import numpy as np
import img_utils.img_utils as iu


R_mat = np.array([
    [1,0,0],
    [0,1,0],
    [0,0,1],
], dtype=np.float32)

R_vec, _ = cv2.Rodrigues(R_mat)
R_mat, _ = cv2.Rodrigues(R_vec)

def reproject_points(world_points, r_vec, t_vec, intrinsics, img):
    img_points, _ = cv2.projectPoints(world_points, r_vec, t_vec, intrinsics, None)
    img_points = img_points.reshape(-1,2).astype(int)
    breakpoint()
    reprojected_img = iu.draw_points_on_img(img, img_points)
    return reprojected_img    

if __name__ == "__main__":

    import click
    from camera_calibration_utils import xc_to_xw

    @click.command
    @iu.prepare_io_path
    @click.option('-w', 'world_points_path', required=True,
                  type=click.Path(exists=True, readable=True))
    @click.option('-in', 'intrinsics_path', required=True,
                  type=click.Path(exists=True, readable=True))
    @click.option('-ex', 'extrinsics_path', required=True,
                  type=click.Path(exists=True, readable=True))
    def main(input_path, output_path, world_points_path, intrinsics_path, extrinsics_path):
        img = iu.load_imgs(input_path)
        world_points = np.loadtxt(world_points_path)
        intrinsics = np.loadtxt(intrinsics_path)
        extrinsics = np.loadtxt(extrinsics_path)
        r_mat = extrinsics[:3, :]
        r_vec, _ = cv2.Rodrigues(r_mat.T)
        t_vec = extrinsics[3, :]
        xc_origin = np.array([0,0,0])
        xc_origin_in_xw = xc_to_xw(xc_origin, R_mat, t_vec)
        print(xc_origin_in_xw)
        # breakpoint()
        # reprojected_img = reproject_points(world_points, r_vec, t_vec, intrinsics, img)
        # iu.show_imgs(reprojected_img)
    
    main()