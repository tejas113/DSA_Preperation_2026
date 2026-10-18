# Alien Dictionary  ·  LeetCode 269  ·  Hard  ·  🔒 Premium

Group 06 — Topological Sort / Cycle Detection  ·  the twist: **you build the
graph yourself** by comparing adjacent words, then it's Kahn's algorithm exactly.

> Premium on LeetCode — the `.md`/`.py` here are fully runnable and tested
> locally.

Prereqs: `01-course-schedule.md`, `02-course-schedule-ii.md`, `concepts/07`
(topological sort). New idea: **the input isn't edges — you extract edges from a
sorted list by comparing consecutive elements.**

---

## 1. Problem

There's an alien language that uses lowercase English letters, but in an
**unknown order**. You're given a list of `words` that is sorted
**lexicographically according to the alien language's rules**.

**Return a string of all unique letters in the alien language's sorted order.**
If no valid order exists (the input is contradictory), return `""`. If several
orders are valid, return **any**.

Constraints:
- `1 <= words.length <= 100`, `1 <= words[i].length <= 100`.
- All characters are lowercase English letters.

Example 1:

```
words = ["wrt","wrf","er","ett","rftt"]
answer = "wertf"
```

Example 2:

```
words = ["z","x"]
answer = "zx"
```

Example 3 (contradiction):

```
words = ["z","x","z"]
answer = ""        # z<x from the first pair, x<z from the second -> impossible
```

Example 4 (invalid prefix):

```
words = ["abc","ab"]
answer = ""        # "ab" is a prefix of "abc" but comes AFTER it -> not a valid sort
```

---

## 2. Explain Like I'm 5

Someone hands you a dictionary written in an alien language. You can't read the
letters, but you know the words are **in alphabetical order** for *their*
alphabet. Your job: figure out their alphabet's order.

Here's the trick. Look at two words that are **next to each other** in the
dictionary. Scan them letter by letter until you find the **first spot where they
differ**. Whatever letter is in the earlier word at that spot must come **before**
the letter in the later word — that's the only reason the earlier word sorts
first. (Letters *after* that first difference tell you nothing.)

Do that for every neighboring pair of words, and you collect a bunch of "this
letter before that letter" facts. Then you just put the alphabet in an order that
respects all those facts — that's a **topological sort**. If the facts
contradict each other (letter A before B, but also B before A), there's no valid
alphabet — return nothing.

One gotcha: if a word like `"ab"` comes *after* `"abc"`, that's impossible in any
alphabet — a shorter word that's a prefix of a longer one must come *first*.
That's also "return nothing."

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| Output is an **ordering** of items | ✅ the alphabet |
| Constraints come from **pairwise "before" facts** | ✅ derived from adjacent words |
| The facts might **contradict** (cycle) | ✅ → return `""` |
| Input is a **sorted list**, not an explicit edge list | ✅ → you must *construct* the edges |

**Reduce it to:** *"Build a directed graph: one edge `c1 -> c2` per adjacent word
pair whose first differing characters are `c1` (earlier word) and `c2` (later
word). Then topologically sort. Return `""` on a cycle or on an invalid prefix."*

**Look-alike:** Course Schedule II — once the graph is built, it's **the identical
algorithm**. The only new work is graph construction.

---

## 4. Intuition

1. A lexicographic sort compares two words character by character and decides
   order at the **first differing character**. So for two adjacent words `w1`
   (earlier) and `w2` (later), the *first* position `i` where `w1[i] != w2[i]`
   tells you exactly one fact: `w1[i]` comes before `w2[i]` in the alien
   alphabet. Add edge `w1[i] -> w2[i]`.
2. **Only adjacent pairs matter.** If `w1 < w2 < w3` in the list, you get facts
   from `(w1, w2)` and `(w2, w3)`; the fact about `(w1, w3)` follows by
   transitivity, which the topological sort handles for free. Comparing all
   `O(n²)` pairs would be wasted work.
