# Backtracking — Topic-by-Topic Roadmap

The full problem set, grouped into **6 topics** in study order. Do them top to bottom.
Within each topic, the **Source** column tells you exactly where each problem comes from.

> **Note on source-tag confidence:** unlike the DP tracker (where you supplied the curated list), this list was
> self-curated from memory since live verification of the exact NeetCode 150 / LeetCode Top 150 category
> contents failed (same truncation/blocking issue hit when building the DP repo). Treat LC150/NC150 tags here
> as best-effort, not independently confirmed.

---

## Source legend

| Badge | Meaning |
|---|---|
| **LC150** | On LeetCode's official *Top Interview 150* list (Backtracking category) |
| **NC150** | On the *NeetCode 150* list (Backtracking category) |
| **LC150 + NC150** | On **both** lists — highest-priority, most-asked |
| **[+] Claude** | Not on either list. Added to close a real gap in backtracking technique coverage. Reason given under the topic. |

**Totals:** 15 problems — 2 on both lists · 3 LC150-only · 7 NC150-only · 3 Claude additions.

**Status key:** ☐ not started · ◐ in progress · ☑ done & code runs.

**Priority key:** **Core** — teaches a distinct backtracking technique not covered by any other problem in the
list, even if a "simpler" sibling in the same topic is also Core. **Stretch** — a genuine second/harder rep of
a mechanic a Core problem already teaches, with no new logic of its own.

**Likelihood key (Google L3):** my own estimate of how likely each problem (or something that uses the same
technique) is to show up, not verified company-tagged data. **High** — a classic, frequently asked at this
level. **Medium** — asked sometimes, often as a follow-up to a High problem. **Low** — rarely asked at L3
(Hard, or a plain rep with no new idea).

> **Scope revision (added after first build):** #3 Combinations and #10 Word Break II were added as Stretch
> problems after the initial 13-problem list. Global numbers were shifted accordingly; no problem files existed
> yet, so nothing else was affected. Expression Add Operators (LC 282) was also added at that point, then
> removed by request as low priority — it is listed under "out of scope" below.

---

## Topic 1 — Subsets Family (Include/Exclude Backtracking)

**Pattern:** at each index, branch into two choices — take the current element, or skip it — recursing forward with a `start` index so earlier elements are never revisited.

| # | Problem | Source | LC # | Difficulty | Priority | Likelihood (L3) | Status | File |
|---|---|---|---|---|---|---|---|---|
| 1 | Subsets | NC150 | 78 | Medium | Core | High | ☑ | [01-subsets-family/01-subsets.md](01-subsets-family/01-subsets.md) |
| 2 | Subsets II | NC150 | 90 | Medium | Core | Medium | ☑ | [01-subsets-family/02-subsets-ii.md](01-subsets-family/02-subsets-ii.md) |
| 3 | Combinations | LC150 | 77 | Medium | Stretch | Medium | ☑ | [01-subsets-family/03-combinations.md](01-subsets-family/03-combinations.md) |

> **Why #2 is Core, not Stretch:** it introduces a genuinely distinct technique — sort first, then skip any
> element equal to the previous one *at the same recursion depth* (`if i > start and nums[i] == nums[i-1]:
> continue`) — to avoid duplicate subsets. That dedup trick doesn't appear anywhere else in this list.
>
> **Why #3 is Stretch:** it's the Subsets template with a fixed result length `k`. The only new idea is a small
> feasibility prune — stop looping once fewer than `k - len(path)` numbers remain. It's on LC150, so it stays in
> the tracker, but it's a quick rep, not a new technique.

---

## Topic 2 — Permutations Family

**Pattern:** build a full-length arrangement of all elements, tracking which have been used via a `used[]` array (or by swapping in place), rather than a `start` index — order matters here, unlike Topic 1.

