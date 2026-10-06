"""
PW2 Lab B Part 5 (bonus) -- find a titration's equivalence point.

titration.csv holds a titration curve: pH versus the volume of base added.
The equivalence point is the volume where the pH changes fastest (the steep
jump). Numerically, that is where the SLOPE of the pH curve is largest.
Run:  python titration.py
"""
import numpy as np
import matplotlib.pyplot as plt

# TODO 1: read titration.csv (columns volume_base, pH) into arrays V, pH.
data = np.genfromtxt("titration.csv", delimiter=",", names=True)
V = data["volume_base"]
pH = data["pH"]

slope = np.gradient(pH, V)
i = np.argmax(slope)
V_eq = V[i]
# TODO 2: compute the slope of the pH curve with np.gradient(pH, V), and find
#         the volume where that slope is largest (np.argmax). That is the
#         equivalence point. Print it.
print("equivalence point volume =", V_eq)
print("pH there =", pH[i])
# TODO 3: make two plots side by side: (left) pH vs volume with a line at the
#         equivalence point; (right) the slope vs volume, showing it peaks
#         at the equivalence point. Save as titration.png.
fig, ax = plt.subplots(1, 2, figsize=(11, 4.5))
ax[0].plot(V, pH)
ax[0].axvline(V_eq, color="k", linestyle="--", label="equivalence = " + str(round(V_eq, 2)))
ax[0].set_xlabel("volume of base")
ax[0].set_ylabel("pH")
ax[0].legend()
ax[0].grid(True)
ax[1].plot(V, slope)
ax[1].axvline(V_eq, color="k", linestyle="--")
ax[1].set_xlabel("volume of base")
ax[1].set_ylabel("dpH/dV")
ax[1].grid(True)
plt.tight_layout()
plt.savefig("titration.png", dpi=150)

