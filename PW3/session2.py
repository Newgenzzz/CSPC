import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

df = pd.read_csv("Heart_disease_cleveland_new.csv")
disease = df[df["target"] == 1]["thalach"]
healthy = df[df["target"] == 0]["thalach"]

print("n disease =", len(disease), " n healthy =", len(healthy))
for name, g in [("disease", disease), ("healthy", healthy)]:
    W, p = stats.shapiro(g)
    print(name, "Shapiro W =", round(W, 4), "p =", p, "skew =", round(stats.skew(g), 3))

U, p_u = stats.mannwhitneyu(disease, healthy, alternative="two-sided")
t, p_t = stats.ttest_ind(disease, healthy)
print("Mann-Whitney U =", U, "p =", p_u)
print("t-test t =", round(t, 3), "p =", p_t)
print("median disease =", disease.median(), " median healthy =", healthy.median())

means = []
sems = []
for name, g in [("disease", disease), ("healthy", healthy)]:
    m = g.mean()
    se = g.std(ddof=1) / np.sqrt(len(g))
    means.append(m)
    sems.append(se)
    print(name, "mean =", round(m, 2), "SEM =", round(se, 2), "95% CI = [", round(m - 2 * se, 2), ",", round(m + 2 * se, 2), "]")

plt.figure(figsize=(5, 5))
plt.errorbar([0, 1], means, yerr=[2 * s for s in sems], fmt="o", capsize=8)
plt.xticks([0, 1], ["disease", "healthy"])
plt.xlim(-0.5, 1.5)
plt.ylabel("mean thalach (bpm)")
plt.title("Mean max heart rate, error bars = 95% CI")
plt.tight_layout()
plt.savefig("thalach_means.png", dpi=150)
plt.close()

r, p_r = stats.pearsonr(df["age"], df["thalach"])
rho, p_rho = stats.spearmanr(df["age"], df["thalach"])
print("Pearson r =", round(r, 3), "p =", p_r)
print("Spearman rho =", round(rho, 3), "p =", p_rho)

plt.figure(figsize=(6, 5))
plt.scatter(df["age"], df["thalach"], s=15)
slope, intercept = np.polyfit(df["age"], df["thalach"], 1)
xs = np.array([df["age"].min(), df["age"].max()])
plt.plot(xs, slope * xs + intercept, color="red")
plt.xlabel("age")
plt.ylabel("thalach")
plt.title("thalach vs age, r = " + str(round(r, 2)))
plt.tight_layout()
plt.savefig("age_thalach.png", dpi=150)
plt.close()

ch = pd.read_csv("chemicals_cancer.csv")
print(ch.shape)
print(ch.head())

for c in ["benzene", "cadmium"]:
    r, p = stats.pearsonr(ch[c], ch["malignancy"])
    print("naive", c, "r =", round(r, 3), "p =", p)

print("cadmium vs pollution_index r =", round(stats.pearsonr(ch["cadmium"], ch["pollution_index"])[0], 3))
print("benzene vs pollution_index r =", round(stats.pearsonr(ch["benzene"], ch["pollution_index"])[0], 3))
print("pollution_index vs malignancy r =", round(stats.pearsonr(ch["pollution_index"], ch["malignancy"])[0], 3))

for lo, hi in [(40, 60), (45, 55)]:
    sub = ch[(ch["pollution_index"] > lo) & (ch["pollution_index"] < hi)]
    print("band", lo, "-", hi, "size =", len(sub))
    for c in ["benzene", "cadmium"]:
        r, p = stats.pearsonr(sub[c], sub["malignancy"])
        print("   ", c, "r =", round(r, 3), "p =", p)
    print("    cadmium vs pollution_index inside band r =", round(stats.pearsonr(sub["cadmium"], sub["pollution_index"])[0], 3))

band = ch[(ch["pollution_index"] > 45) & (ch["pollution_index"] < 55)]

A = np.column_stack([np.ones(len(ch)), ch["pollution_index"]])
def residual(y):
    coef = np.linalg.lstsq(A, y, rcond=None)[0]
    return y - A @ coef
for c in ["benzene", "cadmium"]:
    r, p = stats.pearsonr(residual(ch[c].values), residual(ch["malignancy"].values))
    print("partial", c, "controlling pollution_index r =", round(r, 3), "p =", p)

fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes[0, 0].scatter(ch["benzene"], ch["malignancy"], s=5)
axes[0, 0].set_title("all patients: benzene")
axes[0, 1].scatter(ch["cadmium"], ch["malignancy"], s=5)
axes[0, 1].set_title("all patients: cadmium")
axes[1, 0].scatter(band["benzene"], band["malignancy"], s=8)
axes[1, 0].set_title("pollution 45-55: benzene")
axes[1, 1].scatter(band["cadmium"], band["malignancy"], s=8)
axes[1, 1].set_title("pollution 45-55: cadmium")
for ax in axes.flatten():
    ax.set_ylabel("malignancy")
plt.tight_layout()
plt.savefig("chemicals.png", dpi=150)
plt.close()

props = df["target"].value_counts(normalize=True)
H = -(props * np.log2(props)).sum()
print(props)
print("entropy of target =", round(H, 4), "bits (max 1)")
sp = df["sex"].value_counts(normalize=True)
print(sp)
print("entropy of sex =", round(-(sp * np.log2(sp)).sum(), 4), "bits")
