"""
Making a Large Island  ·  LeetCode 827  ·  Hard  ·  (supplementary)
Group 01 — Grid Flood-Fill

Two-pass "label + probe":
  Pass 1 - flood every island once, stamp a stable id, cache its size.
  Pass 2 - for every water cell, sum the DISTINCT neighboring islands' sizes + 1.
Turns an O(n^4) naive approach (flip each 0, re-flood, O(n^2) x O(n^2)) into O(n^2).

Run:  python 04-making-a-large-island.py
"""

from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    """Primary: DFS labeling into a separate `label` grid (input untouched)."""

    def largestIsland(self, grid: List[List[int]]) -> int:
        n = len(grid)
        label = [[0] * n for _ in range(n)]     # 0 = water / not yet labeled
        size = {}                                # island_id -> cell count
        next_id = 2                              # start above 0/1

        def dfs(r: int, c: int, island_id: int) -> int:
            if not (0 <= r < n and 0 <= c < n):
                return 0
            if grid[r][c] == 0 or label[r][c] != 0:
                return 0
            label[r][c] = island_id
            area = 1
            for dr, dc in DIRS:
                area += dfs(r + dr, c + dc, island_id)
            return area

        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1 and label[r][c] == 0:
                    size[next_id] = dfs(r, c, next_id)
                    next_id += 1

        best = max(size.values(), default=0)     # handles "grid is all land"

        for r in range(n):
            for c in range(n):
                if grid[r][c] == 0:
                    neighbor_ids = set()
                    for dr, dc in DIRS:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n and label[nr][nc] != 0:
                            neighbor_ids.add(label[nr][nc])
                    candidate = 1 + sum(size[i] for i in neighbor_ids)
                    best = max(best, candidate)

        return best


class SolutionInPlace:
    """Alternative: classic LeetCode-accepted version, mutates `grid` directly."""

    def largestIsland(self, grid: List[List[int]]) -> int:
        n = len(grid)
        size = {}
        next_id = 2

        def dfs(r: int, c: int, island_id: int) -> int:
            if not (0 <= r < n and 0 <= c < n) or grid[r][c] != 1:
                return 0
            grid[r][c] = island_id
            area = 1
            for dr, dc in DIRS:
                area += dfs(r + dr, c + dc, island_id)
            return area

        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1:
                    size[next_id] = dfs(r, c, next_id)
                    next_id += 1

        best = max(size.values(), default=0)
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 0:
                    ids = set()
                    for dr, dc in DIRS:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] > 1:
                            ids.add(grid[nr][nc])
                    best = max(best, 1 + sum(size[i] for i in ids))
        return best


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.largestIsland([[1, 0], [0, 1]]) == 3, name
    assert solver.largestIsland([[1, 1], [1, 0]]) == 4, name
    assert solver.largestIsland([[1, 1], [1, 1]]) == 4, name
    assert solver.largestIsland([[0]]) == 1, name
    assert solver.largestIsland([[1]]) == 1, name
    assert solver.largestIsland([[0, 0], [0, 0]]) == 1, name
    assert solver.largestIsland([[1, 1, 0], [1, 0, 0], [0, 0, 1]]) == 4, name
    # far-apart islands (opposite corners of a row) can't be merged by one flip
    far_apart = [
        [1, 0, 0, 0, 1],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0],
    ]
    assert solver.largestIsland([row[:] for row in far_apart]) == 2, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionInPlace())
