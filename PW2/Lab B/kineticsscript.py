"""
PW2 Lab B Part 3 -- fit a reaction's rate constant to measured data.

A first-order reaction decays as  C(t) = C0 * exp(-k*t).  You have noisy
concentration-vs-time measurements; find the k that best matches them.
Complete the TODOs. Run:  python kinetics.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# TODO 1: read kinetics.csv (columns time, concentration) into arrays t, C.
#         Set C0 = the first concentration.
data = np.genfromtxt("kinetics.csv", delimiter=",", names=True)
t = data["time"]
C = data["concentration"]
C0 = C[0]

# TODO 2: write total_error(k) = sum of (measured - C0*exp(-k*t))^2.
#         This is the "how bad" number: small when the model matches the data.
def total_error(k):
    return np.sum((C - C0*np.exp(-k*t))**2)

# TODO 3: minimise total_error with scipy.optimize.minimize (method "SLSQP",
#         bounds [(0, 5)], start x0=0.5). Print the fitted k.
res = minimize(lambda v: total_error(v[0]), [0.5], method="SLSQP", bounds=[(0, 5)])
k_fit = res.x[0]
print("fitted k =", round(k_fit, 5))

# TODO 4: plot the measured data (points) and your fitted curve (line) together.
#         Save as kinetics.png.
tt = np.linspace(t.min(), t.max(), 300)
plt.figure(figsize=(7, 5))
plt.plot(t, C, "o", label="measured")
plt.plot(tt, C0*np.exp(-k_fit*tt), "-", label="fit, k = " + str(round(k_fit, 4)))
plt.xlabel("time")
plt.ylabel("concentration")
plt.legend()
plt.grid(True)
plt.savefig("kinetics.png", dpi=150)

