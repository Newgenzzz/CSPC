import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

data = np.genfromtxt("trajectory.csv", delimiter=",", skip_header=1)
t = data[:, 0]
x = data[:, 1]
y = data[:, 2]

vx = np.gradient(x, t)
vy = np.gradient(y, t)
speed = np.sqrt(vx**2 + vy**2)

print("Mean speed:", speed.mean())
print("Max speed:", speed.max())

fig, axes = plt.subplots(1, 2, figsize=(11, 4.5))

axes[0].plot(x, y)
axes[0].set_xlabel("x (m)")
axes[0].set_ylabel("y (m)")
axes[0].set_title("Path")
axes[0].set_aspect("equal")

axes[1].plot(t, speed)
axes[1].set_xlabel("Time (s)")
axes[1].set_ylabel("Speed (m/s)")
axes[1].set_title("Speed")

fig.tight_layout()
fig.savefig("trajectory.png", dpi=150)
