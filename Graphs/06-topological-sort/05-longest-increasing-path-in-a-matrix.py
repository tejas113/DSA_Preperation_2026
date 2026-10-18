"""
Longest Increasing Path in a Matrix  ·  LeetCode 329  ·  Hard  ·  (supplementary)
Group 06 — Topological Sort / Cycle Detection

An IMPLICIT DAG: strictly-increasing moves make cycles impossible, so memoized
DFS needs NO visited set / NO 3-color scheme. It's "longest path in a DAG":
    f(cell) = 1 + max(f(strictly-greater neighbor)),  or 1 if none.

Run:  python 05-longest-increasing-path-in-a-matrix.py
"""

import sys
from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    """Primary: memoized DFS (DAG longest-path DP)."""

    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        sys.setrecursionlimit(250_000)          # 200x200 monotone path recurses ~40k deep
        m, n = len(matrix), len(matrix[0])
        memo = [[0] * n for _ in range(m)]       # 0 == not computed (real answers are >= 1)

        def dfs(r: int, c: int) -> int:
            if memo[r][c]:
                return memo[r][c]
            best = 1
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                    best = max(best, 1 + dfs(nr, nc))
            memo[r][c] = best
            return best

        return max(dfs(r, c) for r in range(m) for c in range(n))


class SolutionKahn:
    """Alternative: Kahn's / topological layer-peeling. No recursion.
    Edges go smaller -> larger; start from indegree-0 cells (local minima);
    number of BFS layers == longest increasing path length."""

    def longestIncreasingPath(self, matrix: List[List[int]]) -> int:
        if not matrix or not matrix[0]:
            return 0

        m, n = len(matrix), len(matrix[0])
        indegree = [[0] * n for _ in range(m)]

        for r in range(m):
            for c in range(n):
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                        indegree[nr][nc] += 1

        q = deque((r, c) for r in range(m) for c in range(n) if indegree[r][c] == 0)
        length = 0

        while q:
            length += 1
            for _ in range(len(q)):              # freeze the layer
                r, c = q.popleft()
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and matrix[nr][nc] > matrix[r][c]:
                        indegree[nr][nc] -= 1
                        if indegree[nr][nc] == 0:
                            q.append((nr, nc))

        return length


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.longestIncreasingPath([[9, 9, 4], [6, 6, 8], [2, 1, 1]]) == 4, name
    assert solver.longestIncreasingPath([[3, 4, 5], [3, 2, 6], [2, 2, 1]]) == 4, name
    assert solver.longestIncreasingPath([[1]]) == 1, name
    assert solver.longestIncreasingPath([[7, 7], [7, 7]]) == 1, name
    assert solver.longestIncreasingPath([[1, 2, 3], [6, 5, 4], [7, 8, 9]]) == 9, name
    assert solver.longestIncreasingPath([[1, 2], [3, 4]]) == 3, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionKahn())
