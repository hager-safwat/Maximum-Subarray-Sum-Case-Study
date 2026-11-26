"""Kadane's algorithm, in 1-D and extended to 2-D.

1-D: scan once, keeping the best sum of a subarray ending at the current
position; either extend the previous one or start fresh. O(n).

2-D: fix a pair of rows (top, bottom), collapse the rows between them into
one array of column sums, and run 1-D Kadane on it. There are O(R^2) row
pairs and each costs O(C), so O(R^2 * C) overall, against O(R^3 * C^3) for
the brute force.
"""


def kadane_1d(arr):
    """Maximum-sum contiguous subarray of a non-empty list.

    Returns (max_sum, start, end), inclusive indices. Works when every
    value is negative (returns the largest single element).
    """
    best_sum, best_start, best_end = arr[0], 0, 0
    cur_sum, cur_start = arr[0], 0
    for idx in range(1, len(arr)):
        if cur_sum < 0:                 # a negative prefix only hurts: restart
            cur_sum, cur_start = arr[idx], idx
        else:
            cur_sum += arr[idx]
        if cur_sum > best_sum:
            best_sum, best_start, best_end = cur_sum, cur_start, idx
    return best_sum, best_start, best_end


def kadane_2d(A):
    """Maximum-sum rectangle of matrix A in O(R^2 * C).

    Returns (max_sum, first_row, last_row, first_col, last_col), same format
    as ``brute_force.max_subarray``.
    """
    rows, cols = len(A), len(A[0])
    best = (float("-inf"), 0, 0, 0, 0)
    for top in range(rows):
        col_sums = [0] * cols
        for bottom in range(top, rows):
            for c in range(cols):
                col_sums[c] += A[bottom][c]
            s, left, right = kadane_1d(col_sums)
            if s > best[0]:
                best = (s, top, bottom, left, right)
    return best
