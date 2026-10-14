# CSPC - Computer Science for Physics and Chemistry
My coursework repository. Each practical is under PW<n>/Lab <X>/.

## Setup
Create the environment for a given lab:
```bash
conda env create -f "PW<n>/Lab <X>/environment.yml"
conda activate cspc
```
---

# CSPC LABS

## Testing Questions (PW1 / Lab A)

**Which pytest tool checks that an error is raised?**
`pytest.raises()` - used as a context manager. The test passes only if the code inside the `with` block raises the specified exception

**Which pytest tool compares floating-point values with a tolerance?**
`pytest.approx()` — wraps the expected value so that `==` allows a relative
or absolute tolerance instead of requiring exact equality, which is needed since floats (and simulation averages) rarely match exactly

## PW1 — Lab A

**What I built:**
- Two additional pytest tests for decay.py (negative-rate validation and statistical
  agreement with the analytical decay law), plus a speed.py script comparing the
  pure-Python loop and NumPy versions of the simulation.

**Speed comparison (loop vs NumPy):**
- loop : 1.7135 s
- numpy : 0.0002 s
- speed-up: 10119.5x faster

**Tests:** all passing? yes

**Conclusion:**
- I was surprised how big the difference was. Going from checking every atom
  one by one in a loop to letting NumPy handle all 200,000 at once made it run
  about 10,000 times faster. The loop version spends most of its time in
  Python's interpreter, re-checking one atom at a time, while the NumPy version
  does the same work with a single vectorised call to `rng.binomial()` per time
  step, which runs in optimized C code instead. This showed me why vectorized
  operations matter so much for large simulations instead of relying on manual
  loops.


## PW1 — Lab B

**Data:** `decay_observed.csv` contains 40 measurements of particle count vs. time,
starting at N₀ ≈ 5000 counts at t=0 and decaying to below 20 counts by t≈19.5,
consistent with radioactive/exponential decay.

**Comparison to the analytical law:** The observed data closely tracks the analytical
curve N(t) = N₀·e^(−λt) with λ = 0.3 across the full time range. Early and mid-range
points match within a few percent, while later points show larger relative deviations — expected, since low counts are more
sensitive to statistical/measurement noise. Overall, the observed decay follows the
analytical exponential law well.

**Snakemake pipeline:** The pipeline automates the full plotting workflow — reading
`decay_observed.csv`, computing the analytical curve, and generating `figure.png` —
with a single command instead of manual steps.

## PW 2 — Lab A

**The Noise Problem Explanation:** My gravity measurement was way off of the real numerical value of g which was around -9,8. My calculation is around -8,58. Differentiating compares neighbouring measurements that are only 0.1 s apart, so a small position error gets divided by a tiny time step (and by it again for the second derivative), which magnifies the noise enormously, while the position data itself is only off by millimetres.

**Report about the largest difference:** The recovered position differs from the original by at most about 0.78 m, because integration sums the noisy acceleration values and their random errors partly cancel, so integration suppresses noise where differentiation amplified it.

**Integrating back:** integrating the noisy acceleration twice recovered the position to within about 0.78 m of the original. Integration sums values, so random errors partly cancel and the noise is suppressed.
![motion](PW2/Lab%20A/motion.png)
**Bonus:** the tracked path is a figure-eight; the speed computed from np.gradient on x and y has mean about 23.7 m/s but shows small jitter caused by differentiating noisy positions.
![bonus](PW2/Lab%20A/trajectory.png)
## PW2 --- Lab B

### Part 2: how the three methods compared

**2A, f(x) = (x-3)^2 + 1, from x0 = 0.** Gradient descent (lr = 0.1), Newton and SLSQP all reach x = 3. The function is convex with one minimum, so the methods agree.

**2B, g(x) = x^4 - 3x^2 + x + 5.** g has two minima (x = -1.30, the global one, and x = 1.13, a local one) and a maximum at x = 0.17.

| Start | Gradient descent (lr = 0.01) | Newton | SLSQP |
|---|---|---|---|
| x0 = 0 | -1.3008 (global min) | 0.1699 (maximum, g'' = -5.65) | -1.3009 (global min) |
| x0 = 2 | 1.1309 (local min) | 1.1309 (minimum, g'' = 9.35) | -1.3006 (global min) |

