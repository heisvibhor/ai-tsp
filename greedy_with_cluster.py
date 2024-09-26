import random
def greedy_with_cluster(distance: list[list[float]], points: list[int], start = -1, end = -1):
    n_points = len(points)
    if n_points == 1:
        return points
    
    sorted_distance = {}
    for i in points:
        to = []
        for j in points:
            if i != j:
                to.append((distance[i][j], j))
        sorted_distance[i] = sorted(to, key=lambda x: x[0])
    if start == -1 or end == -1:
        start, end = points[0], sorted_distance[points[0]][0][1]

    tour = [end, start]
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

    if start != -1:
        idx = tour.index(start)
    else:    
        idx = tour.index(end)
        if idx == len(tour) - 1:
            return tour
        else:
            idx -= 1
    return tour[idx:] + tour[:idx]


def next_best(distance : dict[list[int]], traversed, point):
    for dist, node in distance[point]:
        if traversed.get(node) is None:
            return dist, node

class TourCluster():
    def __init__(self, all_distance: list[list[float]], distance: list[list[float]], points: list[int], clusters, node_pairs):
        self.n_cluster = len(points)
        self.all_distance = all_distance
        self.node_pairs = node_pairs
        self.clusters = clusters
        if self.n_cluster == 1:
            return 
        
        self.sorted_distance = {}
        temp = []
        for i in points:
            to = []
            for j in points:
                if i != j:
                    to.append((distance[i][j], j))
            self.sorted_distance[i] = sorted(to, key=lambda x: x[0])
            temp.append((self.sorted_distance[i][0][0], self.sorted_distance[i][0][1], i))
        
        r = sorted(temp, key=lambda x: x[0])[0][1]
        
        r = random.randint(0,self.n_cluster -1)
        first, second = points[r], self.sorted_distance[points[r]][0][1]
        self.tour = [first, second]
        self.traversed = {first: True, second: True}
        
        pair = self.first_in_first(node_pairs[first][second], first)
        self.end = [pair[0]]
        self.start = [pair[1]]
        left_best = self.next_best_left()
        right_best = self.next_best_right()

        for i in range(self.n_cluster - 2):
            if left_best[1] == right_best[1]:
                self.tour.append(right_best[1])
                self.start.append(right_best[2])
                self.end.append(right_best[3])
                self.traversed[right_best[1]] = True
                right_best = self.next_best_right()
                left_best = self.next_best_left()
            elif left_best[0] < right_best[0]:
                self.tour.insert(0, left_best[1])
                self.end.insert(0, left_best[2])
                self.start.insert(0, left_best[3])
                self.traversed[left_best[1]] = True
                left_best = self.next_best_left()
            else:
                self.tour.append(right_best[1])
                self.start.append(right_best[2])
                self.end.append(right_best[3])
                self.traversed[right_best[1]] = True
                right_best = self.next_best_right()

        self.end.append(self.start[-1])
        self.start.insert(0, self.end[0])

    def next_best_left(self):
        point = self.tour[0]
        end = self.end[0]
        self.redefine_distance(point)
        for dist, node in self.sorted_distance[point]:
            if self.traversed.get(node) is None and (len(self.clusters[point]) == 1 or end not in self.node_pairs[point][node]):
                f = self.first_in_first(self.node_pairs[point][node], node)
                return dist, node, f[0], f[1]
            
    def next_best_right(self):
        point = self.tour[-1]
        end = self.start[-1]
        self.redefine_distance(point)
        for dist, node in self.sorted_distance[point]:
            if self.traversed.get(node) is None and (len(self.clusters[point]) == 1 or end not in self.node_pairs[point][node]):
                f = self.first_in_first(self.node_pairs[point][node], node)
                return dist, node, f[0], f[1]

    def first_in_first(self, pairs, first):
        if pairs[0] not in self.clusters[first]:
            return pairs[1], pairs[0]
        return pairs

    def interClusterDistance(self, points_1: list[int], points_2: list[int]):
        min_i = points_1[0]
        min_j = points_2[0]
        min_dist = 1000000

        for i in points_1:
            
            for j in points_2:
                if i not in self.start and i not in self.end and j not in self.end and j not in self.start and self.all_distance[i][j] < min_dist:
                    min_dist = self.all_distance[i][j]
                    min_i = i
                    min_j = j
        return min_dist, (min_i, min_j)
    def redefine_distance(self, cluster_index):
        to = []
        if len(self.clusters[cluster_index]) == 1:
            return
        for j in range(0, self.n_cluster):
            if cluster_index != j:
                
                dist, pair = self.interClusterDistance(self.clusters[cluster_index], self.clusters[j])
                self.node_pairs[cluster_index][j],  self.node_pairs[j][cluster_index] = pair, pair
                to.append((dist, j))

        self.sorted_distance[cluster_index] = sorted(to, key=lambda x: x[0])
    
