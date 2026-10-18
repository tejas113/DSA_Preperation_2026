"""
Accounts Merge  ·  LeetCode 721  ·  Medium
Group 07 — Union-Find

DSU over EMAIL strings (accounts connect only via shared emails). Remap each
distinct email to an int id, union all emails within each account, group emails
by DSU root, sort each group, prepend the owner's name.

Run:  python 05-accounts-merge.py
"""

from collections import defaultdict, deque
from typing import List


class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.rank[ra] < self.rank[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        if self.rank[ra] == self.rank[rb]:
            self.rank[ra] += 1
        return True


class Solution:
    """Primary: DSU over email ids."""

    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        email_id = {}                        # email -> integer id
        email_name = {}                      # email -> owner's name

        for account in accounts:
            name = account[0]
            for email in account[1:]:
                if email not in email_id:
                    email_id[email] = len(email_id)
                email_name[email] = name

        dsu = DSU(len(email_id))
        for account in accounts:
            emails = account[1:]
            for e in emails[1:]:
                dsu.union(email_id[emails[0]], email_id[e])

        groups = defaultdict(list)
        for email, eid in email_id.items():
            groups[dsu.find(eid)].append(email)

        return [[email_name[emails[0]]] + sorted(emails) for emails in groups.values()]


class SolutionBFS:
    """Alternative: build an email adjacency graph, BFS each component."""

    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        graph = defaultdict(set)
        email_name = {}

        for account in accounts:
            name, emails = account[0], account[1:]
            for e in emails:
                email_name[e] = name
                graph[emails[0]].add(e)
                graph[e].add(emails[0])

        seen = set()
        result = []
        for email in graph:
            if email in seen:
                continue
            q = deque([email])
            seen.add(email)
            component = []
            while q:
                cur = q.popleft()
                component.append(cur)
                for nei in graph[cur]:
                    if nei not in seen:
                        seen.add(nei)
                        q.append(nei)
            result.append([email_name[email]] + sorted(component))
        return result


def _run_tests(solver) -> None:
    name = type(solver).__name__

    out = solver.accountsMerge([
        ["John", "johnsmith@mail.com", "john_newyork@mail.com"],
        ["John", "johnsmith@mail.com", "john00@mail.com"],
        ["Mary", "mary@mail.com"],
        ["John", "johnnybravo@mail.com"],
    ])
    assert sorted(out) == sorted([
        ["John", "john00@mail.com", "john_newyork@mail.com", "johnsmith@mail.com"],
        ["John", "johnnybravo@mail.com"],
        ["Mary", "mary@mail.com"],
    ]), name

    assert sorted(solver.accountsMerge([["A", "a@x.com"], ["B", "b@x.com"]])) == \
        sorted([["A", "a@x.com"], ["B", "b@x.com"]]), name

    assert sorted(solver.accountsMerge([
        ["X", "1@x.com", "2@x.com"],
        ["X", "2@x.com", "3@x.com"],
        ["X", "3@x.com", "4@x.com"],
    ])) == sorted([["X", "1@x.com", "2@x.com", "3@x.com", "4@x.com"]]), name

    assert sorted(solver.accountsMerge([["Bob", "b1@x.com"], ["Bob", "b2@x.com"]])) == \
        sorted([["Bob", "b1@x.com"], ["Bob", "b2@x.com"]]), name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionBFS())
