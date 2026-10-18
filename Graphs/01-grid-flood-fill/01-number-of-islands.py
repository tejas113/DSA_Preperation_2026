"""
Number of Islands  ·  LeetCode 200  ·  Medium
Group 01 — Grid Flood-Fill

Count connected blobs of "1" cells in an m x n grid (4-directional).

Primary solution: DFS flood fill + outer loop over all cells.
Run:  python 01-number-of-islands.py
"""

from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        m, n = len(grid), len(grid[0])
        seen = set()

        def dfs(r: int, c: int) -> None:
            if not (0 <= r < m and 0 <= c < n):        # off the board
                return
            if grid[r][c] == "0" or (r, c) in seen:    # water, or already visited
                return
            seen.add((r, c))
            for dr, dc in DIRS:
                dfs(r + dr, c + dc)

        count = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == "1" and (r, c) not in seen:
                    count += 1          # a brand-new island
                    dfs(r, c)           # sink the rest of it
        return count


class SolutionBFS:
    """Alternative: BFS flood — no recursion-depth risk on huge solid islands."""

    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid or not grid[0]:
            return 0

        m, n = len(grid), len(grid[0])
        seen = set()

        def bfs(sr: int, sc: int) -> None:
            q = deque([(sr, sc)])
            seen.add((sr, sc))
            while q:
                r, c = q.popleft()
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < m and 0 <= nc < n
                            and grid[nr][nc] == "1" and (nr, nc) not in seen):
                        seen.add((nr, nc))     # mark on enqueue
                        q.append((nr, nc))

        count = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == "1" and (r, c) not in seen:
                    count += 1
                    bfs(r, c)
        return count


def _run_tests(solver) -> None:
    name = type(solver).__name__

    g1 = [
        ["1", "1", "1", "1", "0"],
        ["1", "1", "0", "1", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "0", "0", "0"],
    ]
    assert solver.numIslands([row[:] for row in g1]) == 1, name

    g2 = [
        ["1", "1", "0", "0", "0"],
        ["1", "1", "0", "0", "0"],
        ["0", "0", "1", "0", "0"],
        ["0", "0", "0", "1", "1"],
    ]
    assert solver.numIslands([row[:] for row in g2]) == 3, name

    assert solver.numIslands([["0"]]) == 0, name
    assert solver.numIslands([["1"]]) == 1, name
    assert solver.numIslands([["1", "0", "1", "0", "1"]]) == 3, name    # single row
    assert solver.numIslands([["1"], ["0"], ["1"]]) == 2, name          # single column
    assert solver.numIslands([]) == 0, name

    # diagonal touch => separate islands
    assert solver.numIslands([["1", "0"], ["0", "1"]]) == 2, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionBFS())
