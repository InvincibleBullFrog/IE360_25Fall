import cvxpy as cp
import numpy as np

C=60
K=5
t=np.array([12,8,15,18,10,14,20,16,12,22],dtype=float)
J=10
P=[(1,3),(1,4),(2,4),(2,6),(3,5),(4,7),(5,7),(6,8),(7,9),(8,9),(9,10)]

x=cp.Variable((J,K),boolean=True)
y=cp.Variable(K,boolean=True)

rules=[]

for j in range(J):
    rules+=[cp.sum(x[j,:])==1]
for k in range(K):
    rules+=[t@x[:,k]<=C*y[k]]
for k in range(K):
    rules+=[x[:,k]<=y[k]]

kvec=np.arange(1,K+1,dtype=float)

for (i,j) in P:
    rules += [kvec@x[i-1,:] <= kvec@x[j-1,:]]

cost=np.arange(1,K+1,dtype=float)

objective=cp.Minimize(cost@y)

prob=cp.Problem(objective,rules)
prob.solve(solver=cp.MOSEK)

print("Status:",prob.status)
print("Objective:",round(prob.value,1))

used=[k+1 for k in range(K) if y.value[k]>0.5]
print(f"Stations used:,{used}, count:{len(used)}")

for k in range(K):
    tasks_here=[j+1 for j in range(J) if x.value[j,k]>0.5]
    time_here=sum(t[j-1] for j in tasks_here)
    print(f"Station {k+1}: tasks {tasks_here}, total time {time_here}")