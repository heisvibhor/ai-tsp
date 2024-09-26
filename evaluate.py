def evaluate( distance : list[list[float]], n_points : int, tour: list[int]):
    cost = 0
    for i in range(n_points):
        cost += distance[tour[i]][tour[i-1]]

    return cost