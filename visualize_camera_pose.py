import matplotlib.pyplot as plt
import numpy as np

# $env:TCL_LIBRARY = "C:\Users\naoki\.pyenv\pyenv-win\versions\3.12.0\tcl\tcl8.6" >> $env:TK_LIBRARY  = "C:\Users\naoki\.pyenv\pyenv-win\versions\3.12.0\tcl\tk8.6"

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

    R = np.array(   [[ 7.04571352e-01, -7.09632859e-01, -6.44381456e-04],
                    [-1.16341770e-01, -1.14616097e-01, -9.86573739e-01],
                    [ 7.00031286e-01,  6.95186562e-01, -1.63315162e-01]]    )
    
    t =  np.array( [ 8.15448326, 0.87037408, 3.1269214 ] )

    camera1_origin = calc_camera_origin(R, t)

    camera1_axes = [
        {"origin": camera1_origin, "vector": R[0], "color": "r" },  # X軸
        {"origin": camera1_origin, "vector": R[1], "color": "g" },  # Y軸
        {"origin": camera1_origin, "vector": R[2], "color": "b" },  # Z軸
    ]

    visualize_camera_pose(world_axes + camera1_axes)
