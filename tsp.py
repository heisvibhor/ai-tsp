from greedy import pure_greedy
from evaluate import evaluate
from initialized_greedy import initialized_greedy
from space_print import printer

euc_or_not = input()
n = int(input())
point = []
for i in range(n):
    line = input().strip().split(" ")
    for j in range(2):
        line[j] = float(line[j])
    point.append(line)

distance = []
for i in range(n):
    line = input().strip().split(" ")
    for j in range(n):
        line[j] = float(line[j])
    distance.append(line)

tour_1 = pure_greedy(distance, n)
best_cost = evaluate(distance, n, tour_1)

best_tour = tour_1

for i in range(n):
    for j in range(i):
        tour = initialized_greedy(distance, n, i, j)
        cost = evaluate(distance, n, tour)
        if cost < best_cost:
            printer(best_tour)
            best_tour = tour
            best_cost = cost

printer(best_tour)
