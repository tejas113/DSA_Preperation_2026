"""
Number of Ways to Arrive at Destination  ·  LeetCode 1976  ·  Medium  ·  (supplementary)
Group 10 — Dijkstra (path counting)

Dijkstra from 0, carrying ways[v] alongside dist[v]:
  - strict improvement (nd < dist[v]):  ways[v] = ways[u]        (replace)
  - tie at shortest    (nd == dist[v]): ways[v] += ways[u]       (accumulate, mod)
Works inline because positive weights => every shortest-path predecessor of v is
finalized before v is popped.

Run:  python 04-number-of-ways-to-arrive-at-destination.py
"""

import heapq
from collections import defaultdict
from typing import List


class Solution:
    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        MOD = 10 ** 9 + 7

        graph = defaultdict(list)
        for u, v, w in roads:
            graph[u].append((v, w))
            graph[v].append((u, w))

        dist = [float("inf")] * n
        ways = [0] * n
        dist[0] = 0
        ways[0] = 1
        heap = [(0, 0)]

        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, w in graph[u]:
                nd = d + w
                if nd < dist[v]:
                    dist[v] = nd
                    ways[v] = ways[u]
                    heapq.heappush(heap, (nd, v))
                elif nd == dist[v]:
                    ways[v] = (ways[v] + ways[u]) % MOD

        return ways[n - 1] % MOD


class SolutionDagDp:
    """Alternative: Dijkstra for dist, then DAG-DP for ways in dist order.
    Also handles zero-weight edges correctly."""

    def countPaths(self, n: int, roads: List[List[int]]) -> int:
        MOD = 10 ** 9 + 7
        graph = defaultdict(list)
        for u, v, w in roads:
            graph[u].append((v, w))
            graph[v].append((u, w))

        dist = [float("inf")] * n
        dist[0] = 0
        heap = [(0, 0)]
        while heap:
            d, u = heapq.heappop(heap)
            if d > dist[u]:
                continue
            for v, w in graph[u]:
                if d + w < dist[v]:
                    dist[v] = d + w
                    heapq.heappush(heap, (d + w, v))

        ways = [0] * n
        ways[0] = 1
        for u in sorted(range(n), key=lambda x: dist[x]):
            for v, w in graph[u]:
                if dist[u] + w == dist[v]:
                    ways[v] = (ways[v] + ways[u]) % MOD
        return ways[n - 1] % MOD


def _brute(n: int, roads: List[List[int]]) -> int:
    g = defaultdict(list)
    for u, v, w in roads:
        g[u].append((v, w))
        g[v].append((u, w))
    best = [float("inf")]
    cnt = [0]

    def dfs(node, cost, seen):
        if cost > best[0]:
            return
        if node == n - 1:
            if cost < best[0]:
                best[0] = cost
                cnt[0] = 1
            elif cost == best[0]:
                cnt[0] += 1
            return
        for nx, w in g[node]:
            if nx not in seen:
                seen.add(nx)
                dfs(nx, cost + w, seen)
                seen.discard(nx)

    dfs(0, 0, {0})
    return cnt[0]


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.countPaths(7, [
        [0, 6, 7], [0, 1, 2], [1, 2, 3], [1, 3, 3], [6, 3, 3],
        [3, 5, 1], [6, 5, 1], [2, 5, 1], [0, 4, 3], [4, 6, 4],
    ]) == 4, name
    assert solver.countPaths(2, [[1, 0, 10]]) == 1, name
    assert solver.countPaths(1, []) == 1, name
    assert solver.countPaths(4, [[0, 1, 1], [0, 2, 1], [1, 3, 1], [2, 3, 1]]) == 2, name
    assert solver.countPaths(3, [[0, 1, 1], [1, 2, 1], [0, 2, 2]]) == 2, name
    assert solver.countPaths(
        4, [[0, 1, 10 ** 9], [1, 2, 10 ** 9], [2, 3, 10 ** 9], [0, 3, 1]]) == 1, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    import random

    _run_tests(Solution())
    _run_tests(SolutionDagDp())

    # stress test both solvers against brute-force enumeration
    sol, dag = Solution(), SolutionDagDp()
    for _ in range(1000):
        n = random.randint(2, 7)
        pairs = [(i, j) for i in range(n) for j in range(i + 1, n)]
        random.shuffle(pairs)
        perm = list(range(n))
        random.shuffle(perm)
        tree = {(min(perm[i], perm[i + 1]), max(perm[i], perm[i + 1])) for i in range(n - 1)}
        edges = list(tree | set(pairs[: random.randint(0, len(pairs))]))
        rd = [[u, v, random.randint(1, 6)] for u, v in edges]
        b = _brute(n, rd)
        assert sol.countPaths(n, rd) == b and dag.countPaths(n, rd) == b, rd
    print("stress test vs brute force: all match")
