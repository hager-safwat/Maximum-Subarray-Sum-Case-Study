# Maximum Subarray Sum: Case Study (2-D)

[![tests](https://github.com/hager-safwat/Maximum-Subarray-Sum-Case-Study/actions/workflows/tests.yml/badge.svg)](https://github.com/hager-safwat/Maximum-Subarray-Sum-Case-Study/actions/workflows/tests.yml)
![python](https://img.shields.io/badge/python-3.10%2B-blue)

An Advanced Algorithms coursework project on the **2-D maximum subarray sum**
problem: find the rectangle of contiguous cells in a matrix whose sum is
largest. The project compares several approaches and their time complexity.

## Approaches

| Approach | Module | Complexity | Notes |
|---|---|---|---|
| Brute force | `brute_force.max_subarray` | O(R³ C³) | tries every rectangle and sums it directly; the reference |
| Constrained (area K·L) | `brute_force.max_subarray_constrained` | O(R³ C³) | coursework formulation: the rectangle must contain K·L cells |
| Fixed shape K × L | `brute_force.max_subarray_fixed_shape` | O(R C K L) | strict version: exactly K rows and L columns |
| Kadane 2-D | `kadane.kadane_2d` | O(R² C) | fix two rows, collapse them into column sums, run 1-D Kadane |
| Genetic heuristic | `genetic.genetic_column_selection` | O(G P C R) | population-based search over column masks (see below) |

**Note on the constrained version.** The coursework constrains the *area*,
not the *shape*: with K = L = 2, a 1 × 4 strip is allowed as well as a
2 × 2 block. On the coursework matrix this gives 22 (a 1 × 4 strip) against
19 for the best true 2 × 2 block. Both versions are provided.

**Note on the genetic heuristic.** Each candidate is a binary mask over the
columns, and its fitness is the sum of the selected columns over all rows. It
is a relaxation of the rectangle problem (columns need not be contiguous and
every row is included), kept as an example of a population-based heuristic.
Its exact optimum (keep every column with a positive total) is computed too,
so the heuristic can be checked.

## Run it

```bash
git clone https://github.com/hager-safwat/Maximum-Subarray-Sum-Case-Study.git
cd Maximum-Subarray-Sum-Case-Study
pip install -e .
python -m max_subarray
```

Output on the coursework matrix:

```
Coursework matrix A (4 x 5)
  brute force                sum   29   rows 1-3   cols 1-3
  Kadane 2-D                 sum   29   rows 1-3   cols 1-3
  area = 2*2 (coursework)    sum   22   rows 2-2   cols 0-3
  exact shape 2 x 2          sum   19   rows 1-2   cols 1-2

Genetic heuristic (column selection, a relaxed problem)
  GA best mask [0, 1, 1, 1, 0]  fitness 26
  exact optimum [0, 1, 1, 1, 0]  fitness 26
```

It then times brute force against Kadane on random n × n matrices. On one
run (2-core cloud machine), n = 20 took 0.185 s with brute force and
0.005 s with Kadane, and the gap grows quickly with n, as the complexities
predict.

## Tests

```bash
pip install -e ".[dev]"
pytest -v
```

50 tests, including:

- the known answer for the coursework matrix (sum 29, rows 1 to 3, columns
  1 to 3, as in the report);
- Kadane against brute force on 40 random matrices of random size, checking
  that the returned rectangle really has the claimed sum;
- edge cases: all-negative matrices, a single cell, an impossible area;
- the genetic heuristic never exceeds the exact optimum of its relaxed
  problem, and reaches it with enough generations.

Every push and pull request runs `ruff` and the tests on Python 3.10 and 3.12.

## Fixes compared with the original notebook export

- The first matrix literal was missing a comma between two rows, so the
  script crashed on its first line. Fixed.
- In the genetic algorithm, selection, crossover and mutation were indented
  under the early-exit `break` and never ran, so the population never
  evolved. Fixed, and the random generator is now seeded.

## Files

- `max_subarray/`: the implementations and a command-line entry point.
- `tests/`: pytest suite.
- `explain_the_approaches-2.pdf`: diagrams of the five approaches.
- `Advanced Algorithm Reoprt.pages`: full report (Apple Pages format).

Joint coursework project completed with a team.
