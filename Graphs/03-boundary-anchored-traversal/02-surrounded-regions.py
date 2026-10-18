"""
Surrounded Regions  ·  LeetCode 130  ·  Medium
Group 03 — Boundary-Anchored Traversal

Flood from every border-touching 'O' inward (plain adjacency -- no reversal
needed, unlike Pacific Atlantic, since "connected" is symmetric). Everything the
flood does NOT reach was fully surrounded -> flip to 'X'. Everything it reaches
stays 'O'. The '#' placeholder doubles as the visited mark.

Run:  python 02-surrounded-regions.py
"""

from collections import deque
from typing import List

DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def solve(self, board: List[List[str]]) -> None:
        """Do not return anything, modify board in-place instead."""
        if not board or not board[0]:
            return

        m, n = len(board), len(board[0])
        q = deque()

        for r in range(m):
            for c in range(n):
                if (r == 0 or r == m - 1 or c == 0 or c == n - 1) and board[r][c] == "O":
                    board[r][c] = "#"          # mark safe + visited
                    q.append((r, c))

        while q:
            r, c = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and board[nr][nc] == "O":
                    board[nr][nc] = "#"
                    q.append((nr, nc))

        for r in range(m):
            for c in range(n):
                if board[r][c] == "O":
                    board[r][c] = "X"          # never reached -> captured
                elif board[r][c] == "#":
                    board[r][c] = "O"          # reached -> safe, restore


def _run_tests() -> None:
    sol = Solution()

    board = [["X", "X", "X", "X"],
             ["X", "O", "O", "X"],
             ["X", "X", "O", "X"],
             ["X", "O", "X", "X"]]
    sol.solve(board)
    assert board == [["X", "X", "X", "X"],
                      ["X", "X", "X", "X"],
                      ["X", "X", "X", "X"],
                      ["X", "O", "X", "X"]]

    all_x = [["X"]]
    sol.solve(all_x)
    assert all_x == [["X"]]

    single_o = [["O"]]                 # the only cell IS the border -> safe
    sol.solve(single_o)
    assert single_o == [["O"]]

    ring = [["O", "O", "O"],
            ["O", "X", "O"],
            ["O", "O", "O"]]           # ring touches the border -> all stay 'O'
    sol.solve(ring)
    assert ring == [["O", "O", "O"],
                     ["O", "X", "O"],
                     ["O", "O", "O"]]

    fully_boxed = [["X", "X", "X"],
                   ["X", "O", "X"],
                   ["X", "X", "X"]]
    sol.solve(fully_boxed)
    assert fully_boxed == [["X", "X", "X"],
                            ["X", "X", "X"],
                            ["X", "X", "X"]]

    print("Solution: all tests passed")


if __name__ == "__main__":
    _run_tests()
