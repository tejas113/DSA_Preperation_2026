"""
Walls and Gates  ·  LeetCode 286  ·  Medium  ·  premium
Group 02 — Multi-Source BFS

Fill every empty room in-place with its distance to the nearest gate.
  -1           = wall
   0           = gate
   2147483647  = empty room (INF)

Multi-source BFS: seed the queue with EVERY gate at distance 0, then expand.
Writing the real distance over INF doubles as the visited mark (Flood Fill trick).

Run:  python 01-walls-and-gates.py
"""

from collections import deque
from typing import List

INF = 2147483647
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))


class Solution:
    def wallsAndGates(self, rooms: List[List[int]]) -> None:
        """Do not return anything, modify rooms in-place instead."""
        if not rooms or not rooms[0]:
            return

        m, n = len(rooms), len(rooms[0])
        q = deque()

        for r in range(m):                      # seed the queue with EVERY gate
            for c in range(n):
                if rooms[r][c] == 0:
                    q.append((r, c))

        while q:
            r, c = q.popleft()
            for dr, dc in DIRS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < m and 0 <= nc < n and rooms[nr][nc] == INF:
                    rooms[nr][nc] = rooms[r][c] + 1     # write distance == mark visited
                    q.append((nr, nc))


def _run_tests() -> None:
    sol = Solution()

    rooms = [
        [INF, -1, 0, INF],
        [INF, INF, INF, -1],
        [INF, -1, INF, -1],
        [0, -1, INF, INF],
    ]
    sol.wallsAndGates(rooms)
    assert rooms == [
        [3, -1, 0, 1],
        [2, 2, 1, -1],
        [1, -1, 2, -1],
        [0, -1, 3, 4],
    ]

    no_gates = [[INF, INF], [INF, INF]]
    sol.wallsAndGates(no_gates)
    assert no_gates == [[INF, INF], [INF, INF]]        # nothing reachable -> unchanged

    sealed = [[0, -1], [-1, INF]]
    sol.wallsAndGates(sealed)
    assert sealed == [[0, -1], [-1, INF]]              # sealed off -> stays INF

    single_gate = [[0]]
    sol.wallsAndGates(single_gate)
    assert single_gate == [[0]]

    # small hand-traced grid (see the .md dry run)
    small = [
        [INF, -1, 0],
        [INF, INF, INF],
        [-1, INF, INF],
    ]
    sol.wallsAndGates(small)
    assert small == [
        [4, -1, 0],
        [3, 2, 1],
        [-1, 3, 2],
    ]

    print("Solution: all tests passed")


if __name__ == "__main__":
    _run_tests()