- The methods agree on the easy function but not on g.
- From x0 = 0, Newton landed on a maximum, not a minimum. It solves g'(x) = 0, which a maximum also satisfies, so the sign of g'' has to be checked.
- The starting point changed the result. From x0 = 0 the slope points left, toward the global minimum. From x0 = 2 gradient descent and Newton stay in the right-hand valley and stop at the local minimum. SLSQP took a large first step and jumped to the global minimum.

### Part 3: reaction rate

Fitted rate constant k = __ (SLSQP, bounds (0, 5), start 0.5). The fitted curve passes through the data (`kinetics.png`).

### Part 4: equilibrium composition (K = 15.6)

Newton and SLSQP agree: x = 0.6638.

| Species | Amount (mol) |
|---|---|
| H2 | 0.336 |
| I2 | 0.336 |
| HI | 1.328 |

Plot: `equilibrium.png`.

### Part 5 (bonus): titration

Equivalence point at V = __ mL, where the slope of the pH curve is largest (`titration.png`).
# PW3 - Data, Distributions, Testing, and Causation

## Dataset 1 - Heart Disease (Cleveland)

Source: Cleveland heart disease dataset, UCI Machine Learning Repository (also distributed on Kaggle).
303 patients, 14 columns. No missing values. Columns used: `age`, `chol`, `trestbps`, `thalach`, and `target` (1 = heart disease, 0 = healthy).

Files:
- `session1.py` - loading, distributions, normality checks
- `histograms.png` - histogram of each variable
- `qqplots.png` - normal Q-Q plot of each variable

## Session 1 - Characterise the data

### 1. Loading

`pd.read_csv("heart.csv")` gives a DataFrame of shape (303, 14). The four continuous columns were isolated with `df[["age", "chol", "trestbps", "thalach"]]`.

| variable | mean | std | min | max |
|---|---|---|---|---|
| age | 54.4 | 9.0 | 29 | 77 |
| chol | 246.7 | 51.8 | 126 | 564 |
| trestbps | 131.7 | 17.6 | 94 | 200 |
| thalach | 149.6 | 22.9 | 71 | 202 |

### 2. Shape of each variable

![histograms](histograms.png)

- **age**: wide and uneven. Most patients are between 40 and 70, with the tallest bar around 58-60 and a longer tail toward young ages. It does not form a clean bell.
- **chol**: skewed to the right. Most values sit between 200 and 300, with a few very high ones (up to 564) that stretch the right tail.
- **trestbps**: a hump around 120-140 with a tail to the right up to 200. The bars look jagged because blood pressure is recorded in rounded values (multiples of 10).
- **thalach**: skewed to the left. Most values are between 140 and 170, with a tail down to about 70.

### 3. Are they normally distributed?

I used two checks: a Q-Q plot against a normal distribution (graphical) and the Shapiro-Wilk test (numerical, H0: "the data is normal"). I also computed skewness and excess kurtosis to see how the data departs from normal. A p-value below 0.05 rejects H0, so the variable is declared not normal.

![qq plots](qqplots.png)

| variable | Shapiro-Wilk W | p-value | skew | excess kurtosis | verdict |
|---|---|---|---|---|---|
| age | 0.9865 | 0.0061 | -0.21 | -0.54 | not normal (mildly) |
| chol | 0.9473 | 5.9e-9 | 1.13 | 4.40 | not normal |
| trestbps | 0.9665 | 1.8e-6 | 0.70 | 0.85 | not normal |
| thalach | 0.9765 | 7.0e-5 | -0.54 | -0.07 | not normal |

Reasoning for each variable:

- **age**: the Q-Q points follow the line fairly well in the middle but bend away at both ends. Shapiro-Wilk rejects normality (p = 0.006), but skew and kurtosis are small, so the departure is mild (a flat-topped distribution rather than a bell).
- **chol**: the clearest case. The Q-Q plot curves upward at the top, with one extreme point at 564, and the data has a strong right skew (1.13) and heavy tails (excess kurtosis 4.4). Shapiro-Wilk gives p of about 6e-9.
- **trestbps**: the Q-Q plot lies above the line at high values (right skew) and shows steps caused by the rounded readings. Shapiro-Wilk rejects normality (p = 1.8e-6).
- **thalach**: the Q-Q plot falls below the line at both ends, and the left skew (-0.54) is visible in the histogram. Shapiro-Wilk rejects normality (p = 7e-5).

Conclusion: none of the four variables passes the normality check. With about 300 points Shapiro-Wilk is sensitive to small departures, so age and thalach are only mildly non-normal, while chol is strongly non-normal. I will not assume normality in Session 2: for comparing the two thalach groups I will use a non-parametric test (Mann-Whitney U) instead of the t-test.

