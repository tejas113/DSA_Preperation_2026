# Heap / Priority Queue — Topic-by-Topic Roadmap

The full problem set, grouped into **3 topics** in study order. Do them top to bottom.
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
| **[+] Claude** | Not on either list. Added to close a real gap in heap technique coverage. Reason given under the topic. |

**Totals:** 12 problems — 2 on both lists · 2 LC150-only · 5 NC150-only · 3 Claude additions.
**Priority split:** 7 Core · 5 Stretch.

**Status key:** ☐ not started · ◐ in progress · ☑ done & code runs.

**Priority key:** **Core** — teaches a distinct heap technique not covered by any other problem in the list.
**Stretch** — a second/harder rep of a mechanic a Core problem already teaches.

**Scope:** every LC150 and NC150 problem in the Heap section, plus 3 extras for Google. Merge k Sorted Lists
(which has a heap solution) is in the Linked-List repo, and Top K Frequent Elements (bucket-sort solution) is
in Arrays-Strings.

---

## Topic 1 — Top-K & Kth Element

**Pattern:** keep a heap of size `k` that holds the best `k` items seen so far. The root of the heap is the kth best, and anything worse than the root can be ignored.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 1 | Kth Largest Element in a Stream | NC150 | 703 | Easy | Core | ☑ | [01-kth-largest-element-in-a-stream.md](01-top-k-and-kth-element/01-kth-largest-element-in-a-stream.md) |
| 2 | Kth Largest Element in an Array | **LC150 + NC150** | 215 | Medium | Core | ☑ | [02-kth-largest-element-in-an-array.md](01-top-k-and-kth-element/02-kth-largest-element-in-an-array.md) |
| 3 | K Closest Points to Origin | NC150 | 973 | Medium | Core | ☑ | [03-k-closest-points-to-origin.md](01-top-k-and-kth-element/03-k-closest-points-to-origin.md) |
| 4 | Top K Frequent Words | **[+] Claude** | 692 | Medium | Stretch | ☑ | [04-top-k-frequent-words.md](01-top-k-and-kth-element/04-top-k-frequent-words.md) |
| 5 | Kth Smallest Element in a Sorted Matrix | **[+] Claude** | 378 | Medium | Stretch | ☑ | [05-kth-smallest-element-in-a-sorted-matrix.md](01-top-k-and-kth-element/05-kth-smallest-element-in-a-sorted-matrix.md) |
| 6 | Find K Pairs with Smallest Sums | LC150 | 373 | Medium | Stretch | ☑ | [06-find-k-pairs-with-smallest-sums.md](01-top-k-and-kth-element/06-find-k-pairs-with-smallest-sums.md) |

> **Why #1–#3 are Core:** #1 is the size-`k` min-heap on a stream, #2 is the same on an array (and the
> Quickselect follow-up), and #3 uses a max-heap of size `k` on a computed key (distance).
> **Why #4–#6 are Stretch:** #4 adds a tie-break on the word, #5 pushes matrix cells onto a heap one
> row/column at a time (a binary-search version also exists), and #6 pushes the next pair from a sorted list
> — each is #2's idea with a small twist.

---

## Topic 2 — Scheduling & Greedy with a Heap

**Pattern:** repeatedly take the biggest (or smallest) remaining item, do something with it, and put back what's left.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 7 | Last Stone Weight | NC150 | 1046 | Easy | Core | ☑ | [07-last-stone-weight.md](02-scheduling-and-greedy-with-a-heap/07-last-stone-weight.md) |
| 8 | Task Scheduler | NC150 | 621 | Medium | Core | ☑ | [08-task-scheduler.md](02-scheduling-and-greedy-with-a-heap/08-task-scheduler.md) |
| 9 | Reorganize String | **[+] Claude** | 767 | Medium | Core | ☑ | [09-reorganize-string.md](02-scheduling-and-greedy-with-a-heap/09-reorganize-string.md) |
| 10 | Design Twitter | NC150 | 355 | Medium | Stretch | ☑ | [10-design-twitter.md](02-scheduling-and-greedy-with-a-heap/10-design-twitter.md) |

> **Why #7 is Core:** the plainest "pop the two largest, push back the difference" loop.
> **Why #8 and #9:** both use a max-heap of counts and a **cooldown / no-adjacent** rule (a queue holds items
> that are still cooling down in #8; the previous letter is held back in #9). #9 is a commonly asked
> Google-style question.
> **Why #10 is Stretch:** it's a long design question whose hard part is merging the `k` most recent tweets
> with a heap — the same idea as merging `k` sorted lists.

---

## Topic 3 — Two Heaps

**Pattern:** split the data into a lower half (a max-heap) and an upper half (a min-heap), so the middle is always available at the roots.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 11 | Find Median from Data Stream | **LC150 + NC150** | 295 | Hard | Core | ☑ | [11-find-median-from-data-stream.md](03-two-heaps/11-find-median-from-data-stream.md) |
| 12 | IPO | LC150 | 502 | Hard | Stretch | ☑ | [12-ipo.md](03-two-heaps/12-ipo.md) |

> **Why #11 is Core:** it is the classic two-heaps problem — a max-heap for the smaller half, a min-heap for
> the larger half, kept balanced — and one of the most-asked Hards.
> **Why #12 is Stretch:** two heaps used differently (a min-heap of capital to unlock projects, a max-heap of
> profit to pick from), and it is rarely asked.

---

## Coverage check — is this enough for a Google heap interview?

**Yes.** After these 3 topics you will have hands-on reps in: size-`k` heaps for top-k and kth, heaps on
computed keys, max-heap simulations, cooldown scheduling, no-adjacent rearrangement, and the two-heap median.

**The 5 Stretch problems** (#4, #5, #6, #10, #12) are the ones to drop first if time is tight.

**Deliberately out of scope, with reasons:**
- **Merge k Sorted Lists (LC 23)** — its heap solution is a Core problem in the Linked-List repo.
- **Top K Frequent Elements (LC 347)** — in Arrays-Strings (bucket sort); the heap version is just #2 on
  counts.
- **Meeting Rooms II (LC 253)** — in Arrays-Strings; its min-heap solution is mentioned there.
- **Sliding Window Median, Smallest Range Covering Elements from K Lists, Minimum Cost to Connect Sticks** —
  Hard or narrow variations on Topics 1 and 3.
