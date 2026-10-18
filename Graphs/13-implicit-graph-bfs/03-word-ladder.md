# Word Ladder  ·  LeetCode 127  ·  Hard

Group 13 — Implicit-Graph BFS  ·  **the canonical implicit-graph BFS.** State =
a word; neighbor = a one-letter change that's a real word. If you own this, you
own the pattern.

Prereqs: `02-minimum-genetic-mutation.md` (the smaller version), `concepts/03`
(BFS level counting).

---

## 1. Problem

Given `beginWord`, `endWord`, and a `wordList`. A **transformation sequence** is
`beginWord → s1 → s2 → ... → endWord` where:

- Each adjacent pair of words differs by **exactly one letter**.
- Every `si` is in `wordList` (`beginWord` need **not** be).

**Return the number of words in the shortest transformation sequence, or `0` if
none exists.**

Constraints:
- `1 <= beginWord.length <= 10`, all words the same length, lowercase.
- `1 <= wordList.length <= 5000`, words unique. `beginWord != endWord`.

Example 1:

```
beginWord = "hit", endWord = "cog"
wordList = ["hot","dot","dog","lot","log","cog"]
answer = 5        # hit -> hot -> dot -> dog -> cog  (5 words)
```

Example 2: same but `wordList` lacks `"cog"` → `0`.

---

## 2. Explain Like I'm 5

You have a start word and a target word, both the same length. Each move: change
**one letter**, and the word you land on has to be a real word (in the list).

Get from start to target in the **fewest moves**. Spread outward: all words one
letter from start, then all words one letter from *those*, and so on. The first
time you reach the target, count how many words are in that chain (including both
ends).

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "**Shortest transformation sequence**" / fewest one-letter changes | ✅ → BFS |
| Each intermediate must be **valid** (in the word list) | ✅ → `neighbors` filtered by the word set |
| No explicit graph — words are connected implicitly | ✅ → implicit-graph BFS |
| Answer counts **words** (nodes), not **changes** (edges) | ✅ → start the counter at `1` |

**Reduce it to:** *"BFS over words. `neighbors(w)` = for each of the `L` positions
× 25 other letters, the word with that one change, kept only if it's in the word
set. Answer = the BFS level (in words) at which `endWord` is first reached."*

**Minimum Genetic Mutation is this** with `L = 8`, alphabet `4`, counting edges
instead of nodes.

---

## 4. Intuition

1. Words are nodes; an edge connects two same-length words that differ by one
   letter and are both valid.
2. Every change costs `1`, so **BFS gives the shortest sequence**.
3. From a word there are `L × 25` one-letter variants; keep the ones in the word
   set that haven't been seen.
4. **The count is in *words*, not *changes*.** `beginWord` alone is a sequence of
   length `1`. Each BFS level adds one word. So seed the queue with
   `(beginWord, 1)` and return that number when you reach `endWord`.
5. Early exit: `endWord` must be in the word list, else return `0` immediately.

---

## 5. Approach (primary): BFS over words, count words

1. `word_set = set(wordList)`. If `endWord not in word_set`: return `0`.
2. `seen = {beginWord}`, `q = deque([(beginWord, 1)])`.
3. While `q`: pop `(word, length)`. If `word == endWord`: return `length`. For
   each position `i` and each letter `c != word[i]`: `nxt = word[:i] + c +
   word[i+1:]`; if `nxt in word_set and nxt not in seen`: `seen.add(nxt)`,
   `q.append((nxt, length + 1))`.
4. Return `0`.

Builds on: `concepts/03` BFS; `02-minimum-genetic-mutation.md` (same engine).

---

## 6. Pseudocode

```
function ladderLength(beginWord, endWord, wordList):
    word_set = set(wordList)
    if endWord not in word_set: return 0

    seen = {beginWord}
    q = queue([(beginWord, 1)])                # length in WORDS, starts at 1
    while q not empty:
        (word, length) = dequeue
        if word == endWord: return length
        for i in 0 .. L-1:
            for c in 'a'..'z' where c != word[i]:
                nxt = word with position i replaced by c
                if nxt in word_set and nxt not in seen:
                    add nxt to seen
                    enqueue (nxt, length + 1)
    return 0
```

---

## 7. Dry Run

```
begin = "hit", end = "cog"
wordList = ["hot","dot","dog","lot","log","cog"]
```

`word_set` has all six; `"cog"` is in it. `seen = {"hit"}`, `q = [("hit", 1)]`.

| pop | length | new valid, unseen one-letter variants | enqueue |
|---|---|---|---|
| "hit" | 1 | `"hot"` | ("hot", 2) |
| "hot" | 2 | `"dot"`, `"lot"` | ("dot", 3), ("lot", 3) |
| "dot" | 3 | `"dog"` | ("dog", 4) |
| "lot" | 3 | `"log"` | ("log", 4) |
| "dog" | 4 | `"cog"` | ("cog", 5) |
| "log" | 4 | `"cog"` already seen | — |
| "cog" | 5 | **`word == end`** → return **5** | |

Answer: `5` (the 5 words `hit, hot, dot, dog, cog`). ✅