## Session 2 - Draw conclusions

Files: `session2.py`, `thalach_means.png`, `age_thalach.png`, `chemicals.png`, `chemicals_cancer.csv`.

### 4. Is the effect real? (thalach, disease vs healthy)

Question: do heart-disease patients reach a different maximum heart rate than healthy ones?

Normality inside each group (Shapiro-Wilk):

| group | n | p-value | skew | verdict |
|---|---|---|---|---|
| disease | 139 | 0.35 | -0.31 | normal OK |
| healthy | 164 | 0.0005 | -0.69 | not normal |

The healthy group fails the normality check, so I chose the non-parametric **Mann-Whitney U test** (two-sided, because I care about a difference in either direction). H0: the two groups have the same distribution of thalach.

- Mann-Whitney U = 5806.5, p = 1.9e-13
- Median thalach: disease 142, healthy 161
- For comparison, the two-sample t-test gives t = -7.96, p = 3.5e-14, which leads to the same conclusion.

Conclusion: p is far below 0.05, so I reject H0. Heart-disease patients reach a clearly lower maximum heart rate than healthy patients, and this is very unlikely to be chance. (The test shows the groups differ, not why.)

Mean and uncertainty (standard error of the mean, 95% CI = mean +/- 2 x SEM):

| group | mean thalach | SEM | 95% CI |
|---|---|---|---|
| disease | 139.3 | 1.9 | [135.4, 143.1] |
| healthy | 158.4 | 1.5 | [155.4, 161.4] |

![means](thalach_means.png)

The two intervals do not overlap (the gap is about 19 bpm), so the picture agrees with the Mann-Whitney result.

### 5. Do age and thalach move together?

![age vs thalach](age_thalach.png)

Pearson r = -0.39 (p = 1.1e-12) and Spearman rho = -0.39 (p = 1.5e-12), so the result does not depend on normality. Maximum heart rate tends to fall as age rises, a moderate negative relationship. It is far from perfect, since the scatter around the line is wide.

## Dataset 2 - Chemical-exposure mystery (synthetic)

1000 patients: `benzene`, `cadmium`, `pollution_index`, `age`, `malignancy`.

### 6. Naive analysis

| chemical | Pearson r with malignancy |
|---|---|
| benzene | 0.385 |
| cadmium | 0.880 |

Taken at face value, **cadmium** looks like the cause, because its association is much stronger.

### 7. Look again: controlling for pollution index

Suspected third variable: `pollution_index`. Cadmium is almost perfectly correlated with it (r = 0.98), and the pollution index is itself strongly correlated with malignancy (r = 0.90). Benzene is almost unrelated to it (r = 0.05). So pollution could be driving both cadmium and malignancy.

Method: restrict to patients with a similar pollution index and recompute the correlations inside that group.

| subset | n | r(benzene, malignancy) | r(cadmium, malignancy) |
|---|---|---|---|
| all patients | 1000 | 0.385 | 0.880 |
| pollution 40-60 | 199 | 0.702 | 0.316 |
| pollution 45-55 | 94 | 0.658 | -0.040 (p = 0.70) |

A wide band (40-60) still lets the pollution index vary a lot, and cadmium follows it inside the band (r = 0.77), so some of the confounding is left. In the narrower band (45-55) cadmium's association disappears (r = -0.04, p = 0.70), while benzene stays strong.

As a check, I removed the linear effect of the pollution index from both variables and correlated the leftovers (partial correlation): benzene r = 0.755, cadmium r = 0.013 (p = 0.69).

![chemicals](chemicals.png)

Conclusion: the strong link between cadmium and malignancy came from the pollution index, which drives both. Once pollution is held roughly fixed, cadmium shows no association, so it only looked guilty. **Benzene** keeps (and even strengthens) its association, so benzene is the chemical that actually drives malignancy. This follows the "compare like with like" idea from the lecture. Strictly, a randomized experiment would be needed for full proof, but here the evidence points clearly to benzene.

### Bonus - how unpredictable is a category?

Proportions and entropy H = -sum(p log2 p), in bits (maximum 1 bit for two categories):

| column | proportions | entropy |
|---|---|---|
| target | 0.541 (healthy) / 0.459 (disease) | 0.995 bits |
| sex | 0.680 (male) / 0.320 (female) | 0.905 bits |

`target` is almost perfectly balanced, so it is nearly as hard to guess as a fair coin. `sex` is more lopsided, so guessing "male" is right about two times out of three.
