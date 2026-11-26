"""Maximum subarray sum in 2-D: brute force, Kadane, and a genetic heuristic."""

from .brute_force import max_subarray, max_subarray_constrained, max_subarray_fixed_shape
from .genetic import best_column_selection, genetic_column_selection
from .kadane import kadane_1d, kadane_2d

__version__ = "0.2.0"

__all__ = [
    "best_column_selection",
    "genetic_column_selection",
    "kadane_1d",
    "kadane_2d",
    "max_subarray",
    "max_subarray_constrained",
    "max_subarray_fixed_shape",
]
