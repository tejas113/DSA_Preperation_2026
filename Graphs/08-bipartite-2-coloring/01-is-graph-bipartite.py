"""
Is Graph Bipartite?  ·  LeetCode 785  ·  Medium
Group 08 — Bipartite / 2-Coloring

2-color the graph (BFS): color each neighbor the opposite color; a same-color
edge -> not bipartite (you just walked an odd cycle). Loop over ALL components.

Run:  python 01-is-graph-bipartite.py
"""

from collections import deque
from typing import List


class Solution:
    """Primary: BFS 2-coloring."""

    def isBipartite(self, graph: List[List[int]]) -> bool:
        n = len(graph)
        color = [0] * n                       # 0 = uncolored; 1 / -1 = the two sides

        for start in range(n):
            if color[start] != 0:
                continue
            color[start] = 1
            q = deque([start])
            while q:
                node = q.popleft()
                for nei in graph[node]:
                    if color[nei] == 0:
                        color[nei] = -color[node]
                        q.append(nei)
                    elif color[nei] == color[node]:
                        return False
        return True


class SolutionDFS:
    """Alternative: DFS 2-coloring."""

    def isBipartite(self, graph: List[List[int]]) -> bool:
        n = len(graph)
        color = [0] * n

        def dfs(node: int, c: int) -> bool:
            color[node] = c
            for nei in graph[node]:
                if color[nei] == 0:
                    if not dfs(nei, -c):
                        return False
                elif color[nei] == c:
                    return False
            return True

        return all(dfs(i, 1) for i in range(n) if color[i] == 0)


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.isBipartite([[1, 2, 3], [0, 2], [0, 1, 3], [0, 2]]) is False, name
    assert solver.isBipartite([[1, 3], [0, 2], [1, 3], [0, 2]]) is True, name
    assert solver.isBipartite([[]]) is True, name
    assert solver.isBipartite([[1], [0], [3], [2]]) is True, name
    assert solver.isBipartite([[1, 2], [0, 2], [0, 1]]) is False, name
    assert solver.isBipartite([[1], [0], []]) is True, name
    assert solver.isBipartite([[1, 4], [0, 2], [1, 3], [2, 4], [0, 3]]) is False, name  # 5-cycle
    assert solver.isBipartite([[1, 5], [0, 2], [1, 3], [2, 4], [3, 5], [4, 0]]) is True, name  # 6-cycle

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionDFS())
