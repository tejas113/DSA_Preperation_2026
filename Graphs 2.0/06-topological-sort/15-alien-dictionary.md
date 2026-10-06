# 269. Alien Dictionary

**LC 269 🔒** · **Source:** NC150 · **Difficulty:** Hard · **Priority:** Stretch · **Pattern:** Topological sort (Kahn's algorithm) on letters, with edges taken from adjacent word pairs

---

## 1. Intuition

You're given a dictionary from an alien language, already sorted, and you have to work out their alphabet.
Compare the words the way you'd check a real dictionary: two neighbouring words agree up to some letter,
and the **first letter where they differ** tells you which letter comes first. Each such clue is a directed
edge "letter A before letter B". Then the alphabet is a topological sort of those letters, which is
Course Schedule II with letters instead of courses.

* **Every letter is a node, even the ones with no clues:** `indegree = {c: 0 for word in words for c in word}` registers every letter that appears, so letters with no ordering clue still end up in the answer.
* **Only the first difference counts:** in the inner loop, `if w1[j] != w2[j]` adds the edge `w1[j] → w2[j]` and then `break`s. Letters after the first difference tell you nothing, because the words were already decided by that letter.
* **The impossible prefix case:** `if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]: return ""`. A word can't come *before* its own prefix (like `"abc"` before `"ab"`), so the input is invalid.
* **Skip duplicate edges:** `if w2[j] not in graph[w1[j]]` makes sure `indegree` counts each edge once. `graph` is a set, so the later decrease happens only once too.
* **Cycle check by count:** `len(res) == len(indegree)` is true only if every letter was popped. Letters on a cycle (contradicting clues) never reach indegree `0`, so the code returns `""`.

**Recall:** Compare each pair of adjacent words. The first letter that differs gives an edge, and a longer word before its own prefix means `""`. Then run Kahn's algorithm on the letters, and if not all letters come out, return `""`.

## 2. Approach

* **Idea:** Turn the sorted word list into "letter before letter" edges, then topologically sort the letters. A cycle or a prefix violation means no valid alphabet exists.
* **Graph representation:** **adjacency sets** (`defaultdict(set)`) over letters. **Directed** (`earlier letter → later letter`) and unweighted. The nodes are the unique letters that appear in `words`.
* **Data structure / pointers:**
  * `graph[a]`: the set of letters known to come **after** `a`. Using a set removes duplicate edges.
  * `indegree[c]`: how many known "comes before `c`" letters haven't been placed yet. Its keys are also the full list of letters.
  * `w1, w2, min_len`: the current pair of adjacent words, and how far they can be compared.
  * `queue` (`deque`): letters that are ready to place (indegree `0`). Each letter is pushed **once**, when its indegree reaches `0`, so no visited set is needed.
  * `res`: the alphabet built so far, in pop order.
* **Invariant:** every letter in `res` comes after all the letters that must come before it, so `res` never breaks a clue.
* **Edge cases:**
  * A longer word before its own prefix (`["abc", "ab"]`): returns `""` straight away.
  * Contradicting clues, i.e. a cycle (`["z", "x", "z"]` gives `z → x` and `x → z`): returns `""`.
  * A single word: there are no pairs and no edges, so its unique letters come back in first-appearance order.
  * The same word twice in a row, or a short word before a longer word that starts with it (`["ab", "abc"]`): no difference is found and it's valid, so no edge is added and nothing is returned early.
  * Letters with no clue: they start at indegree `0`, so they can appear anywhere. Any position is accepted.
  * **More than one valid answer:** LeetCode accepts any of them. `graph[char]` is a **set**, and the order you loop over a set of strings can change between Python runs, so the exact string returned can differ from run to run. It's always a valid answer, though.
  * Only *adjacent* pairs are compared. That's enough, because order clues carry through: if A < B and B < C, then A < C.
  * It's iterative, so there's no recursion-depth risk.

## 3. Code

```python
from collections import defaultdict, deque
from typing import List

class Solution:
    def alienOrder(self, words: List[str]) -> str:
        graph = defaultdict(set)
        indegree = {c: 0 for word in words for c in word}

        # Step 1: Build the dependency graph
        for i in range(len(words) - 1):
            w1, w2 = words[i], words[i + 1]
            min_len = min(len(w1), len(w2))
            
            # Invalid case: prefix comes after longer word (e.g., "abc" before "ab")
            if len(w1) > len(w2) and w1[:min_len] == w2[:min_len]:
                return ""
            
            for j in range(min_len):
                if w1[j] != w2[j]:
                    if w2[j] not in graph[w1[j]]:
                        graph[w1[j]].add(w2[j])
                        indegree[w2[j]] += 1
                    break  # Only the first differing character gives order

        # Step 2: Kahn's Algorithm (BFS Topological Sort)
        queue = deque([c for c in indegree if indegree[c] == 0])
        res = []

        while queue:
            char = queue.popleft()
            res.append(char)
            
            for neighbor in graph[char]:
                indegree[neighbor] -= 1
                if indegree[neighbor] == 0:
                    queue.append(neighbor)

        # Step 3: Check if all unique characters were processed (no cycles)
        return "".join(res) if len(res) == len(indegree) else ""
```

## 4. Dry Run

Input (LC Example 1): `words = ["wrt", "wrf", "er", "ett", "rftt"]`

Letters in order of first appearance: `w, r, t, f, e`, all starting at indegree `0`.

**Step 1: build the edges from adjacent pairs**

| `w1` | `w2` | First difference | Edge added | `indegree` after |
| --- | --- | --- | --- | --- |
| `wrt` | `wrf` | `j=2`: `t` vs `f` | `t → f` | `f:1` |
| `wrf` | `er` | `j=0`: `w` vs `e` | `w → e` | `e:1` |
| `er` | `ett` | `j=1`: `r` vs `t` | `r → t` | `t:1` |
| `ett` | `rftt` | `j=0`: `e` vs `r` | `e → r` | `r:1` |

The final indegrees are `w:0, r:1, t:1, f:1, e:1`. No pair hit the prefix rule.

**Step 2: Kahn's algorithm**

| Pop | `res` | Indegree changes | `queue` after |
| --- | --- | --- | --- |
| (start) | `[]` | — | `[w]` |
| `w` | `w` | `e` 1 → **0** (push) | `[e]` |
| `e` | `we` | `r` 1 → **0** (push) | `[r]` |
| `r` | `wer` | `t` 1 → **0** (push) | `[t]` |
| `t` | `wert` | `f` 1 → **0** (push) | `[f]` |
| `f` | `wertf` | none | `[]` |

`len(res) == 5 == len(indegree)`, so it returns **`"wertf"`**. Here the clues form a single chain, so this is the only valid answer.

## 5. Complexity

Let **C** = the total number of characters across all words, **U** = the number of unique letters (at most 26), and **E** = the number of distinct edges (at most one per adjacent pair, and never more than U²).

* **Time: O(C + U + E)**, which is effectively **O(C)** because U ≤ 26
  Think of it as: building `indegree` reads every character once. Each adjacent pair is compared only up to `min_len`, and the prefix slice is at most that long too, so all the pairs together read each character only a few times. Kahn's algorithm then pops each letter once and walks each edge once, which is U + E. With only 26 possible letters, that part is tiny.
* **Space: O(U + E)**, which is effectively **O(1)** with a 26-letter alphabet
  Think of it as: `graph`, `indegree`, `queue` and `res` only store letters and edges between letters, never whole words. Even in the worst case that's 26 letters and 26 × 26 edges. The `w1[:min_len]` slices are temporary copies the length of one word.

## 6. Recall (30 seconds)

* Compare **adjacent** words. The first differing letter gives an edge `w1[j] → w2[j]`, then `break`. If a longer word comes before its own prefix, return `""`.
* Register **every** letter in `indegree` up front, and only increase indegree for edges you haven't seen (the `graph` set).
* Kahn's algorithm on the letters. If `len(res) < len(indegree)` there's a cycle, so return `""`. Any valid order is accepted.
