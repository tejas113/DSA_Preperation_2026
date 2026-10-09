# Arrays & Strings — Topic-by-Topic Roadmap

The full problem set, grouped into **9 topics** in study order. Do them top to bottom.
Within each topic, the **Source** column tells you exactly where each problem comes from.

An appendix of **10 optional [+] Claude problems** sits at the very end of this file. Each one is an extra
rep of a technique a mandatory problem already teaches — they are not part of the numbered study path.
Do them only if you finish everything else with time to spare.

> **Note on source-tag confidence:** same caveat as the Backtracking tracker. This list was self-curated from
> memory, because live verification of the exact LeetCode Top 150 / NeetCode 150 category contents isn't
> possible here. Treat LC150 / NC150 tags as best-effort, not independently confirmed. The **[+] Claude**
> extras are picked from general knowledge of commonly asked interview problems, not from verified
> company-tagged data.

---

## Source legend

| Badge | Meaning |
|---|---|
| **LC150** | On LeetCode's official *Top Interview 150* list |
| **NC150** | On the *NeetCode 150* list |
| **LC150 + NC150** | On **both** lists — highest-priority, most-asked |
| **[+] Claude** | Not on either list. Added to close a real gap in array/string technique coverage. Reason given under the topic. |

**Totals:** 70 mandatory problems — 24 on both lists · 28 LC150-only · 11 NC150-only · 7 Claude additions.
10 more optional **[+] Claude** problems live in the appendix at the end of this file, outside the numbered
study path (so the full set, main + appendix, is still 80).
**Priority split (mandatory list):** 52 Core · 18 Stretch.

**Status key:** ☐ not started · ◐ in progress · ☑ done & code runs.

**Priority key:** **Core** — teaches a distinct array/string technique not covered by any other problem in the
list. **Stretch** — a second/harder rep of a mechanic a Core problem already teaches, or a niche problem
that is unlikely to be asked.

**Premium note:** five problems are LeetCode Premium — #7 Encode and Decode Strings (271), #29 Longest
Substring with At Most K Distinct Characters (340), #37 Meeting Rooms II (253) and #41 Meeting Rooms (252)
in the main list, plus One Edit Distance (161) in the optional appendix. All five have free equivalents
(LintCode, or the same problem restated in an interview).

**Scope:** every LC150 problem in the Array/String, Two Pointers, Sliding Window, Matrix, Hashmap and Intervals
sections, plus Plus One (LC150 Math); every NC150 problem in Arrays & Hashing, Two Pointers, Sliding Window and
Intervals, plus the array-shaped ones from Math & Geometry and Greedy; plus 7 extras for Google baked into the
main path. 10 more optional extras sit in the appendix at the end of this file.

---

## Topic 1 — Arrays & Hashing

