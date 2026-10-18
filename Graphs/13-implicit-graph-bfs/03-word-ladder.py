"""
Word Ladder  ·  LeetCode 127  ·  Hard
Group 13 — Implicit-Graph BFS  (the canonical one)

BFS over words. neighbors(w) = every one-letter change that is in wordList.
The answer counts WORDS (nodes), not changes -- seed the length at 1.

Run:  python 03-word-ladder.py
"""

import string
from collections import defaultdict, deque
from typing import List


class Solution:
    """Primary: BFS, generating the L * 25 one-letter variants per word."""

    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        word_set = set(wordList)
        if endWord not in word_set:
            return 0

        seen = {beginWord}
        q = deque([(beginWord, 1)])             # length in WORDS -> starts at 1
        while q:
            word, length = q.popleft()
            if word == endWord:
                return length
            for i in range(len(word)):
                for c in string.ascii_lowercase:
                    if c != word[i]:
                        nxt = word[:i] + c + word[i + 1:]
                        if nxt in word_set and nxt not in seen:
                            seen.add(nxt)
                            q.append((nxt, length + 1))
        return 0


class SolutionWildcard:
    """Alternative: precompute a wildcard-pattern adjacency index -> O(L) neighbor
    lookup, no alphabet enumeration."""

    def ladderLength(self, beginWord: str, endWord: str, wordList: List[str]) -> int:
        word_set = set(wordList)
        if endWord not in word_set:
            return 0

        L = len(beginWord)
        patterns = defaultdict(list)
        for w in word_set:
            for i in range(L):
                patterns[w[:i] + "*" + w[i + 1:]].append(w)

        seen = {beginWord}
        q = deque([(beginWord, 1)])
        while q:
            word, length = q.popleft()
            if word == endWord:
                return length
            for i in range(L):
                for nxt in patterns[word[:i] + "*" + word[i + 1:]]:
                    if nxt not in seen:
                        seen.add(nxt)
                        q.append((nxt, length + 1))
        return 0


def _run_tests(solver) -> None:
    name = type(solver).__name__

    assert solver.ladderLength("hit", "cog",
                               ["hot", "dot", "dog", "lot", "log", "cog"]) == 5, name
    assert solver.ladderLength("hit", "cog",
                               ["hot", "dot", "dog", "lot", "log"]) == 0, name
    assert solver.ladderLength("a", "c", ["a", "b", "c"]) == 2, name
    assert solver.ladderLength("hot", "dog", ["hot", "dog"]) == 0, name
    assert solver.ladderLength("hot", "dog", ["hot", "dog", "dot"]) == 3, name
    assert solver.ladderLength("hit", "hot", ["hot"]) == 2, name

    print(f"{name}: all tests passed")


if __name__ == "__main__":
    _run_tests(Solution())
    _run_tests(SolutionWildcard())
