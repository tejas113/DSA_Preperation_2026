"""
Evaluate Division  ·  LeetCode 399  ·  Medium
Group 09 — Weighted DFS (ratio propagation)

Build a graph: equation a/b = v adds edge a->b weight v and b->a weight 1/v.
A query x/y = product of edge weights along any path from x to y (DFS carrying a
running PRODUCT), or -1.0 if x/y is unknown or unreachable.

Order matters: check "variable exists" BEFORE the x == y -> 1.0 shortcut.

Run:  python 01-evaluate-division.py
"""

from collections import defaultdict, deque
from typing import List


class Solution:
    """Primary: weighted DFS per query."""

    def calcEquation(self, equations: List[List[str]], values: List[float],
                     queries: List[List[str]]) -> List[float]:
        graph = defaultdict(dict)               # graph[a][b] = a / b
        for (a, b), v in zip(equations, values):
            graph[a][b] = v
            graph[b][a] = 1 / v

        def dfs(src: str, dst: str, seen: set) -> float:
            if src not in graph or dst not in graph:
                return -1.0                      # unknown variable -- check BEFORE src == dst
            if src == dst:
                return 1.0
            seen.add(src)
            for nei, w in graph[src].items():
                if nei not in seen:
                    sub = dfs(nei, dst, seen)
                    if sub != -1.0:
                        return w * sub
            return -1.0

        return [dfs(c, d, set()) for c, d in queries]


class SolutionBFS:
    """Alternative: BFS, carrying the running product in the queue."""

    def calcEquation(self, equations: List[List[str]], values: List[float],
                     queries: List[List[str]]) -> List[float]:
        graph = defaultdict(dict)
        for (a, b), v in zip(equations, values):
            graph[a][b] = v
            graph[b][a] = 1 / v

        def bfs(src: str, dst: str) -> float:
            if src not in graph or dst not in graph:
                return -1.0
            q = deque([(src, 1.0)])
            seen = {src}
            while q:
                node, prod = q.popleft()
                if node == dst:
                    return prod
                for nei, w in graph[node].items():
                    if nei not in seen:
                        seen.add(nei)
                        q.append((nei, prod * w))
            return -1.0

        return [bfs(c, d) for c, d in queries]


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.calcEquation(
        [["a", "b"], ["b", "c"]], [2.0, 3.0],
        [["a", "c"], ["b", "a"], ["a", "e"], ["a", "a"], ["x", "x"]]
    ) == [6.0, 0.5, -1.0, 1.0, -1.0], name

    assert solver.calcEquation(
        [["a", "b"], ["b", "c"], ["bc", "cd"]], [1.5, 2.5, 5.0],
        [["a", "c"], ["c", "b"], ["bc", "cd"], ["cd", "bc"]]
    ) == [3.75, 0.4, 5.0, 0.2], name

    assert solver.calcEquation(
        [["a", "b"]], [0.5],
        [["a", "b"], ["b", "a"], ["a", "c"], ["x", "y"]]
    ) == [0.5, 2.0, -1.0, -1.0], name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionBFS())
