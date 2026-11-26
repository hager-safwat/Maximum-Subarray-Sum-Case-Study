"""Run every approach on the coursework matrix and time brute force vs Kadane.

    python -m max_subarray
"""

import random
import time

from . import (
    best_column_selection,
    genetic_column_selection,
    kadane_2d,
    max_subarray,
    max_subarray_constrained,
    max_subarray_fixed_shape,
)

A = [[1, 2, -1, -4, -20],
     [-8, -3, 4, 2, 1],
     [3, 8, 10, 1, 3],
     [-4, -1, 1, 7, -6]]


def fmt(result):
    s, r0, r1, c0, c1 = result
    return f"sum {s:>4}   rows {r0}-{r1}   cols {c0}-{c1}"


def main():
    print("Coursework matrix A (4 x 5)")
    print(f"  brute force                {fmt(max_subarray(A))}")
    print(f"  Kadane 2-D                 {fmt(kadane_2d(A))}")
    print(f"  area = 2*2 (coursework)    {fmt(max_subarray_constrained(A, 2, 2))}")
    print(f"  exact shape 2 x 2          {fmt(max_subarray_fixed_shape(A, 2, 2))}")

    mask, score = genetic_column_selection(A, population_size=10, generations=10)
    exact_mask, exact_score = best_column_selection(A)
    print("\nGenetic heuristic (column selection, a relaxed problem)")
    print(f"  GA best mask {mask.tolist()}  fitness {score:.0f}")
    print(f"  exact optimum {exact_mask.tolist()}  fitness {exact_score:.0f}")

    print("\nRuntime on random n x n integer matrices (seconds, one run each)")
    print(f"  {'n':>3}  {'brute force':>12}  {'Kadane 2-D':>12}")
    rng = random.Random(0)
    for n in (5, 10, 15, 20):
        M = [[rng.randint(-10, 10) for _ in range(n)] for _ in range(n)]
        t0 = time.perf_counter()
        b = max_subarray(M)
        t1 = time.perf_counter()
        k = kadane_2d(M)
        t2 = time.perf_counter()
        assert b[0] == k[0]
        print(f"  {n:>3}  {t1 - t0:>12.4f}  {t2 - t1:>12.5f}")


if __name__ == "__main__":
    main()
