"""Brute-force solutions to the 2-D maximum subarray sum problem.

A "subarray" of a matrix is a contiguous rectangle of cells, given by its
first and last row and its first and last column. The brute force tries every
rectangle and sums its cells directly: O(R^2 * C^2) rectangles, each summed
in O(R * C), so O(R^3 * C^3) overall. Slow, but obviously correct, which
makes it the reference the faster methods are tested against.
"""


def max_subarray(A):
    """Maximum-sum rectangle of matrix A (list of equal-length lists).

    Returns
    -------
    (max_sum, first_row, last_row, first_col, last_col)
        Indices are inclusive and 0-based. Ties keep the first rectangle
        found in row-major order of its top-left corner.
    """
    rows, cols = len(A), len(A[0])
    best = (float("-inf"), 0, 0, 0, 0)
    for i in range(rows):                     # first row
        for j in range(cols):                 # first column
            for k in range(i, rows):          # last row
                for m in range(j, cols):      # last column
                    s = sum(A[r][c] for r in range(i, k + 1) for c in range(j, m + 1))
                    if s > best[0]:
                        best = (s, i, k, j, m)
    return best


def max_subarray_constrained(A, K, L):
    """Maximum-sum rectangle whose AREA equals K * L cells.

    This follows the coursework formulation, which constrains the number of
    cells rather than the exact shape: for K = L = 2, rectangles of shape
    2 x 2, 1 x 4 and 4 x 1 are all allowed. Use ``exact_shape=True`` in
    ``max_subarray_fixed_shape`` for the strict K x L version.

    Returns (max_sum, first_row, last_row, first_col, last_col), or
    (-inf, 0, 0, 0, 0) if no rectangle has that area.
    """
    rows, cols = len(A), len(A[0])
    best = (float("-inf"), 0, 0, 0, 0)
    for i in range(rows):
        for j in range(cols):
            for k in range(i, rows):
                for m in range(j, cols):
                    if (k - i + 1) * (m - j + 1) != K * L:
                        continue
                    s = sum(A[r][c] for r in range(i, k + 1) for c in range(j, m + 1))
                    if s > best[0]:
                        best = (s, i, k, j, m)
    return best


def max_subarray_fixed_shape(A, K, L):
    """Maximum-sum rectangle of exactly K rows and L columns."""
    rows, cols = len(A), len(A[0])
    best = (float("-inf"), 0, 0, 0, 0)
    for i in range(rows - K + 1):
        for j in range(cols - L + 1):
            s = sum(A[r][c] for r in range(i, i + K) for c in range(j, j + L))
            if s > best[0]:
                best = (s, i, i + K - 1, j, j + L - 1)
    return best
