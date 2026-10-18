"""
Rotting Oranges  ·  LeetCode 994  ·  Medium
Group 02 — Multi-Source BFS

Multi-source BFS where the answer is the NUMBER OF ROUNDS (not a per-cell
distance), with an "impossible" (-1) case when some fresh orange is unreachable.

Classic bug: overcounting by 1 if you don't stop the instant `fresh` hits 0
(the queue can still hold cells whose round would rot nothing).

Run:  python 03-rotting-oranges.py
"""

from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    """Primary: ring-counting BFS with a fresh-count guard."""

    def orangesRotting(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        q = deque()
        fresh = 0

        for r in range(m):
            for c in range(n):
                if grid[r][c] == 2:
                    q.append((r, c))
                elif grid[r][c] == 1:
                    fresh += 1

        if fresh == 0:                          # nothing to wait for
            return 0

        minutes = 0
        while q and fresh > 0:                  # stop the instant nothing fresh remains
            minutes += 1
            for _ in range(len(q)):              # one ring == one minute
                r, c = q.popleft()
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                        grid[nr][nc] = 2         # rot it == mark visited
                        fresh -= 1
                        q.append((nr, nc))

        return minutes if fresh == 0 else -1


class SolutionTimestamped:
    """Alternative: carry the minute with each queue entry -- structurally
    immune to the off-by-one, since `minutes` only updates when a cell rots."""

    def orangesRotting(self, grid: List[List[int]]) -> int:
        m, n = len(grid), len(grid[0])
        q = deque()
        fresh = 0

        for r in range(m):
            for c in range(n):
                if grid[r][c] == 2:
                    q.append((r, c, 0))
                elif grid[r][c] == 1:
                    fresh += 1

        if fresh == 0:
            return 0

        minutes = 0
        while q:
            r, c, t = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    minutes = t + 1
                    q.append((nr, nc, t + 1))

        return minutes if fresh == 0 else -1


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.orangesRotting([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4, name
    assert solver.orangesRotting([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1, name
    assert solver.orangesRotting([[0, 2]]) == 0, name
    assert solver.orangesRotting([[1]]) == -1, name
    assert solver.orangesRotting([[2]]) == 0, name
    assert solver.orangesRotting([[0, 0, 0]]) == 0, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionTimestamped())
