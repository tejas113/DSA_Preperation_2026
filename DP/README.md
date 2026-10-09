# Dynamic Programming — Google Interview Study Repo

A small, readable set of notes for mastering **general (non-tree) Dynamic Programming** for a Google SWE
interview: 1D DP, 2D grid DP, knapsack, string DP, palindrome/interval DP, and state-machine DP.
Tree-shaped DP (Diameter, House Robber III, Max Path Sum) lives in the sibling **Trees** repo, not here.

Every file is built to be re-read in ~3 minutes and fully recalled — this is a reference you come back to,
not a one-time cram sheet.

---

## How to use this repo

1. Work through the topics in order, 1 → 10 (see [problems.md](problems.md)) — each topic in the repo root
   is its own folder, and the pattern it teaches tends to build on the one before it.
2. Each problem file is self-contained: it teaches its own idea from scratch, so you can also jump straight
   to any single file later as a refresher without re-reading the whole topic.
3. When you come back after weeks away, don't reread everything — open [problems.md](problems.md), scan the
   topic tables, and re-read just the file(s) covering whatever pattern you're rusty on.
4. There is no `concepts/` guide by default. If a topic ever needs a standalone concept primer, it gets added
   there explicitly and linked from that topic's problems.

Every problem file has the same six sections:

| Section | What you get |
|---|---|
| **1. Intuition** | A 2–3 line story, then bullets that tie each idea to a specific line or variable in the code, ending with a one-line **Recall** |
| **2. Template** | State / Choice / Recurrence / Base / Guard — the whole DP pattern in five lines |
| **3. Code** | The top-down **memoization** solution (primary), then `### Alternative: Tabulation`: a four-move conversion of that memo (cache → array, base cases → starting values, recursion direction → loop direction, calls → lookups) with a side-by-side table, plus the space-optimized version |
| **4. Dry Run** | One small example, one drawing: the memo call tree with cache hits marked, or the filled table |
| **5. Complexity** | **States** (what the memo is keyed by), **Time** (states × work per state), **Space** (memo + recursion depth, and what tabulation changes) |
| **6. Recall (30 seconds)** | Three bullets to re-read before an interview |

A few problems are not naturally a memoization (Maximum Product Subarray, and the two palindrome
expand-around-center problems). There the primary code is that approach, and the DP view sits under an
`### Alternative:` heading.

---

## House style

- **Explicit, state-meaningful names.** `dp`, `memo`, `curr_sum`, `prev`, `prev2`, `min_cost[i][j]` — never
  single letters except loop counters (`i`, `j`, `_`).
- **Type hints** on every function signature and return value.
- **Base cases first, always spelled out** — what does `dp[0]` or `memo[""]` mean, in plain English, before
  any code.