3. **Only the first difference matters.** Once `w1` and `w2` differ at position
   `i`, characters at positions `> i` are unconstrained by *this* pair — stop.
4. **The prefix trap:** if you scan all `min(len(w1), len(w2))` characters and
   find no difference, but `w1` is **longer** than `w2`, then `w2` is a proper
   prefix of `w1` appearing *after* it — impossible in a valid sort. Return `""`.
5. Every character that appears anywhere must be in the output, even ones with no
   ordering constraint at all — initialize `graph`/`indegree` for **all** of
   them.
6. After the graph is built, run Kahn's algorithm (`concepts/07`). If the
   produced order doesn't include every character, there's a cycle → `""`.

---

## 5. Approach (primary): build the graph from adjacent words, then Kahn's

1. `graph = {c: set() for every char c in any word}` (a `set` per node, to dedupe
   edges). `indegree = {c: 0 for c in graph}`.
2. For each adjacent pair `(w1, w2)` in `zip(words, words[1:])`:
   - Scan `i` from `0` to `min(len(w1), len(w2)) - 1`. At the first `i` with
     `w1[i] != w2[i]`: if `w2[i] not in graph[w1[i]]`, add it and
     `indegree[w2[i]] += 1`; then **break**.
   - If the loop finishes with no difference **and** `len(w1) > len(w2)`: return
     `""` (invalid prefix).
3. Kahn's algorithm over `graph`/`indegree`. Collect `order`.
4. Return `"".join(order)` if `len(order) == len(indegree)`, else `""` (cycle).

Builds on: `concepts/07` Kahn's algorithm; the new part is steps 1–2.

---

## 6. Pseudocode

```
function alienOrder(words):
    graph = {c: empty set for each char c across all words}
    indegree = {c: 0 for c in graph}

    for (w1, w2) in adjacent pairs of words:
        for i in 0 .. min(len(w1), len(w2)) - 1:
            if w1[i] != w2[i]:
                if w2[i] not in graph[w1[i]]:
                    graph[w1[i]].add(w2[i])
                    indegree[w2[i]] += 1
                break
        else:                                  # no break -> no differing char found
            if len(w1) > len(w2): return ""    # invalid prefix

    q = queue of all chars with indegree 0
    order = []
    while q not empty:
        c = dequeue; order.append(c)
        for nei in graph[c]:
            indegree[nei] -= 1
            if indegree[nei] == 0: enqueue nei

    return join(order) if len(order) == len(indegree) else ""
```

---

## 7. Dry Run

```
words = ["wrt","wrf","er","ett","rftt"]
```

Characters: `{w, r, t, f, e}`. `indegree = {w:0, r:0, t:0, f:0, e:0}`.

Adjacent pairs:

| pair | first differing chars | edge added | indegree after |
|---|---|---|---|
| ("wrt", "wrf") | `t` vs `f` (index 2) | `t -> f` | f:1 |
| ("wrf", "er") | `w` vs `e` (index 0) | `w -> e` | e:1 |
| ("er", "ett") | `r` vs `t` (index 1) | `r -> t` | t:1 |
| ("ett", "rftt") | `e` vs `r` (index 0) | `e -> r` | r:1 |

`graph = {w:{e}, e:{r}, r:{t}, t:{f}, f:{}}`. `indegree = {w:0, e:1, r:1, t:1, f:1}`.

Kahn's: `q = [w]` (only `w` has indegree 0).

| pop | order | neighbor updates | queue after |
|---|---|---|---|
| w | w | indeg[e]: 1→0 → enqueue e | [e] |
| e | we | indeg[r]: 1→0 → enqueue r | [r] |
| r | wer | indeg[t]: 1→0 → enqueue t | [t] |
| t | wert | indeg[f]: 1→0 → enqueue f | [f] |
| f | wertf | — | [] |

`len(order) == 5 == len(indegree)` → return `"wertf"`. ✅

---

## 8. Python Code (primary — build graph + Kahn's)

