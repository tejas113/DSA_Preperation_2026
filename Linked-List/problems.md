# Linked List — Topic-by-Topic Roadmap

The full problem set, grouped into **4 topics** in study order. Do them top to bottom.
Within each topic, the **Source** column tells you exactly where each problem comes from.

> **Note on source-tag confidence:** same caveat as the other trackers. This list was self-curated from
> memory, because live verification of the exact LeetCode Top 150 / NeetCode 150 category contents isn't
> possible here. Treat LC150 / NC150 tags as best-effort. The **[+] Claude** extras are picked from general
> knowledge of commonly asked interview problems, not from verified company-tagged data.

---

## Source legend

| Badge | Meaning |
|---|---|
| **LC150** | On LeetCode's official *Top Interview 150* list |
| **NC150** | On the *NeetCode 150* list |
| **LC150 + NC150** | On **both** lists — highest-priority, most-asked |
| **[+] Claude** | Not on either list. Added to close a real gap in linked-list technique coverage. Reason given under the topic. |

**Totals:** 20 problems — 7 on both lists · 5 LC150-only · 4 NC150-only · 4 Claude additions.
**Priority split:** 15 Core · 5 Stretch.

**Status key:** ☐ not started · ◐ in progress · ☑ done & code runs.

**Priority key:** **Core** — teaches a distinct linked-list technique not covered by any other problem in the
list. **Stretch** — a second/harder rep of a mechanic a Core problem already teaches.

**Scope:** every LC150 problem in the Linked List section, every NC150 problem in the Linked List section
(including Find the Duplicate Number), Sort List (LC150 Divide & Conquer), plus 4 extras for Google.

---

## Topic 1 — Reversal & Pointer Rewiring

**Pattern:** walk the list and re-point each node's `next` using three pointers (`prev`, `curr`, `next`). Reversing a whole list, part of a list, or groups all use the same move.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 1 | Reverse Linked List | NC150 | 206 | Easy | Core | ☑ | [01-reverse-linked-list.md](01-reversal-and-rewiring/01-reverse-linked-list.md) |
| 2 | Reverse Linked List II | LC150 | 92 | Medium | Core | ☑ | [02-reverse-linked-list-ii.md](01-reversal-and-rewiring/02-reverse-linked-list-ii.md) |
| 3 | Reverse Nodes in k-Group | **LC150 + NC150** | 25 | Hard | Core | ☑ | [03-reverse-nodes-in-k-group.md](01-reversal-and-rewiring/03-reverse-nodes-in-k-group.md) |
| 4 | Rotate List | LC150 | 61 | Medium | Stretch | ☑ | [04-rotate-list.md](01-reversal-and-rewiring/04-rotate-list.md) |

> **Why these are Core:** #1 is the base move; #2 reverses only the middle section, so you must reconnect
> both ends; #3 repeats that in groups and needs "is there a full group left?" logic.
> **Why #4 is Stretch:** it is "find the length, find the new tail, reconnect" — no new pointer idea.

---

## Topic 2 — Fast & Slow (and Gap) Pointers

**Pattern:** two pointers walking the same list at different speeds, or with a fixed gap between them, so you find a position (middle, cycle, n-th from the end) in one pass.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 5 | Middle of the Linked List | **[+] Claude** | 876 | Easy | Core | ☐ | TBD |
| 6 | Linked List Cycle | **LC150 + NC150** | 141 | Easy | Core | ☑ | [06-linked-list-cycle.md](02-fast-slow-and-gap-pointers/06-linked-list-cycle.md) |
| 7 | Linked List Cycle II | **[+] Claude** | 142 | Medium | Core | ☐ | TBD |
| 8 | Remove Nth Node From End of List | **LC150 + NC150** | 19 | Medium | Core | ☑ | [08-remove-nth-node-from-end-of-list.md](02-fast-slow-and-gap-pointers/08-remove-nth-node-from-end-of-list.md) |
| 9 | Reorder List | NC150 | 143 | Medium | Core | ☐ | TBD |
| 10 | Intersection of Two Linked Lists | **[+] Claude** | 160 | Easy | Core | ☐ | TBD |
| 11 | Palindrome Linked List | **[+] Claude** | 234 | Easy | Stretch | ☐ | TBD |
| 12 | Find the Duplicate Number | NC150 | 287 | Medium | Stretch | ☐ | TBD |

