import numpy as np
from scipy.integrate import cumulative_trapezoid
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

data = np.genfromtxt("freefall.csv", delimiter = ",", skip_header = 1)
t = data[:, 0]
y = data[:, 1]

v = np.gradient(y, t)
a = np.gradient(v, t)

print("Mean acceleration:", np.mean(a))
print("Std acceleration:", a.std())

v_rec = cumulative_trapezoid(a,t,initial=0) + v[0]
y_rec = cumulative_trapezoid(v_rec,t,initial=0) + y[0]

print("Largest difference", np.max(np.abs(y_rec-y)))

fig, axes = plt.subplots(3,1,sharex=True, figsize = (8,9))

axes[0].plot(t,y)
axes[0].set_ylabel("Position (m)")

axes[1].plot(v,t)
axes[1].set_ylabel("Velocity (m/sec)")

axes[2].plot(t,a)
axes[2].axhline(-9.81, linestyle="--", color="black", label="-9.81")
axes[2].set_ylabel("Acceleration (m/s²)")
axes[2].set_xlabel("Time (s)")
axes[2].legend()

fig.tight_layout()
fig.savefig("motion.png", dpi=150)
