"""
01 Matrix  ·  LeetCode 542  ·  Medium
Group 02 — Multi-Source BFS

For every cell, return its distance to the nearest 0 cell. No walls; the grid
is guaranteed to contain at least one 0.

Sentinel gotcha: the input only holds 0/1, and a cell's REAL answer can also be 1,
so we can't reuse mat's own values as a "visited" flag (unlike Walls and Gates,
where INF could never collide with a real distance). Use a separate `dist` grid
seeded with -1 instead.

Run:  python 02-01-matrix.py
"""

from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    """Primary: multi-source BFS."""

    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        m, n = len(mat), len(mat[0])
        dist = [[-1] * n for _ in range(m)]      # -1 = not yet computed
        q = deque()

        for r in range(m):
            for c in range(n):
                if mat[r][c] == 0:
                    dist[r][c] = 0
                    q.append((r, c))

        while q:
            r, c = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and dist[nr][nc] == -1:
                    dist[nr][nc] = dist[r][c] + 1
                    q.append((nr, nc))

        return dist


class SolutionDP:
    """Alternative: two-pass DP (distance transform). O(1) extra space.

    Only valid because this grid has NO obstacles -- see the .md, section 9a
    and Scenario 5, for why this breaks the moment walls exist.
    """

    def updateMatrix(self, mat: List[List[int]]) -> List[List[int]]:
        m, n = len(mat), len(mat[0])
        INF = float("inf")
        dist = [[0 if mat[r][c] == 0 else INF for c in range(n)] for r in range(m)]

        for r in range(m):                            # forward: up + left
            for c in range(n):
                if r > 0:
                    dist[r][c] = min(dist[r][c], dist[r - 1][c] + 1)
                if c > 0:
                    dist[r][c] = min(dist[r][c], dist[r][c - 1] + 1)

        for r in range(m - 1, -1, -1):                 # backward: down + right
            for c in range(n - 1, -1, -1):
                if r < m - 1:
                    dist[r][c] = min(dist[r][c], dist[r + 1][c] + 1)
                if c < n - 1:
                    dist[r][c] = min(dist[r][c], dist[r][c + 1] + 1)

        return [[int(v) for v in row] for row in dist]


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.updateMatrix([[0, 0, 0], [0, 1, 0], [0, 0, 0]]) == \
        [[0, 0, 0], [0, 1, 0], [0, 0, 0]], name

    assert solver.updateMatrix([[0, 0, 0], [0, 1, 0], [1, 1, 1]]) == \
        [[0, 0, 0], [0, 1, 0], [1, 2, 1]], name

    assert solver.updateMatrix([[0]]) == [[0]], name
    assert solver.updateMatrix([[1, 1], [1, 0]]) == [[2, 1], [1, 0]], name
    assert solver.updateMatrix([[0, 0, 0, 0, 0]]) == [[0, 0, 0, 0, 0]], name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionDP())
