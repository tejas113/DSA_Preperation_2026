"""
Find if Path Exists in Graph  ·  LeetCode 1971  ·  Easy
Group 04 — Graph Traversal / Connectivity (non-grid)

First non-grid graph problem: build an adjacency list from the edge list, then
run one plain BFS to check reachability from source to destination.

Run:  python 01-find-if-path-exists-in-graph.py
"""

from collections import defaultdict, deque
from typing import List


class Solution:
    """Primary: adjacency list + BFS."""

    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        seen = {source}
        q = deque([source])
        while q:
            node = q.popleft()
            if node == destination:      # covers source == destination too, on the first pop
                return True
            for nei in graph[node]:
                if nei not in seen:
                    seen.add(nei)
                    q.append(nei)

        return False


class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1


class SolutionDSU:
    """Alternative: Union-Find -- the right tool once there are many queries
    against the same static graph, or edges arrive incrementally (Group 07)."""

    def validPath(self, n: int, edges: List[List[int]], source: int, destination: int) -> bool:
        dsu = DSU(n)
        for u, v in edges:
            dsu.union(u, v)
        return dsu.find(source) == dsu.find(destination)


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.validPath(3, [[0, 1], [1, 2], [2, 0]], 0, 2) is True, name
    assert solver.validPath(6, [[0, 1], [0, 2], [3, 5], [5, 4], [4, 3]], 0, 5) is False, name
    assert solver.validPath(1, [], 0, 0) is True, name
    assert solver.validPath(2, [], 0, 1) is False, name
    assert solver.validPath(5, [[0, 1], [1, 2], [2, 3], [3, 4]], 0, 4) is True, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionDSU())
