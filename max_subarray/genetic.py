"""Genetic-algorithm heuristic from the coursework.

What it optimises: each candidate is a binary mask over the COLUMNS of the
matrix (1 = include). Its fitness is the sum of all cells in the included
columns, over all rows. That is a relaxation of the subarray problem:
the selected columns need not be contiguous and every row is always
included. It is kept as an example of a population-based heuristic, not as
a solver for the rectangle problem (see ``kadane_2d`` for that).

Fix compared with the original notebook export: the selection, crossover
and mutation steps were indented under the early-exit ``break`` and so never
ran; they now run every generation.
"""

import numpy as np


def initial_population(population_size, n_genes, rng):
    return [rng.integers(0, 2, n_genes) for _ in range(population_size)]


def fitness(mask, matrix):
    """Sum of the cells in the selected columns (mask broadcast over rows)."""
    return float(np.sum(mask * np.asarray(matrix)))


def mutate(mask, rng):
    """Flip one random gene (returns a new array)."""
    child = mask.copy()
    point = rng.integers(len(child))
    child[point] = 1 - child[point]
    return child


def crossover(parent1, parent2, rng):
    """Single-point crossover."""
    point = rng.integers(len(parent1))
    return np.concatenate((parent1[:point], parent2[point:]))


def genetic_column_selection(matrix, population_size=10, generations=10,
                             mutation_rate=0.1, seed=0):
    """Evolve column masks with elitism, random parent choice, single-point
    crossover and bit-flip mutation.

    Returns (best_mask, best_fitness).
    """
    rng = np.random.default_rng(seed)
    n_cols = len(matrix[0])
    population = initial_population(population_size, n_cols, rng)

    for _ in range(generations):
        scores = [fitness(c, matrix) for c in population]
        best = population[int(np.argmax(scores))]
        new_population = [best]                          # elitism
        for _ in range(population_size - 1):
            p1 = population[rng.integers(population_size)]
            p2 = population[rng.integers(population_size)]
            child = crossover(p1, p2, rng)
            if rng.random() < mutation_rate:
                child = mutate(child, rng)
            new_population.append(child)
        population = new_population

    scores = [fitness(c, matrix) for c in population]
    best = population[int(np.argmax(scores))]
    return best, fitness(best, matrix)


def best_column_selection(matrix):
    """Exact optimum of the same relaxed problem: include every column whose
    total is positive. Used to check the heuristic."""
    totals = np.asarray(matrix).sum(axis=0)
    mask = (totals > 0).astype(int)
    return mask, float(totals[totals > 0].sum())