- **Memoization first, in every file:**
  - **Top-down (memoization)** — `memo = {}`, recursion that mirrors the problem statement directly. This is
    the primary solution, and it only computes the states you actually visit.
  - **Bottom-up (tabulation)** — presented as a *conversion* of that memo: same state, same recurrence, and a
    loop order chosen so that whatever the recursion asks for is already filled. Use it when recursion depth
    is a problem (Python's default limit is 1000) or when an interviewer asks for it.
  - **Space-optimized (rolling variables / one row)** — noted after the table, when `dp[i]` only reads the
    last row or the last one or two values.

---

## Pattern-recognition cheat sheet

Read the prompt, match a phrase, reach for the pattern.

| If the problem says... | Reach for | Core template |
|---|---|---|
| "number of ways to climb/reach", "min cost to reach the top" | **1D linear DP** — `dp[i]` from `dp[i-1]`, `dp[i-2]` | `dp[i] = dp[i-1] + dp[i-2]` (or min/cost variant) |
| "houses in a row/circle, can't pick adjacent" | **1D linear DP with a skip-or-take choice** | `dp[i] = max(dp[i-1], dp[i-2] + val[i])` |
| "decode/segment a string into valid pieces, count the ways" | **String segmentation DP** — `dp[i]` = ways to handle prefix of length `i` | `dp[i] += dp[i-k]` for each valid split of length `k` ending at `i` |
| "subset sums to target", "partition into two equal halves", "min coins", "ways to make change" | **0/1 or unbounded knapsack** — take-or-skip each item vs. take-any-number-of-times | `dp[amount] = min(dp[amount], dp[amount - coin] + 1)` |
| "max/min subarray product" (sign can flip) | **Running max AND min** carried together | `curr_max, curr_min = max(x, curr_max*x, curr_min*x), min(...)` |
| "longest increasing subsequence" (not contiguous) | **1D DP over "best ending at i"**, or patience-sorting for O(n log n) | `dp[i] = 1 + max(dp[j] for j < i if a[j] < a[i])` |
| "grid, count/min paths from top-left to bottom-right" | **2D grid DP** — `dp[r][c]` from `dp[r-1][c]` and `dp[r][c-1]` | `dp[r][c] = dp[r-1][c] + dp[r][c-1]` |
| "grid, path must be strictly increasing" (irregular dependency order) | **Memoized DFS on the grid** | `dfs(r, c) = 1 + max(dfs(nr, nc) for valid increasing neighbor)`, cached |
| "longest/count palindromic substring" (contiguous) | **Interval DP, expand from center OR `dp[i][j]` table** | `dp[i][j] = dp[i+1][j-1] and s[i] == s[j]` |
| "common subsequence/substring", "edit distance", "interleaving", "wildcard/regex match" | **Two-string 2D DP** — `dp[i][j]` = fact about `A[:i]` vs `B[:j]` | `dp[i][j] = dp[i-1][j-1] + 1` if `A[i]==B[j]` else combine neighbors |
| "buy/sell stock, at most k transactions, cooldown, transaction fee" | **State-machine DP** — a `dp` value per (day, state) | `dp[day][holding] = max(carry over, transition in from other state)` |
| "burst all balloons for max coins", "merge/split a range for min/max cost" | **Interval/partition DP** — try every last-element / split point in the range | `dp[i][j] = max(dp[i][k-1] + dp[k+1][j] + cost(i, k, j) for k in range)`, fill by increasing range length |

---

## Problem index

The full topic-by-topic problem list — with each problem's source (LC150 / NC150 / both / Claude addition),
LeetCode number, difficulty, status, and a link to its file — lives in **[problems.md](problems.md)**.

That file is the single tracker. Each topic gets its own folder in the repo root
(e.g. `01-1d-dp-linear-sequences/`), and the problem write-ups (`01`–`29`) live inside it.

---

## Complexity quick-reference

Every DP problem's cost is: **(number of distinct states) × (cost to compute one state's transition)**.

- **The state definition is the hard part — not the loop.** Once you know exactly what `dp[i]` or
  `dp[i][j]` *means* in plain English, the recurrence and the loop almost write themselves. Most of the
  thinking time in a DP interview question should go into pinning down the state, not the implementation.
- **Counting states tells you the complexity before you write a line of code.** 1D DP over an array of
  length `n` → `n` states. 2D DP over two strings of length `m` and `n` → `m × n` states. Interval DP over
  a sequence of length `n` → `n²` states (every `(i, j)` pair). Knapsack over `n` items and target sum `T`
  → `n × T` states.
- **Memoization (top-down) vs. tabulation (bottom-up):** same states, same complexity — the difference is
  direction. Memoization only computes states actually reached by the recursion (can be a real win when the
  full grid of states is never fully visited); tabulation computes every state in a hand-chosen safe order
  and avoids recursion-depth limits. Default to whichever one you can state the recurrence in most naturally,
  then switch if asked.
- **Space-optimized (rolling array):** if `dp[i]` only ever reads from `dp[i-1]` (and maybe `dp[i-2]`), or
  `dp[row]` only reads from `dp[row-1]`, you don't need the whole table — a couple of variables (`prev`,
  `prev2`) or a single 1D array (for 2D grid problems) is enough. This is a common "can you optimize the
  space?" follow-up once the table version works.
