"""
Graph Valid Tree  ·  LeetCode 261  ·  Medium  ·  premium
Group 07 — Union-Find

A graph is a valid tree  <=>  exactly n-1 edges AND no cycle.
(For n nodes, any two of {connected, acyclic, n-1 edges} imply the third.)

Check the two cheapest: edge count O(1), then DSU cycle detection (union failure).

Run:  python 02-graph-valid-tree.py
"""

from collections import defaultdict, deque
from typing import List


class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


class Solution:
    """Primary: edge-count check + DSU cycle check."""

    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False

        dsu = DSU(n)                          # 0-indexed -> size n
        for u, v in edges:
            if not dsu.union(u, v):
                return False                  # cycle
        return True


class SolutionBFS:
    """Alternative: edge-count check + connectivity BFS."""

    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        if len(edges) != n - 1:
            return False

        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        seen = {0}
        q = deque([0])
        while q:
            node = q.popleft()
            for nei in graph[node]:
                if nei not in seen:
                    seen.add(nei)
                    q.append(nei)

        return len(seen) == n


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.validTree(5, [[0, 1], [0, 2], [0, 3], [1, 4]]) is True, name
    assert solver.validTree(5, [[0, 1], [1, 2], [2, 3], [1, 3], [1, 4]]) is False, name
    assert solver.validTree(4, [[0, 1], [2, 3]]) is False, name
    assert solver.validTree(1, []) is True, name
    assert solver.validTree(2, []) is False, name
    assert solver.validTree(3, [[0, 1], [1, 2], [2, 0]]) is False, name
    assert solver.validTree(4, [[0, 1], [1, 2], [2, 3]]) is True, name
    assert solver.validTree(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) is True, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionBFS())
