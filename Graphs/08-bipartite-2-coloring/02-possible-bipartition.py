"""
Possible Bipartition  ·  LeetCode 886  ·  Medium
Group 08 — Bipartite / 2-Coloring

Is Graph Bipartite?, but you build the adjacency list from a list of "dislikes"
pairs first. People are 1-indexed -> color array sized n + 1.

Run:  python 02-possible-bipartition.py
"""

from collections import defaultdict, deque
from typing import List


class Solution:
    """Primary: build adjacency list from dislikes, then BFS 2-coloring."""

    def possibleBipartition(self, n: int, dislikes: List[List[int]]) -> bool:
        graph = defaultdict(list)
        for a, b in dislikes:
            graph[a].append(b)
            graph[b].append(a)

        color = [0] * (n + 1)                  # 1-indexed people; index 0 unused

        for start in range(1, n + 1):
            if color[start] != 0:
                continue
            color[start] = 1
            q = deque([start])
            while q:
                node = q.popleft()
                for nei in graph[node]:
                    if color[nei] == 0:
                        color[nei] = -color[node]
                        q.append(nei)
                    elif color[nei] == color[node]:
                        return False
        return True


def _run_tests() -> None:
    sol = Solution()

    assert sol.possibleBipartition(4, [[1, 2], [1, 3], [2, 4]]) is True
    assert sol.possibleBipartition(3, [[1, 2], [1, 3], [2, 3]]) is False
    assert sol.possibleBipartition(5, [[1, 2], [2, 3], [3, 4], [4, 5], [1, 5]]) is False
    assert sol.possibleBipartition(5, [[1, 2], [3, 4], [4, 5], [3, 5]]) is False   # triangle 3-4-5
    assert sol.possibleBipartition(4, []) is True
    assert sol.possibleBipartition(1, []) is True
    assert sol.possibleBipartition(10, [[1, 2], [3, 4], [5, 6], [7, 8], [9, 10]]) is True

    print("Solution: all tests passed")


if __name__ == "__main__":
    _run_tests()
