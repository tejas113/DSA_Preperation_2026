# Minimum Genetic Mutation  ·  LeetCode 433  ·  Medium

Group 13 — Implicit-Graph BFS  ·  the "training-wheels" version of Word Ladder:
fixed length 8, 4-letter alphabet. Same pattern, smaller.

Prereqs: `01-snakes-and-ladders.md`, `concepts/03` (BFS level counting).

---

## 1. Problem

A gene string has exactly **8** characters, each `'A'`, `'C'`, `'G'`, or `'T'`. A
**mutation** changes a single character. Given `startGene`, `endGene`, and a
`bank` of valid genes, **return the minimum number of mutations** to turn
`startGene` into `endGene`, where **every mutated gene along the way must be in
the bank**. Return `-1` if impossible.

Constraints:
- `0 <= bank.length <= 10`.
- All strings are length 8 over `{A, C, G, T}`.

Example 1: `start="AACCGGTT"`, `end="AACCGGTA"`, `bank=["AACCGGTA"]` → `1`.
Example 2: `start="AACCGGTT"`, `end="AAACGGTA"`,
`bank=["AACCGGTA","AACCGCTA","AAACGGTA"]` → `2`.
Example 3: `start="AAAAACCC"`, `end="AACCCCCC"`,
`bank=["AAAACCCC","AAACCCCC","AACCCCCC"]` → `3`.

---

## 2. Explain Like I'm 5

You have an 8-letter word made of only A, C, G, T. Each step you may change
**one** letter — but the new word has to be on an approved list (the bank).

You want to get from the start word to the end word in the **fewest** single-
letter changes. So try every one-letter change from the start (keeping only the
approved ones), then every one-letter change from *those*, spreading outward. The
first time you reach the end word, count the steps.

---

## 3. Pattern Identification

| Signal | Here? |
|---|---|
| "**Minimum number of mutations / transformations**" | ✅ → BFS |
| Each step = one small change, and the result must be **valid** (in the bank) | ✅ → `neighbors` filtered by the bank |
| No explicit graph — genes are connected implicitly by "differs by one char and both valid" | ✅ → implicit-graph BFS |

**Reduce it to:** *"BFS over gene strings. `neighbors(g)` = for each of the 8
positions × 3 other letters, the string with that one change, kept only if it's
in the bank. First BFS level that reaches `endGene` = the answer."*

**This is Word Ladder** with `L = 8` fixed and alphabet size `4`.

---

## 4. Intuition

1. Genes are nodes; an edge connects two genes that differ by exactly one
   character **and** are both in the bank (or one is the start).
2. Every mutation costs `1`, so **BFS gives the minimum number of mutations**.
3. From a gene, there are `8 × 3 = 24` single-character variants. Generate all
   24, keep the ones in the bank set (`O(1)` membership) that haven't been seen.
4. Quick exits: if `startGene == endGene` → `0`. If `endGene` isn't in the bank
   (and isn't the start) → `-1` (the final gene must itself be a valid bank
   gene).

---

## 5. Approach (primary): BFS over gene strings

1. If `startGene == endGene`: return `0`.
2. `bank_set = set(bank)`. If `endGene not in bank_set`: return `-1`.
3. `seen = {startGene}`, `q = deque([(startGene, 0)])`.
4. While `q`: pop `(gene, steps)`. If `gene == endGene`: return `steps`. For each
   position `i` in `0..7`, for each `c` in `"ACGT"` with `c != gene[i]`:
   `nxt = gene[:i] + c + gene[i+1:]`; if `nxt in bank_set and nxt not in seen`:
   `seen.add(nxt)`, `q.append((nxt, steps + 1))`.
5. Return `-1`.

Builds on: `concepts/03` BFS; the new work is generating the 24 variants and
filtering by `bank_set`.

---

## 6. Pseudocode

```
function minMutation(startGene, endGene, bank):
    if startGene == endGene: return 0
    bank_set = set(bank)
    if endGene not in bank_set: return -1

    seen = {startGene}
    q = queue([(startGene, 0)])
    while q not empty:
        (gene, steps) = dequeue
        if gene == endGene: return steps
        for i in 0..7:
            for c in "ACGT" where c != gene[i]:
                nxt = gene with position i replaced by c
                if nxt in bank_set and nxt not in seen:
                    add nxt to seen
                    enqueue (nxt, steps + 1)
    return -1
```

