"""
Course Schedule  ·  LeetCode 207  ·  Medium
Group 06 — Topological Sort / Cycle Detection

"Can you finish all courses?" == "does the prerequisite graph have no cycle?"
Kahn's algorithm answers both at once: if every course can be peeled off by
repeatedly removing indegree-0 nodes, there's no cycle.

Run:  python 01-course-schedule.py
"""

from collections import defaultdict, deque
from typing import List


class Solution:
    """Primary: Kahn's algorithm (BFS, indegree-based)."""

    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = defaultdict(list)
        indegree = [0] * numCourses

        for a, b in prerequisites:            # "a requires b" -> edge b -> a
            graph[b].append(a)
            indegree[a] += 1

        q = deque(course for course in range(numCourses) if indegree[course] == 0)
        processed = 0

        while q:
            course = q.popleft()
            processed += 1
            for nei in graph[course]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    q.append(nei)

        return processed == numCourses


class SolutionDFS:
    """Alternative: DFS with 3 colors (white/gray/black) for directed cycle
    detection. Never use a single `visited` set here -- see concepts/06's
    "diamond trap" for why that silently gives wrong answers."""

    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        graph = defaultdict(list)
        for a, b in prerequisites:
            graph[b].append(a)

        WHITE, GRAY, BLACK = 0, 1, 2
        color = [WHITE] * numCourses

        def dfs(node: int) -> bool:
            color[node] = GRAY
            for nei in graph[node]:
                if color[nei] == GRAY:
                    return False            # back edge to an ancestor -> cycle
                if color[nei] == WHITE and not dfs(nei):
                    return False
            color[node] = BLACK
            return True

        return all(color[c] != WHITE or dfs(c) for c in range(numCourses))


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.canFinish(2, [[1, 0]]) is True, name
    assert solver.canFinish(2, [[1, 0], [0, 1]]) is False, name
    assert solver.canFinish(4, [[1, 0], [2, 0], [3, 1], [3, 2]]) is True, name
    assert solver.canFinish(1, []) is True, name
    assert solver.canFinish(3, [[0, 1], [1, 2], [2, 0]]) is False, name
    assert solver.canFinish(5, []) is True, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionDFS())
