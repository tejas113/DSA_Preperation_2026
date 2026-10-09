# Backtracking — Google Interview Study Repo

A small, readable set of notes for mastering **backtracking** for a Google SWE interview: subsets,
permutations, the combination-sum family, string partitioning, grid/board placement, and build-a-string
problems. Tree-shaped backtracking (root-to-leaf path problems) lives in the sibling **Trees** repo, not here.

Every file is built to be re-read in ~3 minutes and fully recalled — this is a reference you come back to,
not a one-time cram sheet.

---

## How to use this repo

1. Work through the topics in order, 1 → 6 (see [backtracking_problems.md](backtracking_problems.md)) — each topic
   in the repo root is its own folder, and later topics reuse ideas from earlier ones (for example, the
   "skip equal siblings" trick from Subsets II comes back in Permutations II and Combination Sum II).
2. Each problem file is self-contained: it teaches its own idea from scratch, so you can also jump straight
   to any single file later as a refresher without re-reading the whole topic.
3. When you come back after weeks away, don't reread everything — open
   [backtracking_problems.md](backtracking_problems.md), scan the topic tables, and re-read just the file(s)
   covering whatever pattern you're rusty on. The cheat sheet below tells you which pattern to reach for.
4. Do the **Core** problems first; **Stretch** problems are extra reps of an idea you already have.
5. There is no `concepts/` guide by default. If a topic ever needs a standalone concept primer, it gets added
   there explicitly and linked from that topic's problems.

