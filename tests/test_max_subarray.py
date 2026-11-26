"""Tests: known answer, agreement between methods, and edge cases."""

import random

import numpy as np
import pytest

from max_subarray import (
    best_column_selection,
    genetic_column_selection,
    kadane_1d,
    kadane_2d,
    max_subarray,
    max_subarray_constrained,
    max_subarray_fixed_shape,
)

A = [[1, 2, -1, -4, -20],
     [-8, -3, 4, 2, 1],
     [3, 8, 10, 1, 3],
     [-4, -1, 1, 7, -6]]


def rect_sum(M, r0, r1, c0, c1):
    return sum(M[r][c] for r in range(r0, r1 + 1) for c in range(c0, c1 + 1))


def test_coursework_matrix_known_answer():
    """Sum 29 at rows 1-3, columns 1-3, as in the coursework report."""
    assert max_subarray(A) == (29, 1, 3, 1, 3)
    assert kadane_2d(A) == (29, 1, 3, 1, 3)


@pytest.mark.parametrize("seed", range(40))
def test_kadane_matches_brute_force_on_random_matrices(seed):
    rng = random.Random(seed)
    rows, cols = rng.randint(1, 6), rng.randint(1, 6)
    M = [[rng.randint(-9, 9) for _ in range(cols)] for _ in range(rows)]
    b, k = max_subarray(M), kadane_2d(M)
    assert b[0] == k[0]
    # The rectangle Kadane returns really has the sum it claims.
    assert rect_sum(M, *k[1:]) == k[0]


def test_all_negative_matrix_returns_largest_cell():
    M = [[-5, -2], [-7, -3]]
    assert max_subarray(M)[0] == -2
    assert kadane_2d(M)[0] == -2


def test_single_cell():
    assert kadane_2d([[4]]) == (4, 0, 0, 0, 0)
    assert max_subarray([[-4]]) == (-4, 0, 0, 0, 0)


def test_kadane_1d():
    assert kadane_1d([-2, 1, -3, 4, -1, 2, 1, -5, 4]) == (6, 3, 6)
    assert kadane_1d([-3, -1, -2]) == (-1, 1, 1)


def test_constrained_uses_area_not_shape():
    """K = L = 2 allows any rectangle of 4 cells (2x2, 1x4, 4x1)."""
    s, r0, r1, c0, c1 = max_subarray_constrained(A, 2, 2)
    assert (r1 - r0 + 1) * (c1 - c0 + 1) == 4
    assert rect_sum(A, r0, r1, c0, c1) == s
    # It can never be worse than the strict 2 x 2 version.
    assert s >= max_subarray_fixed_shape(A, 2, 2)[0]


def test_fixed_shape_matches_exhaustive_check():
    s, r0, r1, c0, c1 = max_subarray_fixed_shape(A, 2, 2)
    assert (r1 - r0, c1 - c0) == (1, 1)
    best = max(rect_sum(A, i, i + 1, j, j + 1) for i in range(3) for j in range(4))
    assert s == best == 19


def test_constrained_with_impossible_area():
    assert max_subarray_constrained([[1, 2]], 3, 3)[0] == float("-inf")


def test_genetic_never_worse_than_its_initial_best_and_bounded_by_optimum():
    _, exact = best_column_selection(A)
    for seed in range(5):
        mask, score = genetic_column_selection(A, population_size=20, generations=30, seed=seed)
        assert score <= exact
        assert score == pytest.approx(float(np.sum(mask * np.asarray(A))))


def test_genetic_finds_optimum_with_enough_generations():
    _, exact = best_column_selection(A)
    _, score = genetic_column_selection(A, population_size=30, generations=50, seed=0)
    assert score == exact


def test_cli_runs(capsys):
    from max_subarray.__main__ import main

    main()
    out = capsys.readouterr().out
    assert "sum   29" in out
