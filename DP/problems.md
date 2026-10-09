# Problems — Topic-by-Topic Roadmap

The full problem set, grouped into **10 topics** in study order. Do them top to bottom.
Within each topic, the **Source** column tells you exactly where each problem comes from, and the
**Priority** column tells you whether it's a first pass (Core, 22 problems) or a deeper second pass
(Stretch, 7 problems) — see the Priority key below.

---

## Source legend

| Badge | Meaning |
|---|---|
| **LC150** | On LeetCode's official *Top Interview 150* list |
| **NC150** | On the *NeetCode 150* list |
| **LC150 + NC150** | On **both** lists — highest-priority, most-asked |

**Totals:** 29 problems — 8 on both lists · 6 LC150-only · 15 NC150-only. This is exactly your original
curated list (minus House Robber III, which stays in the sibling **Trees** repo since it's tree-shaped DP),
re-grouped by pattern instead of by day. No Claude additions — see the Coverage check at the bottom for the
real (minor) pattern gaps that were considered and deliberately left out.

**Status key:** ☐ not started · ◐ in progress · ☑ done & code runs.

**Priority key:** **Core** — at least one rep of every *technique* in the repo, not just every topic: this
includes a topic's sole problem even when it's Hard, and any problem whose transition logic doesn't appear
in any other Core problem (e.g. Regular Expression Matching's `*`-collapse branch, or Stock III's
transaction-count state dimension), even if a "simpler" sibling in the same topic is also Core. This alone is
enough to walk into an interview feeling ready. **Stretch** — a genuine second/harder rep of a mechanic a
Core problem *already* teaches, with no new transition logic of its own. Do these for depth and for a
permanent reference, not because they're required.

---

## Topic 1 — 1D DP: Linear Sequences

**Pattern:** the answer at position `i` depends on a small fixed window of earlier positions (`i-1`, `i-2`, ...). Fibonacci is the "hello world" of this whole repo.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 1 | Climbing Stairs | **LC150 + NC150** | 70 | Easy | Core | ☑ | [01-climbing-stairs.md](01-1d-dp-linear-sequences/01-climbing-stairs.md) |
| 2 | Min Cost Climbing Stairs | NC150 | 746 | Easy | Stretch | ☑ | [02-min-cost-climbing-stairs.md](01-1d-dp-linear-sequences/02-min-cost-climbing-stairs.md) |
| 3 | House Robber | **LC150 + NC150** | 198 | Medium | Core | ☑ | [03-house-robber.md](01-1d-dp-linear-sequences/03-house-robber.md) |
| 4 | House Robber II | NC150 | 213 | Medium | Core | ☑ | [04-house-robber-ii.md](01-1d-dp-linear-sequences/04-house-robber-ii.md) |

---

## Topic 2 — String Counting / Segmentation DP

**Pattern:** `dp[i]` = "in how many ways (or: can it at all) can the string up to index `i` be validly split/decoded." Transitions look back at the last 1–2 characters or check every valid dictionary word ending at `i`.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 5 | Decode Ways | NC150 | 91 | Medium | Core | ☑ | [05-decode-ways.md](02-string-counting-dp/05-decode-ways.md) |
| 6 | Word Break | **LC150 + NC150** | 139 | Medium | Core | ☑ | [06-word-break.md](02-string-counting-dp/06-word-break.md) |

---

## Topic 3 — Knapsack DP (0/1 and Unbounded)

**Pattern:** for each item, decide take-or-skip (0/1) or take-any-number-of-times (unbounded), building toward a target sum or capacity. The single most-reused shape in interview DP.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 7 | Coin Change | **LC150 + NC150** | 322 | Medium | Core | ☑ | [07-coin-change.md](03-knapsack-dp/07-coin-change.md) |
| 8 | Coin Change II | NC150 | 518 | Medium | Core | ☑ | [08-coin-change-ii.md](03-knapsack-dp/08-coin-change-ii.md) |
| 9 | Partition Equal Subset Sum | NC150 | 416 | Medium | Core | ☑ | [09-partition-equal-subset-sum.md](03-knapsack-dp/09-partition-equal-subset-sum.md) |
| 10 | Target Sum | NC150 | 494 | Medium | Core | ☑ | [10-target-sum.md](03-knapsack-dp/10-target-sum.md) |

---

## Topic 4 — Subarray / Subsequence Tracking DP

**Pattern:** walk the array once, carrying forward a running best (or a couple of running bests) that can flip sign or reset depending on the current element.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 11 | Maximum Product Subarray | NC150 | 152 | Medium | Core | ☑ | [11-maximum-product-subarray.md](04-subarray-subsequence-tracking/11-maximum-product-subarray.md) |
| 12 | Longest Increasing Subsequence | **LC150 + NC150** | 300 | Medium | Core | ☑ | [12-longest-increasing-subsequence.md](04-subarray-subsequence-tracking/12-longest-increasing-subsequence.md) |

---

## Topic 5 — Grid / Path DP

**Pattern:** `dp[r][c]` depends on `dp[r-1][c]` and `dp[r][c-1]` (or similar neighbors) — the 2D generalization of Topic 1's "look back a fixed window" idea.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 13 | Unique Paths | NC150 | 62 | Medium | Core | ☑ | [13-unique-paths.md](05-grid-path-dp/13-unique-paths.md) |
| 14 | Unique Paths II | LC150 | 63 | Medium | Stretch | ☑ | [14-unique-paths-ii.md](05-grid-path-dp/14-unique-paths-ii.md) |
| 15 | Minimum Path Sum | LC150 | 64 | Medium | Core | ☑ | [15-minimum-path-sum.md](05-grid-path-dp/15-minimum-path-sum.md) |
| 16 | Triangle | LC150 | 120 | Medium | Stretch | ☑ | [16-triangle.md](05-grid-path-dp/16-triangle.md) |
| 17 | Maximal Square | LC150 | 221 | Medium | Core | ☑ | [17-maximal-square.md](05-grid-path-dp/17-maximal-square.md) |

---

## Topic 6 — Memoized DFS on Grid

**Pattern:** the grid isn't a simple top-left-to-bottom-right sweep — the dependency order is irregular, so you DFS from each cell and cache the result instead of filling a table in a fixed order.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 18 | Longest Increasing Path in a Matrix | NC150 | 329 | Hard | Core | ☑ | [18-longest-increasing-path-in-a-matrix.md](06-memoized-dfs-on-grid/18-longest-increasing-path-in-a-matrix.md) |

---

## Topic 7 — Palindrome DP

**Pattern:** `dp[i][j]` = a fact about the substring spanning `i..j`, built from the inside out (shorter spans first).

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 19 | Longest Palindromic Substring | **LC150 + NC150** | 5 | Medium | Core | ☑ | [19-longest-palindromic-substring.md](07-palindrome-dp/19-longest-palindromic-substring.md) |
| 20 | Palindromic Substrings | NC150 | 647 | Medium | Stretch | ☑ | [20-palindromic-substrings.md](07-palindrome-dp/20-palindromic-substrings.md) |

---

## Topic 8 — Two-String DP

**Pattern:** `dp[i][j]` = a fact about "the first `i` characters of string A vs. the first `j` characters of string B." Almost every two-string interview question reduces to this table.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 21 | Longest Common Subsequence | NC150 | 1143 | Medium | Core | ☑ | [21-longest-common-subsequence.md](08-two-string-dp/21-longest-common-subsequence.md) |
| 22 | Edit Distance | **LC150 + NC150** | 72 | Medium | Core | ☑ | [22-edit-distance.md](08-two-string-dp/22-edit-distance.md) |
| 23 | Interleaving String | **LC150 + NC150** | 97 | Medium | Stretch | ☑ | [23-interleaving-string.md](08-two-string-dp/23-interleaving-string.md) |
| 24 | Distinct Subsequences | NC150 | 115 | Hard | Stretch | ☑ | [24-distinct-subsequences.md](08-two-string-dp/24-distinct-subsequences.md) |
| 25 | Regular Expression Matching | NC150 | 10 | Hard | Core | ☑ | [25-regular-expression-matching.md](08-two-string-dp/25-regular-expression-matching.md) |

---

## Topic 9 — State-Machine DP (Stock Trading)

**Pattern:** define a small set of "states" (holding a share vs. not, cooldown vs. not, transactions used so far) and a `dp` value per state per day. Transitions are just "what could I have done yesterday to be in this state today."

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 26 | Best Time to Buy and Sell Stock III | LC150 | 123 | Hard | Core | ☑ | [26-best-time-to-buy-and-sell-stock-iii.md](09-state-machine-dp-stocks/26-best-time-to-buy-and-sell-stock-iii.md) |
| 27 | Best Time to Buy and Sell Stock IV | LC150 | 188 | Hard | Stretch | ☑ | [27-best-time-to-buy-and-sell-stock-iv.md](09-state-machine-dp-stocks/27-best-time-to-buy-and-sell-stock-iv.md) |
| 28 | Best Time to Buy and Sell Stock with Cooldown | NC150 | 309 | Medium | Core | ☑ | [28-best-time-to-buy-and-sell-stock-with-cooldown.md](09-state-machine-dp-stocks/28-best-time-to-buy-and-sell-stock-with-cooldown.md) |

---

## Topic 10 — Interval / Partition DP

**Pattern:** `dp[i][j]` = the best answer for the range `i..j`, computed by trying every way to split the range into two (or by picking one element inside the range to resolve last). Ranges are filled in order of increasing length.

| # | Problem | Source | LC # | Difficulty | Priority | Status | File |
|---|---|---|---|---|---|---|---|
| 29 | Burst Balloons | NC150 | 312 | Hard | Core | ☑ | [29-burst-balloons.md](10-interval-partition-dp/29-burst-balloons.md) |

---

## Coverage check — is this enough for a Google DP interview?

**Yes.** After these 10 topics you will have hands-on reps in every core DP pattern Google draws from outside
of tree-shaped recursion (tree DP — Diameter, House Robber III, Max Path Sum — is already covered in the
sibling **Trees** repo, so it's intentionally not duplicated here):

- 1D linear DP (fixed-window lookback);
- counting/segmentation DP over strings;
- 0/1 and unbounded knapsack — the most-reused shape in the entire topic;
- running-best subarray/subsequence tracking, including sign-flip state (max product);
- 2D grid path DP, both in fixed sweep order and in memoized-DFS order for irregular dependencies;
- interval DP over contiguous spans (palindromic substrings), plus general interval/partition DP (Burst
  Balloons);
- two-string DP (LCS family, edit distance, wildcard/regex matching);
- state-machine DP (the stock-trading family, which generalizes to any "small state, one transition per
  step" problem).

**Deliberately out of scope, with reasons:**
- **Jump Game II** (min-steps reachability DP), **Word Break II** (boolean DP + backtracking to enumerate
  segmentations), and **Longest Palindromic Subsequence** (interval DP on subsequences, not just contiguous
  spans) — these were flagged as real, if minor, pattern gaps and briefly added, then removed by request to
  keep this list strictly to the originally-curated LC150/NC150 problems. Worth revisiting individually later
  if you want a rep of "min-steps DP," "DP + backtracking," or "subsequence interval DP" specifically — none
  of them are required for the core patterns above, which are each already covered by a different problem.
- **Best Time to Buy/Sell Stock I & II** — same state-machine pattern already taught by III/IV/Cooldown, just
  easier instances of it. No new pattern, so left out to avoid redundancy.
- **Perfect Squares** — same "minimize count, unbounded knapsack" shape as Coin Change. Redundant, not a gap.
- **Bitmask DP and Digit DP** — real, recognizable patterns, but they show up far more in competitive
  programming than in a generalist Google SWE loop. Left out of this core reference; worth a dedicated
  problem only if you specifically want exposure to one.
- **Tree-shaped DP** (Diameter of Binary Tree, House Robber III, Binary Tree Max Path Sum) — a different unit
  entirely, already fully covered in the **Trees** repo. Not duplicated here.
