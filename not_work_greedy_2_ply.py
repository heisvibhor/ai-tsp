
class Greedy2Ply:
    def __init__(self, distance: list[list[float]], n_points: int):
        self.distance = distance
        self.n_points = n_points

        self.sorted_distance = []
        for i in range(n_points):
            to = []
            for j in range(n_points):
                if i != j:
                    to.append((distance[i][j], j))
            self.sorted_distance.append(sorted(to, key=lambda x: x[0]))

        self.tour = [0, self.sorted_distance[0][0][1]]
        self.traversed = {0: True, self.sorted_distance[0][0][1]: True}
        left_best = self.next_best(0)
        right_best = self.next_best(self.sorted_distance[0][0][1])
        for i in range(n_points - 2):
            if left_best[1] == right_best[1]:
                self.tour.append(right_best[1])
                self.traversed[right_best[1]] = True
                right_best = self.next_2_best(right_best[1])
                left_best = self.next_2_best(self.tour[0])
            elif left_best[0] < right_best[0]:
                self.tour.insert(0, left_best[1])
                self.traversed[left_best[1]] = True
                left_best = self.next_2_best(left_best[1])
            else:
                self.tour.append(right_best[1])
                self.traversed[right_best[1]] = True
                right_best = self.next_2_best(right_best[1])
        return

    def next_best(self, point):
        for dist, node in self.sorted_distance[point]:
            if self.traversed.get(node) is None:
                return dist, node

    def next_2_best(self, point):
        best_res = self.next_best(point)
        if best_res is None:
            # Not requires
            return
        best_normal_dist, best_normal_node = best_res
        for dist, node in self.sorted_distance[point]:
            if self.traversed.get(node) is None:
                return dist, node, -1, -1
            else:
                index = self.tour.index(node)
                if index == 0 or index + 1 == len(self.tour):
                    continue
                else:
                    left = self.tour[index - 1]
                    right = self.tour[index + 1]

                    # remove that node
                    if (
                        self.distance[left][right] + dist
                        < self.distance[left][node] + self.distance[right][node]
                    ):
                        self.tour.remove(node)
                        self.traversed[node] = None
                        return dist, node, -1, -1
                    
                    res = self.common_best(point, node, index, best_normal_dist, best_normal_node)
                    if res != None:
                        print('Improvement ', res)
                        return res
                    # replace another node

    def common_best(self, point, node, node_index, best_dist, best_normal_node):
        prev_cost = self.distance[self.tour[node_index - 1]][node] + self.distance[self.tour[node_index + 1]][node] + best_dist
        best_cost = prev_cost
        best_node = 0
        for i in range(self.n_points):
            if i!=best_normal_node and i!=node and self.traversed.get(i) is None:
                new_cost = self.distance[self.tour[node_index - 1]][i] + self.distance[self.tour[node_index + 1]][i] + self.distance[point][i]
                if new_cost < best_cost:
                    best_node = i
                    best_cost = new_cost

        if best_cost < prev_cost:
            return best_cost - (prev_cost - best_dist), best_node, node, node_index
        else:
            return None