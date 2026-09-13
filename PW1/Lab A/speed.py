import time
from decay import simulate, simulate_loop

N0 = 200_000
lam = 0.4

# Time the pure-Python loop version
start = time.perf_counter()
simulate_loop(N0, lam)
loop_time = time.perf_counter() - start

# Time the vectorised NumPy version
start = time.perf_counter()
simulate(N0, lam)
numpy_time = time.perf_counter() - start

print(f"simulate_loop: {loop_time:.4f} s")
print(f"simulate:      {numpy_time:.4f} s")
print(f"NumPy version is {loop_time / numpy_time:.1f}x faster")
