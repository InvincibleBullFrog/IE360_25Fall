import numpy as np

depts = ["GS","FS","SE","OF","FC","WC","FR","SH","UP","RE"]

centroids_before = {
    "GS": (20, 28),
    "FS": (60, 50),
    "SE": (60, 76),
    "OF": (20, 80),
    "FC": (60, 34),
    "WC": (20, 52),
    "FR": (20, 10),
    "SH": (88, 30),
    "UP": (60, 14),
    "RE": (88, 76),
}

F = np.array([
    [0,5,0,0,0,50,10,0,5,0],
    [5,0,20,0,50,0,0,0,0,5],
    [0,20,0,0,5,5,5,0,5,20],
    [0,0,0,0,5,20,0,10,0,10],
    [0,50,5,5,0,0,0,0,10,0],
    [50,0,5,20,0,0,10,5,0,5],
    [10,0,5,0,0,10,0,0,10,0],
    [0,0,0,10,0,5,0,0,5,20],
    [5,0,5,0,10,0,10,5,0,0],
    [0,5,20,10,0,5,0,20,0,0],
], float)

C = np.array([
    [0,4,2,1,2,2,2,4,2,4],
    [4,0,2,1,2,8,2,4,2,2],
    [2,2,0,1,2,4,2,4,2,2],
    [1,1,1,0,1,1,1,1,1,1],
    [2,2,2,1,0,2,2,4,2,4],
    [2,8,4,1,2,0,4,8,4,8],
    [2,2,2,1,2,4,0,4,2,2],
    [4,4,4,1,4,8,4,0,4,2],
    [2,2,2,1,2,4,2,4,0,2],
    [4,2,2,1,4,8,2,2,2,0],
], float)

def craft_score(centroids):
    n = len(depts)
    D = np.zeros((n,n))
    for i, di in enumerate(depts):
        xi, yi = centroids[di]
        for j, dj in enumerate(depts):
            xj, yj = centroids[dj]
            D[i,j] = abs(xi - xj) + abs(yi - yj)
    G = F * C * D
    return np.triu(G, k=1).sum()


before = craft_score(centroids_before)

centroids_after = centroids_before.copy()
centroids_after["GS"], centroids_after["FR"] = centroids_before["FR"], centroids_before["GS"]

after = craft_score(centroids_after)

delta = after - before
print("Before:", before)
print("After: ", after)
print("Change:", delta)