---

## 8. Python Code (primary — BFS)

```python
import string
from collections import deque
from typing import List


class Solution:
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


if __name__ == "__main__":
    sol = Solution()

    assert sol.ladderLength("hit", "cog", ["hot", "dot", "dog", "lot", "log", "cog"]) == 5
    assert sol.ladderLength("hit", "cog", ["hot", "dot", "dog", "lot", "log"]) == 0
    assert sol.ladderLength("a", "c", ["a", "b", "c"]) == 2
    assert sol.ladderLength("hot", "dog", ["hot", "dog"]) == 0            # no bridge word
    assert sol.ladderLength("hot", "dog", ["hot", "dog", "dot"]) == 3
    assert sol.ladderLength("hit", "hot", ["hot"]) == 2

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. Wildcard-pattern adjacency (the classic scale trick)

Neighbor generation as written is `O(L × 26)` per word. Instead, precompute a map
from each **wildcard pattern** to the words matching it:

```python
from collections import defaultdict

patterns = defaultdict(list)
for w in word_set:
    for i in range(len(w)):
        patterns[w[:i] + "*" + w[i + 1:]].append(w)
# neighbors of w:  for each i, patterns[w[:i] + "*" + w[i+1:]]
```

Neighbor lookup is now `O(L)` (plus the matches). Preprocessing is `O(N × L)`.
Essential when the alphabet is large (Scenario 6) or `L` is big.

### 9b. Bidirectional BFS

Expand from `beginWord` **and** `endWord` simultaneously, always growing the
smaller frontier; stop when the two frontiers intersect. Turns `b^d` work into
`~2·b^(d/2)` — a large win on long ladders. The standard optimization for this
problem at scale.

### The BFS↔DFS answer the interviewer wants

> "Shortest one-letter-change sequence through a dictionary → BFS over words,
> `neighbors` = one-letter variants filtered by the word set. Answer counts words
> (nodes), so I start the length at `1`. At scale I'd use a wildcard-pattern
> adjacency index and bidirectional BFS. DFS gives *a* ladder, not the shortest."

---

## 10. Complexity — derived step by step

Let `N = len(wordList)`, `L = word length`, `Σ = 26`.

**Time (primary):**
- Reachable states `≤ N + 1`.
- Per state: `L × (Σ - 1)` variants, each `O(L)` to build + `O(L)` hash →
  `O(L² × Σ)` per state.
- **Total: `O(N × L² × Σ)`** (`≈ 5000 × 100 × 26 ≈ 1.3 × 10⁷` at the limits).

Wildcard-pattern variant (9a): `O(N × L)` preprocessing, then `O(N × L)` for the
BFS itself → `O(N × L)`. Bidirectional (9b) cuts the exponent in half.

**Space:**
- `word_set` + `seen` + queue: `O(N × L)`.
- Wildcard map: `O(N × L)` additional.
- **Total: `O(N × L)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `endWord` not in `wordList` | early `return 0` |
| No transformation path exists | BFS exhausts reachable words → `0` |
| `beginWord` not in `wordList` | fine — BFS starts from it regardless |
| `beginWord` and `endWord` differ by one letter, with `endWord` in the list | `hit → hot` → `2` |
| Single-letter words (`L = 1`) | 25 neighbors each; works |
| Off-by-one on the count | seeding `(beginWord, 1)` and `+1` per level makes the answer count *words* |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Counting changes (edges) instead of words (nodes).** Answer is the number
      of *words* in the sequence. Seed `(beginWord, 1)`, not `(beginWord, 0)`.
      This is *the* difference from Minimum Genetic Mutation.
- [ ] **`wordList` as a list, not a set** — `O(N)` membership per check; must be a
      `set`.
- [ ] **Skipping the `endWord not in word_set` early-out** — still correct (BFS
      returns `0`), but the check is standard and clarifies intent.
- [ ] **Generating the no-op variant** (`c == word[i]`) — wasted work; skip it.
- [ ] **Marking `seen` at dequeue** — the same word can be queued from many
      predecessors. Mark on enqueue.
- [ ] **Using DFS** — returns *a* ladder length, not the minimum.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **Word Ladder is the reference implicit-graph BFS.** State = word, `neighbors`
   = "one-letter change into the valid word set." Every other problem in this
   group is a variation on it.
2. **Nodes vs edges in the answer.** Some problems count steps/changes (edges),
   some count states visited (nodes = edges + 1). Read the question — Word Ladder
   counts nodes, Minimum Genetic Mutation counts edges.
3. **Wildcard-pattern adjacency** (`"h*t" → {hat, hit, hot}`) makes neighbor
   lookup `O(L)` instead of `O(Σ × L)` — mandatory for large alphabets.
4. **Bidirectional BFS** halves the exponent on long shortest paths.

| Problem | How this transfers |
|---|---|
| Minimum Genetic Mutation | this, with `L = 8`, `Σ = 4`, counting edges |
| Word Ladder II | this + reconstruct **all** shortest sequences (predecessor graph + backtrack) |
| Open the Lock (LC 752) | BFS over 4-digit strings, `neighbors` = wheel ±1, minus a deadends set |
| Sliding puzzle / lock combos | BFS over configurations; `neighbors` = legal single moves |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Return the actual transformation sequence (or *all* shortest ones)."

