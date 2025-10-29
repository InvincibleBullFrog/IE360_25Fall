import cvxpy as cp
import numpy as np

D = np.array([
    [0, 6, 3, 3, 2, 4, 3, 2, 1, 6],
    [6, 0, 3, 3, 4, 2, 3, 4, 5, 0],
    [3, 3, 0, 4, 5, 1, 2, 5, 2, 3],
    [3, 3, 4, 0, 3, 3, 4, 3, 2, 3],
    [2, 4, 5, 3, 0, 6, 3, 0, 3, 4],
    [4, 2, 1, 3, 6, 0, 3, 6, 3, 2],
    [3, 3, 2, 4, 3, 3, 0, 3, 4, 3],
    [2, 4, 5, 3, 0, 6, 3, 0, 3, 4],
    [1, 5, 2, 2, 3, 3, 4, 3, 0, 5],
    [6, 0, 3, 3, 4, 2, 3, 4, 5, 0]
], dtype=float)
n = D.shape[0]
P = 2

x = cp.Variable((n, n), boolean=True)   # assignment vars
y = cp.Variable(n, boolean=True)        # medoid open vars

obj = cp.Minimize(cp.sum(cp.multiply(D, x)))

cons = []

for i in range(n):
    cons += [cp.sum(x[i, :]) == 1]
for i in range(n):
    for j in range(n):
        cons += [x[i, j] <= y[j]]

cons += [cp.sum(y) == P]

prob = cp.Problem(obj, cons)
prob.solve()

print("Objective:", prob.value)
print("Chosen medoids (y=1):", [j+1 for j in range(n) if y.value[j] > 0.5])
assign = [np.argwhere(x.value[i] > 0.5).flatten()[0]+1 for i in range(n)]
print("Assigned medoid for each part:", assign)