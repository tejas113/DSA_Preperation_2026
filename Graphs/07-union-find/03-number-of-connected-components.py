"""
Number of Connected Components in an Undirected Graph  ·  LeetCode 323  ·  Medium  ·  premium
Group 07 — Union-Find

The group's second idiom in its purest form:
    count = n
    for each edge: if union(u, v): count -= 1

Run:  python 03-number-of-connected-components.py
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
    """Primary: DSU, count -= 1 per successful union."""

    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        dsu = DSU(n)
        count = n
        for u, v in edges:
            if dsu.union(u, v):
                count -= 1
        return count


class SolutionBFS:
    """Alternative: flood-fill counting (concepts/05 skeleton)."""

    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        graph = defaultdict(list)
        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        seen = set()
        count = 0
        for start in range(n):
            if start in seen:
                continue
            count += 1
            q = deque([start])
            seen.add(start)
            while q:
                node = q.popleft()
                for nei in graph[node]:
                    if nei not in seen:
                        seen.add(nei)
                        q.append(nei)
        return count


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.countComponents(5, [[0, 1], [1, 2], [3, 4]]) == 2, name
    assert solver.countComponents(5, [[0, 1], [1, 2], [2, 3], [3, 4]]) == 1, name
    assert solver.countComponents(4, []) == 4, name
    assert solver.countComponents(1, []) == 1, name
    assert solver.countComponents(6, [[0, 1], [2, 3], [4, 5], [0, 2], [0, 4]]) == 1, name
    assert solver.countComponents(5, [[0, 1], [1, 2], [0, 2], [3, 4]]) == 2, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionBFS())
