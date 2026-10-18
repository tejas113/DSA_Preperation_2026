"""
Clone Graph  ·  LeetCode 133  ·  Medium
Group 05 — Hashmap + Traversal (structural copy)

Deep-copy a connected undirected graph of Node objects. The old-node -> new-node
map IS the visited set AND the output at the same time. Register a clone in the
map BEFORE recursing into its neighbors -- otherwise any cycle (and this graph
is guaranteed connected, so cycles are the norm) causes infinite recursion.

Run:  python 01-clone-graph.py
"""

from collections import deque
from typing import Optional


class Node:
    def __init__(self, val=0, neighbors=None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []


class Solution:
    """Primary: recursive DFS with an old->new map."""

    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if node is None:
            return None

        old_to_new = {}

        def dfs(n: 'Node') -> 'Node':
            if n in old_to_new:
                return old_to_new[n]

            copy = Node(n.val)
            old_to_new[n] = copy            # register BEFORE recursing into neighbors
            for nei in n.neighbors:
                copy.neighbors.append(dfs(nei))
            return copy

        return dfs(node)


class SolutionBFS:
    """Alternative: BFS with the same map, marking on first-sight (enqueue)."""

    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        if node is None:
            return None

        old_to_new = {node: Node(node.val)}
        q = deque([node])

        while q:
            curr = q.popleft()
            for nei in curr.neighbors:
                if nei not in old_to_new:
                    old_to_new[nei] = Node(nei.val)
                    q.append(nei)
                old_to_new[curr].neighbors.append(old_to_new[nei])

        return old_to_new[node]


# --- test helpers -----------------------------------------------------------

def build_graph(adj):
    """adj[i] is the list of 1-indexed neighbor values for node i+1."""
    if not adj:
        return None
    nodes = {i + 1: Node(i + 1) for i in range(len(adj))}
    for i, neighbor_vals in enumerate(adj):
        nodes[i + 1].neighbors = [nodes[v] for v in neighbor_vals]
    return nodes[1]


def to_adjlist(start):
    """BFS the graph, return {val: sorted neighbor vals} for structural comparison."""
    if start is None:
        return {}
    seen = {start.val: start}
    q = [start]
    result = {}
    while q:
        node = q.pop()
        result[node.val] = sorted(n.val for n in node.neighbors)
        for nei in node.neighbors:
            if nei.val not in seen:
                seen[nei.val] = nei
                q.append(nei)
    return result


def _run_tests(solver) -> None:
    name = type(solver).__name__

    original = build_graph([[2, 4], [1, 3], [2, 4], [1, 3]])
    clone = solver.cloneGraph(original)

    assert to_adjlist(clone) == to_adjlist(original), name    # same shape
    assert clone is not original, name                         # different object

    # confirm every cloned node is a NEW object, not a reused original
    orig_ids = set()
    stack = [original]
    seen_orig = {original}
    while stack:
        n = stack.pop()
        orig_ids.add(id(n))
        for nei in n.neighbors:
            if nei not in seen_orig:
                seen_orig.add(nei)
                stack.append(nei)

    seen_clone_ids, stack = set(), [clone]
    while stack:
        n = stack.pop()
        if id(n) in seen_clone_ids:
            continue
        seen_clone_ids.add(id(n))
        assert id(n) not in orig_ids, name
        stack.extend(n.neighbors)

    assert solver.cloneGraph(None) is None, name

    single = build_graph([[]])
    single_clone = solver.cloneGraph(single)
    assert single_clone.val == 1 and single_clone.neighbors == [], name
    assert single_clone is not single, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionBFS())
