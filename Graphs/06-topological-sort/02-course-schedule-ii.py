"""
Course Schedule II  ·  LeetCode 210  ·  Medium
Group 06 — Topological Sort / Cycle Detection

Course Schedule, but return the actual order. Kahn's dequeue sequence IS a valid
topological order -- just keep the list instead of counting. Return [] on a cycle
(len(order) < numCourses).

Run:  python 02-course-schedule-ii.py
"""

from collections import defaultdict, deque
from typing import List


class Solution:
    """Primary: Kahn's algorithm, keeping the order list."""

    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        graph = defaultdict(list)
        indegree = [0] * numCourses

        for a, b in prerequisites:            # "a requires b" -> edge b -> a
            graph[b].append(a)
            indegree[a] += 1

        q = deque(course for course in range(numCourses) if indegree[course] == 0)
        order = []

        while q:
            course = q.popleft()
            order.append(course)
            for nei in graph[course]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    q.append(nei)

        return order if len(order) == numCourses else []


class SolutionDFS:
    """Alternative: DFS post-order (reverse the finish order)."""

    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        graph = defaultdict(list)
        for a, b in prerequisites:
            graph[b].append(a)

        WHITE, GRAY, BLACK = 0, 1, 2
        color = [WHITE] * numCourses
        order = []

        def dfs(node: int) -> bool:
            color[node] = GRAY
            for nei in graph[node]:
                if color[nei] == GRAY:
                    return False
                if color[nei] == WHITE and not dfs(nei):
                    return False
            color[node] = BLACK
            order.append(node)          # post-order
            return True

        for c in range(numCourses):
            if color[c] == WHITE and not dfs(c):
                return []
        return order[::-1]


def _is_valid_order(order, numCourses, prerequisites) -> bool:
    if sorted(order) != list(range(numCourses)):
        return False
    position = {course: i for i, course in enumerate(order)}
    return all(position[b] < position[a] for a, b in prerequisites)


def _run_tests(solver) -> None:
    name = type(solver).__name__

    cases = [
        (2, [[1, 0]]),
        (4, [[1, 0], [2, 0], [3, 1], [3, 2]]),
        (1, []),
        (3, []),
        (5, [[1, 0], [2, 1], [3, 2], [4, 3]]),
    ]
    for numCourses, prereqs in cases:
        result = solver.findOrder(numCourses, prereqs)
        assert _is_valid_order(result, numCourses, prereqs), (name, numCourses, prereqs, result)

    # cycles -> empty
    assert solver.findOrder(2, [[0, 1], [1, 0]]) == [], name
    assert solver.findOrder(3, [[1, 0], [2, 1], [0, 2]]) == [], name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionDFS())
