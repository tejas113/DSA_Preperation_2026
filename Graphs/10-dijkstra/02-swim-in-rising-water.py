"""
Swim in Rising Water  ·  LeetCode 778  ·  Hard
Group 10 — Dijkstra (minimize-max variant)

A path's cost is its HIGHEST cell, not its total. Dijkstra with
    nd = max(d, grid[nr][nc])       instead of    nd = d + w
First pop of the destination is the answer (max is monotonic along a path).

Run:  python 02-swim-in-rising-water.py
"""

import heapq
from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    """Primary: minimize-max Dijkstra."""

    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)
        seen = set()
        heap = [(grid[0][0], 0, 0)]             # (max elevation so far, r, c)

        while heap:
            t, r, c = heapq.heappop(heap)
            if (r, c) == (n - 1, n - 1):
                return t
            if (r, c) in seen:
                continue
            seen.add((r, c))
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < n and 0 <= nc < n and (nr, nc) not in seen:
                    heapq.heappush(heap, (max(t, grid[nr][nc]), nr, nc))

        return -1


class SolutionBinarySearch:
    """Alternative: binary search the threshold t + BFS reachability check."""

    def swimInWater(self, grid: List[List[int]]) -> int:
        n = len(grid)

        def can_reach(t: int) -> bool:
            if grid[0][0] > t:
                return False
            seen = {(0, 0)}
            q = deque([(0, 0)])
            while q:
                r, c = q.popleft()
                if (r, c) == (n - 1, n - 1):
                    return True
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < n and 0 <= nc < n
                            and (nr, nc) not in seen and grid[nr][nc] <= t):
                        seen.add((nr, nc))
                        q.append((nr, nc))
            return False

        lo, hi = max(grid[0][0], grid[n - 1][n - 1]), n * n - 1
        while lo < hi:
            mid = (lo + hi) // 2
            if can_reach(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.swimInWater([[0, 2], [1, 3]]) == 3, name
    assert solver.swimInWater([
        [0, 1, 2, 3, 4],
        [24, 23, 22, 21, 5],
        [12, 13, 14, 15, 16],
        [11, 17, 18, 19, 20],
        [10, 9, 8, 7, 6],
    ]) == 16, name
    assert solver.swimInWater([[0]]) == 0, name
    assert solver.swimInWater([[3, 4], [2, 1]]) == 3, name
    assert solver.swimInWater([[1, 2, 3], [4, 5, 6], [7, 8, 9]]) == 9, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionBinarySearch())
