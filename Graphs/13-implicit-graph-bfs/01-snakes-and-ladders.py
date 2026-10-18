"""
Snakes and Ladders  ·  LeetCode 909  ·  Medium
Group 13 — Implicit-Graph BFS

State = a board square 1..n^2. Move = one die roll (+1..+6, capped), then the
forced snake/ladder at that square (once). Every move costs 1, so BFS gives the
minimum number of rolls.

The fiddly part: the board is numbered boustrophedon (zigzag), so square s maps
to a cell via a small formula.

Run:  python 01-snakes-and-ladders.py
"""

from collections import deque
from typing import List


class Solution:
    def snakesAndLadders(self, board: List[List[int]]) -> int:
        n = len(board)
        target = n * n

        def get_dest(s: int) -> int:
            s0 = s - 1
            row_from_bottom, col = divmod(s0, n)
            r = n - 1 - row_from_bottom
            c = col if row_from_bottom % 2 == 0 else n - 1 - col
            return board[r][c]

        seen = {1}
        q = deque([(1, 0)])
        while q:
            square, rolls = q.popleft()
            if square == target:
                return rolls
            for roll in range(1, 7):
                nxt = square + roll
                if nxt > target:
                    break
                dest = get_dest(nxt)
                if dest != -1:
                    nxt = dest
                if nxt not in seen:
                    seen.add(nxt)
                    q.append((nxt, rolls + 1))
        return -1


def _run_tests() -> None:
    sol = Solution()

    b1 = [
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, 35, -1, -1, 13, -1],
        [-1, -1, -1, -1, -1, -1],
        [-1, 15, -1, -1, -1, -1],
    ]
    assert sol.snakesAndLadders(b1) == 4
    assert sol.snakesAndLadders([[-1, -1], [-1, 3]]) == 1
    assert sol.snakesAndLadders([[-1]]) == 0
    assert sol.snakesAndLadders([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]]) == 1
    assert sol.snakesAndLadders([[-1, -1, -1, -1],
                                 [-1, -1, -1, -1],
                                 [-1, -1, -1, -1],
                                 [-1, -1, -1, -1]]) == 3

    print("Solution: all tests passed")


if __name__ == "__main__":
    _run_tests()