```python
from collections import deque
from typing import List


class Solution:
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


if __name__ == "__main__":
    sol = Solution()

    assert sol.alienOrder(["wrt", "wrf", "er", "ett", "rftt"]) == "wertf"
    assert sol.alienOrder(["z", "x"]) == "zx"
    assert sol.alienOrder(["z", "x", "z"]) == ""         # contradiction (cycle)
    assert sol.alienOrder(["abc", "ab"]) == ""            # invalid prefix
    assert sol.alienOrder(["a", "b", "a"]) == ""          # contradiction
    assert sol.alienOrder(["abc"]) == "abc"               # one word: any order of its letters
    assert sorted(sol.alienOrder(["ac", "ab", "zc", "zb"])) == ["a", "b", "c", "z"]

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. DFS post-order (after the same graph construction)

Build `graph` from adjacent word pairs exactly as above (including the invalid-
prefix check), then use the DFS 3-color post-order topological sort from
`02-course-schedule-ii.md` section 9a. A gray node re-encountered → cycle →
return `""`. Same `O(...)`.

### The BFS↔DFS answer the interviewer wants

> "The graph construction is the same either way — comparing adjacent words for
> their first differing character. Then it's a standard topological sort: I'd
> use Kahn's BFS for the natural cycle check (`len(order) != number of unique
> chars`). DFS post-order works identically after the graph is built."

---

## 10. Complexity — derived step by step

Let `W = len(words)` and `L` = the maximum word length. Total characters
`C = O(W * L)`. The alphabet size `A` is at most 26 (or the number of distinct
characters).

**Time:**
- Building `graph`/`indegree`: scanning every character once → `O(C)`.
- Comparing adjacent word pairs: `W - 1` pairs, each compared up to `L`
  characters → `O(W * L) = O(C)`.
- Kahn's algorithm: `O(A + edges)`, and there are at most `A²` edges (one per
  ordered pair of letters) and at most `W - 1` distinct edges added → `O(A + A²)`,
  effectively `O(1)` given `A ≤ 26`.
- **Total: `O(C)` = `O(W * L)`** — dominated by reading the input.

**Space:**
- `graph`/`indegree`: `O(A + edges)` = `O(A²)`, effectively `O(1)` for a bounded
  alphabet.
- **Total: `O(C)`** for holding the input references, `O(A²)` for the graph.

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| One word (`["abc"]`) | no adjacent pairs → no edges → all letters returned in insertion order (any order is valid) |
| Two identical adjacent words (`["ab","ab"]`) | no differing char, `len` equal → not invalid; contributes no edge |
| `"abc"` before `"ab"` | no differing char in first 2, `len(w1) > len(w2)` → return `""` |
| Contradiction (`["z","x","z"]`) | `z->x` then `x->z` → cycle → Kahn's leaves nodes unprocessed → `""` |
| A letter appears with no ordering constraint | still initialized in `graph`/`indegree`, still emitted in the output |
| Repeated letters within a word (`["aa","ab"]`) | scan stops at first difference (`a` vs `b` at index 1) → edge `a -> b` |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Comparing all pairs of words instead of only adjacent ones.** Wastes
      time and can add redundant (though not incorrect) edges — but the real
      danger is if you *also* compare non-adjacent pairs incorrectly. Only
      `zip(words, words[1:])`.
- [ ] **Not `break`ing after the first differing character.** Characters past
      the first difference carry no ordering info — adding edges for them
      invents false constraints and can fabricate a cycle.
- [ ] **Missing the invalid-prefix check.** `["abc","ab"]` must return `""`;
      forgetting this returns a bogus non-empty order.
- [ ] **Double-counting indegree** when the same letter pair appears as the first
      difference in multiple adjacent word pairs. Guard with
      `if w2[i] not in graph[w1[i]]` before incrementing.
- [ ] **Only initializing nodes that have edges.** A letter that appears but has
      no constraints still must be in `indegree` (at 0) and in the output.
- [ ] **Returning the partial order on a cycle.** Must check
      `len(order) == len(indegree)` and return `""` otherwise.
- [ ] **Using `for/else` wrong** — the `else` of a `for` runs only if the loop
      completed *without* `break` (i.e. no differing char was found). Easy to
      misplace.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **Extract a graph from implicit signal.** The input is a sorted list, not
   edges — you derive edges by comparing consecutive elements. This "the
   structure hides the graph" move recurs constantly (reconstruct a sequence
   from hints, infer a schema, merge histories).
2. **Adjacent comparisons + transitive closure = all the information.** You never
   need all `O(n²)` pairwise relations when the input is already sorted; adjacent
   pairs plus the topological sort's transitivity capture everything. (Same
   reason merge-sort's merge step only ever compares the two fronts.)
3. **Multiple independent "invalid" conditions.** Here: a cycle *and* an invalid
   prefix, both mapping to `""`. Enumerating every way an input can be malformed
   is a code-quality signal.
4. **Once the graph exists, it's a solved problem** — Kahn's / DFS post-order,
   unchanged from Course Schedule II.

| Problem | How this transfers |
|---|---|
| Course Schedule II | the topological sort half is identical |
| "Reconstruct the original array from adjacent-pair hints" | build edges from the hints, topologically sort |
| Verify an Alien Dictionary is sorted (LC 953) | the same adjacent-pair comparison logic, just checking against a *given* order instead of deriving one |
| Rank players from "A beat B" match results | each result is an edge; topological sort = the ranking; a cycle = inconsistent results |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "The words can contain any Unicode characters (uppercase, digits, emoji), not just 26 lowercase letters."

- **(b) Pattern:** a check that your solution didn't hardcode "26 letters."
- **(c) Adapt:** the primary solution already handles this — `graph` and
  `indegree` are built from `{c for w in words for c in w}`, so they hold
  exactly the characters that appear, whatever they are. No `ord('a')` arithmetic
  anywhere. Complexity is unchanged except the alphabet-size term `A` is now "the
  number of distinct characters" instead of "≤ 26."
- **(d) Say:** "Because I keyed the graph by the actual characters that appear
  rather than by array index into a 26-slot table, this generalizes to any
  alphabet for free — a reason to prefer dict-keyed-by-value over
  array-indexed-by-`ord` unless the alphabet is guaranteed small and dense."

### Scenario 2 — "Return the **lexicographically smallest** valid alien order, breaking ties by normal English alphabetical order."

- **(b) Pattern:** Kahn's with a **priority queue** (same as Course Schedule II
  Scenario 1).
- **(c) Adapt:** replace the `deque` with a min-heap of characters. Whenever
  multiple letters have indegree 0, `heappop` returns the alphabetically
  smallest. `O(C + A log A)`.
- **(d) Say:** "Any deterministic tie-break on a topological order is a
  queue-discipline change — min-heap for smallest-first — nothing else moves."

### Scenario 3 — "If the dictionary is contradictory, report **which pair of words** caused it (for debugging a corrupted data file)."

- **(b) Pattern:** cycle detection + provenance tracking.
- **(c) Adapt:** when adding an edge `c1 -> c2`, also record `edge_source[(c1,c2)]
  = (w1, w2)` (the word pair that produced it). If Kahn's leaves nodes
  unprocessed, run a DFS on just those leftover nodes to find an actual cycle
  (sequence of edges), then map each of that cycle's edges back through
  `edge_source` to name the offending word pairs. The invalid-prefix case
  already knows its exact `(w1, w2)` at the point the check fires.
- **(d) Say:** "Attach the originating word pair to each edge as you build it;
  then a detected cycle can be traced back to the specific inputs that caused
  it."

### Scenario 4 — "The dictionary is **streamed** — words arrive one at a time (in sorted order). After each new word, output the current best-known ordering, noting which letters' relative order is still undetermined."

- **(b) Pattern:** incremental graph building + repeated topological sort, with
  "multiple valid orders" detection.
- **(c) Adapt:** keep `graph`/`indegree` across the stream; on each new word,
  compare it with the previous one and add the (at most one) new edge. Re-run
  Kahn's — cheap, since the alphabet is bounded (`O(A + A²)` per word). "Order
  still undetermined between two letters" corresponds to a moment during Kahn's
  when the queue holds **more than one** indegree-0 node — their relative order
  isn't forced by any fact yet.
- **(d) Say:** "Bounded alphabet means a full re-sort per new word is trivially
  cheap. And 'undetermined order' has a precise meaning: the queue having
  multiple ready nodes at once means those nodes' order isn't pinned down."

### Scenario 5 — "Some words are noise (typos putting them out of order). Given a budget to delete at most `K` words, determine whether a consistent order becomes derivable."

- **(b) Pattern:** flag it — this becomes combinatorial.
- **(c) Adapt:** for small `K`, brute-force: try each subset of up to `K` words
  to remove, rebuild the graph from the remaining words, test for
  consistency (no cycle, no invalid prefix). `O(C(W, K) * C)` — fine for tiny
  `K`. For general `K`, note that "minimum words to delete to make it consistent"
  is related to feedback-arc-set-style problems and is NP-hard in general — offer
  a heuristic (e.g. remove the word involved in the most cycle-forming edges) but
  be explicit it's not provably optimal.
- **(d) Say:** "Small `K` is brute-forceable; general `K` is a
  feedback-arc-set-flavored problem, so I'd name the hardness and give a
  heuristic rather than pretend there's a clean polynomial answer."

### Scenario 6 — "Generalize: you're given a set of pairwise comparison results ('X ranks above Y') from a tournament, and must produce a full ranking or report the results are inconsistent."

- **(b) Pattern:** this is Alien Dictionary with the graph construction removed —
  the comparisons *are* the edges.
- **(c) Adapt:** each `"X above Y"` is a directed edge `X -> Y`. Topologically
  sort — the order is the ranking; leftover nodes (a cycle) mean the results
  contradict each other (X > Y > Z > X). If the queue ever has multiple ready
  nodes, the ranking isn't fully determined by the given comparisons (a tie /
  unknown). `O(V + E)`.
- **(d) Say:** "Any 'infer a total order from pairwise facts' problem —
  rankings, dependency inference, merging partial orders — is topological sort;
  Alien Dictionary is just that with an extra step to *derive* the pairwise
  facts from a sorted word list first."

---

## 15. Flashcards

**Q:** What's the "new" work in Alien Dictionary vs Course Schedule II?
**A:** Building the graph. You derive edges by comparing **adjacent** words and
taking the **first** position where they differ: `w1[i] -> w2[i]`.

**Q:** Why only adjacent word pairs, and why only the first differing char?
**A:** The list is already sorted — adjacent pairs plus the topological sort's
transitivity give all the info. Characters after the first difference are
unconstrained by that pair.

**Q:** The two independent ways the answer can be `""`?
**A:** (1) A cycle (contradictory facts) — Kahn's leaves nodes unprocessed.
(2) Invalid prefix — a longer word appears before its own prefix
(`["abc","ab"]`).

**Q:** Why must you initialize `indegree` for every character, not just ones
with edges?
**A:** A letter with no ordering constraints still appears in the output; if it's
not in `indegree` at 0, it's never enqueued and never emitted.

**Q:** The double-counting bug?
**A:** The same first-difference letter pair can occur across multiple adjacent
word pairs — guard `indegree[w2[i]] += 1` with `if w2[i] not in graph[w1[i]]`.

**Q:** Time and space?
**A:** `O(total characters)` = `O(W * L)` time (dominated by reading input),
`O(A²)` graph space (`≈ O(1)` for a bounded alphabet).

**Q:** How does "rank players from match results" relate?
**A:** It's this problem minus the graph-construction step — each "X beat Y" is
already a directed edge; topological sort gives the ranking, a cycle means
inconsistent results.