**Pattern:** walk the input once and remember what you've seen in a `set` or `dict`, so every later check is O(1).

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 1 | Contains Duplicate | NC150 | 217 | Easy | Core | ☑ | [01-arrays-and-hashing/01-contains-duplicate.md](01-arrays-and-hashing/01-contains-duplicate.md) |
| 2 | Valid Anagram | **LC150 + NC150** | 242 | Easy | Core | ☑ | [01-arrays-and-hashing/02-valid-anagram.md](01-arrays-and-hashing/02-valid-anagram.md) |
| 3 | Two Sum | **LC150 + NC150** | 1 | Easy | Core | ☑ | [01-arrays-and-hashing/03-two-sum.md](01-arrays-and-hashing/03-two-sum.md) |
| 4 | Group Anagrams | **LC150 + NC150** | 49 | Medium | Core | ☑ | [01-arrays-and-hashing/04-group-anagrams.md](01-arrays-and-hashing/04-group-anagrams.md) |
| 5 | Top K Frequent Elements | NC150 | 347 | Medium | Core | ☑ | [01-arrays-and-hashing/05-top-k-frequent-elements.md](01-arrays-and-hashing/05-top-k-frequent-elements.md) |
| 6 | Longest Consecutive Sequence | **LC150 + NC150** | 128 | Medium | Core | ☑ | [01-arrays-and-hashing/06-longest-consecutive-sequence.md](01-arrays-and-hashing/06-longest-consecutive-sequence.md) |
| 7 | Encode and Decode Strings | NC150 | 271 | Medium | Core | ☑ | [01-arrays-and-hashing/07-encode-and-decode-strings.md](01-arrays-and-hashing/07-encode-and-decode-strings.md) |
| 8 | Insert Delete GetRandom O(1) | LC150 | 380 | Medium | Core | ☑ | [01-arrays-and-hashing/08-insert-delete-getrandom-o1.md](01-arrays-and-hashing/08-insert-delete-getrandom-o1.md) |
| 9 | Isomorphic Strings | LC150 | 205 | Easy | Core | ☑ | [01-arrays-and-hashing/09-isomorphic-strings.md](01-arrays-and-hashing/09-isomorphic-strings.md) |
| 10 | Ransom Note | LC150 | 383 | Easy | Stretch | ☑ | [01-arrays-and-hashing/10-ransom-note.md](01-arrays-and-hashing/10-ransom-note.md) |
| 11 | Word Pattern | LC150 | 290 | Easy | Stretch | ☑ | [01-arrays-and-hashing/11-word-pattern.md](01-arrays-and-hashing/11-word-pattern.md) |
| 12 | Contains Duplicate II | LC150 | 219 | Easy | Stretch | ☑ | [01-arrays-and-hashing/12-contains-duplicate-ii.md](01-arrays-and-hashing/12-contains-duplicate-ii.md) |
| 13 | Happy Number | **LC150 + NC150** | 202 | Easy | Stretch | ☑ | [01-arrays-and-hashing/13-happy-number.md](01-arrays-and-hashing/13-happy-number.md) |

