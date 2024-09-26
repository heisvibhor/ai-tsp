from cluster import cluster
from greedy_with_cluster import greedy_with_cluster, TourCluster

def tsp(distances: list[list[int]], n_points: int):
    n_cluster = int(n_points**0.5)
    clusters = cluster(distances, n_points, n_cluster)
    print(clusters)
    cluster_distance = [[0 for i in range(n_cluster)] for j in range(n_cluster)]
    cluster_close_nodes = [[(0, 0) for i in range(n_cluster)] for j in range(n_cluster)]

    for i in range(n_cluster):
        for j in range(i + 1, n_cluster):
            cluster_distance[i][j], cluster_close_nodes[i][j] = interClusterDistance(distances, clusters[i], clusters[j])
            cluster_distance[j][i], cluster_close_nodes[j][i] = cluster_distance[i][j], cluster_close_nodes[i][j]
        # clusters[i] = greedy_with_cluster(distances, clusters[i])

    cluster_representation = [i for i in range(n_cluster)]
    cl = TourCluster(distances, cluster_distance, cluster_representation, clusters, cluster_close_nodes)
    tour_set = []
    tour = []
    for i in range(n_cluster):
        cluster_index = cl.tour[i]
        if i == 0:
            var = greedy_with_cluster(distances, clusters[cluster_index], end = cl.end[i])
        elif i == n_cluster -1:
            var = greedy_with_cluster(distances, clusters[cluster_index], start = cl.start[i])
        else:
            var = greedy_with_cluster(distances, clusters[cluster_index], end = cl.end[i], start = cl.start[i])
        tour_set.append(var)
        tour += var
    print(cl.tour)
    print(cl.start)
    print(cl.end)
    cluster_tour = cl.tour
    print(cluster_tour)
    print('Tour', tour)

    return tour

    

    cluster_1 = []
    cluster_2 = [[] for i in range(n_cluster)]
    start = []
    for i in range(0, n_cluster):
        prev_near = cluster_close_nodes[cluster_tour[i]][cluster_tour[i-1]]
        if prev_near[1] not in clusters[cluster_tour[i]]:
            prev_near = prev_near[1], prev_near[0]
        idx = clusters[cluster_tour[i]].index(prev_near[1])

        cluster_2[i] = (clusters[cluster_tour[i]])
        print(prev_near, end = ',')
    print(cluster_2)
    return 

    cluster_a = []
    cluster_b = []
    print('Hoi')
    for i in range(0, n_cluster):
        prev_near = cluster_close_nodes[cluster_tour[i]][cluster_tour[(i+1)%n_cluster]]
        if prev_near[1] not in cluster_2[i]:
            prev_near = prev_near[1], prev_near[0]
        idx = cluster_2[i].index(prev_near[1])

        cluster_a.append(cluster_2[i][idx + 1: ])
        cluster_b.append(cluster_2[i][: idx +1])
        # cluster_2[-1].reverse()
        print(prev_near, end=',')

    print('')
    print(cluster_2)
    print(cluster_b)
    print(cluster_a)

    tour_1 = []
    tour_2 = []
    for i in range(n_cluster):
        tour_1 += cluster_b[i]
        tour_2 += cluster_a[i]
    tour_2.reverse()
    tour_1 += tour_2
    return tour_1    


def interClusterDistance(distances: list[list[int]], points_1: list[int], points_2: list[int]):
    min_i = points_1[0]
    min_j = points_2[0]
    min_dist = distances[min_i][min_j]

    for i in points_1:
        for j in points_2:
            if distances[i][j] < min_dist:
                min_dist = distances[i][j]
                min_i = i
                min_j = j
    return min_dist, (min_i, min_j)