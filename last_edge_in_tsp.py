def cluster(distance, n):
    clusters = [{i} for i in range(n)]
    distances = []

    for i in range(n):
        for j in range(i + 1, n):
            distances.append((distance[i][j], i, j))

    distances = sorted(distances)

    index = 0
    s = 0
    edges = []
    while len(clusters) > 10:
        (d, i, j) = distances[index]
        idx_i = find_index(clusters, i)
        idx_j = find_index(clusters, j)

        if idx_i != idx_j:
            s += d
            clusters[idx_i] = clusters[idx_i].union(clusters[idx_j])
            clusters.pop(idx_j)
            edges.append((i,j))

        index += 1
    
    edges.pop(0)
    return edges


def find_index(clusters: list[set[int]], node: int):
    for i in range(len(clusters)):
        if node in clusters[i]:
            return i