> **Why these are Core:** each teaches a different hashing move — a seen-set (#1), a frequency count (#2), a
> complement lookup (#3), a canonical key for grouping (#4), bucketing by frequency (#5), starting only at the
> beginning of a run (#6), length-prefix encoding (#7), a map + array with swap-with-last (#8), and a
> two-way mapping (#9).
> **Why the rest are Stretch:** #10 is #2's frequency count, #11 is #9's mapping on words, #12 is #1's set
> with a window, and #13 is a cycle check with a set.

---

## Topic 2 — Two Pointers

**Pattern:** two indices walk the array — toward each other or side by side — and the current values tell you which one to move.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 14 | Valid Palindrome | **LC150 + NC150** | 125 | Easy | Core | ☑ | [02-two-pointers/14-valid-palindrome.md](02-two-pointers/14-valid-palindrome.md) |
| 15 | Valid Palindrome II | **[+] Claude** | 680 | Easy | Core | ☑ | [02-two-pointers/15-valid-palindrome-ii.md](02-two-pointers/15-valid-palindrome-ii.md) |
| 16 | Is Subsequence | LC150 | 392 | Easy | Core | ☑ | [02-two-pointers/16-is-subsequence.md](02-two-pointers/16-is-subsequence.md) |
| 17 | Two Sum II — Input Array Is Sorted | **LC150 + NC150** | 167 | Medium | Core | ☑ | [02-two-pointers/17-two-sum-ii.md](02-two-pointers/17-two-sum-ii.md) |
| 18 | 3Sum | **LC150 + NC150** | 15 | Medium | Core | ☑ | [02-two-pointers/18-3sum.md](02-two-pointers/18-3sum.md) |
| 19 | Container With Most Water | **LC150 + NC150** | 11 | Medium | Core | ☑ | [02-two-pointers/19-container-with-most-water.md](02-two-pointers/19-container-with-most-water.md) |
| 20 | Trapping Rain Water | **LC150 + NC150** | 42 | Hard | Core | ☑ | [02-two-pointers/20-trapping-rain-water.md](02-two-pointers/20-trapping-rain-water.md) |
| 21 | Sort Colors | **[+] Claude** | 75 | Medium | Core | ☑ | [02-two-pointers/21-sort-colors.md](02-two-pointers/21-sort-colors.md) |

> **Why #15:** #14 only compares the two ends. #15 asks what to do on the first mismatch — try skipping either
> side — which is the "one mistake allowed" wrinkle that interviewers often add as a follow-up.
> **Why #21:** it's the three-pointer (`low`, `mid`, `high`) partition, a different move from every other
> two-pointer problem here, and a commonly asked in-place question.
> **Two Stretch problems that used to sit here** (Backspace String Compare, One Edit Distance) have been
> moved to the optional appendix at the end of this file — see there for why.

---

## Topic 3 — Sliding Window

**Pattern:** keep a window `[left, right]` over a contiguous chunk. Grow `right`, and shrink `left` whenever the window becomes invalid.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 22 | Best Time to Buy and Sell Stock | **LC150 + NC150** | 121 | Easy | Core | ☑ | [03-sliding-window/22-best-time-to-buy-and-sell-stock.md](03-sliding-window/22-best-time-to-buy-and-sell-stock.md) |
| 23 | Longest Substring Without Repeating Characters | **LC150 + NC150** | 3 | Medium | Core | ☑ | [03-sliding-window/23-longest-substring-without-repeating-characters.md](03-sliding-window/23-longest-substring-without-repeating-characters.md) |
| 24 | Longest Repeating Character Replacement | NC150 | 424 | Medium | Core | ☑ | [03-sliding-window/24-longest-repeating-character-replacement.md](03-sliding-window/24-longest-repeating-character-replacement.md) |
| 25 | Permutation in String | NC150 | 567 | Medium | Core | ☑ | [03-sliding-window/25-permutation-in-string.md](03-sliding-window/25-permutation-in-string.md) |
| 26 | Minimum Size Subarray Sum | LC150 | 209 | Medium | Core | ☑ | [03-sliding-window/26-minimum-size-subarray-sum.md](03-sliding-window/26-minimum-size-subarray-sum.md) |
| 27 | Minimum Window Substring | **LC150 + NC150** | 76 | Hard | Core | ☑ | [03-sliding-window/27-minimum-window-substring.md](03-sliding-window/27-minimum-window-substring.md) |
| 28 | Sliding Window Maximum | NC150 | 239 | Hard | Core | ☑ | [03-sliding-window/28-sliding-window-maximum.md](03-sliding-window/28-sliding-window-maximum.md) |
| 29 | Longest Substring with At Most K Distinct Characters | **[+] Claude** | 340 | Medium | Core | ☑ | [03-sliding-window/29-longest-substring-with-at-most-k-distinct-characters.md](03-sliding-window/29-longest-substring-with-at-most-k-distinct-characters.md) |
| 30 | Substring with Concatenation of All Words | LC150 | 30 | Hard | Stretch | ☑ | [03-sliding-window/30-substring-with-concatenation-of-all-words.md](03-sliding-window/30-substring-with-concatenation-of-all-words.md) |

> **Why these are Core:** #22 tracks a running minimum, #23 a window with no repeats, #24 a window that is
> valid when `size - max_freq <= k`, #25 a fixed-size window compared by frequency, #26 a shrinking window on
> positive numbers, #27 a window that must cover a set of required characters, and #28 a monotonic deque.
> **Why #29:** it is the general "at most K distinct" window (a hash map of counts), which also solves
> "at most two distinct" and "Fruit Into Baskets". It is a commonly asked Google-style variant.
> **Why #30 is Stretch:** it's #27's idea (covering a required set) applied to whole words instead of
> characters, which is heavy to code and rarely asked.
> **Two Stretch problems that used to sit here** (Find All Anagrams in a String, Max Consecutive Ones III)
> have been moved to the optional appendix at the end of this file — see there for why.

---

## Topic 4 — Prefix Sum, Kadane & Running Products

**Pattern:** precompute a running total (or product) so any range can be answered in O(1), or carry a running best while you scan.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 31 | Product of Array Except Self | **LC150 + NC150** | 238 | Medium | Core | ☑ | [04-prefix-sum-and-kadane/31-product-of-array-except-self.md](04-prefix-sum-and-kadane/31-product-of-array-except-self.md) |
| 32 | Maximum Subarray | NC150 | 53 | Medium | Core | ☑ | [04-prefix-sum-and-kadane/32-maximum-subarray.md](04-prefix-sum-and-kadane/32-maximum-subarray.md) |
| 33 | Subarray Sum Equals K | **[+] Claude** | 560 | Medium | Core | ☑ | [04-prefix-sum-and-kadane/33-subarray-sum-equals-k.md](04-prefix-sum-and-kadane/33-subarray-sum-equals-k.md) |

> **Why #33:** #26 finds a subarray sum with a window, but that only works when every number is positive.
> #33 works with negatives too, using prefix sums plus a hash map. That is the technique the sliding window
> can't replace, and it is one of the most commonly asked array questions.
> **One Stretch problem that used to sit here** (Contiguous Array) has been moved to the optional appendix
> at the end of this file — see there for why.

---

## Topic 5 — Intervals

**Pattern:** sort the intervals (by start, or by end), then decide by comparing each one with the previous one.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 34 | Merge Intervals | **LC150 + NC150** | 56 | Medium | Core | ☑ | [05-intervals/34-merge-intervals.md](05-intervals/34-merge-intervals.md) |
| 35 | Insert Interval | **LC150 + NC150** | 57 | Medium | Core | ☑ | [05-intervals/35-insert-interval.md](05-intervals/35-insert-interval.md) |
| 36 | Non-overlapping Intervals | NC150 | 435 | Medium | Core | ☑ | [05-intervals/36-non-overlapping-intervals.md](05-intervals/36-non-overlapping-intervals.md) |
| 37 | Meeting Rooms II | NC150 | 253 | Medium | Core | ☑ | [05-intervals/37-meeting-rooms-ii.md](05-intervals/37-meeting-rooms-ii.md) |
| 38 | Interval List Intersections | **[+] Claude** | 986 | Medium | Core | ☑ | [05-intervals/38-interval-list-intersections.md](05-intervals/38-interval-list-intersections.md) |
| 39 | Summary Ranges | LC150 | 228 | Easy | Stretch | ☑ | [05-intervals/39-summary-ranges.md](05-intervals/39-summary-ranges.md) |
| 40 | Minimum Number of Arrows to Burst Balloons | LC150 | 452 | Medium | Stretch | ☑ | [05-intervals/40-minimum-number-of-arrows-to-burst-balloons.md](05-intervals/40-minimum-number-of-arrows-to-burst-balloons.md) |
| 41 | Meeting Rooms | NC150 | 252 | Easy | Stretch | ☑ | [05-intervals/41-meeting-rooms.md](05-intervals/41-meeting-rooms.md) |

> **Why #36 and #37 are Core:** #36 is the greedy "sort by end, keep the earliest-ending" idea, and #37 is a
> sweep line or heap for counting how many overlap at once — different from merging.
> **Why #38:** it's two pointers across *two* sorted interval lists, a move none of the others use, and a
> common Google-style question.
> **Why the rest are Stretch:** #39 is a simple scan for runs, #40 is #36's greedy again, and #41 is just
> "does the sorted list overlap".

---

## Topic 6 — Matrix / 2D Array

**Pattern:** index math on rows and columns, usually done in place — transposing, peeling layers, or using the first row and column as markers.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 42 | Valid Sudoku | **LC150 + NC150** | 36 | Medium | Core | ☑ | [06-matrix/42-valid-sudoku.md](06-matrix/42-valid-sudoku.md) |
| 43 | Rotate Image | **LC150 + NC150** | 48 | Medium | Core | ☑ | [06-matrix/43-rotate-image.md](06-matrix/43-rotate-image.md) |
| 44 | Spiral Matrix | **LC150 + NC150** | 54 | Medium | Core | ☑ | [06-matrix/44-spiral-matrix.md](06-matrix/44-spiral-matrix.md) |
| 45 | Set Matrix Zeroes | **LC150 + NC150** | 73 | Medium | Core | ☑ | [06-matrix/45-set-matrix-zeroes.md](06-matrix/45-set-matrix-zeroes.md) |
| 46 | Game of Life | LC150 | 289 | Medium | Stretch | ☑ | [06-matrix/46-game-of-life.md](06-matrix/46-game-of-life.md) |

> **Why #46 is Stretch:** it reuses #45's "store extra state inside the matrix so it can be updated in place"
> idea, with more cases. It is rarely asked.
> **One Stretch problem that used to sit here** (Diagonal Traverse) has been moved to the optional appendix
> at the end of this file — see there for why.

---

## Topic 7 — In-Place Array Manipulation

**Pattern:** overwrite the array using a read pointer and a write pointer, fill from the back, or reverse pieces — with no extra array.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 47 | Merge Sorted Array | LC150 | 88 | Easy | Core | ☑ | [07-in-place-array-manipulation/47-merge-sorted-array.md](07-in-place-array-manipulation/47-merge-sorted-array.md) |
| 48 | Remove Element | LC150 | 27 | Easy | Core | ☑ | [07-in-place-array-manipulation/48-remove-element.md](07-in-place-array-manipulation/48-remove-element.md) |
| 49 | Remove Duplicates from Sorted Array | LC150 | 26 | Easy | Core | ☑ | [07-in-place-array-manipulation/49-remove-duplicates-from-sorted-array.md](07-in-place-array-manipulation/49-remove-duplicates-from-sorted-array.md) |
| 50 | Rotate Array | LC150 | 189 | Medium | Core | ☑ | [07-in-place-array-manipulation/50-rotate-array.md](07-in-place-array-manipulation/50-rotate-array.md) |
| 51 | Next Permutation | **[+] Claude** | 31 | Medium | Core | ☑ | [07-in-place-array-manipulation/51-next-permutation.md](07-in-place-array-manipulation/51-next-permutation.md) |
| 52 | Plus One | **LC150 + NC150** | 66 | Easy | Stretch | ☑ | [07-in-place-array-manipulation/52-plus-one.md](07-in-place-array-manipulation/52-plus-one.md) |
| 53 | Remove Duplicates from Sorted Array II | LC150 | 80 | Medium | Stretch | ☑ | [07-in-place-array-manipulation/53-remove-duplicates-from-sorted-array-ii.md](07-in-place-array-manipulation/53-remove-duplicates-from-sorted-array-ii.md) |

> **Why these are Core:** #47 fills from the back, #48 and #49 are the read/write pointer pair, #50 is three
> reversals, and #51 is "find the pivot, swap, reverse the tail".
> **Why #51:** it is a classic asked at Google and Amazon, and it is the one array problem here where the
> algorithm itself has to be figured out, not just applied.
> **Two Stretch problems that used to sit here** (Move Zeroes, First Missing Positive) have been moved to
> the optional appendix at the end of this file — see there for why.

---

## Topic 8 — Greedy & One-Pass Array Scans

**Pattern:** scan once, keeping a running summary (farthest reach, tank level, candidate) so you never have to undo an earlier choice.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 54 | Majority Element | LC150 | 169 | Easy | Core | ☑ | [08-greedy-one-pass-scans/54-majority-element.md](08-greedy-one-pass-scans/54-majority-element.md) |
| 55 | Jump Game | **LC150 + NC150** | 55 | Medium | Core | ☑ | [08-greedy-one-pass-scans/55-jump-game.md](08-greedy-one-pass-scans/55-jump-game.md) |
| 56 | Jump Game II | **LC150 + NC150** | 45 | Medium | Core | ☑ | [08-greedy-one-pass-scans/56-jump-game-ii.md](08-greedy-one-pass-scans/56-jump-game-ii.md) |
| 57 | Gas Station | **LC150 + NC150** | 134 | Medium | Core | ☑ | [08-greedy-one-pass-scans/57-gas-station.md](08-greedy-one-pass-scans/57-gas-station.md) |
| 58 | Best Time to Buy and Sell Stock II | LC150 | 122 | Medium | Stretch | ☑ | [08-greedy-one-pass-scans/58-best-time-to-buy-and-sell-stock-ii.md](08-greedy-one-pass-scans/58-best-time-to-buy-and-sell-stock-ii.md) |
| 59 | H-Index | LC150 | 274 | Medium | Stretch | ☑ | [08-greedy-one-pass-scans/59-h-index.md](08-greedy-one-pass-scans/59-h-index.md) |
| 60 | Candy | LC150 | 135 | Hard | Stretch | ☑ | [08-greedy-one-pass-scans/60-candy.md](08-greedy-one-pass-scans/60-candy.md) |

> **Why these are Core:** #54 is Boyer-Moore voting, #55 tracks the farthest reachable index, #56 counts jumps
> level by level, and #57 resets the starting point when the tank goes negative.
> **Why the rest are Stretch:** #58 adds up every rise, #59 is a sort or count trick, and #60 is a two-pass
> greedy that is Hard and rarely asked.

---

## Topic 9 — String Manipulation & Parsing

**Pattern:** scan the string with an index, apply the rules exactly, and build the result in a list that you `join` at the end.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 61 | Longest Common Prefix | LC150 | 14 | Easy | Core | ☑ | [09-string-manipulation-and-parsing/61-longest-common-prefix.md](09-string-manipulation-and-parsing/61-longest-common-prefix.md) |
| 62 | Reverse Words in a String | LC150 | 151 | Medium | Core | ☑ | [09-string-manipulation-and-parsing/62-reverse-words-in-a-string.md](09-string-manipulation-and-parsing/62-reverse-words-in-a-string.md) |
| 63 | Roman to Integer | LC150 | 13 | Easy | Core | ☑ | [09-string-manipulation-and-parsing/63-roman-to-integer.md](09-string-manipulation-and-parsing/63-roman-to-integer.md) |
| 64 | Find the Index of the First Occurrence in a String | LC150 | 28 | Easy | Core | ☑ | [09-string-manipulation-and-parsing/64-find-the-index-of-the-first-occurrence-in-a-string.md](09-string-manipulation-and-parsing/64-find-the-index-of-the-first-occurrence-in-a-string.md) |
| 65 | Multiply Strings | NC150 | 43 | Medium | Core | ☑ | [09-string-manipulation-and-parsing/65-multiply-strings.md](09-string-manipulation-and-parsing/65-multiply-strings.md) |
| 66 | String to Integer (atoi) | **[+] Claude** | 8 | Medium | Core | ☑ | [09-string-manipulation-and-parsing/66-string-to-integer-atoi.md](09-string-manipulation-and-parsing/66-string-to-integer-atoi.md) |
| 67 | Length of Last Word | LC150 | 58 | Easy | Stretch | ☑ | [09-string-manipulation-and-parsing/67-length-of-last-word.md](09-string-manipulation-and-parsing/67-length-of-last-word.md) |
| 68 | Integer to Roman | LC150 | 12 | Medium | Stretch | ☑ | [09-string-manipulation-and-parsing/68-integer-to-roman.md](09-string-manipulation-and-parsing/68-integer-to-roman.md) |
| 69 | Zigzag Conversion | LC150 | 6 | Medium | Stretch | ☑ | [09-string-manipulation-and-parsing/69-zigzag-conversion.md](09-string-manipulation-and-parsing/69-zigzag-conversion.md) |
| 70 | Text Justification | LC150 | 68 | Hard | Stretch | ☑ | [09-string-manipulation-and-parsing/70-text-justification.md](09-string-manipulation-and-parsing/70-text-justification.md) |

> **Why #66:** it's the standard "handle every edge case" parsing question — leading spaces, a sign,
> non-digit characters and overflow — and tests careful step-by-step coding more than an algorithm.
> **Why the rest are Stretch:** #67–#69 are easy simulation with no new idea, and #70 is long to code and
> rarely asked.
> **Two Stretch problems that used to sit here** (String Compression, Compare Version Numbers) have been
> moved to the optional appendix at the end of this file — see there for why.

---

## Coverage check — is this enough for a Google arrays & strings interview?

**Yes, for the core technique set.** After these 9 topics you will have hands-on reps in: hash-based lookup,
counting and grouping; two pointers on sorted arrays, palindromes and partitions; fixed and variable sliding
windows (including the deque); prefix sums with a hash map, Kadane and prefix/suffix products; interval
merging, greedy and sweeping; in-place 2D matrix moves; read/write pointers and in-place rearrangement;
one-pass greedy scans; and careful string parsing.

**The 18 Stretch problems remaining in the main list** are the ones to drop first if time is tight — the 52
Core problems alone already cover every distinct technique. The 10 optional **[+] Claude** problems have
already been set aside in the appendix below; they're extra reps, not required.

**Deliberately out of scope, with reasons:**
- **Binary Search** (Search in Rotated Sorted Array, Search a 2D Matrix, Find Minimum in Rotated Sorted
  Array, …) — the **Binary-Search** repo.
- **Stack** (Valid Parentheses, Daily Temperatures, Largest Rectangle in Histogram, …) — the **Stack** repo,
  even though the input is an array or string.
- **Heap / priority queue** (Kth Largest Element, Task Scheduler, …) — the **Heap** repo.
- **Linked List** — the **Linked-List** repo. **Trees, Graphs, DP, Backtracking** — their own repos. The DP
  repo also holds Longest Palindromic Substring, Word Break and Maximum Product Subarray.
- **NC150 Greedy items that aren't array scans** — Hand of Straights, Merge Triplets, Partition Labels,
  Valid Parenthesis String — in the **Math-Bits-Greedy** repo (Topic 3), along with Maximum Sum Circular
  Subarray.
- **NC150 Math & Geometry items that aren't arrays or strings** — Pow(x, n), Detect Squares, Max Points on a
  Line — in the **Math-Bits-Greedy** repo (Topic 2).
- **Minimum Interval to Include Each Query (LC 1851)** — a very hard mix of intervals and a heap; not
  needed to cover the interval techniques above.

---

## Appendix — Optional [+] Claude Stretch Problems (not mandatory)

These 10 problems are not part of the numbered study path above. Every one of them is a second rep of a
technique a mandatory problem (Core or Stretch) already teaches you — that's exactly why they were cut from
the main list. Do them only if you finish everything above with time to spare. They keep numbers 71–80, so
the full set (main + appendix) is still numbered 1–80 and file paths stay consistent if you ever build them.

| # | Problem | Source | LC # | Difficulty | Extends | Status | File |
|---|---|---|---|---|---|---|---|
| 71 | Backspace String Compare | **[+] Claude** | 844 | Easy | Topic 2 — Two Pointers | ☐ | TBD |
| 72 | One Edit Distance | **[+] Claude** | 161 | Medium | Topic 2 — Two Pointers | ☐ | TBD |
| 73 | Find All Anagrams in a String | **[+] Claude** | 438 | Medium | Topic 3 — Sliding Window | ☐ | TBD |
| 74 | Max Consecutive Ones III | **[+] Claude** | 1004 | Medium | Topic 3 — Sliding Window | ☐ | TBD |
| 75 | Contiguous Array | **[+] Claude** | 525 | Medium | Topic 4 — Prefix Sum, Kadane & Running Products | ☐ | TBD |
| 76 | Diagonal Traverse | **[+] Claude** | 498 | Medium | Topic 6 — Matrix / 2D Array | ☐ | TBD |
| 77 | Move Zeroes | **[+] Claude** | 283 | Easy | Topic 7 — In-Place Array Manipulation | ☐ | TBD |
| 78 | First Missing Positive | **[+] Claude** | 41 | Hard | Topic 7 — In-Place Array Manipulation | ☐ | TBD |
| 79 | String Compression | **[+] Claude** | 443 | Medium | Topic 9 — String Manipulation & Parsing | ☐ | TBD |
| 80 | Compare Version Numbers | **[+] Claude** | 165 | Medium | Topic 9 — String Manipulation & Parsing | ☐ | TBD |

> **Why #71 and #72:** #71 scans both strings from the back with two pointers, so it needs `O(1)` space
> where a stack would need `O(n)`. #72 is two pointers on two strings that must handle the three "one edit"
> cases (replace, insert, delete). Both are common follow-up-style questions to Valid Palindrome / Is
> Subsequence (#14–#16), and neither adds a new technique. The general version of #72 (Edit Distance DP)
> lives in the DP repo.
> **Why #73:** it's Permutation in String (#25) returning every start index instead of just true/false.
> **Why #74:** it's Longest Repeating Character Replacement's (#24) variable window, where "invalid" means
> "more than `k` zeros inside".
> **Why #75:** treat every `0` as `-1`, and the question becomes "longest subarray with sum 0" — Subarray
> Sum Equals K's (#33) prefix sum + hash map, storing the *first index* of each prefix instead of a count.
> **Why #76:** no new idea — it's careful row/column index math (change direction at the edges), a common
> matrix warm-up that Rotate Image and Spiral Matrix (#43/#44) don't cover.
> **Why #77:** the same read/write pointer as Remove Element / Remove Duplicates (#48/#49), moving zeros to
> the end instead of removing a value.
> **Why #78:** it uses the array's own indices as a hash table. It's Hard, and clever more than commonly
> asked.
> **Why #79:** a read/write pointer on characters — Topic 7's idea applied to a string instead of a plain
> array.
> **Why #80:** split on `.` and compare the numbers segment by segment (a missing segment counts as `0`) —
> parsing with a few edge cases, and a quick add-on to atoi (#66).
