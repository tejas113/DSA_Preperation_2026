"""
Max Area of Island  ·  LeetCode 695  ·  Medium
Group 01 — Grid Flood-Fill

Number of Islands, but the flood RETURNS a number (the island's cell count) and we
keep the maximum.  Recurrence:  area(cell) = 1 + sum(area(neighbor)).

Run:  python 03-max-area-of-island.py
"""

from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    """Primary: recursive DFS that returns an area."""

    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        m, n = len(grid), len(grid[0])
        seen = set()

        def dfs(r: int, c: int) -> int:
            if not (0 <= r < m and 0 <= c < n):        # off the board
                return 0
            if grid[r][c] == 0 or (r, c) in seen:      # water, or already counted
                return 0
            seen.add((r, c))
            area = 1                                   # count myself
            for dr, dc in DIRS:
                area += dfs(r + dr, c + dc)            # plus everything reachable
            return area

        best = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 1 and (r, c) not in seen:
                    best = max(best, dfs(r, c))
        return best


class SolutionBFS:
    """Alternative: BFS, counting cells on pop."""

    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid or not grid[0]:
            return 0

        m, n = len(grid), len(grid[0])
        seen = set()

        def bfs(sr: int, sc: int) -> int:
            q = deque([(sr, sc)])
            seen.add((sr, sc))
            area = 0
            while q:
                r, c = q.popleft()
                area += 1
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < m and 0 <= nc < n
                            and grid[nr][nc] == 1 and (nr, nc) not in seen):
                        seen.add((nr, nc))
                        q.append((nr, nc))
            return area

        best = 0
        for r in range(m):
            for c in range(n):
                if grid[r][c] == 1 and (r, c) not in seen:
                    best = max(best, bfs(r, c))
        return best


def _run_tests(solver) -> None:
    name = type(solver).__name__

    g = [[0, 0, 1, 0, 0],
         [0, 1, 1, 1, 0],
         [0, 0, 1, 0, 0],
         [1, 0, 0, 0, 1]]
    assert solver.maxAreaOfIsland([row[:] for row in g]) == 5, name

    assert solver.maxAreaOfIsland([[0, 0, 0], [0, 0, 0]]) == 0, name
    assert solver.maxAreaOfIsland([[1, 1], [1, 1]]) == 4, name
    assert solver.maxAreaOfIsland([[1]]) == 1, name
    assert solver.maxAreaOfIsland([[0]]) == 0, name
    assert solver.maxAreaOfIsland([[1, 0, 1, 0, 1]]) == 1, name
    assert solver.maxAreaOfIsland(
        [[1, 1, 0, 0, 0],
         [1, 1, 0, 0, 0],
         [0, 0, 0, 1, 1],
         [0, 0, 0, 1, 1]]) == 4, name

    # classic LeetCode 695 sample -> 6
    big = [
        [0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0],
        [0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0],
    ]
    assert solver.maxAreaOfIsland([row[:] for row in big]) == 6, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionBFS())
