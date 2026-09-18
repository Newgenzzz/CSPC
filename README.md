# CSPC - Computer Science for Physics and Chemistry
My coursework repository. Each practical is under PW<n>/Lab <X>/.

## Setup
Create the environment for a given lab:
conda env create -f PW<n>/Lab\ <X>/environment.yml
conda activate cspc

---

# CSPC Lab A

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