Every problem file has the same header line (LC #, source, difficulty, priority, pattern) and the same six
sections, in the same order:

| Section | What you get |
|---|---|
| **1. Intuition** | A short story + bullets tied to specific lines of the code + a one-line **Recall** |
| **2. Template** | Choose / Explore / Un-choose in the code's own terms, plus the one prune / dedup check |
| **3. Code** | The solution (any alternative approach sits under it as a sub-heading) |
| **4. Dry Run** | One small example, drawn as a tree |
| **5. Complexity** | Time and space, each with a one-line "why" based on the code |
| **6. Recall (30 seconds)** | Three bullets to re-read before an interview |

---

## House style

- **Explicit, state-meaningful names.** `path`, `used`, `start`, `result`, `open_count`, `close_count`,
  `remaining`, `curr_sum` — never single letters except loop counters (`i`, `j`, `r`, `c`, `_`).
- **Type hints** on every function signature and return value.
- **Base cases first, always spelled out** — what does "a complete answer" look like (`len(path) == k`,
  `start == len(s)`, `open_count == close_count == n`), in plain English, before any code.
- **Every file names the core template and its pruning check.** The template is always:

  ```
  choose   → add the next option to `path` (and mark it used / update counters)
  explore  → recurse on what's left
  un-choose→ undo exactly what "choose" did, so the next sibling starts from a clean state
  ```

  Before any code, the file says in plain English which check keeps the search small — a sorted-array skip,
  a `used[]` check, a feasibility bound, a validity test, or a constraint set.
- **Save a copy, not the live list.** When a complete answer is found, append `path[:]` (or `"".join(path)`),
  never `path` itself — otherwise every saved answer ends up empty after un-choosing.
- **Every problem file is runnable.** It ends with an `if __name__ == "__main__":` block of `assert`s against
  the examples from the problem statement (compare results as sorted lists / sets when order isn't specified).

---

## Pattern-recognition cheat sheet

Read the prompt, match a phrase, reach for the pattern.

| If the problem says... | Reach for | Core template / key line |
|---|---|---|
| "return all subsets", "all combinations of size k" | **Include/exclude with a `start` index** — loop `i` from `start`, recurse at `i + 1` so earlier items are never revisited | `for i in range(start, n): path.append(nums[i]); backtrack(i + 1); path.pop()` |
| "arrange / reorder all the elements", "all permutations" | **Permutation backtracking with `used[]`** — every unused element is a candidate at every depth | `if used[i]: continue; used[i] = True; path.append(...); backtrack(); path.pop(); used[i] = False` |
| "input has duplicates, but no duplicate results" (subsets / combinations) | **Sort first, skip equal siblings at the same depth** | `if i > start and nums[i] == nums[i-1]: continue` |
| "input has duplicates, but no duplicate results" (permutations) | **Sort first, skip an equal element whose twin isn't in use** | `if i > 0 and nums[i] == nums[i-1] and not used[i-1]: continue` |
| "the same number may be used unlimited times" | **Recurse without advancing the index** | `backtrack(i, remaining - nums[i])` — `i`, not `i + 1` |
| "each number may be used at most once" | **Recurse advancing the index** | `backtrack(i + 1, remaining - nums[i])` |
| "sum to a target, all numbers positive" | **Prune when the running sum overshoots** (or `break` early on a sorted array) | `if remaining < 0: return`; sorted: `if nums[i] > remaining: break` |
| "all sub-lists of length exactly k" | **Fixed-length prune** — stop when too few elements are left to reach `k` | `for i in range(start, n - (k - len(path)) + 1)` |
| "split / cut a string into pieces where each piece is valid" | **String-partition backtracking** — try every next cut, keep only valid pieces | `for end in range(start + 1, n + 1): piece = s[start:end]; if valid(piece): ...` |
| "split into exactly N parts" (IP address) | **Feasibility bound before recursing** — remaining characters must fit the remaining parts | `if len(s) - start > 3 * parts_left or len(s) - start < parts_left: return` |
| "list *every* valid split / sentence" where the same suffix repeats | **Backtracking + memo on `start`** — solve each suffix once | `memo[start] = [piece + " " + rest for ...]` |
| "search for a word / path in a grid, no cell reused" | **Grid DFS with mark / unmark** | `board[r][c] = "#"; ...4 directions...; board[r][c] = original` |
| "place one item per row/position with conflict rules" (N-Queens) | **Placement backtracking with constraint sets** — one placement per row, check column and both diagonals | `cols`, `diag1` (`r - c`), `diag2` (`r + c`) sets; add on choose, remove on un-choose |
| "count the arrangements" (don't need the boards) | **Same placement search, return a count** | `total += backtrack(row + 1)` |
| "build a string from digit → letters (or similar fixed mapping)" | **Depth = input position, branch over the mapping** | `for ch in mapping[digits[pos]]: ...` |
| "generate all valid parentheses / balanced strings" | **Build with counters as the pruning bound** | `if open_count < n: add "("`; `if close_count < open_count: add ")"` |

Quick decision test when you're stuck:

- Does **order matter** in the answer? Yes → permutation style (`used[]`). No → subset style (`start` index).
- Can an element be **reused**? Yes → recurse at `i`. No → recurse at `i + 1`.
- Are there **duplicates in the input** but the output must be unique? → sort, then skip equal siblings.
- Is there an obvious **"this branch is already doomed"** test? Put it at the top of the function (or the top of the loop) so the branch dies immediately.

---

## Problem index

The full topic-by-topic problem list — with each problem's source (LC150 / NC150 / both / Claude addition),
LeetCode number, difficulty, priority (Core / Stretch), status, and a link to its file — lives in
**[backtracking_problems.md](backtracking_problems.md)**.

That file is the single tracker and the single source of truth; this README deliberately does not repeat the
checklist. Each topic gets its own folder in the repo root (e.g. `01-subsets-family/`), and the problem
write-ups (`01`–`15`, global numbering) live inside it. Every topic folder also has its own `README.md`
with the pattern that topic follows, how to recognize a problem that belongs to it, and what changes from
problem to problem — start there when you're not sure which topic a problem falls under.

---

## Complexity quick-reference

Backtracking cost is roughly **(branching factor) ^ (recursion depth)** *before pruning* — you're walking a
decision tree, and the total work is the number of nodes you actually visit times the work at each node.

- **Look at the tree first.** Subsets: every element is in or out → 2^n leaves. Permutations: n choices, then
  n-1, then n-2 … → n! leaves. Letter Combinations: up to 4 letters per digit → 4^n. Once you can draw the
  tree, you know the worst case before writing any code.
- **The output size is a hard floor.** If the answer really contains 2^n subsets (or n! permutations), no
  algorithm can beat that — so "exponential" here is not a flaw, it's the problem. Also remember each saved
  answer costs O(length) to copy, which is why subsets are O(n · 2^n) in full.
- **Pruning is what makes it tractable.** Without it, N-Queens tries n^n placements; with the "one queen per
  row + column and diagonal sets" check, whole subtrees are cut the moment a conflict appears. The same idea
  shows up as: the sorted-array skip (never re-explore an equal sibling), the `used[]` check (never reuse an
  element), the overshoot check (`remaining < 0`), the feasibility bound (too few / too many characters left),
  and the open/close-count rule. A good prune doesn't change the worst-case formula much, but it collapses the
  tree in practice — and interviewers usually care that you *name* the prune.
- **Space** is the recursion depth (the height of the tree) plus the current `path` — usually O(n) — not
  counting the output list itself.
- **Backtracking vs. DP:** DP answers "give me one optimal number" and wins by noticing many paths lead to the
  *same* state, so each state is solved once and cached. Backtracking here answers "give me *every* valid
  result" — the whole point is enumerating distinct paths, and two different paths are usually different
  answers, so there is nothing to reuse and **you generally can't memoize**. The exception is when different
  paths converge on an identical remaining subproblem (Word Break II reaches the same suffix by many routes) —
  there you can memoize that subproblem's answer. If a problem only asks for a **count** or a **min/max** and
  the state repeats, that's a signal to switch to DP.
