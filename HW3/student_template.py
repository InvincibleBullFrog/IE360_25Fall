#!/usr/bin/env python3
"""
IE 360 Homework 3 - Student Template
Fall 2025

Author: [Han Tian]
Student ID: [669434334]
"""

import numpy as np
from math import sqrt

def main():
    print("IE 360 Homework 3 - Numerical Solver")
    print("=" * 50)
    
    # Question 1: From-To Matrix Calculation
    print("\nQuestion 1: From-To Matrix")
    print("-" * 30)
    
    from_to_matrix = calculate_from_to_matrix()
    print_from_to_matrix(from_to_matrix)
    
    # Question 2: Flow Dominance Calculation  
    print("\nQuestion 2: Flow Dominance")
    print("-" * 30)
    
    flow_results = calculate_flow_dominance()
    print_flow_dominance_results(flow_results)

def calculate_from_to_matrix():
    """Calculate the from-to matrix for the semiconductor facility"""
    
    # Wafer data from Table 1 (wafer_id, routing_sequence, wafers_per_month, wafers_per_batch)
    wafer_data = [
        (1, "3-7-11-14", 120000, 60),
        (2, "2-5-8-12", 180000, 90),
        (3, "7-2-9-11-4", 75000, 25),
        (4, "2-4-9-12-14", 90000, 30),
        (5, "4-8-6-10-12", 300000, 100),
        (6, "8-14-2-4-13", 60000, 15),
        (7, "8-6-10-14", 250000, 50),
        (8, "7-2-1-8-4-10-12", 150000, 75),
        (9, "4-7-8-2", 80000, 40),
        (10, "6-9-6-10", 60000, 30),
        (11, "8-4", 280000, 140),
        (12, "13-9-1-6-10-9", 120000, 40),
        (13, "13-1", 140000, 70),
        (14, "2-4-7-9-13", 160000, 80),
        (15, "2-9-10-14-13-1", 180000, 60),
        (16, "13-9-1-14", 70000, 35),
        (17, "8-9-14-4-3-2", 90000, 45),
        (18, "14", 100000, 50),
        (19, "1-3-6-8-11", 110000, 55),
        (20, "5-7-9-11-13-14", 140000, 35)
    ]
    
    # Initialize the from-to matrix (14 stations)
    from_to_matrix = np.zeros((14, 14), dtype=int)
    
    # TODO: Implement the from-to matrix calculation
    # For each wafer type:
    # 1. Calculate flow = monthly_volume / batch_size  
    # 2. Parse the routing sequence
    # 3. Add flows between consecutive stations in the route
    
    return from_to_matrix

def calculate_flow_dominance():
    """Calculate flow dominance measure for the given 6x6 matrix"""
    
    # From-to matrix from Question 2 of the homework
    flow_matrix = np.array([
        [ 0, 35, 15,  5, 25,  0],  # Row A
        [20,  0, 40, 30, 15, 10],  # Row B
        [10, 25,  0, 35, 20, 15],  # Row C
        [ 5, 15, 10,  0,  8, 25],  # Row D
        [15, 20, 25, 30,  0, 12],  # Row E
        [ 0,  8, 12, 20, 18,  0],  # Row F
    ])
    
    M = 6  # Matrix size
    
    # TODO: Implement flow dominance calculation
    # 1. Extract off-diagonal flows
    # 2. Calculate mean flow and sum of squares
    # 3. Calculate coefficient of variation f
    # 4. Calculate theoretical bounds f_U and f_L
    # 5. Calculate flow dominance measure f'
    
    return {
        'M': M,
        'flow_matrix': flow_matrix,
        'off_diagonal_flows': [],
        'sum_flows': 0,
        'sum_squares': 0,
        'f_bar': 0,
        'f': 0,
        'f_U': 0,
        'f_L': 0,
        'f_prime': 0
    }

def print_from_to_matrix(matrix):
    """Print the from-to matrix in a readable format"""
    print("\nFrom-To Matrix:")
    print("=" * 60)
    
    # Print column headers
    print("From\\To", end="")
    for j in range(matrix.shape[1]):
        print(f"{j+1:>6}", end="")
    print()
    
    print("-" * 60)
    
    # Print matrix rows
    for i in range(matrix.shape[0]):
        print(f"  {i+1:>2}   ", end="")
        for j in range(matrix.shape[1]):
            print(f"{matrix[i][j]:>6}", end="")
        print()

def print_flow_dominance_results(results):
    """Print the flow dominance calculation results"""
    print("\nFlow Dominance Calculation Results:")
    print("=" * 50)
    
    print(f"Matrix size (M): {results['M']}")
    print(f"Off-diagonal flows: {results['off_diagonal_flows']}")
    print(f"Sum of flows: {results['sum_flows']}")
    print(f"Sum of squares: {results['sum_squares']}")
    print(f"Mean flow (f̄): {results['f_bar']:.3f}")
    print(f"Coefficient of variation (f): {results['f']:.3f}")
    print(f"Upper bound (f_U): {results['f_U']:.3f}")
    print(f"Lower bound (f_L): {results['f_L']:.3f}")
    print(f"Flow dominance measure (f'): {results['f_prime']:.3f}")
    
    print("\nInterpretation:")
    if results['f_prime'] > 0.8:
        print("Strong flow dominance - suitable for process layout")
    elif results['f_prime'] > 0.5:
        print("Moderate flow dominance - mixed layout considerations")  
    else:
        print("Weak flow dominance - product layout may be better")

if __name__ == "__main__":
    main()