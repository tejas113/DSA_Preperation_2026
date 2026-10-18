"""
Min Cost to Connect All Points  ·  LeetCode 1584  ·  Medium
Group 12 — Minimum Spanning Tree

MST of the COMPLETE graph on the points, edge weight = Manhattan distance.
Prim fits a complete graph: grow one tree from a heap, always add the cheapest
edge to a point not yet in the tree.

Run:  python 01-min-cost-to-connect-all-points.py
"""

import heapq
from typing import List


class Solution:
    """Primary: Prim with a min-heap."""

    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        if n <= 1:
            return 0

        def dist(i: int, j: int) -> int:
            return abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])

        seen = {0}
        heap = [(dist(0, j), j) for j in range(1, n)]
        heapq.heapify(heap)
        total = 0

        while len(seen) < n:
            w, u = heapq.heappop(heap)
            if u in seen:
                continue
            seen.add(u)
            total += w
            for v in range(n):
                if v not in seen:
                    heapq.heappush(heap, (dist(u, v), v))

        return total


class SolutionPrimNoHeap:
    """Alternative: Prim with a min_dist array, no heap -- O(n^2), best constant."""

    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        INF = float("inf")
        min_dist = [INF] * n
        min_dist[0] = 0
        in_tree = [False] * n
        total = 0

        for _ in range(n):
            u = min((v for v in range(n) if not in_tree[v]), key=lambda v: min_dist[v])
            in_tree[u] = True
            total += min_dist[u]
            for v in range(n):
                if not in_tree[v]:
                    d = abs(points[u][0] - points[v][0]) + abs(points[u][1] - points[v][1])
                    if d < min_dist[v]:
                        min_dist[v] = d
        return total


class SolutionKruskal:
    """Alternative: Kruskal -- build all n^2 edges, sort, Union-Find."""

    def minCostConnectPoints(self, points: List[List[int]]) -> int:
        n = len(points)
        edges = []
        for i in range(n):
            for j in range(i + 1, n):
                w = abs(points[i][0] - points[j][0]) + abs(points[i][1] - points[j][1])
                edges.append((w, i, j))
        edges.sort()

        parent = list(range(n))

        def find(x):
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        total, used = 0, 0
        for w, i, j in edges:
            ri, rj = find(i), find(j)
            if ri != rj:
                parent[ri] = rj
                total += w
                used += 1
                if used == n - 1:
                    break
        return total


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.minCostConnectPoints([[0, 0], [2, 2], [3, 10], [5, 2], [7, 0]]) == 20, name
    assert solver.minCostConnectPoints([[3, 12], [-2, 5], [-4, 1]]) == 18, name
    assert solver.minCostConnectPoints([[0, 0]]) == 0, name
    assert solver.minCostConnectPoints([[0, 0], [1, 1]]) == 2, name
    assert solver.minCostConnectPoints(
        [[-1000000, -1000000], [1000000, 1000000]]) == 4000000, name
    assert solver.minCostConnectPoints([[0, 0], [1, 0], [2, 0], [3, 0]]) == 3, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionPrimNoHeap())
    _run_tests(SolutionKruskal())
