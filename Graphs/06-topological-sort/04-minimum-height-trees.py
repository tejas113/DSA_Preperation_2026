"""
Minimum Height Trees  ·  LeetCode 310  ·  Medium  ·  (supplementary)
Group 06 — Topological Sort / Cycle Detection

Leaf-peeling: Kahn's "remove the boundary inward" idea for an undirected tree.
Repeatedly strip ALL degree-1 nodes, one whole layer at a time, until <= 2 nodes
remain -- those are the 1 or 2 centers (minimum-height roots).

Run:  python 04-minimum-height-trees.py
"""

from collections import defaultdict, deque
from typing import List


class Solution:
    """Primary: leaf-peeling (BFS by degree)."""

    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if n <= 2:
            return list(range(n))

        graph = defaultdict(set)
        for a, b in edges:
            graph[a].add(b)
            graph[b].add(a)

        degree = [len(graph[i]) for i in range(n)]
        leaves = deque(i for i in range(n) if degree[i] == 1)
        remaining = n

        while remaining > 2:
            layer = len(leaves)
            remaining -= layer
            for _ in range(layer):
                leaf = leaves.popleft()
                for nei in graph[leaf]:
                    degree[nei] -= 1
                    if degree[nei] == 1:
                        leaves.append(nei)

        return list(leaves)


class SolutionDiameter:
    """Alternative: find a diameter with two BFS passes, return its middle 1-2 nodes."""

    def findMinHeightTrees(self, n: int, edges: List[List[int]]) -> List[int]:
        if n <= 2:
            return list(range(n))

        graph = defaultdict(list)
        for a, b in edges:
            graph[a].append(b)
            graph[b].append(a)

        def bfs_farthest(start):
            parent = {start: None}
            q = deque([start])
            last = start
            while q:
                node = q.popleft()
                last = node
                for nei in graph[node]:
                    if nei not in parent:
                        parent[nei] = node
                        q.append(nei)
            return last, parent

        u, _ = bfs_farthest(0)
        v, parent = bfs_farthest(u)

        path = []
        cur = v
        while cur is not None:
            path.append(cur)
            cur = parent[cur]

        L = len(path)
        return [path[L // 2]] if L % 2 else [path[L // 2 - 1], path[L // 2]]


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert sorted(solver.findMinHeightTrees(4, [[1, 0], [1, 2], [1, 3]])) == [1], name
    assert sorted(solver.findMinHeightTrees(
        6, [[3, 0], [3, 1], [3, 2], [3, 4], [5, 4]])) == [3, 4], name
    assert solver.findMinHeightTrees(1, []) == [0], name
    assert sorted(solver.findMinHeightTrees(2, [[0, 1]])) == [0, 1], name
    assert sorted(solver.findMinHeightTrees(5, [[0, 1], [1, 2], [2, 3], [3, 4]])) == [2], name
    assert sorted(solver.findMinHeightTrees(4, [[0, 1], [1, 2], [2, 3]])) == [1, 2], name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionDiameter())
