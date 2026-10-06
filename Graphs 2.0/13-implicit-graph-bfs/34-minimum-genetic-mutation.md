# 433. Minimum Genetic Mutation

**LC 433** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** BFS on an implicit graph (genes are nodes, a one-letter change is an edge)

---

## 1. Intuition

A gene is an 8-letter string of `A C G T`. One mutation changes **one letter**, and the result must be in the
`bank`. "Fewest mutations from start to end" is a shortest path where every step costs 1, so it's BFS
again. The graph isn't given. From any gene, you make the neighbours yourself by trying every position
with every letter, and keeping only the ones that are in the bank.

* **Generate neighbours on the fly:** the two loops `for i in range(len(gene))` and `for char in ['A','C','G','T']` build `modified_gene = gene[:i] + char + gene[i+1:]`. That's every gene one letter away.
* **The bank is the list of allowed nodes:** `if modified_gene in bank`. Turning `bank` into a `set` first makes this check fast.
* **Removing from the bank is the visited set:** `bank.remove(modified_gene)` right after pushing means each gene is queued at most once. That's marking it **when pushed**, with no separate `visited`.
* **BFS order gives the minimum:** `queue` holds `[gene, mutations]`. The first time `gene == endGene` is popped, `mutations` is the fewest steps.

**Recall:** BFS from `startGene`. Try every position × `ACGT`, and push a candidate if it's in the bank set, removing it from the bank as you push. Return `mutations` at `endGene`, or `-1`.

## 2. Approach

* **Idea:** Shortest path in an unweighted graph is BFS. The nodes are genes, and two genes are connected if they differ in exactly one position and the new one is in the bank.
* **Graph representation:** **implicit graph**. The nodes are `startGene` plus the bank genes, and the edges are created on the fly by the one-letter changes. Undirected in spirit, unweighted.
* **Data structure / pointers:**
  * `bank` (a `set`): genes that are allowed **and not yet queued**. A gene is removed the moment it's pushed, so the set doubles as "not visited yet".
  * `queue` (`deque`): `[gene, mutations]`, where `mutations` = the steps from `startGene`.
  * `modified_gene`: a candidate that is `gene` with position `i` replaced by `char`.
* **Invariant:** genes come off `queue` in order of `mutations`, and each gene's first (and only) push carries the fewest mutations needed to reach it.
* **Edge cases:**
  * `endGene` not in `bank` (and different from `startGene`): it can never be pushed, so it returns `-1`.
  * `startGene == endGene`: the first pop matches, so it returns `0`.
  * An empty `bank`: no neighbour passes the check, so it returns `-1` (unless start == end).
  * `startGene` is in the bank too: harmless. It isn't removed at the start, so it may be pushed once more later (or by itself when `char == gene[i]`), but it can never lower an answer.
  * `char == gene[i]` makes `modified_gene == gene`. It's pushed only if `gene` is still in the bank, and that can only be `startGene`, as above.
  * It's iterative, so there's no recursion-depth risk.

## 3. Code

```python
from collections import deque
from typing import List

class Solution:
    def minMutation(self, startGene: str, endGene: str, bank: List[str]) -> int:
        bank =  set(bank)

        queue = deque([[startGene,0]])

        while queue:
            gene,mutations = queue.popleft()

            if gene == endGene:
                return mutations

            for i in range(len(gene)):
                for char in ['A','C','G','T']:
                    modified_gene = gene[:i] + char + gene[i+1:]

                    if modified_gene in bank:
                        queue.append([modified_gene,mutations + 1])
                        bank.remove(modified_gene)
        return -1
```

## 4. Dry Run

Input (LC Example 2): `startGene = "AACCGGTT"`, `endGene = "AAACGGTA"`, `bank = {"AACCGGTA", "AACCGCTA", "AAACGGTA"}`

| Pop `[gene, mutations]` | Candidates found in `bank` (position: change) | Pushed, then removed from `bank` | `queue` after |
| --- | --- | --- | --- |
| `[AACCGGTT, 0]` | `i=7`: T→A gives `AACCGGTA` | `AACCGGTA` (1) | `[AACCGGTA, 1]` |
| `[AACCGGTA, 1]` | `i=2`: C→A gives `AAACGGTA`. `i=5`: G→C gives `AACCGCTA` | `AAACGGTA` (2), `AACCGCTA` (2) | `[AAACGGTA, 2] [AACCGCTA, 2]` |
| `[AAACGGTA, 2]` | it equals `endGene` | — | return **2** |

`bank` is empty after the second pop, so nothing can be pushed twice.

## 5. Complexity

Let **L** = gene length (8 on LC) and **B** = `len(bank)` (at most 10 on LC).

* **Time: O(B × L²)**
  Think of it as: each gene is popped at most once, and for each one you try L × 4 candidate strings. Building each candidate (`gene[:i] + char + gene[i+1:]`) copies L characters, and checking the set hashes L characters. So one pop costs about 4 × L × L, and there are at most B + 1 pops. With LC's limits (L = 8, B ≤ 10) that's a tiny, almost fixed amount of work.
* **Space: O(B × L)**
  Think of it as: the `bank` set and the `queue` each hold at most B genes of length L. Only one candidate string exists at a time.

## 6. Recall (30 seconds)

* Genes are nodes and one-letter changes that land in the bank are edges, so it's **BFS** for the fewest mutations.
* Turn `bank` into a **set**. Try every position × `ACGT`, and on a hit, push it and **remove it from the bank**. Removing it is the visited mark, applied when pushed.
* Return `mutations` when you pop `endGene`, otherwise `-1`. This is Word Ladder's little brother (#35).
