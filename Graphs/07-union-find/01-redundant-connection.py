"""
Redundant Connection  ·  LeetCode 684  ·  Medium
Group 07 — Union-Find

A tree + one extra edge = exactly one cycle. Process edges in order with a DSU;
the first edge whose union() returns False (endpoints already connected) is the
one to remove -- and it's automatically the last cycle edge in input order.

Run:  python 01-redundant-connection.py
"""

from collections import defaultdict
from typing import List


class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]     # path compression
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False                                     # already connected -> cycle edge
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


class Solution:
    """Primary: DSU, return the first union() failure."""

    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        dsu = DSU(len(edges) + 1)                # nodes are 1..n
        for u, v in edges:
            if not dsu.union(u, v):
                return [u, v]
        return []


class SolutionDFS:
    """Alternative: DFS per edge (O(E^2)) -- correct, but doesn't scale."""

    def findRedundantConnection(self, edges: List[List[int]]) -> List[int]:
        graph = defaultdict(set)

        def connected(u, v, seen):
            if u == v:
                return True
            seen.add(u)
            return any(connected(nei, v, seen) for nei in graph[u] if nei not in seen)

        for u, v in edges:
            if u in graph and v in graph and connected(u, v, set()):
                return [u, v]
            graph[u].add(v)
            graph[v].add(u)
        return []


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.findRedundantConnection([[1, 2], [1, 3], [2, 3]]) == [2, 3], name
    assert solver.findRedundantConnection(
        [[1, 2], [2, 3], [3, 4], [1, 4], [1, 5]]) == [1, 4], name
    assert solver.findRedundantConnection([[1, 2], [2, 3], [1, 3]]) == [1, 3], name
    assert solver.findRedundantConnection(
        [[3, 4], [1, 2], [2, 4], [3, 5], [2, 5]]) == [2, 5], name
    assert solver.findRedundantConnection(
        [[1, 4], [3, 4], [1, 3], [1, 2], [4, 5]]) == [1, 3], name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionDFS())