---

## 7. Dry Run

```
start = "AACCGGTT", end = "AAACGGTA"
bank  = ["AACCGGTA", "AACCGCTA", "AAACGGTA"]
```

`bank_set` contains all three. `end` is in it. `seen = {"AACCGGTT"}`,
`q = [("AACCGGTT", 0)]`.

| pop | steps | in-bank one-char variants not seen | enqueue |
|---|---|---|---|
| "AACCGGTT" | 0 | position 7 `T→A`: `"AACCGGTA"` ✓ (in bank) | ("AACCGGTA", 1) |
| "AACCGGTA" | 1 | pos 5 `G→C`: `"AACCGCTA"` ✓ ; pos 2 `C→A`: `"AAACGGTA"` ✓ | ("AACCGCTA", 2), ("AAACGGTA", 2) |
| "AACCGCTA" | 2 | not `end`; its bank variants already seen | — |
| "AAACGGTA" | 2 | **`gene == end`** → return **2** | |

Answer: `2`. ✅

---

## 8. Python Code (primary — BFS)

```python
from collections import deque
from typing import List


class Solution:
    def minMutation(self, startGene: str, endGene: str, bank: List[str]) -> int:
        if startGene == endGene:
            return 0

        bank_set = set(bank)
        if endGene not in bank_set:
            return -1                            # the final gene must be a valid bank gene

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


if __name__ == "__main__":
    sol = Solution()

    assert sol.minMutation("AACCGGTT", "AACCGGTA", ["AACCGGTA"]) == 1
    assert sol.minMutation("AACCGGTT", "AAACGGTA",
                           ["AACCGGTA", "AACCGCTA", "AAACGGTA"]) == 2
    assert sol.minMutation("AAAAACCC", "AACCCCCC",
                           ["AAAACCCC", "AAACCCCC", "AACCCCCC"]) == 3
    assert sol.minMutation("AACCGGTT", "AACCGGTA", []) == -1
    assert sol.minMutation("AAAAAAAA", "AAAAAAAA", []) == 0       # start == end
    assert sol.minMutation("AAAAAAAA", "CCCCCCCC", ["AAAAAAAC", "AAAAAACC"]) == -1

    print("all tests passed")
```

---

## 9. Alternative Approaches

### 9a. Bidirectional BFS

Search from `startGene` and `endGene` at once; expand whichever frontier is
smaller; stop when they meet. Roughly halves the number of levels explored —
matters for Word Ladder-scale problems. Here `bank ≤ 10`, so the state space is
tiny and plain BFS is fine, but it's the standard optimization to mention.

### 9b. "Iterate the bank" instead of "generate 24 variants"

