import matplotlib
matplotlib.use("Agg")   # ← これを一番最初に！

import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

ax.quiver(0,0,0, 1,0,0, color='r')
ax.quiver(0,0,0, 0,1,0, color='g')
ax.quiver(0,0,0, 0,0,1, color='b')

ax.set_xlabel("X")
ax.set_ylabel("Y")
ax.set_zlabel("Z")
ax.set_box_aspect([1,1,1])
ax.set_title("World Coordinate Axes")

plt.savefig("world_axes.png")
plt.close()
