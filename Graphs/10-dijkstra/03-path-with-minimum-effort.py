"""
Path With Minimum Effort  ·  LeetCode 1631  ·  Medium
Group 10 — Dijkstra (minimize-max variant)

Swim in Rising Water, with two tiny changes:
  - the cost lives on EDGES: abs(height[cell] - height[neighbor])
  - the start is seeded at effort 0 (no step taken yet), not grid[0][0]
Relaxation:  ne = max(e, abs(diff))

Run:  python 03-path-with-minimum-effort.py
"""

import heapq
from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    """Primary: minimize-max Dijkstra on edge height-differences."""

    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        m, n = len(heights), len(heights[0])
        effort = [[float("inf")] * n for _ in range(m)]
        effort[0][0] = 0
        heap = [(0, 0, 0)]                      # (effort so far, r, c)

        while heap:
            e, r, c = heapq.heappop(heap)
            if (r, c) == (m - 1, n - 1):
                return e
            if e > effort[r][c]:
                continue
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n:
                    ne = max(e, abs(heights[nr][nc] - heights[r][c]))
                    if ne < effort[nr][nc]:
                        effort[nr][nc] = ne
                        heapq.heappush(heap, (ne, nr, nc))

        return 0


class SolutionBinarySearch:
    """Alternative: binary search the effort budget B + BFS reachability."""

    def minimumEffortPath(self, heights: List[List[int]]) -> int:
        m, n = len(heights), len(heights[0])

        def can(B: int) -> bool:
            seen = {(0, 0)}
            q = deque([(0, 0)])
            while q:
                r, c = q.popleft()
                if (r, c) == (m - 1, n - 1):
                    return True
                for dr, dc in DIRS:
                    nr, nc = r + dr, c + dc
                    if (0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen
                            and abs(heights[nr][nc] - heights[r][c]) <= B):
                        seen.add((nr, nc))
                        q.append((nr, nc))
            return False

        lo, hi = 0, 10 ** 6
        while lo < hi:
            mid = (lo + hi) // 2
            if can(mid):
                hi = mid
            else:
                lo = mid + 1
        return lo


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.minimumEffortPath([[1, 2, 2], [3, 8, 2], [5, 3, 5]]) == 2, name
    assert solver.minimumEffortPath([[1, 2, 3], [3, 8, 4], [5, 3, 5]]) == 1, name
    assert solver.minimumEffortPath([
        [1, 2, 1, 1, 1],
        [1, 2, 1, 2, 1],
        [1, 2, 1, 2, 1],
        [1, 2, 1, 2, 1],
        [1, 1, 1, 2, 1],
    ]) == 0, name
    assert solver.minimumEffortPath([[1]]) == 0, name
    assert solver.minimumEffortPath([[1, 10, 6, 7, 9, 10, 4, 9]]) == 9, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionBinarySearch())
