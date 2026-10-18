"""
Flood Fill  ·  LeetCode 733  ·  Easy
Group 01 — Grid Flood-Fill

Single-source flood fill: recolor the connected same-color region around (sr, sc).

Key trick : the recolor itself is the "visited" mark -> no visited set needed.
Key guard : if start_color == color, return early (else infinite recursion).

Run:  python 02-flood-fill.py
"""

from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    """Primary: recursive DFS."""

    def floodFill(self, image: List[List[int]], sr: int, sc: int,
                  color: int) -> List[List[int]]:
        m, n = len(image), len(image[0])
        start_color = image[sr][sc]

        if start_color == color:            # nothing to do; avoids infinite recursion
            return image

        def dfs(r: int, c: int) -> None:
            if not (0 <= r < m and 0 <= c < n):     # off the board
                return
            if image[r][c] != start_color:          # wrong color OR already recolored
                return
            image[r][c] = color                     # recolor == mark visited
            for dr, dc in DIRS:
                dfs(r + dr, c + dc)

        dfs(sr, sc)
        return image


class SolutionBFS:
    """Alternative: BFS — no recursion-depth risk on a huge single-color region."""

    def floodFill(self, image: List[List[int]], sr: int, sc: int,
                  color: int) -> List[List[int]]:
        m, n = len(image), len(image[0])
        start_color = image[sr][sc]
        if start_color == color:
            return image

        q = deque([(sr, sc)])
        image[sr][sc] = color                       # recolor on enqueue

        while q:
            r, c = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and image[nr][nc] == start_color:
                    image[nr][nc] = color
                    q.append((nr, nc))
        return image


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.floodFill([[1, 1, 1], [1, 1, 0], [1, 0, 1]], 1, 1, 2) == \
        [[2, 2, 2], [2, 2, 0], [2, 0, 1]], name

    # start color already equals target -> unchanged (infinite-loop guard)
    assert solver.floodFill([[0, 0, 0], [0, 0, 0]], 0, 0, 0) == \
        [[0, 0, 0], [0, 0, 0]], name

    assert solver.floodFill([[5]], 0, 0, 9) == [[9]], name

    assert solver.floodFill([[1, 2, 1], [2, 1, 2], [1, 2, 1]], 1, 1, 7) == \
        [[1, 2, 1], [2, 7, 2], [1, 2, 1]], name

    assert solver.floodFill([[3, 3], [3, 3]], 0, 0, 4) == [[4, 4], [4, 4]], name

    # corner start, L-shaped region
    assert solver.floodFill([[1, 1, 0], [0, 1, 0], [0, 1, 1]], 0, 0, 9) == \
        [[9, 9, 0], [0, 9, 0], [0, 9, 9]], name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionBFS())
