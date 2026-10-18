"""
Network Delay Time  ·  LeetCode 743  ·  Medium
Group 10 — Dijkstra

Classic sum-of-weights Dijkstra from source k. The answer is the MAX shortest
distance (the last node to receive the signal), or -1 if some node is unreachable.

Run:  python 01-network-delay-time.py
"""

import heapq
from collections import defaultdict
from typing import List


class Solution:
    """Primary: Dijkstra; dist-dict doubles as the finalized set."""

    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        graph = defaultdict(list)
        for u, v, w in times:
            graph[u].append((v, w))

        dist = {}
        heap = [(0, k)]

        while heap:
            d, u = heapq.heappop(heap)
            if u in dist:
                continue
            dist[u] = d
            for v, w in graph[u]:
                if v not in dist:
                    heapq.heappush(heap, (d + w, v))

        return max(dist.values()) if len(dist) == n else -1


class SolutionBellmanFord:
    """Alternative: Bellman-Ford -- O(V*E), no heap; the tool for negative weights."""

    def networkDelayTime(self, times: List[List[int]], n: int, k: int) -> int:
        dist = [float("inf")] * (n + 1)
        dist[k] = 0
        for _ in range(n - 1):
            updated = False
            for u, v, w in times:
                if dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True
            if not updated:
                break
        ans = max(dist[1:])
        return ans if ans < float("inf") else -1


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.networkDelayTime([[2, 1, 1], [2, 3, 1], [3, 4, 1]], 4, 2) == 2, name
    assert solver.networkDelayTime([[1, 2, 1]], 2, 1) == 1, name
    assert solver.networkDelayTime([[1, 2, 1]], 2, 2) == -1, name
    assert solver.networkDelayTime([[1, 2, 1], [2, 3, 2], [1, 3, 4]], 3, 1) == 3, name
    assert solver.networkDelayTime([[1, 2, 0]], 2, 1) == 0, name
    assert solver.networkDelayTime([[1, 2, 1], [2, 1, 3]], 2, 1) == 1, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionBellmanFord())
