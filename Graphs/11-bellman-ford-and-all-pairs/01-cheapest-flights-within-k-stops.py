"""
Cheapest Flights Within K Stops  ·  LeetCode 787  ·  Medium
Group 11 — Bellman-Ford / All-Pairs

"At most k stops" = at most k+1 flights. Run Bellman-Ford for exactly k+1 rounds,
relaxing every flight against a FROZEN snapshot of dist from the round's start --
so each round adds at most one flight. That frozen copy is the whole trick.

Run:  python 01-cheapest-flights-within-k-stops.py
"""

import heapq
from collections import defaultdict
from typing import List


class Solution:
    """Primary: hop-limited Bellman-Ford."""

    def findCheapestPrice(self, n: int, flights: List[List[int]],
                          src: int, dst: int, k: int) -> int:
        INF = float("inf")
        dist = [INF] * n
        dist[src] = 0

        for _ in range(k + 1):                  # at most k stops => at most k+1 flights
            snapshot = dist[:]                  # freeze -> one flight per round
            for u, v, w in flights:
                if snapshot[u] + w < dist[v]:
                    dist[v] = snapshot[u] + w

        return dist[dst] if dist[dst] != INF else -1


class SolutionDijkstraState:
    """Alternative: Dijkstra where the state is (cost, city, stops_used)."""

    def findCheapestPrice(self, n: int, flights: List[List[int]],
                          src: int, dst: int, k: int) -> int:
        graph = defaultdict(list)
        for u, v, w in flights:
            graph[u].append((v, w))

        heap = [(0, src, 0)]
        best = {}

        while heap:
            cost, city, stops = heapq.heappop(heap)
            if city == dst:
                return cost
            if stops > k:
                continue
            if best.get((city, stops), float("inf")) < cost:
                continue
            for nei, w in graph[city]:
                if cost + w < best.get((nei, stops + 1), float("inf")):
                    best[(nei, stops + 1)] = cost + w
                    heapq.heappush(heap, (cost + w, nei, stops + 1))
        return -1


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.findCheapestPrice(
        4, [[0, 1, 100], [1, 2, 100], [2, 0, 100], [1, 3, 600], [2, 3, 200]], 0, 3, 1) == 700, name
    assert solver.findCheapestPrice(
        3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 1) == 200, name
    assert solver.findCheapestPrice(
        3, [[0, 1, 100], [1, 2, 100], [0, 2, 500]], 0, 2, 0) == 500, name
    assert solver.findCheapestPrice(
        3, [[0, 1, 2], [1, 2, 1], [2, 0, 10]], 1, 2, 1) == 1, name
    assert solver.findCheapestPrice(
        5, [[0, 1, 1], [1, 2, 1], [2, 3, 1], [3, 4, 1]], 0, 4, 1) == -1, name
    assert solver.findCheapestPrice(2, [[1, 0, 10]], 0, 1, 0) == -1, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionDijkstraState())
