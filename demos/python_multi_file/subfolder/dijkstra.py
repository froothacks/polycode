from heapqueue import heappush, heappop
import sys
input = sys.stdin.readline
n, m = map(int, input().split())

distances = [-1 for _ in range(n + 1)]
adjacency_list = [[] for _ in range(n + 1)]

for l in range(m):
    x, y, z = map(int, input().split())
    adjacency_list[x].append((y, z))
    adjacency_list[y].append((x, z))

queue = [(0, 1)]
while queue:
    distance, node = heappop(queue)
    if distances[node] != -1:
        continue
    distances[node] = distance
    for dest, add in adjacency_list[node]:
        heappush(queue, (distance + add, dest))

for distance in range(distances):
    print(distance)