For each gene in the queue, scan the whole bank and keep entries that differ in
exactly one position: `O(bank_size × 8)` per state. Better than the
generate-24 approach only when the bank is **small** relative to `8 × 3 = 24`
(here they're comparable). For a huge bank, generate-and-hash-check wins.

### The BFS↔DFS answer the interviewer wants

> "Fewest single-character changes through a set of valid strings → BFS over
> strings, `neighbors` = one-char variants filtered by the bank set. It's Word
> Ladder with length fixed at 8 and a 4-letter alphabet. Bidirectional BFS if the
> state space were large."

---

## 10. Complexity — derived step by step

Let `B = len(bank)` (`≤ 10`), `L = 8`, alphabet `Σ = 4`.

**Time:**
- Reachable states `≤ B + 1`.
- Per state: generate `L × (Σ - 1) = 24` variants, each `O(L)` to build the
  string + `O(L)` hash → `O(L² × Σ)` per state.
- **Total: `O(B × L² × Σ)`** — tiny here; for general `L`, `Σ` it's
  `O(states × L² × Σ)`.

**Space:**
- `bank_set` + `seen` + queue: `O(B × L)`.
- **Total: `O(B × L)`.**

---

## 11. Edge Cases

| Case | Handled by |
|---|---|
| `startGene == endGene` | early `return 0` (even if `endGene` isn't in the bank) |
| `endGene` not in the bank | early `return -1` (the last mutation must land on a bank gene) |
| Empty bank | `endGene not in bank_set` → `-1` (unless `start == end`) |
| `endGene` in the bank but no valid chain reaches it | BFS exhausts the reachable states → `-1` |
| Several genes at the same mutation distance | BFS level order handles it |

---

## 12. Debugging Checklist (bugs most likely in *this* problem)

- [ ] **Not checking `startGene == endGene` first.** If they're equal but
      `endGene` isn't in the bank, you'd wrongly return `-1` instead of `0`.
- [ ] **`bank` as a list, not a set.** `O(B)` membership per check instead of
      `O(1)` — fine at `B ≤ 10`, bad habit for scale.
- [ ] **Generating `nxt` with `c == gene[i]`** — a no-op "mutation"; skip it
      (`if c != gene[i]`).
- [ ] **String slice off-by-one** — `gene[:i] + c + gene[i+1:]` (note `i + 1`).
- [ ] **Marking `seen` at dequeue instead of enqueue** — same string can be
      queued multiple times.
- [ ] **Forgetting the `-1` return** at the end.

---

## 13. Learnings & Transfer

**Reusable ideas:**
1. **BFS over strings, `neighbors` = "one small change, kept only if valid."**
   The valid set is a hash set for `O(1)` membership.
2. **Two ways to generate neighbors** — enumerate all single-char variants and
   filter by the valid set, *or* scan the valid set for "differs by one." Pick
   by which is smaller: `L × Σ` vs `|valid set|`.
3. This is a **micro Word Ladder** — recognizing "same pattern, smaller
   parameters" is the skill.

| Problem | How this transfers |
|---|---|
| Word Ladder | this, with `L` = word length and `Σ = 26` |
| Open the Lock (LC 752) | BFS over 4-digit strings; `neighbors` = turn one wheel ±1, minus a deadends set |
| "Min edits, each intermediate must be a real word" | BFS over words, `neighbors` filtered by a dictionary |
| Snakes and Ladders | same BFS engine, `neighbors` = die rolls instead of char changes |

---

## 14. Scenario-Based Questions (Google standard)

### Scenario 1 — "Genes can be any length `L`, over any alphabet of size `Σ`."

- **(b) Pattern:** unchanged — this *becomes* Word Ladder.
- **(c) Adapt:** the neighbor loop is `L` positions × `(Σ - 1)` letters;
  everything else is identical. Per-state work is `O(L² × Σ)` (string builds +
  hashes).
- **(d) Say:** "Length and alphabet are just the branching factor of `neighbors`
  — Minimum Genetic Mutation *is* Word Ladder with `L = 8`, `Σ = 4`."

### Scenario 2 — "Return the actual sequence of mutations."

- **(b) Pattern:** BFS + parent pointers.
- **(c) Adapt:** `parent[nxt] = gene` on enqueue. From `endGene`, walk `parent`
  back to `startGene` and reverse. `O(states × L)` extra.
- **(d) Say:** "One parent pointer per discovered gene; reconstruct from the
  end."

### Scenario 3 — "The bank has `10^5` genes and `L` is large."

- **(b) Pattern:** choose the cheaper neighbor-generation, and consider
  bidirectional.
- **(c) Adapt:** with a huge bank, **generate the `L × (Σ-1)` variants and
  hash-check** (independent of bank size) rather than scanning the bank per
  state. Add **bidirectional BFS** to cut the explored frontier. A common Word
  Ladder trick: precompute a map from wildcard patterns (`"A*CCGGTT"`) to the
  genes matching them, so neighbor lookup is `O(L)`.
- **(d) Say:** "Huge bank ⟹ generate-and-hash-check (bank-size-independent), plus
  bidirectional BFS, plus optionally a wildcard-pattern adjacency index."

### Scenario 4 — "Some mutations are **lethal** — a forbidden set of genes you must never pass through, even if they're in the bank."

- **(b) Pattern:** same BFS, extra filter.
- **(c) Adapt:** `forbidden = set(lethal)`; when checking a variant,
  `if nxt in bank_set and nxt not in forbidden and nxt not in seen`. Or
  precompute `bank_set -= forbidden`.
- **(d) Say:** "A forbidden set is just another membership check in the neighbor
  filter."

### Scenario 5 — "Each position has a different **mutation cost**; minimize total cost, not step count."

- **(b) Pattern:** the move graph is **weighted** → BFS is wrong.
- **(c) Adapt:** Dijkstra with a min-heap keyed by total cost; changing position
  `i` adds `cost[i]`. `O(states × L × Σ × log)`.
- **(d) Say:** "Per-position costs mean Dijkstra — same state graph, weighted
  edges."

### Scenario 6 — "Count the number of **distinct shortest** mutation sequences."

- **(b) Pattern:** BFS + a `ways` counter (like Number of Ways to Arrive at
  Destination).
- **(c) Adapt:** process BFS level by level. `ways[start] = 1`. When you first
  reach a gene at distance `d`, `ways[gene] = ways[predecessor]`; if you reach it
  *again at the same `d`* from another predecessor, `ways[gene] +=
  ways[predecessor]`. Answer is `ways[endGene]`.
- **(d) Say:** "Carry a `ways` count alongside the BFS distance: set it on first
  arrival, add to it on same-distance re-arrivals."

---

## 15. Flashcards

**Q:** What is this problem, in one line?
**A:** Word Ladder with length fixed at 8 and a 4-letter alphabet — BFS over gene
strings, `neighbors` = one-char changes kept only if in the bank.

**Q:** The two quick exits?
**A:** `start == end` → `0`; `end not in bank` (and `!= start`) → `-1` (the final
gene must be a valid bank gene).

**Q:** How many neighbors per gene, and how do you filter them?
**A:** `8 positions × 3 other letters = 24` variants; keep those in the
`bank_set` (an `O(1)` hash-set membership check) and not yet `seen`.

**Q:** Two ways to generate neighbors, and when to use each?
**A:** (1) Enumerate all `L × (Σ-1)` single-char variants and hash-check the bank
— best for a **large** bank. (2) Scan the bank for "differs by one" — best for a
**small** bank.

**Q:** Time and space?
**A:** `O(states × L² × Σ)` time, `O(states × L)` space. Tiny here (`bank ≤ 10`).

**Q:** Per-position mutation costs — what changes?
**A:** Weighted move graph → Dijkstra instead of BFS.

**Q:** Huge bank + large `L` — the optimizations?
**A:** Generate-and-hash-check (bank-size-independent), bidirectional BFS, and a
wildcard-pattern adjacency index (`"A*CCGGTT" → genes`).

---

## Appendix — Tejas's LeetCode Practice Answer

Solved and accepted on LeetCode. BFS, but instead of a separate `seen` set, it
**removes each visited gene from the bank** — the bank doubles as
"still-unvisited valid genes." This is the mutation-as-visited-mark trick from
Flood Fill / Walls and Gates, applied to a set.

```python
class Solution:
    def minMutation(self, startGene: str, endGene: str, bank: List[str]) -> int:
        bank = set(bank)

        queue = deque([[startGene, 0]])

        while queue:
            gene, mutations = queue.popleft()

            if gene == endGene:
                return mutations

            for i in range(len(gene)):
                for char in ['A', 'C', 'G', 'T']:
                    modified_gene = gene[:i] + char + gene[i + 1:]

                    if modified_gene in bank:
                        queue.append([modified_gene, mutations + 1])
                        bank.remove(modified_gene)      # visited-mark = remove from bank
        return -1
```

**Correct** — verified against all the section-8 tests plus a "start is in the
bank" case. Two things worth noting (neither breaks it):

1. **`bank` as the visited set.** Removing a gene the moment it's enqueued means
   it can never be re-enqueued — same effect as a `seen` set, one fewer
   structure. It mutates `bank`, but since you already rebound `bank = set(bank)`
   to a local copy, the caller's list is untouched. Clean and idiomatic.
2. **No `char != gene[i]` skip.** You generate the "no-op" mutation
   (`modified_gene == gene`). Normally harmless because `gene` was removed from
   the bank when it was enqueued — *except* for `startGene`, which is never
   removed. If `startGene` happens to be in the bank, the no-op re-enqueues it
   once as `[startGene, 1]`; that entry does nothing useful and never affects the
   answer (if `start == end` you already returned `0`). Still, adding
   `if char != gene[i]: continue` (or `bank.discard(startGene)` up front) tidies
   it up.
3. **No early-outs** for `start == end` or `end not in bank`. Works fine — the
   BFS returns `0` on the first pop, or exhausts and returns `-1` — just a hair
   less efficient than checking up front.
