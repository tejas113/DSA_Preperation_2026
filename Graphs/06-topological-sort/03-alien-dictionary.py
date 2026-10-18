"""
Alien Dictionary  ·  LeetCode 269  ·  Hard  ·  premium
Group 06 — Topological Sort / Cycle Detection

The words are sorted by an unknown alphabet order. BUILD the graph: for each pair
of ADJACENT words, the FIRST differing character gives one edge (earlier -> later).
Then Kahn's algorithm.

Return "" if:  a cycle (contradiction), OR an invalid prefix ("abc" before "ab").

Run:  python 03-alien-dictionary.py
"""

from collections import deque
from typing import List


class Solution:
    """Primary: build graph from adjacent words, then Kahn's algorithm."""

    def alienOrder(self, words: List[str]) -> str:
        graph = {c: set() for w in words for c in w}
        indegree = {c: 0 for c in graph}

        for w1, w2 in zip(words, words[1:]):
            found_diff = False
            for i in range(min(len(w1), len(w2))):
                if w1[i] != w2[i]:
                    if w2[i] not in graph[w1[i]]:
                        graph[w1[i]].add(w2[i])
                        indegree[w2[i]] += 1
                    found_diff = True
                    break
            if not found_diff and len(w1) > len(w2):
                return ""                         # "abc" before "ab" -> invalid

        q = deque(c for c in indegree if indegree[c] == 0)
        order = []
        while q:
            c = q.popleft()
            order.append(c)
            for nei in graph[c]:
                indegree[nei] -= 1
                if indegree[nei] == 0:
                    q.append(nei)

        return "".join(order) if len(order) == len(indegree) else ""


def _is_valid_alien_order(result: str, words: List[str]) -> bool:
    """True iff `result` is a permutation of all letters in `words` that is
    consistent with every adjacent-word ordering constraint."""
    all_chars = {c for w in words for c in w}
    if set(result) != all_chars or len(result) != len(all_chars):
        return False
    pos = {c: i for i, c in enumerate(result)}
    for w1, w2 in zip(words, words[1:]):
        diff = False
        for i in range(min(len(w1), len(w2))):
            if w1[i] != w2[i]:
                if pos[w1[i]] >= pos[w2[i]]:
                    return False
                diff = True
                break
        if not diff and len(w1) > len(w2):
            return False
    return True


def _run_tests() -> None:
    sol = Solution()

    assert sol.alienOrder(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"
    assert sol.alienOrder(["z", "x"]) == "zx"
    assert sol.alienOrder(["z", "x", "z"]) == ""          # contradiction (cycle)
    assert sol.alienOrder(["abc", "ab"]) == ""             # invalid prefix
    assert sol.alienOrder(["a", "b", "a"]) == ""           # contradiction
    assert sol.alienOrder(["abc"]) == "abc"                # one word: any order

    r = sol.alienOrder(["ac", "ab", "zc", "zb"])
    assert _is_valid_alien_order(r, ["ac", "ab", "zc", "zb"]), r

    words2 = ["ba", "bc", "ac", "ca"]        # constraints: a<c, b<a  ->  "bac"
    assert _is_valid_alien_order(sol.alienOrder(words2), words2), sol.alienOrder(words2)

    # a genuinely contradictory dictionary (b<a from "bc","ac" and a<b from "cda","cdb")
    assert sol.alienOrder(["ba", "bc", "ac", "cab", "cda", "cdb"]) == ""

    print("Solution: all tests passed")


if __name__ == "__main__":
    _run_tests()
