#!/usr/bin/env python3
"""
IE 360 Fall 2025 HW8 - Student Template
Graph-Theoretic Layout Planning - Adjacency Maximization

Student Name: [Han Tian]
Student ID: [669434334]
"""

import numpy as np
import cvxpy as cp


def main():
    print("IE 360 Fall 2025 HW8 - Student Solution")
    print("=" * 70)

    # Define problem data
    n_departments = 10

    # Dimensions (length c_i, width d_i) for each department
    dimensions = {
        1: (1, 1), 2: (1, 1), 3: (1, 1), 4: (1, 1), 5: (1, 2),
        6: (2, 1), 7: (1, 2), 8: (2, 2), 9: (1, 2), 10: (3, 4)
    }

    # Weight matrix w_ij (symmetric)
    w = np.zeros((n_departments, n_departments))

    # Fill in weights from problem statement (upper triangle)
    weights_upper = [
        (1, 2, 25), (1, 3, 10), (1, 6, 15), (1, 8, 40), (1, 10, 50),
        (2, 3, 35), (2, 7, 10),
        (3, 4, 30), (3, 6, 20), (3, 10, 15),
        (4, 5, 5), (4, 8, 15), (4, 9, 25),
        (5, 9, 18),
        (6, 7, 3), (6, 8, 20),
        (7, 10, 12),
        (9, 10, 30)
    ]

    # Make weight matrix symmetric
    for i, j, weight in weights_upper:
        w[i-1, j-1] = weight
        w[j-1, i-1] = weight

    # Part a) Calculate upper bounds u_ij
    print("\nPart a) Upper Bound Calculation")
    print("-" * 70)

    u = calculate_upper_bounds(dimensions, n_departments)

    # Print upper bounds
    print("\nUpper bounds u_ij:")
    for i in range(n_departments):
        for j in range(i+1, n_departments):
            if u[i, j] > 0:
                print(f"u[{i+1},{j+1}] = {u[i, j]:.1f}")

    # Part b) Calculate perimeter requirements b_i
    print("\n\nPart b) Perimeter Requirements")
    print("-" * 70)

    b = calculate_perimeters(dimensions, n_departments)

    print("\nPerimeter requirements b_i:")
    for i in range(n_departments):
        c_i, d_i = dimensions[i+1]
        print(f"b_{i+1} = 2({c_i} + {d_i}) = {b[i]:.1f}")

    # Part c) Solve optimization model
    print("\n\nPart c) Optimization Model")
    print("-" * 70)

    optimal_value, x_optimal = solve_adjacency_model(w, u, b, n_departments)

    # Part d) Display results
    print("\n\nPart d) Results")
    print("-" * 70)
    print(f"\nOptimal objective value: {optimal_value:.4f}")

    print("\nNon-zero adjacencies (x_ij > 0.01):")
    print(f"{'Dept i':<8} {'Dept j':<8} {'x_ij':<10}")
    print("-" * 30)

    for i in range(n_departments):
        for j in range(i+1, n_departments):
            if x_optimal[i, j] > 0.01:
                print(f"{i+1:<8} {j+1:<8} {x_optimal[i, j]:<10.3f}")


def calculate_upper_bounds(dimensions, n_departments):
    """
    Calculate upper bounds u_ij based on department dimensions

    TODO: Implement the upper bound calculation according to the problem statement
    - Case 1: If neither i nor j is department 10 (Building)
    - Case 2: If one of them is department 10 (Building)
    """

    u = np.zeros((n_departments, n_departments))
    building_idx = 9  # Department 10 has index 9 (0-based indexing)

    for i in range(n_departments):
        for j in range(i+1, n_departments):
            c_i, d_i = dimensions[i+1]
            c_j, d_j = dimensions[j+1]

            # TODO: Implement Case 1 and Case 2 logic here
            # Case 1: Neither is the Building
            if i != building_idx and j != building_idx:
                u[i, j] = min(max(c_i,d_i),max(c_j,d_j))
            else:
                if i == building_idx:
                    c_nb, d_nb = c_j, d_j
                else:
                    c_nb, d_nb = c_i, d_i
                
                max_nb = max(c_nb, d_nb)
                min_nb = min(c_nb, d_nb)
                
                if max_nb in (dimensions[10][0], dimensions[10][1]):
                    u[i, j] = max(c_nb + d_nb, 
                                  max_nb,
                                  max_nb + 2 * min_nb)
                else:
                    u[i, j] = c_nb + d_nb

            u[j, i] = u[i, j]  # Make symmetric

    return u


def calculate_perimeters(dimensions, n_departments):
    """
    Calculate perimeter requirements b_i = 2(c_i + d_i)

    TODO: Implement the perimeter calculation
    """

    b = np.zeros(n_departments)

    for i in range(n_departments):
        c_i, d_i = dimensions[i+1]
        b[i] = 2 * (c_i + d_i)
    return b


def solve_adjacency_model(w, u, b, n_departments):
    """
    Solve the adjacency maximization optimization model

    TODO: Implement the CVXPY optimization model
    - Calculate normalized weights omega_ij = w_ij / u_ij
    - Define decision variable x_ij (continuous, non-negative)
    - Define objective function: maximize sum of omega_ij * x_ij
    - Add perimeter constraints: sum of adjacencies = b_i
    - Add upper bound constraints: x_ij <= u_ij
    - Solve and return optimal value and solution
    """

    # TODO: Calculate normalized weights omega_ij
    omega = np.zeros((n_departments, n_departments))
    for i in range(n_departments):
        for j in range(n_departments):
            if u[i,j] > 0:
                omega[i,j] = w[i,j] / u[i,j]
            else: 
                omega[i,j] = 0

    # TODO: Define decision variables using CVXPY
    x = cp.Variable((n_departments, n_departments), nonneg=True)

    # TODO: Define objective function
    objective = cp.Maximize(0.5 * cp.sum(cp.multiply(omega, x)))

    # TODO: Define constraints list
    constraints = []

    for i in range(n_departments):
        constraints.append(cp.sum(x[i, :]) - x[i, i] == b[i])

    for i in range(n_departments):
        for j in range(i + 1, n_departments):
            constraints.append(x[i, j] <= u[i, j])
            constraints.append(x[j, i] == x[i, j])

    # TODO: Create and solve the problem
    problem = cp.Problem(objective, constraints)

    # Try MOSEK first, fall back to ECOS if not available
    try:
        problem.solve(solver=cp.MOSEK)
    except cp.error.SolverError:
        print("MOSEK not available, using ECOS solver...")
        problem.solve(solver=cp.ECOS)

    if problem.status != cp.OPTIMAL:
        print(f"Warning: Solver status is {problem.status}")

    return problem.value, x.value


if __name__ == "__main__":
    main()
