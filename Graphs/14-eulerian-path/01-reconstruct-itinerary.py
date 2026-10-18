"""
Reconstruct Itinerary  ·  LeetCode 332  ·  Hard
Group 14 — Eulerian Path

Find the lexicographically smallest Eulerian path from "JFK" (use every ticket
exactly once). Hierholzer's algorithm: DFS taking the smallest next edge, append
each node to the route ON THE WAY OUT (post-order), reverse at the end.

Run:  python 01-reconstruct-itinerary.py
"""

import heapq
from collections import defaultdict
from typing import List


class Solution:
    """Primary: recursive Hierholzer."""

    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        graph = defaultdict(list)
        for src, dst in tickets:
            heapq.heappush(graph[src], dst)        # min-heap -> smallest ticket first

        route = []

        def dfs(node: str) -> None:
            while graph[node]:
                dfs(heapq.heappop(graph[node]))    # consume a ticket, fly there
            route.append(node)                     # POST-ORDER

        dfs("JFK")
        return route[::-1]


class SolutionIterative:
    """Alternative: iterative Hierholzer with an explicit stack."""

    def findItinerary(self, tickets: List[List[str]]) -> List[str]:
        graph = defaultdict(list)
        for src, dst in tickets:
            heapq.heappush(graph[src], dst)

        stack = ["JFK"]
        route = []
        while stack:
            while graph[stack[-1]]:
                stack.append(heapq.heappop(graph[stack[-1]]))
            route.append(stack.pop())
        return route[::-1]


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.findItinerary(
        [["MUC", "LHR"], ["JFK", "MUC"], ["SFO", "SJC"], ["LHR", "SFO"]]
    ) == ["JFK", "MUC", "LHR", "SFO", "SJC"], name

    assert solver.findItinerary(
        [["JFK", "SFO"], ["JFK", "ATL"], ["SFO", "ATL"], ["ATL", "JFK"], ["ATL", "SFO"]]
    ) == ["JFK", "ATL", "JFK", "SFO", "ATL", "SFO"], name

    assert solver.findItinerary([["JFK", "AAA"]]) == ["JFK", "AAA"], name
    assert solver.findItinerary(
        [["JFK", "KUL"], ["JFK", "NRT"], ["NRT", "JFK"]]
    ) == ["JFK", "NRT", "JFK", "KUL"], name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionIterative())
