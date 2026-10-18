"""
Minimum Genetic Mutation  ·  LeetCode 433  ·  Medium
Group 13 — Implicit-Graph BFS

Word Ladder with length fixed at 8 and a 4-letter alphabet. BFS over gene
strings; neighbors = every one-character change that is in `bank`. Count levels.

Run:  python 02-minimum-genetic-mutation.py
"""

from collections import deque
from typing import List


class Solution:
    def minMutation(self, startGene: str, endGene: str, bank: List[str]) -> int:
        if startGene == endGene:
            return 0

        bank_set = set(bank)
        if endGene not in bank_set:
            return -1

        seen = {startGene}
        q = deque([(startGene, 0)])
        while q:
            gene, steps = q.popleft()
            if gene == endGene:
                return steps
            for i in range(8):
                for c in "ACGT":
                    if c != gene[i]:
                        nxt = gene[:i] + c + gene[i + 1:]
                        if nxt in bank_set and nxt not in seen:
                            seen.add(nxt)
                            q.append((nxt, steps + 1))
        return -1


def _run_tests() -> None:
    sol = Solution()

    assert sol.minMutation("AACCGGTT", "AACCGGTA", ["AACCGGTA"]) == 1
    assert sol.minMutation("AACCGGTT", "AAACGGTA",
                           ["AACCGGTA", "AACCGCTA", "AAACGGTA"]) == 2
    assert sol.minMutation("AAAAACCC", "AACCCCCC",
                           ["AAAACCCC", "AAACCCCC", "AACCCCCC"]) == 3
    assert sol.minMutation("AACCGGTT", "AACCGGTA", []) == -1
    assert sol.minMutation("AAAAAAAA", "AAAAAAAA", []) == 0
    assert sol.minMutation("AAAAAAAA", "CCCCCCCC", ["AAAAAAAC", "AAAAAACC"]) == -1

    print("Solution: all tests passed")


if __name__ == "__main__":
    _run_tests()
