"""
Find the City With the Smallest Number of Neighbors at a Threshold Distance
LeetCode 1334  ·  Medium  ·  (supplementary)
Group 11 — Bellman-Ford / All-Pairs

All-pairs shortest path with Floyd-Warshall (n <= 100 -> O(V^3) is fine), then
for each city count the others within distanceThreshold. Return the city with the
smallest count; ties -> the LARGEST index.

Run:  python 02-find-the-city-smallest-neighbors.py
"""

import heapq
from collections import defaultdict
from typing import List


class Solution:
    """Primary: Floyd-Warshall + per-city count."""

    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        INF = float("inf")
        dist = [[INF] * n for _ in range(n)]
        for i in range(n):
            dist[i][i] = 0
        for u, v, w in edges:
            dist[u][v] = min(dist[u][v], w)
            dist[v][u] = min(dist[v][u], w)

        for k in range(n):                       # k MUST be outermost
            for i in range(n):
                dik = dist[i][k]
                if dik == INF:
                    continue
                for j in range(n):
                    if dik + dist[k][j] < dist[i][j]:
                        dist[i][j] = dik + dist[k][j]

        best_city, best_count = -1, INF
        for i in range(n):
            cnt = sum(1 for j in range(n) if i != j and dist[i][j] <= distanceThreshold)
            if cnt <= best_count:                 # <= -> ties resolve to the larger index
                best_count = cnt
                best_city = i
        return best_city


class SolutionDijkstra:
    """Alternative: Dijkstra from every source (better on sparse / large graphs)."""

    def findTheCity(self, n: int, edges: List[List[int]], distanceThreshold: int) -> int:
        graph = defaultdict(list)
        for u, v, w in edges:
            graph[u].append((v, w))
            graph[v].append((u, w))

        def dijkstra(src: int) -> List[float]:
            dist = [float("inf")] * n
            dist[src] = 0
            heap = [(0, src)]
            while heap:
                d, u = heapq.heappop(heap)
                if d > dist[u]:
                    continue
                for v, w in graph[u]:
                    if d + w < dist[v]:
                        dist[v] = d + w
                        heapq.heappush(heap, (d + w, v))
            return dist

        best_city, best_count = -1, float("inf")
        for i in range(n):
            d = dijkstra(i)
            cnt = sum(1 for j in range(n) if i != j and d[j] <= distanceThreshold)
            if cnt <= best_count:
                best_count, best_city = cnt, i
        return best_city


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.findTheCity(4, [[0, 1, 3], [1, 2, 1], [1, 3, 4], [2, 3, 1]], 4) == 3, name
    assert solver.findTheCity(
        5, [[0, 1, 2], [0, 4, 8], [1, 2, 3], [1, 4, 2], [2, 3, 1], [3, 4, 1]], 2) == 0, name
    assert solver.findTheCity(
        6, [[0, 3, 7], [2, 4, 1], [0, 1, 5], [2, 3, 10], [1, 3, 6], [1, 2, 1]], 417) == 5, name
    assert solver.findTheCity(2, [[0, 1, 10]], 5) == 1, name
    assert solver.findTheCity(3, [[0, 1, 1], [1, 2, 1], [0, 2, 1]], 2) == 2, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionDijkstra())
