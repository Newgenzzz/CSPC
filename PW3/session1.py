import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("Heart_disease_cleveland_new.csv")
print(df.shape)
print(df.head())

cols = ["age", "chol", "trestbps", "thalach"]
data = df[cols]
print(data.describe())

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for ax, c in zip(axes.flatten(), cols):
    ax.hist(data[c], bins=20)
    ax.set_xlabel(c)
    ax.set_ylabel("how often")
    ax.set_title(c)
plt.tight_layout()
plt.savefig("histograms.png", dpi=150)
plt.close()

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
for ax, c in zip(axes.flatten(), cols):
    stats.probplot(data[c], dist="norm", plot=ax)
    ax.set_title("Q-Q plot: " + c)
plt.tight_layout()
plt.savefig("qqplots.png", dpi=150)
plt.close()

for c in cols:
    W, p = stats.shapiro(data[c])
    sk = stats.skew(data[c])
    ku = stats.kurtosis(data[c])
    print(c, "W =", round(W, 4), "p =", p, "skew =", round(sk, 3), "excess kurtosis =", round(ku, 3))
    if p < 0.05:
        print("   reject H0 -> not normal")
    else:
        print("   fail to reject H0 -> normal OK")