| # | Problem | Source | LC # | Difficulty | Priority | Likelihood (L3) | Status | File |
|---|---|---|---|---|---|---|---|---|
| 4 | Permutations | NC150 | 46 | Medium | Core | High | ☑ | [02-permutations-family/04-permutations.md](02-permutations-family/04-permutations.md) |
| 5 | Permutations II | **[+] Claude** | 47 | Medium | Core | Medium | ☑ | [02-permutations-family/05-permutations-ii.md](02-permutations-family/05-permutations-ii.md) |

> **Why #5:** Topic 1 already teaches "sort + skip duplicates," but that trick relied on a `start` index.
> Permutations has no `start` index (every element is a candidate at every depth), so its dedup check is
> mechanically different: `if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue`. Skipping this
> problem would leave that specific — and commonly tested — variant completely uncovered.

---

## Topic 3 — Combination Sum Family (Target-Sum Backtracking)

**Pattern:** pick numbers (in some order) that sum to a target, backtracking when the running sum exceeds it. The key branch point: can you reuse the same number, or not?

| # | Problem | Source | LC # | Difficulty | Priority | Likelihood (L3) | Status | File |
|---|---|---|---|---|---|---|---|---|
| 6 | Combination Sum | **LC150 + NC150** | 39 | Medium | Core | High | ☑ | [03-combination-sum-family/06-combination-sum.md](03-combination-sum-family/06-combination-sum.md) |
| 7 | Combination Sum II | NC150 | 40 | Medium | Core | Medium | ☑ | [03-combination-sum-family/07-combination-sum-ii.md](03-combination-sum-family/07-combination-sum-ii.md) |

> **Why #7:** #6 allows unlimited reuse of the same number (recurse staying at index `i`). #7 forbids reuse
> (recurse at `i + 1`) *and* the input can contain duplicate values, so it also needs Topic 1's dedup trick on
> top of the no-reuse index bump. The reuse-vs-no-reuse index choice (`i` vs `i + 1`) is the exact backtracking
> analogue of unbounded vs. 0/1 knapsack in DP — a classic, easy-to-get-wrong detail with no other rep here.

---

## Topic 4 — String Partitioning Backtracking

**Pattern:** try every possible "next cut" of the remaining string, recurse on what's left, backtrack if it doesn't pan out.

| # | Problem | Source | LC # | Difficulty | Priority | Likelihood (L3) | Status | File |
|---|---|---|---|---|---|---|---|---|
| 8 | Palindrome Partitioning | NC150 | 131 | Medium | Core | Medium | ☑ | [04-string-partitioning/08-palindrome-partitioning.md](04-string-partitioning/08-palindrome-partitioning.md) |
| 9 | Restore IP Addresses | **[+] Claude** | 93 | Medium | Core | Medium | ☑ | [04-string-partitioning/09-restore-ip-addresses.md](04-string-partitioning/09-restore-ip-addresses.md) |
| 10 | Word Break II | **[+] Claude** | 140 | Hard | Stretch | Low | ☑ | [04-string-partitioning/10-word-break-ii.md](04-string-partitioning/10-word-break-ii.md) |