- **(b) Pattern:** BFS builds a **predecessor graph**, then backtrack (this is
  Word Ladder II).
- **(c) Adapt:** run BFS **level by level**. For each word, record every
  predecessor that reached it *at its own minimum level* (`preds[word]`). Stop
  the level BFS as soon as `endWord` appears. Then DFS/backtrack from `endWord`
  through `preds` back to `beginWord`, emitting each path reversed. Enumerating
  *all* is exponential in the number of shortest paths; one path is `O(L ×
  depth)`.
- **(d) Say:** "Keep predecessor lists during a leveled BFS, then walk them
  backward from the end. One path is cheap; *all* paths can be exponentially
  many."

### Scenario 2 — "`wordList` has `10^6` words and `L` is large."

- **(b) Pattern:** wildcard-pattern adjacency + bidirectional BFS.
- **(c) Adapt:** precompute `patterns[w[:i] + "*" + w[i+1:]] → [words]` in `O(N ×
  L)`. Neighbor lookup becomes `O(L)`. Run **bidirectional BFS** from both ends
  to cut the frontier. `O(N × L)` overall instead of `O(N × L² × 26)`.
- **(d) Say:** "Precompute a wildcard adjacency index so neighbor lookup is
  `O(L)`, and search from both ends."

### Scenario 3 — "Transformations may also **insert or delete** a letter (edit distance 1), not just substitute."

- **(b) Pattern:** same BFS, a wider `neighbors`.
- **(c) Adapt:** in addition to the `L × 25` substitutions, generate all
  length-`(L±1)` strings one insert/delete away and keep those in the word set.
  Words are no longer all the same length, so the word set spans multiple
  lengths. BFS is otherwise unchanged.
- **(d) Say:** "Insert/delete just adds more neighbor candidates per state — the
  BFS engine doesn't change, only the `neighbors` function."

### Scenario 4 — "Each word has a **difficulty cost**; minimize the total difficulty of the ladder."

- **(b) Pattern:** the move graph is **weighted** → Dijkstra.
- **(c) Adapt:** Dijkstra with a min-heap keyed by accumulated difficulty;
  stepping onto word `w` adds `cost[w]`. `O(N × L × 26 × log N)`.
- **(d) Say:** "Per-word costs mean Dijkstra — same implicit graph, weighted
  nodes/edges."

### Scenario 5 — "Count the number of **distinct shortest** ladders."

- **(b) Pattern:** leveled BFS + a `ways` counter.
- **(c) Adapt:** `ways[beginWord] = 1`. Process BFS level by level; when a word is
  first reached at level `d`, `ways[word] = sum of ways of predecessors at level
  d-1`; if reached again at the same `d` from another predecessor, add to it.
  Answer is `ways[endWord]`. Stop once `endWord`'s level is done.
- **(d) Say:** "Carry a `ways` count through the leveled BFS — sum predecessors'
  counts at the previous level."

### Scenario 6 — "Words are over a huge alphabet (Unicode) — you can't enumerate 26 letters."

- **(b) Pattern:** the wildcard-pattern adjacency approach is now **mandatory**.
- **(c) Adapt:** you can't loop over "all possible letters," so build the
  `patterns` map once and derive neighbors purely from it: two words are adjacent
  iff they share a wildcard pattern. Neighbor generation no longer touches the
  alphabet at all.
- **(d) Say:** "With an unbounded alphabet, enumerate *from the word list* via
  wildcard patterns instead of enumerating letters."

---

## 15. Flashcards

**Q:** What's the canonical implicit-graph BFS, and what's its state?
**A:** Word Ladder. State = a word; `neighbors` = one-letter changes that are in
the word set.

**Q:** Does the answer count words or transformations?
**A:** **Words** (nodes). Seed `(beginWord, 1)` and add 1 per level. (Minimum
Genetic Mutation counts *edges* — that's the difference.)

**Q:** How many neighbors per word, and how are they filtered?
**A:** `L × 25` one-letter variants; keep those in `set(wordList)` (an `O(1)`
hash check) and not yet `seen`.

**Q:** The two scale optimizations?
**A:** (1) Wildcard-pattern adjacency (`"h*t" → words`) → `O(L)` neighbor lookup.
(2) Bidirectional BFS → halves the shortest-path exponent.

**Q:** Time and space (primary)?
**A:** `O(N × L² × 26)` time, `O(N × L)` space. Wildcard variant: `O(N × L)`.

**Q:** The #1 bug?
**A:** Counting edges instead of nodes — starting the length at `0` gives an
answer one too small.

**Q:** Return *all* shortest ladders — how?
**A:** Word Ladder II: leveled BFS recording predecessor lists, then backtrack
from `endWord` through them (exponential in the number of paths).

**Q:** Huge / unbounded alphabet — what's forced?
**A:** Wildcard-pattern adjacency — you can't enumerate letters, so derive
neighbors from shared patterns among the word list.
