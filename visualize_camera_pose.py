import matplotlib.pyplot as plt
import numpy as np

def calc_camera_origin(R, t):
    return np.dot(R.T, -t)

def visualize_camera_pose(axes, length=0.5):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    for axis in axes:
        ax.quiver(
            axis["origin"][0], axis["origin"][1], axis["origin"][2], 
            axis["vector"][0], axis["vector"][1], axis["vector"][2], 
            color=axis["color"], length=length
        )

    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    ax.set_box_aspect([1,1,1])
    all_points = np.array([axis["origin"] + np.array(axis["vector"])*length for axis in axes])
    max_val = np.max(np.abs(all_points)) * 1.2  # 少し余裕を持たせる
    ax.set_xlim(-max_val, max_val)
    ax.set_ylim(-max_val, max_val)
    ax.set_zlim(-max_val, max_val)

    plt.show()

if __name__ == "__main__":
    
    world_axes = [
        {"origin": np.array([0,0,0]), "vector": np.array([1,0,0]), "color": "r" },  # X軸
        {"origin": np.array([0,0,0]), "vector": np.array([0,1,0]), "color": "g" },  # Y軸
        {"origin": np.array([0,0,0]), "vector": np.array([0,0,1]), "color": "b" },  # Z軸
    ]

    R_camera_1 = np.array(  [[ 7.04571352e-01, -7.09632859e-01, -6.44381456e-04],
                            [-1.16341770e-01, -1.14616097e-01, -9.86573739e-01],
                            [ 7.00031286e-01,  6.95186562e-01, -1.63315162e-01]]    )
    
    t_camera_1 =  np.array( [ 8.15448326, 0.87037408, 3.1269214 ] )

    R_camera_2 = np.array ( [[-0.43387278, -0.90063983, -0.02454209],
                            [-0.0543961,  -0.00100457,  0.99851893],
                            [-0.89933057,  0.43456518, -0.04855544]] )

    t_camera_2 = np.array( [ 5.52211489, 0.03038446, -3.23528489 ] )


    camera_1_origin = calc_camera_origin(R_camera_1, t_camera_1)
    camera_2_origin = calc_camera_origin(R_camera_2, t_camera_2)

    camera1_axes = [
        {"origin": camera_1_origin, "vector": R_camera_1[0], "color": "r" },  # X軸
        {"origin": camera_1_origin, "vector": R_camera_1[1], "color": "g" },  # Y軸
        {"origin": camera_1_origin, "vector": R_camera_1[2], "color": "b" },  # Z軸
        {"origin": camera_2_origin, "vector": R_camera_2[0], "color": "r" },  # X軸
        {"origin": camera_2_origin, "vector": R_camera_2[1], "color": "g" },  # Y軸
        {"origin": camera_2_origin, "vector": R_camera_2[2], "color": "b" },  # Z軸
        ]
    visualize_camera_pose(world_axes + camera1_axes)

# $env:TCL_LIBRARY = "C:\Users\naoki\.pyenv\pyenv-win\versions\3.12.0\tcl\tcl8.6" 
# $env:TK_LIBRARY  = "C:\Users\naoki\.pyenv\pyenv-win\versions\3.12.0\tcl\tk8.6"