> **Why #9:** #8's only pruning check is "is this piece valid" (a palindrome). Restore IP Addresses adds a
> genuinely different pruning technique — arithmetic feasibility bounding: if the remaining string is too long
> or too short to possibly fit in the remaining required segments (`4 - segments_so_far`), abandon the branch
> immediately without even trying it. That bounding-before-exploring skill doesn't show up elsewhere here.
>
> **Why #10 is Stretch:** it's "try every next cut" exactly like #8, but the goal is to list every valid
> sentence, and the same suffix gets reached by many different paths. The one new idea is memoizing the answer
> for each `start` index so a repeated suffix is solved once — the only place in this repo where memoization
> rescues backtracking (see the README's complexity section). It also pairs with DP's Word Break (#06 there).

---

## Topic 5 — Grid/Board Backtracking

**Pattern:** two different flavors of "search a 2D space with backtracking" — exploring outward from a cell (marking/unmarking visited), vs. placing one item per row and checking constraints against everything placed so far.

| # | Problem | Source | LC # | Difficulty | Priority | Likelihood (L3) | Status | File |
|---|---|---|---|---|---|---|---|---|
| 11 | Word Search | NC150 | 79 | Medium | Core | High | ☑ | [05-grid-board-backtracking/11-word-search.md](05-grid-board-backtracking/11-word-search.md) |
| 12 | N-Queens | NC150 | 51 | Hard | Core | Medium | ☑ | [05-grid-board-backtracking/12-n-queens.md](05-grid-board-backtracking/12-n-queens.md) |
| 13 | N-Queens II | LC150 | 52 | Hard | Stretch | Low | ☑ | [05-grid-board-backtracking/13-n-queens-ii.md](05-grid-board-backtracking/13-n-queens-ii.md) |

> **Why #11 and #12 are both Core:** Word Search is "explore in 4 directions, mark/unmark as you go" — a
> different mechanic from N-Queens, which is "commit to one placement per row, check row/column/diagonal
> constraints against every prior placement." Neither teaches the other's technique.
> **Why #13 is Stretch:** it's the identical backtracking logic as #12, just returning a count instead of the
> actual board configurations. No new logic — skip unless you want the rep.

---

## Topic 6 — Build-a-String Backtracking

**Pattern:** construct a result string one choice at a time from a small fixed set of options per position, pruning branches that can't lead to a valid result.

| # | Problem | Source | LC # | Difficulty | Priority | Likelihood (L3) | Status | File |
|---|---|---|---|---|---|---|---|---|
| 14 | Letter Combinations of a Phone Number | **LC150 + NC150** | 17 | Medium | Core | High | ☑ | [06-build-a-string-backtracking/14-letter-combinations-of-a-phone-number.md](06-build-a-string-backtracking/14-letter-combinations-of-a-phone-number.md) |
| 15 | Generate Parentheses | LC150 | 22 | Medium | Core | High | ☑ | [06-build-a-string-backtracking/15-generate-parentheses.md](06-build-a-string-backtracking/15-generate-parentheses.md) |

> **Why #14 and #15 are both Core:** #14 branches over a fixed external mapping (digit → letters) with no
> validity constraint beyond length. #15 instead tracks two running counters (open/close count) as its pruning
> bound — a genuinely different constraint-tracking mechanic, not just a harder version of #14.

---

## Coverage check — is this enough for a Google backtracking interview?

**Yes, for the core technique set.** After these 6 topics you will have hands-on reps in: include/exclude
subsets (with and without duplicate handling, plus a fixed-length variant), permutation generation (with and
without duplicate handling), target-sum backtracking with and without reuse, string-partitioning with two
different pruning strategies (validity-check vs. arithmetic feasibility bounding) plus one memoized-enumeration
rep, grid exploration vs. row-by-row constrained placement, and string-building with two different branching
or state sources (external mapping vs. internal counters).

**The 3 Stretch problems** (#3, #10, #13) are the ones to drop first if time is tight — the 12 Core
problems alone already cover every distinct technique.

**Deliberately out of scope, with reasons:**
- **Sudoku Solver (LC 37)** — a real, classic backtracking problem, but Hard, long to fully implement live,
  and not a typical generalist Google ask (more of a take-home/competitive-programming staple).
- **Expression Add Operators (LC 282)** — Hard build-a-string problem that carries `running_value` and
  `last_operand` to get `*` precedence right. Removed from the list by request: it teaches no new backtracking
  template beyond #14/#15, and a Hard like this is unlikely for an entry-level interview. Add it back later if
  you want an extra rep.
- **Word Search II (LC 212)** — Trie + backtracking on a grid. A strong Hard, but its new idea is the Trie, not
  the backtracking; better placed in a Tries topic. Worth adding here later if you want it.
- **Tree-shaped backtracking** (root-to-leaf path backtracking, e.g. Path Sum II) — already covered in the
  **Trees** repo's path-state-DFS topic. Not duplicated here.
- **Bitmask-hybrid backtracking** (e.g. Partition to K Equal Sum Subsets) — narrow, competitive-programming
  leaning pattern, excluded for the same reason bitmask DP was excluded from the DP repo.
