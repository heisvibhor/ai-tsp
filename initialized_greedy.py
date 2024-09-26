def initialized_greedy(distance: list[list[float]], n_points: int, start, end):
    points = []
    sorted_distance = []
    for i in range(n_points):
        to = []
        for j in range(n_points):
            if i != j:
                to.append((distance[i][j], j))
        sorted_distance.append(sorted(to, key=lambda x: x[0]))

    tour = [start, end]
    traversed = {start: True, end: True}
    left_best = next_best(sorted_distance, traversed, start)
    right_best = next_best(sorted_distance, traversed, end)
    for i in range(n_points - 2):
        if left_best[1] == right_best[1]:
            tour.append(right_best[1])
            traversed[right_best[1]] = True
            right_best = next_best(sorted_distance, traversed, right_best[1])
            left_best = next_best(sorted_distance, traversed, tour[0])
        elif left_best[0] < right_best[0]:
            tour.insert(0, left_best[1])
            traversed[left_best[1]] = True
            left_best = next_best(sorted_distance, traversed, left_best[1])
        else:
            tour.append(right_best[1])
            traversed[right_best[1]] = True
            right_best = next_best(sorted_distance, traversed, right_best[1])
    return tour


def next_best(distance, traversed, point):
    for dist, node in distance[point]:
        if traversed.get(node) is None:
            return dist, node

