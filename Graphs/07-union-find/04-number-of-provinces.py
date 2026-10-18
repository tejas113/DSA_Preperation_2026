"""
Number of Provinces  ·  LeetCode 547  ·  Medium
Group 07 — Union-Find

Number of Connected Components, with the graph given as a SYMMETRIC adjacency
matrix. Edges are the 1s in the upper triangle (j > i).

Run:  python 04-number-of-provinces.py
"""

from collections import deque
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
    """Primary: DSU over the matrix's upper triangle."""

    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        dsu = DSU(n)
        count = n
        for i in range(n):
            for j in range(i + 1, n):
                if isConnected[i][j] == 1 and dsu.union(i, j):
                    count -= 1
        return count


class SolutionBFS:
    """Alternative: flood-fill over the matrix."""

    def findCircleNum(self, isConnected: List[List[int]]) -> int:
        n = len(isConnected)
        seen = set()
        count = 0
        for start in range(n):
            if start in seen:
                continue
            count += 1
            q = deque([start])
            seen.add(start)
            while q:
                i = q.popleft()
                for j in range(n):
                    if isConnected[i][j] == 1 and j not in seen:
                        seen.add(j)
                        q.append(j)
        return count


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.findCircleNum([[1, 1, 0], [1, 1, 0], [0, 0, 1]]) == 2, name
    assert solver.findCircleNum([[1, 0, 0], [0, 1, 0], [0, 0, 1]]) == 3, name
    assert solver.findCircleNum([[1]]) == 1, name
    assert solver.findCircleNum([[1, 1, 1], [1, 1, 1], [1, 1, 1]]) == 1, name
    assert solver.findCircleNum(
        [[1, 0, 0, 1],
         [0, 1, 1, 0],
         [0, 1, 1, 0],
         [1, 0, 0, 1]]) == 2, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionBFS())
