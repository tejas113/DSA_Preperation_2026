"""
Shortest Bridge  ·  LeetCode 934  ·  Medium  ·  (supplementary)
Group 02 — Multi-Source BFS

Hybrid: iterative-DFS flood-fill to fully identify + mark ONE island (also
collecting it as multi-source BFS seeds), then multi-source BFS through water
until the first cell of the OTHER island is reached. That distance is the answer.

Sentinel `2` does triple duty: marks island A's cells, marks visited water,
and can't collide with the input's own 0/1 values (same trick as 01 Matrix).

Run:  python 04-shortest-bridge.py
"""

import sys
from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    """Primary: iterative DFS (stack) for Phase 1 -- an island can be up to
    n*n = 10^4 cells, which can exceed Python's default recursion limit."""

    def shortestBridge(self, grid: List[List[int]]) -> int:
        n = len(grid)

        start = None
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1:
                    start = (r, c)
                    break
            if start:
                break

        # Phase 1: flood-fill island A, collect it as BFS seeds
        stack = [start]
        grid[start[0]][start[1]] = 2
        q = deque([(start[0], start[1], 0)])

        while stack:
            r, c = stack.pop()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    stack.append((nr, nc))
                    q.append((nr, nc, 0))

        # Phase 2: multi-source BFS from ALL of island A, through water
        while q:
            r, c, d = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n:
                    if grid[nr][nc] == 1:
                        return d
                    if grid[nr][nc] == 0:
                        grid[nr][nc] = 2
                        q.append((nr, nc, d + 1))

        return -1     # never reached given the problem's "exactly two islands" guarantee


class SolutionRecursiveDFS:
    """Alternative: recursive DFS for Phase 1, with the recursion limit raised."""

    def shortestBridge(self, grid: List[List[int]]) -> int:
        sys.setrecursionlimit(20000)
        n = len(grid)

        start = None
        for r in range(n):
            for c in range(n):
                if grid[r][c] == 1:
                    start = (r, c)
                    break
            if start:
                break

        q = deque()

        def flood(r: int, c: int) -> None:
            if not (0 <= r < n and 0 <= c < n) or grid[r][c] != 1:
                return
            grid[r][c] = 2
            q.append((r, c, 0))
            for dr, dc in DIRS:
                flood(r + dr, c + dc)

        flood(start[0], start[1])

        while q:
            r, c, d = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n:
                    if grid[nr][nc] == 1:
                        return d
                    if grid[nr][nc] == 0:
                        grid[nr][nc] = 2
                        q.append((nr, nc, d + 1))

        return -1


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.shortestBridge([[0, 1], [1, 0]]) == 1, name
    assert solver.shortestBridge([[0, 1, 0], [0, 0, 0], [0, 0, 1]]) == 2, name
    assert solver.shortestBridge(
        [[1, 1, 1, 1, 1],
         [1, 0, 0, 0, 1],
         [1, 0, 1, 0, 1],
         [1, 0, 0, 0, 1],
         [1, 1, 1, 1, 1]]) == 1, name
    assert solver.shortestBridge([[1, 0, 0], [0, 0, 0], [0, 0, 1]]) == 3, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionRecursiveDFS())
