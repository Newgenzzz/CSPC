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
