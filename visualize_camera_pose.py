import matplotlib.pyplot as plt
import numpy as np
from camera_calibration_utils import xc_to_xw

def draw_tennis_court(ax, color="white", lw=1.5):
    # テニスコートの寸法 (m)
    half_length = 23.77 / 2  # 全長の半分 (11.885)
    half_width_double = 10.97 / 2  # ダブルス幅の半分 (5.485)
    half_width_single = 8.23 / 2   # シングルス幅の半分 (4.115)
    service_line_dist = 6.40       # ネットからのサービスラインまでの距離

    # ラインを描画するヘルパー関数
    def plot_line(p1, p2):
        ax.plot([p1[0], p2[0]], [p1[1], p2[1]], [p1[2], p2[2]], color=color, linewidth=lw, alpha=0.7)

    # 1. 外枠（ダブルスサイドラインとベースライン）
    # 四隅の点
    corners = [
        [-half_width_double, -half_length, 0],
        [ half_width_double, -half_length, 0],
        [ half_width_double,  half_length, 0],
        [-half_width_double,  half_length, 0]
    ]
    for i in range(4):
        plot_line(corners[i], corners[(i+1)%4])

    # 2. シングルスサイドライン
    plot_line([-half_width_single, -half_length, 0], [-half_width_single,  half_length, 0])
    plot_line([ half_width_single, -half_length, 0], [ half_width_single,  half_length, 0])

    # 3. サービスライン
    plot_line([-half_width_single, -service_line_dist, 0], [ half_width_single, -service_line_dist, 0])
    plot_line([-half_width_single,  service_line_dist, 0], [ half_width_single,  service_line_dist, 0])

    # 4. センターサービスライン
    plot_line([0, -service_line_dist, 0], [0, service_line_dist, 0])

    # 5. ネット（簡易表示：高さ0.914mの線を引く）
    plot_line([-half_width_double, 0, 0], [half_width_double, 0, 0]) # 地面のネットライン
    # オプション：ネットの高さを表現したい場合
    # ax.plot([-half_width_double, half_width_double], [0, 0], [0.914, 0.914], color=color, linestyle="--", alpha=0.5)

def visualize_camera_pose(axes, length=0.5):
    fig = plt.figure(figsize=(10, 10))
    ax = fig.add_subplot(111, projection='3d')
    draw_tennis_court(ax, color="green")
    # 全ポイントの座標を格納するリスト
    points = []

    for axis in axes:
        # 起点
        o = np.array(axis["origin"]).flatten()
        # 終点 (ベクトル方向)
        v = o + np.array(axis["vector"]).flatten() * length
        
        ax.quiver(
            o[0], o[1], o[2],  
            axis["vector"][0], axis["vector"][1], axis["vector"][2],  
            color=axis["color"], length=length
        )
        
        # 範囲計算用に起点と終点を保存
        points.append(o)
        points.append(v)

    # numpy配列に変換 [N, 3]
    points = np.array(points)
    
    # 各軸の最小・最大を取得
    min_xyz = points.min(axis=0)
    max_xyz = points.max(axis=0)
    
    # 少し余白を持たせる (10%程度)
    padding = (max_xyz - min_xyz) * 0.1
    min_xyz -= padding
    max_xyz += padding

    ranges = max_xyz - min_xyz
    ax.set_box_aspect(ranges)
    # 軸のラベル
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Z")
    # 各軸の描画範囲を設定
    ax.set_xlim(min_xyz[0], max_xyz[0])
    ax.set_ylim(min_xyz[1], max_xyz[1])
    ax.set_zlim(min_xyz[2], max_xyz[2])
    # ax.view_init(elev=0, azim=0, roll=0)
    ax.view_init(elev=90, azim=-90, roll=-90)
    plt.show()

def create_axes(r_mat, t_vec):
    cam_origin = xc_to_xw(np.zeros((3, 1)), r_mat, t_vec)
    axes = [
        {"origin": cam_origin, "vector": r_mat[0], "color": "r" },  # X軸
        {"origin": cam_origin, "vector": r_mat[1], "color": "g" },  # Y軸
        {"origin": cam_origin, "vector": r_mat[2], "color": "b" },  # Z軸
    ]
    return axes

from pathlib import Path
def get_file_paths(dir_path: str, pattern: str) :
    target_dir = Path(dir_path)
    if not target_dir.exists():
        raise FileNotFoundError()
    file_paths = sorted([str(p) for p in target_dir.glob(pattern)])
    print(file_paths)
    return file_paths

if __name__ == "__main__":
    
    import sys    
    from camera_calibration_utils import load_extrinsics_file

    extrinsics_dir = sys.argv[1]

    axes = []
    # 世界座標系の定義
    r_mat_world = np.array( [[1,0,0],
                            [0,1,0],
                            [0,0,1]], dtype=np.float32)
    t_vec_world = np.zeros((3,1))
    world_origin_axes = create_axes(r_mat_world, t_vec_world)
    axes.extend(world_origin_axes)

    extrinsics_paths = get_file_paths(extrinsics_dir, "*extrinsics*")
    for extrinsics_path in extrinsics_paths: 
        r_mat, t_vec = load_extrinsics_file(extrinsics_path) 
        camera_axes = create_axes(r_mat, t_vec)
        axes.extend(camera_axes)

    visualize_camera_pose(axes, 1)

# 実行前の準備（パスの指定）
# $env:TCL_LIBRARY = "C:\Users\naoki\.pyenv\pyenv-win\versions\3.12.0\tcl\tcl8.6" 
# $env:TK_LIBRARY  = "C:\Users\naoki\.pyenv\pyenv-win\versions\3.12.0\tcl\tk8.6"

