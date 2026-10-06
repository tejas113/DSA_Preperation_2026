# Binary Search — Topic-by-Topic Roadmap

The full problem set, grouped into **3 topics** in study order. Do them top to bottom.
Within each topic, the **Source** column tells you exactly where each problem comes from.

> **Note on source-tag confidence:** same caveat as the other trackers. This list was self-curated from
> memory, because live verification of the exact LeetCode Top 150 / NeetCode 150 category contents isn't
> possible here. Treat LC150 / NC150 tags as best-effort. The **[+] Claude** extras are picked from general
> knowledge of commonly asked interview problems, not from verified company-tagged data.

> **Scope note (2026-10-02):** the main tables below hold only the **12 Core** problems — the ones that each
> teach a distinct binary-search technique and that cover every shape asked in a Google L3 interview. The
> **4 Stretch** problems (second reps of a technique a Core problem already teaches) are moved to
> [Extra — Stretch problems](#extra--stretch-problems) at the end, in the same topic order, to do only if time allows.

---

## Source legend

| Badge | Meaning |
|---|---|
| **LC150** | On LeetCode's official *Top Interview 150* list |
| **NC150** | On the *NeetCode 150* list |
| **LC150 + NC150** | On **both** lists — highest-priority, most-asked |
| **[+] Claude** | Not on either list. Added to close a real gap in binary-search technique coverage. Reason given under the topic. |

**Totals:** 16 problems — 4 on both lists · 4 LC150-only · 3 NC150-only · 5 Claude additions.
**Priority split:** 12 Core · 4 Stretch.

**Status key:** ☐ not started · ◐ in progress · ☑ done & code runs.

**Priority key:** **Core** — teaches a distinct binary-search technique not covered by any other problem in the
list. **Stretch** — a second/harder rep of a mechanic a Core problem already teaches.

**Scope:** every LC150 problem in the Binary Search section, every NC150 problem in the Binary Search
section, Sqrt(x) (LC150 Math, since it is a binary search on the answer), plus 5 extras for Google.

---

## Topic 1 — Binary Search on a Sorted Sequence

**Pattern:** keep a range `[lo, hi]`, look at the middle, and throw away the half that cannot contain the answer. Two forms: find an exact target, or find the **first index where a condition becomes true** (a boundary).

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 1 | Binary Search | NC150 | 704 | Easy | Core | ☑ | [01-binary-search.md](01-binary-search-on-sorted-sequences/01-binary-search.md) |
| 2 | Search Insert Position | LC150 | 35 | Easy | Core | ☑ | [02-search-insert-position.md](01-binary-search-on-sorted-sequences/02-search-insert-position.md) |
| 3 | Find First and Last Position of Element in Sorted Array | LC150 | 34 | Medium | Core | ☑ | [03-find-first-and-last-position-of-element-in-sorted-array.md](01-binary-search-on-sorted-sequences/03-find-first-and-last-position-of-element-in-sorted-array.md) |
| 4 | Search a 2D Matrix | **LC150 + NC150** | 74 | Medium | Core | ☑ | [04-search-a-2d-matrix.md](01-binary-search-on-sorted-sequences/04-search-a-2d-matrix.md) |
| 5 | Find K Closest Elements | **[+] Claude** | 658 | Medium | Core | ☑ | [05-find-k-closest-elements.md](01-binary-search-on-sorted-sequences/05-find-k-closest-elements.md) |
| 6 | Time Based Key-Value Store | NC150 | 981 | Medium | Core | ☑ | [06-time-based-key-value-store.md](01-binary-search-on-sorted-sequences/06-time-based-key-value-store.md) |

> **Why #2 is Core:** it introduces the boundary form (`while lo < hi`, `hi = mid`) that #3 builds on twice.
> **Why #5:** it searches for the *start of a window* (`lo` in `[0, n - k]`) by comparing the distance to each
> end of the window — a different thing to search for than a value, and a common Google-style question.
> **Why #6:** a real design question — one sorted list of timestamps per key, and "find the latest timestamp
> at or before the query" is a boundary search.

---

## Topic 2 — Rotated, Modified & Partition Searches

**Pattern:** the array isn't plainly sorted, but a comparison at `mid` still tells you which half to keep.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 7 | Search in Rotated Sorted Array | **LC150 + NC150** | 33 | Medium | Core | ☑ | [07-search-in-rotated-sorted-array.md](02-rotated-modified-and-partition-searches/07-search-in-rotated-sorted-array.md) |
| 8 | Find Minimum in Rotated Sorted Array | **LC150 + NC150** | 153 | Medium | Core | ☑ | [08-find-minimum-in-rotated-sorted-array.md](02-rotated-modified-and-partition-searches/08-find-minimum-in-rotated-sorted-array.md) |
| 9 | Find Peak Element | LC150 | 162 | Medium | Core | ☑ | [09-find-peak-element.md](02-rotated-modified-and-partition-searches/09-find-peak-element.md) |
| 10 | Median of Two Sorted Arrays | **LC150 + NC150** | 4 | Hard | Core | ☑ | [10-median-of-two-sorted-arrays.md](02-rotated-modified-and-partition-searches/10-median-of-two-sorted-arrays.md) |

> **Why #9 is Core:** the array isn't sorted at all — you binary search by comparing `nums[mid]` with a
> neighbor and moving uphill.
> **Why #10 is Core:** it searches for a *cut* in the smaller array rather than a value, which is the hardest
> and most-asked binary-search idea in the list.

---

## Topic 3 — Binary Search on the Answer

**Pattern:** you aren't searching an array — you are searching the range of possible **answers**. Pick a guess `mid`, test whether it is feasible, and use that yes/no to halve the range.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 11 | Koko Eating Bananas | NC150 | 875 | Medium | Core | ☑ | [11-koko-eating-bananas.md](03-binary-search-on-the-answer/11-koko-eating-bananas.md) |
| 12 | Sqrt(x) | LC150 | 69 | Easy | Core | ☑ | [12-sqrtx.md](03-binary-search-on-the-answer/12-sqrtx.md) |

> **Why #11 and #12 are Core:** #11 has a feasibility function (`can Koko finish in h hours at speed k?`), and
> #12 is the simplest possible search on the answer (`is mid * mid <= x?`). Together they teach the whole idea.

---

## Coverage check — is this enough for a Google binary-search interview?

**Yes.** After these 12 Core problems you will have hands-on reps in: exact-match search, boundary search, searching a
2D matrix as a flat list, searching for a window start, floor lookups by timestamp, rotated arrays,
neighbor-comparison peak finding, partition search (median), and search-on-the-answer with a feasibility check.

**Deliberately out of scope, with reasons:**
- **Search in Rotated Sorted Array II (LC 81, with duplicates)** — the same idea as #7 plus a worst case of
  `O(n)`. Add later if you want the follow-up.
- **Kth Smallest Element in a Sorted Matrix (LC 378)** — lives in the Heap repo; the binary-search version is
  mentioned there as the follow-up.
- **Random Pick with Weight (LC 528)** — a prefix sum plus a boundary search; a fine extra, but it needs no
  new binary-search idea.
- **Find in Mountain Array, Search in Infinite Array, and similar** — variations on Topic 1 and Topic 2.

---

## Extra — Stretch problems

Second/harder reps of a technique a Core problem above already teaches. Do these only if time allows, in this
same topic order; they're the first thing to drop if time is tight.

| # | Problem | Source | LC # | Difficulty | Priority | Topic | Status | File |
|---|---|---|---|---|---|---|---|---|
| 13 | First Bad Version | **[+] Claude** | 278 | Easy | Stretch | 1 | ☑ | [13-first-bad-version.md](01-binary-search-on-sorted-sequences/13-first-bad-version.md) |
| 14 | Single Element in a Sorted Array | **[+] Claude** | 540 | Medium | Stretch | 2 | ☐ | TBD |
| 15 | Capacity To Ship Packages Within D Days | **[+] Claude** | 1011 | Medium | Stretch | 3 | ☐ | TBD |
| 16 | Split Array Largest Sum | **[+] Claude** | 410 | Hard | Stretch | 3 | ☐ | TBD |

> **Why #13 is Stretch:** it is the same boundary search as #2, with a yes/no function instead of a comparison.
> **Why #14 is Stretch:** it is a neat parity trick (pairs start at even indexes until the single element),
> but it is a one-off idea.
> **Why #15 and #16 are Stretch:** both reuse #11's shape — search the answer, check feasibility with one
> pass. #16 is the Hard version (minimize the largest subarray sum).