> **Why #5 and #7:** #5 is the tool (slow/fast finds the middle) that #9 and #11 use. #7 goes one step
> beyond #6 — *where* the cycle starts — which is the most commonly asked cycle question.
> **Why #10:** two pointers that switch to the other list's head after reaching the end, so both walk the
> same total distance and meet at the intersection — a distinct and frequently asked trick.
> **Why #11 and #12 are Stretch:** #11 is middle + reverse + compare, which #9 already teaches. #12 is
> Floyd's algorithm on an array instead of a list, so it needs #6 and #7 first.

---

## Topic 3 — Merge, Split & Dummy-Node Construction

**Pattern:** build a new list (or rewire an old one) with a **dummy node** in front and a `tail` pointer, so you never special-case the head.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 13 | Merge Two Sorted Lists | **LC150 + NC150** | 21 | Easy | Core | ☑ | [13-merge-two-sorted-lists.md](03-merge-split-and-dummy-node/13-merge-two-sorted-lists.md) |
| 14 | Add Two Numbers | **LC150 + NC150** | 2 | Medium | Core | ☑ | [14-add-two-numbers.md](03-merge-split-and-dummy-node/14-add-two-numbers.md) |
| 15 | Remove Duplicates from Sorted List II | LC150 | 82 | Medium | Core | ☑ | [15-remove-duplicates-from-sorted-list-ii.md](03-merge-split-and-dummy-node/15-remove-duplicates-from-sorted-list-ii.md) |
| 16 | Merge k Sorted Lists | NC150 | 23 | Hard | Core | ☐ | TBD |
| 17 | Partition List | LC150 | 86 | Medium | Stretch | ☑ | [17-partition-list.md](03-merge-split-and-dummy-node/17-partition-list.md) |
| 18 | Sort List | LC150 | 148 | Medium | Stretch | ☐ | TBD |

> **Why these are Core:** #13 is the dummy + tail template; #14 adds a carry; #15 shows why a dummy is needed
> (the head itself may be removed); #16 is the same merge idea at scale with a heap or divide and conquer.
> **Why #17 and #18 are Stretch:** #17 builds two dummy lists and joins them; #18 is merge sort on a list
> and just combines #5 (middle) with #13 (merge).

---

## Topic 4 — Hash Map + List / Design

**Pattern:** a plain list can't do random access, so pair it with a hash map — either to remember which new node matches which old node, or to jump straight to a node.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 19 | Copy List with Random Pointer | **LC150 + NC150** | 138 | Medium | Core | ☑ | [19-copy-list-with-random-pointer.md](04-hash-map-and-design/19-copy-list-with-random-pointer.md) |
| 20 | LRU Cache | **LC150 + NC150** | 146 | Medium | Core | ☑ | [20-lru-cache.md](04-hash-map-and-design/20-lru-cache.md) |

> **Why both are Core:** #19 uses a map from old node to new node (or interleaving as an `O(1)`-space
> alternative). #20 combines a hash map with a **doubly** linked list so both `get` and `put` are `O(1)` — one
> of the most-asked design questions of all.

---

## Coverage check — is this enough for a Google linked-list interview?

**Yes.** After these 4 topics you will have hands-on reps in: reversing a whole list, a range and groups;
finding the middle, a cycle and its start; the n-th node from the end; list intersection; merging two and `k`
lists; the dummy-node pattern; deep-copying with a map; and an LRU cache built from a hash map and a doubly
linked list.

**The 5 Stretch problems** (#4, #11, #12, #17, #18) are the ones to drop first if time is tight.

**Deliberately out of scope, with reasons:**
- **LFU Cache (LC 460)** — a Hard extension of #20; add later if you want it.
- **Flatten a Multilevel Doubly Linked List, Odd Even Linked List, Swap Nodes in Pairs** — variations on the
  pointer-rewiring moves already covered (Swap Nodes in Pairs is #3 with a group size of 2).
- **Design Browser History and other small design questions** — array or stack versions are simpler and
  covered elsewhere.
- **Convert Sorted List to BST** — covered by the Trees repo.
