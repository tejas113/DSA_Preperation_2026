"""
Pacific Atlantic Water Flow  ·  LeetCode 417  ·  Medium
Group 03 — Boundary-Anchored Traversal

Flood from EACH ocean's border cells inward, using the REVERSED flow condition
(height[neighbor] >= height[current] instead of the real <=), then intersect the
two reachable sets. O(m*n) instead of the naive O((m*n)^2) per-cell simulation.

Run:  python 01-pacific-atlantic-water-flow.py
"""

from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:
        if not heights or not heights[0]:
            return []

        m, n = len(heights), len(heights[0])

        def bfs(sources):
            seen = set(sources)
            q = deque(sources)
            while q:
                r, c = q.popleft()
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen
                            and heights[nr][nc] >= heights[r][c]):   # reversed flow
                        seen.add((nr, nc))
                        q.append((nr, nc))
            return seen

        pacific_sources = [(0, c) for c in range(n)] + [(r, 0) for r in range(1, m)]
        atlantic_sources = [(m - 1, c) for c in range(n)] + [(r, n - 1) for r in range(m - 1)]

        pacific = bfs(pacific_sources)
        atlantic = bfs(atlantic_sources)

        return [[r, c] for r, c in pacific & atlantic]


def _run_tests(solver) -> None:
    name = type(solver).__name__

    heights = [[1, 2, 2, 3, 5],
               [3, 2, 3, 4, 4],
               [2, 4, 5, 3, 1],
               [6, 7, 1, 4, 5],
               [5, 1, 1, 2, 4]]
    result = solver.pacificAtlantic(heights)
    expected = [[0, 4], [1, 3], [1, 4], [2, 2], [3, 0], [3, 1], [4, 0]]
    assert sorted(result) == sorted(expected), name

    assert solver.pacificAtlantic([[1]]) == [[0, 0]], name

    assert sorted(solver.pacificAtlantic([[2, 1], [1, 2]])) == \
        sorted([[0, 0], [0, 1], [1, 0], [1, 1]]), name

    # single row -> row0 is both the top row and bottom row -> everything qualifies
    assert sorted(solver.pacificAtlantic([[3, 1, 6, 4]])) == \
        sorted([[0, 0], [0, 1], [0, 2], [0, 3]]), name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
