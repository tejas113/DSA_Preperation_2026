# 127. Word Ladder

**LC 127** · **Source:** LC150 + NC150 · **Difficulty:** Hard · **Priority:** Stretch · **Pattern:** BFS on an implicit graph (words are nodes, a one-letter change is an edge)

---

## 1. Intuition

Turn `hit` into `cog` one letter at a time, where every word along the way must be in the dictionary. That's a
shortest path where each step costs 1, so it's BFS. As with Genetic Mutation (#34), nobody gives you the
edges. From each word, try changing every position to every letter `a–z`, and keep only the results that are
real, not-yet-used words.

* **The answer counts words, not steps:** the queue starts at `(beginWord, 1)`, so `beginWord` counts as word 1. `hit → hot → dot → dog → cog` returns `5`.
* **Quick exit:** `if endWord not in word_set: return 0`. If the target isn't a valid word, no ladder can end there.
* **Generate neighbours:** for every `i` and every `c` in `"abc…z"` (skipping `c == word[i]`), `next_word = word[:i] + c + word[i+1:]`. That's up to 25 × L candidates per word.
* **Removing from the set is the visited mark:** `word_set.remove(next_word)` happens **when the word is pushed**, so each word is queued at most once, and the first time it's reached is by the shortest ladder.

**Recall:** Put the words in a set and return `0` if `endWord` is missing. BFS from `(beginWord, 1)`, try every position × `a–z`, and on a hit remove it from the set and push `length + 1`. Return `length` at `endWord`, otherwise `0`.

## 2. Approach

* **Idea:** The shortest transformation sequence is the shortest path in an unweighted graph, so BFS. Two words are connected if they differ in exactly one letter, and the new word is in `wordList`.
* **Graph representation:** **implicit graph**. The nodes are `beginWord` plus the words in `wordList`, and the edges are created on the fly by one-letter changes. Undirected in spirit, unweighted.
* **Data structure / pointers:**
  * `word_set`: words that are allowed **and not yet queued**. A word is removed the moment it's pushed, so the set is also "not visited yet".
  * `queue` (`deque`): `(word, length)`, where `length` = how many words are in the ladder so far, including `beginWord` and `word`.
  * `next_word`: a candidate, which is `word` with position `i` replaced by `c`.
* **Invariant:** words come off `queue` in order of `length`, and each word's single push carries the shortest ladder length that reaches it.
* **Edge cases:**
  * `endWord` not in `wordList`: returns `0` immediately.
  * No ladder exists (the words don't connect): the queue empties, so it returns `0`.
  * `beginWord` doesn't have to be in `wordList`. If it is, it isn't removed at the start, so it may be pushed back once later, which is harmless and can't shorten the answer.
  * `beginWord == endWord` isn't allowed on LC. If it happened, it would return `1` (as long as `endWord` is in the list).
  * Duplicate words in `wordList`: the `set` removes them.
  * It's iterative, so there's no recursion-depth risk.
  * **Common follow-up:** *bidirectional BFS*. Search from both ends at once, always growing the smaller frontier, and stop when they meet. It's the same big-O, but in practice it explores far fewer words.

## 3. Code

```python
from collections import deque
from typing import List


class Solution:
    def ladderLength(
        self, beginWord: str, endWord: str, wordList: List[str]
    ) -> int:
        word_set = set(wordList)

        # Early exit guard clause
        if endWord not in word_set:
            return 0

        queue = deque([(beginWord, 1)])

        while queue:
            word, length = queue.popleft()

            if word == endWord:
                return length

            # Try changing each character to 'a' through 'z'
            for i in range(len(word)):
                for c in "abcdefghijklmnopqrstuvwxyz":
                    if c == word[i]:
                        continue

                    next_word = word[:i] + c + word[i + 1 :]

                    if next_word in word_set:
                        word_set.remove(next_word)  # Mark visited
                        queue.append((next_word, length + 1))

        return 0
```

## 4. Dry Run

Input (LC Example 1): `beginWord = "hit"`, `endWord = "cog"`, `wordList = ["hot","dot","dog","lot","log","cog"]`

`"cog"` is in `word_set`, so there's no early exit. Start: `queue = [(hit, 1)]`.

| Pop `(word, length)` | Hits found in `word_set` (each one is pushed, then removed) | `queue` after |
| --- | --- | --- |
| `(hit, 1)` | `i=1`: i→o gives **hot** | `(hot,2)` |
| `(hot, 2)` | `i=0`: h→d gives **dot**, h→l gives **lot** | `(dot,3) (lot,3)` |
| `(dot, 3)` | `i=2`: t→g gives **dog** | `(lot,3) (dog,4)` |
| `(lot, 3)` | `i=2`: t→g gives **log** | `(dog,4) (log,4)` |
| `(dog, 4)` | `i=0`: d→c gives **cog** | `(log,4) (cog,5)` |
| `(log, 4)` | `cog` was already removed from the set, so nothing new | `(cog,5)` |
| `(cog, 5)` | `word == endWord` | return **5** |

The ladder is `hit → hot → dot → dog → cog`, which is 5 words.

## 5. Complexity

Let **N** = `len(wordList)` and **L** = the word length.

* **Time: O(N × L² × 26)**, usually written **O(N × L²)**
  Think of it as: each word is popped at most once, and for each one you try every position (L) times every other letter (25). Building each candidate copies L letters, and checking the set hashes L letters, so one pop costs about 25 × L × L. With up to N + 1 pops, that's N × L² × 26. (Comparing every pair of words instead would be N² × L. That's much worse when N is large, like 5,000.)
* **Space: O(N × L)**
  Think of it as: `word_set` and `queue` each hold at most N words of length L. Only one candidate string exists at a time.

## 6. Recall (30 seconds)

* Words are nodes and one-letter changes are edges, so **BFS** gives the shortest ladder. Start at `(beginWord, 1)`, because the answer counts **words**.
* Use a set of words and return `0` if `endWord` is missing. Try every position × `a–z`, and on a hit **remove it from the set and push it** (marked when pushed).
* O(N·L²·26) time and O(N·L) space. The follow-up is bidirectional BFS.
