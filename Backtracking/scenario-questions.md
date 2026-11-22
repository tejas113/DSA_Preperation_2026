# Backtracking: Scenario Question Bank (Google L3 style)

Google doesn't say "use backtracking". It gives a short, vague scenario, "list every way to ...", "how many arrangements ...", "can this be spelled out ...", and **you** have to notice that the answer is a search through a tree of choices, work out what one level of that tree is, and decide how to prune it.
This file has one scenario per solved problem in this repo, plus two more variants of each, so you practise the *recognition* step and not just the solution.
Problem numbers match [backtracking_problems.md](backtracking_problems.md). All 15 tracked problems have write-ups.

**Disguised on purpose:** scenarios avoid words like "backtracking", "subset", "permutation", "combination", "recursion" and "N-Queens" when those words would give the technique away. Each one has an **Ask first** line (the clarifying questions a good candidate asks), a **Spot it** line (the clue that gives backtracking away), and a **Brute force** line (so you can say what the pruning improves).

**How to use:** read only the **Scenario** line, then say out loud: *am I asked to list everything, count, or just decide yes/no? what is one "level" of the choice tree? what is the choice at each level, and when is a branch already doomed?* Only then read the rest. About half of the variants deliberately cross over into a neighbouring technique (DP, BFS, math, a trie, iteration, a bitmask) so you learn where backtracking stops being the right tool.

---

## Part 1. The 5-step "Is this backtracking?" framework

1. **What is the question really asking for?**
   - **"List / return every ..."** (all subsets, all valid sentences, all boards): **backtracking**. The output itself is exponential, so enumeration is unavoidable.
   - **"How many ways ..."**, **"the minimum / maximum ..."**, **"is it possible ..."** *and the same sub-situation shows up again and again*: that is **DP**, not backtracking (see Part 2). Try backtracking only if the input is tiny, or the state is the whole path.
   - **"Is there any ..."** (does the word exist, is there a valid placement): backtracking with an **early return** on the first success.
   - A **tree or graph** structure with a root-to-leaf path: that is tree DFS (Trees repo).

2. **Draw one level of the decision tree.** Answer three things in plain English:
   - **What is a level?** An index in the input, a position in the answer, a row on the board, or a cut position in the string.
   - **What are the choices at that level?** Take/skip, "any unused element", "any amount to take", "the next piece length", "any letter this digit stands for", "any column in this row".
   - **When is the answer complete?** `len(path) == k`, `start == len(s)`, `open == close == n`, `row == n`, `remaining == 0`.

3. **Pick the template** (see the cheat sheet in Part 2):
   - **Order doesn't matter, pick a subset:** loop `i` from a `start` index and recurse at `i + 1`.
   - **Order matters, use every element:** a `used[]` array; every unused element is a candidate at every level.
   - **Reuse allowed:** recurse at `i`, not `i + 1`.
   - **Cut a string into valid pieces:** try every next cut.
   - **Search a grid:** mark, explore four neighbours, unmark.
   - **Place one thing per row with conflicts:** constraint sets for columns and diagonals.
   - **Build a string from a fixed mapping or counters:** depth is the position in the output.

4. **Name the prune and the dedup** *before* coding. This is what interviewers listen for.
   - **Overshoot:** `remaining < 0 → return` (or `break` on a sorted array).
   - **Feasibility bound:** not enough items left to reach length `k`; remaining characters can't fit the remaining parts.
   - **Validity test:** only recurse on a palindrome, a legal IP part, a dictionary word.
   - **Counters:** add `(` only if `open < n`, add `)` only if `close < open`.
   - **Duplicates in the input, unique output:** **sort**, then skip an equal sibling at the same depth (`i > start and nums[i] == nums[i - 1]`), or for permutations skip an equal element whose twin is not in use (`not used[i - 1]`).

5. **Cost: say it before you code.**
   - **Draw the tree.** Branching factor `b`, depth `d`: about `b^d` nodes before pruning. Subsets `2^n`, permutations `n!`, letter combinations `4^n`, valid parentheses the Catalan number `≈ 4^n / (n·√n)`.
   - **The output is a floor.** If the answer has `2^n` subsets, no algorithm beats `2^n`. Each saved answer also costs `O(length)` to copy, hence `O(n · 2^n)`.
   - **Space** is the recursion depth plus `path`, usually `O(n)`, not counting the output.
   - **Memoise only when different paths reach the same remaining sub-problem** (Word Break II's repeated suffix), and then it is really DP.

**The template, always:**
```
choose    -> add the next option to `path` (and mark it used / update counters)
explore   -> recurse on what is left
un-choose -> undo exactly what "choose" did, so the next sibling starts from a clean state
```
Save a **copy** of `path` (`path[:]`) when you find an answer, never `path` itself.

**Say-it-out-loud template:** *"This asks for every [arrangement / selection / split / placement], so I'll search a decision tree. A level is [index / row / cut]. At each level I choose [options]. I stop when [base case]. I prune with [overshoot / bound / validity / counters], and I dedup by [sort + skip equal siblings]. The tree has about [`b^d`] nodes, so the time is [formula] and the space is `O(depth)`."*

**Questions to ask the interviewer (cheap and impressive):**
- **Goal:** Do you want all the answers, just one, or only a count? (a count or a best-value question usually means DP or math)
- **Size:** How large can `n` get? (decides whether exponential is acceptable, `n ≤ 15` to `20` usually means brute force with pruning)
- **Duplicates:** Can the input contain duplicates? Must the output have no duplicate answers?
- **Reuse:** Can an element be used more than once? Can the same cell be visited twice?
- **Order:** Does the order of the answers, or of the items inside an answer, matter? Does `[1, 2]` differ from `[2, 1]`?
- **Edge cases:** Empty input? `k` larger than `n`? Target `0`? Does the empty selection count?
- **Constraints:** Are all numbers positive (so I can prune on overshoot and `break` on a sorted array)?
- **Output limit:** Must results be in a particular order? Can I return a generator or iterator instead of building the whole list?
- **Mutation:** May I modify the input (sort it, mark the board in place)?

---

## Part 2. Signal → technique cheat sheet

Problem numbers match [backtracking_problems.md](backtracking_problems.md). **gap** means the repo has no write-up for it yet (see Part 6). Techniques owned by other repos are named so you still recognise them.

| What the question says | It is really | Technique | Problems |
|---|---|---|---|
| "list every possible selection of these items", "every subset" | take / skip each element | **`start` index loop, recurse at `i + 1`** | 1 |
| "the input has repeats, but don't list the same selection twice" | duplicates at the same level | **sort + skip equal siblings** (`i > start and nums[i] == nums[i-1]`) | 2 |
| "choose exactly `k` of `n`", "every group of size `k`" | subsets with a fixed length | **`start` loop + length check + feasibility bound** | 3 |
| "every possible ordering / arrangement / schedule of all the items" | order matters, all used | **`used[]` array, every unused element at every level** | 4 |
| "every distinct ordering, with repeats in the input" | permutations with duplicates | **sort + skip an equal twin that isn't in use** (`not used[i-1]`) | 5 |
| "make a target with unlimited copies of each value, list every mix" | combinations with reuse | **recurse at `i` (same index) + overshoot prune** | 6 |
| "make a target, each item once, repeats in the input, no repeated answers" | no reuse + duplicates | **recurse at `i + 1` + skip equal siblings + overshoot prune** | 7 |
| "cut a string into pieces where each piece is valid, list every way" | string partition | **try every next cut, keep only valid pieces** | 8 |
| "insert separators to make exactly `N` valid parts" | partition with a part count | **feasibility bound before recursing** | 9 |
| "insert spaces to make sentences from a dictionary, list all" | partition where suffixes repeat | **backtracking + memo on `start`** | 10 |
| "can the word be traced through adjacent cells, no cell twice" | path search in a grid | **mark / explore 4 neighbours / unmark** | 11 |
| "place `n` items on a board, none attacking another, list the layouts" | one placement per row with conflicts | **constraint sets (columns, two diagonals)** | 12 |
| "how many valid layouts" (no need to list them) | the same search, returning a count | **same placement search, `+= 1` at the base** (bitmask for speed) | 13 |
| "every string a key sequence could stand for" | depth = input position, fixed mapping | **loop over the mapping at each position** | 14 |
| "every well-formed arrangement of `n` pairs" | build a string with counters | **`open < n`, `close < open`** | 15 |
| "how many ways", "minimum cost", "is it possible" and sub-situations repeat | overlapping subproblems | **DP** (not backtracking) | DP repo |
| "all root-to-leaf paths that ...", "path sum" | tree DFS | **DFS with a path list** | Trees repo |
| "shortest transformation / fewest moves" | a graph with equal costs | **BFS** | Graphs repo |
| "find every word from a dictionary in a grid" | many words, shared prefixes | **trie + grid backtracking** | gap |
| "fill a partial board so that all rules hold (Sudoku)" | placement with row/column/box sets | **placement backtracking, pick the most constrained cell** | gap |
| "split into `k` groups with equal sums" | assign items to buckets | **backtracking over buckets with pruning** | gap |
| "next permutation / k-th permutation" | no enumeration needed | **in-place algorithm / factorial number system** | Arrays-Strings (#51) |

**Red flags that you're being tested on backtracking:** "all", "every", "list", "generate", "enumerate", "all possible", "all valid", "find any", "can you spell", "place without attacking", "split into valid parts", "each element at most once", and any brute force that is "try everything and check".

### Backtracking or DP?

They are the **same recursion** with a different goal.

| | Backtracking | DP |
|---|---|---|
| Asks for | **every** valid result (a list) | **one number or yes/no** (count, min, max, possible) |
| Why it works | the whole path is part of the answer; different paths are different answers, so nothing is reusable | many paths reach the **same state**, so each state is solved once and cached |
| Cost | exponential, matching the output size | polynomial in the number of states |
| Switch when | the question says "list" or the path matters (N-Queens: where every earlier queen is) | the question says "how many" / "min" / "is it possible" and the state is small |

- **"Count the subsets / paths / ways"** → DP (or a closed form). Do *not* enumerate and take `len()`.
- **The exception:** Word Break II must list sentences, but the same suffix is reached by many routes, so you may **memoise the answer for each `start`** (backtracking + memo). That is DP's idea inside a backtracking shell.
- **Rule of thumb:** If the interviewer says "return the number of ..." and `n` is large, say "this is DP, backtracking would be exponential".

### Backtracking or BFS?

- **A shortest path or fewest moves with equal costs:** BFS (Graphs repo). Backtracking would explore every path.
- **Does a path exist, or list all paths:** backtracking (DFS). Grid path with "no cell reused" (Word Search) is backtracking because the visited set belongs to the *current path*, not to the whole search.

### Include/exclude or loop-over-choices?

Two ways to write the same subset-style search:
- **Loop over choices** (`for i in range(start, n)`): save the answer at every node (subsets) or at a fixed length (combinations). Recurse at `i + 1`.
- **Binary include/exclude** (`dfs(i)`: take `nums[i]` or skip it): save at the leaf `i == n`. For duplicates, when you *exclude* a value you must also skip every later copy of it.
- Both give the same answers. **Permutations, string partitions, grids and N-Queens have no binary version**, because every element is always used and the choice is "which one", not "in or out".

### Sort, `used[]`, or `start`?

- **`start` index** when order **doesn't** matter (selections): earlier elements are never revisited.
- **`used[]`** when order **does** matter (arrangements): every unused element is a candidate at every depth.
- **Sorting** is needed only when you must **skip duplicates**; it puts equal values next to each other.

---

## Part 3. Complexity patterns

Every backtracking cost is **(number of nodes in the search tree you actually visit) × (work per node)**. Draw the tree first.

| Pattern | Tree shape | Time | Extra space | Notes |
|---|---|---|---|---|
| Subsets (take / skip) | `2^n` leaves | `O(n · 2^n)` | `O(n)` | `2^n` answers, each copied at up to `n` |
| Subsets with duplicates (sorted, skip equal siblings) | at most `2^n` | `O(n · 2^n)` (+ `O(n log n)` sort) | `O(n)` | fewer subsets when values repeat |
| Combinations of size `k` | `C(n, k)` leaves | `O(k · C(n, k))` | `O(k)` | the feasibility bound avoids dead ends; the binary version is `O(2^n)` |
| Permutations with `num in path` | `n!` leaves | `O(n² · n!)` | `O(n)` | the `in path` scan is `O(n)` |
| Permutations with `used[]` | `n!` leaves | `O(n · n!)` | `O(n)` | an `O(1)` check; each result copied at `n` |
| Permutations with duplicates | at most `n!` | `O(n · n!)` (+ sort) | `O(n)` | fewer results with repeats |
| Combination Sum (reuse) | depth `T / M` (target over the smallest candidate), up to `N` children | `O(N^(T/M))` loose bound | `O(T / M)` | passing `remaining` instead of `sum(path)` removes an extra factor |
| Combination Sum II (no reuse) | `2^N` | `O(N · 2^N)` | `O(N)` | sorting adds `O(N log N)` |
| Palindrome Partitioning | up to `2^(n-1)` cuts | `O(n · 2^n)` | `O(n)` | a palindrome test per piece costs up to `n`; DP precomputation makes it `O(1)` |
| Restore IP Addresses | depth 4, ≤ 3 children | `O(1)` (≤ 81 paths) | `O(1)` | the length is capped at 12 |
| Word Break II (no memo) | up to `2^(n-1)` sentences | `O(n · 2^n)` | `O(n + W)` | dead-end branches are re-explored; memo on `start` fixes that |
| Word Search | `M·N` starts, then ≤ 3 branches per step, depth `L` | `O(M · N · 3^L)` | `O(L)` | the 4th neighbour is where you came from |
| N-Queens (list boards) | about `n!`, cut by diagonals | `O(n!)` (+ `O(n²)` per solution to copy) | `O(n²)` board + `O(n)` sets | |
| N-Queens II (count) | the same | `O(n!)` | `O(n)` | no board copy; bitmask is about the same count of nodes but with a much smaller constant |
| Letter Combinations | `≤ 4^n` leaves | `O(n · 4^n)` | `O(n)` | the digits `7` and `9` have 4 letters; each string costs `n` to build |
| Generate Parentheses | Catalan(n) leaves | `O(4^n / √n)` | `O(n)` | only valid prefixes are ever built |

**How to work out complexity (say it in this order):**
1. **Draw the first two levels.** How many children does a node have? Does that number shrink as you go deeper?
2. **Estimate the number of leaves:** `2^n` (take/skip), `n!` (arrangements), `C(n, k)` (fixed-size selections), `b^d` (general), Catalan (balanced parentheses).
3. **Add the work per node.** Copying an answer costs its length. A palindrome test costs the piece length. A `sum(path)` costs the path length.
4. **Space** = recursion depth + `path` (+ `used[]` or the sets). The output isn't counted.
5. **Say what the pruning does.** It rarely changes the worst-case formula but removes most nodes in practice.

**Rules of thumb**
- **The output size is a hard floor.** `2^n` subsets or `n!` permutations can't be beaten, so "exponential" is the problem, not a flaw.
- **Pass state instead of recomputing it.** Carry `remaining` (not `sum(path)`), counters (not `path.count("(")`), and a `used[]` (not `num in path`).
- **Strings are immutable in Python:** passing `string + char` creates a new string per call (fine for short strings, and it makes "un-choose" automatic). Use a list and `join` for long outputs.
- **Memoise only when the remaining sub-problem repeats**, and then think DP.
- **Recursion depth** is `n`, `2n` or `L`. That is fine for these problems, but say it for long inputs.

---

## Part 4. The scenarios

Each entry has: **Original question** (the formal LeetCode statement), then **Scenario** (what you'd actually hear), **Ask first**, **Spot it** (the clue that reveals the technique), **Brute force** (the naive answer and its cost), **Solve** (the answer from your write-up), **Cost** (time and space, with the reasoning), **Follow-up** (what they'd push on), and **two more variants (A and B)** on the same pattern. Each variant gives the formal **Question** first, then the disguised **Scenario**, then **Pattern and cost**. Variants marked **(crossover)** leave the entry's technique on purpose, to show you where it stops working. A variant with no LC number is a classic interview question that has no single canonical LeetCode entry.

---

### Topic 1. Subsets Family (Include / Exclude)

---

### 1. Subsets (#1)

**Original question:** LC 78. Given an integer array `nums` of **unique** elements, return all possible subsets (the power set). The solution set must not contain duplicate subsets. Return the solution in any order.

**Scenario:** A pizza shop has `n` different toppings. List every possible set of toppings a customer could order, including a plain pizza with none.

**Ask first:**
1. Does the empty selection count? Does the order of toppings inside a selection matter (is "ham + olives" the same as "olives + ham")?
2. How large can `n` get, and do you need them in a particular order?

**Spot it:** "**Every** possible selection." Each topping is either in or out, so there are `2^n` answers. The answer is a *list of everything*, so I enumerate, and I only move **forward** through the toppings so that "ham + olives" is never produced a second time as "olives + ham".

**Brute force:** There is no cheaper way to *list* `2^n` selections. The naive version tries every ordering of every selection and removes repeats (exponentially worse). The `start` index is the improvement.

**Solve:** ([01-subsets.md](01-subsets-family/01-subsets.md))
```python
def subsets(nums: list[int]) -> list[list[int]]:
    res, n = [], len(nums)

    def backtrack(start: int, path: list[int]) -> None:
        res.append(path.copy())              # every node of the tree is a valid subset
        for i in range(start, n):
            path.append(nums[i])             # choose
            backtrack(i + 1, path)           # explore: only move forward
            path.pop()                       # un-choose

    backtrack(0, [])
    return res

def subsetsBinary(nums: list[int]) -> list[list[int]]:      # include / exclude version
    res, n = [], len(nums)

    def dfs(i: int, path: list[int]) -> None:
        if i == n:
            res.append(path.copy())          # saved only at the leaves
            return
        path.append(nums[i])                 # include nums[i]
        dfs(i + 1, path)
        path.pop()
        dfs(i + 1, path)                     # exclude nums[i]

    dfs(0, [])
    return res
```

**Cost:** `2^n` subsets are saved and each `path.copy()` costs up to `n`: `O(n · 2^n)` time. Recursion depth and `path` are at most `n`: `O(n)` space (the output isn't counted).
**Follow-up:** *Duplicates in the input?* #2. *Only subsets of size `k`?* #3. *Only count them?* `2^n`, no search needed. *Avoid recursion?* Iterative: start with `[[]]` and, for each number, add a copy of every existing subset with that number appended. *Why `path.copy()`?* Otherwise every saved answer ends up empty after un-choosing.

**More scenarios on the same pattern**

**Variant A (a binary choice per position)**
- **Question:** LC 784 Letter Case Permutation. Given a string `s`, you can transform every letter individually to be lowercase or uppercase. Return a list of all possible strings.
- **Scenario:** A password tool wants every spelling of a code in which each letter may be written in upper or lower case (digits stay as they are).
- **Pattern and cost:** At each position there is a binary decision (flip the case or not), but only for letters. The include/exclude shape: at a letter, branch twice; at a digit, branch once. `O(n · 2^L)` for `L` letters, `O(n)` space.

**Variant B (crossover: bitmask, no recursion)**
- **Question:** Generate all subsets of a set of `n` distinct numbers **without recursion**. (A classic follow-up to LC 78.)
- **Scenario:** The toppings list is short (`n ≤ 20`) and the shop wants a plain loop with no function calling itself.
- **Pattern and cost:** Every number from `0` to `2^n - 1` is a subset: bit `j` set means "include `nums[j]`". `O(n · 2^n)` time, `O(1)` extra space beyond the output. The bitmask is also the base of bitmask DP when `n ≤ 20` and you need *counts* or *best values* instead of the lists.

---

### 2. Subsets II (#2)

**Original question:** LC 90. Given an integer array `nums` that **may contain duplicates**, return all possible subsets. The solution set must not contain duplicate subsets. Return the solution in any order.

**Scenario:** The same pizza shop now lists some toppings twice (two identical "extra cheese" items on the stock sheet). List every distinct set of toppings, and never list the same set twice.

**Ask first:**
1. Are two equal values interchangeable (so "cheese + olives" using the first or the second cheese is the same answer)?
2. May I sort the input?

**Spot it:** Duplicates in the input would produce duplicate answers. The fix: **sort**, then at any one level skip an element that equals the one just tried.

**Brute force:** Generate all `2^n` subsets as in #1 and remove repeats with a set of tuples: correct, but it builds every duplicate first. Pruning at the source avoids that.

**Solve:** ([02-subsets-ii.md](01-subsets-family/02-subsets-ii.md))
```python
def subsetsWithDup(nums: list[int]) -> list[list[int]]:
    res = []
    nums.sort()                                 # equal values become neighbours
    n = len(nums)

    def backtrack(start: int, path: list[int]) -> None:
        res.append(path.copy())
        for i in range(start, n):
            if i > start and nums[i] == nums[i - 1]:
                continue                        # same value already tried at THIS level
            path.append(nums[i])
            backtrack(i + 1, path)
            path.pop()

    backtrack(0, [])
    return res
```

**Cost:** At most `2^n` subsets (fewer with repeats), each copied at up to `n`, plus `O(n log n)` for the sort: `O(n · 2^n)` time, `O(n)` space.
**Follow-up:** *Why `i > start` and not `i > 0`?* Skipping when `i > 0` would also stop you from using a repeated value *deeper* in the same branch (`[1, 2, 2]` needs both 2s in `[1, 2, 2]`). The rule only blocks a repeat **at the same level**. *Binary version?* After excluding a value, jump past all its later copies. *Why sort?* So equal values are adjacent.

**More scenarios on the same pattern**

**Variant A (crossover: can't sort, so dedup with a set per level)**
- **Question:** LC 491 Non-decreasing Subsequences. Given an integer array, return all different possible non-decreasing subsequences of at least two elements. You may not reorder the input.
- **Scenario:** A sensor's readings must be picked in time order, each at least as large as the last, and the same sequence of values must not be reported twice.
- **Pattern and cost:** The order of the input matters, so **sorting would destroy the problem**. Instead, at each level keep a small `seen` set of values already tried and skip repeats. `O(n · 2^n)` time, `O(n)` space. The dedup *idea* is the same; the *mechanism* changes.

**Variant B (crossover: choose a count per distinct value)**
- **Question:** Generate all distinct subsets of a multiset by treating the input as a map `value → count`. (An alternative to LC 90.)
- **Scenario:** The stock sheet is given as "cheese ×2, olives ×1, ham ×3", and the shop wants every distinct selection.
- **Pattern and cost:** One level per **distinct value**; at each level choose how many copies to take (`0..count`). No duplicate check is needed because each value is decided once. `O(n · 2^n)` worst case, `O(d)` depth for `d` distinct values. Often the cleanest way to explain the dedup.

---

### 3. Combinations (#3)

**Original question:** LC 77. Given two integers `n` and `k`, return all possible combinations of `k` numbers chosen from the range `[1, n]`. You may return the answer in any order.

**Scenario:** A company has `n` numbered departments and must form a committee of exactly `k` of them. List every possible committee.

**Ask first:**
1. Is a committee `{2, 5}` the same as `{5, 2}` (does order matter)? (It doesn't.)
2. What are the ranges of `n` and `k`? Can `k > n`?

**Spot it:** Same as #1 (selections, move forward only) with a **fixed length**: stop as soon as the path has `k` items.

**Brute force:** Generate every subset (`2^n`) and keep those of size `k`: wasteful when `k` is small. Stopping at length `k` avoids growing longer paths.

**Solve:** ([03-combinations.md](01-subsets-family/03-combinations.md))
```python
def combine(n: int, k: int) -> list[list[int]]:
    res = []

    def bt_dfs(start: int, path: list[int]) -> None:
        if len(path) == k:                       # complete: save and stop
            res.append(path.copy())
            return
        for i in range(start, n + 1):
            path.append(i)
            bt_dfs(i + 1, path)
            path.pop()

    bt_dfs(1, [])
    return res
```

**Cost:** There are `C(n, k)` combinations, each copied at cost `k`: `O(k · C(n, k))` time. Recursion depth and `path` are at most `k`: `O(k)` space. The binary include/exclude version without the length prune is `O(2^n)`.
**Follow-up:** *Faster pruning?* Loop `i` only up to `n - (k - len(path)) + 1`, since fewer than `k - len(path)` numbers remaining can never fill the path (the optional feasibility bound in your write-up). *Only count them?* `C(n, k)` by formula or Pascal's triangle. *Lazily, one at a time?* Variant B.

**More scenarios on the same pattern**

**Variant A (a target as well as a size)**
- **Question:** LC 216 Combination Sum III. Find all valid combinations of `k` numbers that sum to `n`, using only the digits `1` to `9`, each digit used at most once.
- **Scenario:** A safe has a `k`-digit code with no repeated digits, and the digits must add up to a given total. List every code the owner could have set (digits in increasing order).
- **Pattern and cost:** #3 plus a running remainder: stop when the path has `k` digits (valid only if the remainder is `0`), and prune when the remainder goes negative. `O(k · C(9, k))` time, `O(k)` space.

**Variant B (crossover: counting, and generating lazily)**
- **Question:** LC 1286 Iterator for Combination. Design `CombinationIterator(characters, combinationLength)` with `next()` returning the next combination in lexicographic order and `hasNext()`.
- **Scenario:** A test tool needs the committees one at a time, on demand, without building all of them in memory first.
- **Pattern and cost:** Instead of precomputing all `C(n, k)` results, keep the current combination as a bitmask or index array and advance to the next one with a small update. `O(k)` per `next()`, `O(k)` space. Counting only: `C(n, k)` with Pascal's triangle (DP), no search.

---

### Topic 2. Permutations Family

---

### 4. Permutations (#4)

**Original question:** LC 46. Given an array `nums` of **distinct** integers, return all the possible permutations. You can return the answer in any order.

**Scenario:** A tour operator has `n` landmarks and wants every possible order in which a group could visit all of them, each exactly once.

**Ask first:**
1. Must every landmark appear in each tour exactly once? Are all landmarks distinct?
2. How large can `n` get? (the number of tours is `n!`)

**Spot it:** "Every **order**." Unlike selections, `[A, B]` and `[B, A]` are different answers, so *every unused element is a candidate at every level*, and I track which ones are already used.

**Brute force:** There's no way around producing `n!` answers. A naive version generates `n^n` sequences (repeating landmarks) and filters; the `used` check prunes those branches at once.

**Solve:** ([04-permutations.md](02-permutations-family/04-permutations.md))
```python
def permute(nums: list[int]) -> list[list[int]]:
    result, n = [], len(nums)

    def bt_dfs(path: list[int]) -> None:
        if len(path) == n:                       # every element placed
            result.append(path.copy())
            return
        for num in nums:
            if num in path:                      # already used in this branch (O(n) scan)
                continue
            path.append(num)
            bt_dfs(path)
            path.pop()

    bt_dfs([])
    return result

def permuteUsed(nums: list[int]) -> list[list[int]]:     # the O(1)-check version
    result, n = [], len(nums)
    used = [False] * n

    def bt_dfs(path: list[int]) -> None:
        if len(path) == n:
            result.append(path.copy())
            return
        for i in range(n):
            if used[i]:
                continue
            used[i] = True
            path.append(nums[i])
            bt_dfs(path)
            path.pop()
            used[i] = False

    bt_dfs([])
    return result
```

**Cost:** `n!` permutations. With `num in path` each call scans up to `n`: `O(n² · n!)`. With a `used[]` array the check is `O(1)`, giving `O(n · n!)` (the copy at each leaf costs `n`). Space `O(n)`. There is no binary include/exclude version: every element is always used, the choice is *where*, not *whether*.
**Follow-up:** *Duplicates?* #5. *Only the next permutation, or the `k`-th?* Variant A, Variant B (no enumeration needed). *Without extra `used` memory?* Swap elements in place (`swap(start, i)`). *Only a count?* `n!`.

**More scenarios on the same pattern**

**Variant A (crossover: step to the next one, don't generate all)**
- **Question:** LC 31 Next Permutation. Rearrange `nums` into the lexicographically next greater permutation, in place with `O(1)` extra memory.
- **Scenario:** A digit lock steps through all arrangements in dictionary order. Given the current one, produce the next.
- **Pattern and cost:** No search. Find the last ascent (the pivot), swap it with the smallest larger value to its right, and reverse the tail. `O(n)` time, `O(1)` space. Enumerating `n!` to find one successor would be absurd (Arrays-Strings repo, #51).

**Variant B (crossover to math)**
- **Question:** LC 60 Permutation Sequence. The set `[1, 2, ..., n]` has `n!` permutations in order. Return the `k`-th permutation.
- **Scenario:** A game wants the 1000th arrangement of `n` tokens without listing the earlier 999.
- **Pattern and cost:** Use the **factorial number system**: the first digit is index `(k-1) // (n-1)!` of the remaining digits, and so on. `O(n²)` time with list removals, `O(n)` space. Backtracking would be `O(k · n)` at best and explodes for large `k`.

---

### 5. Permutations II (#5)

**Original question:** LC 47. Given a collection of numbers `nums` that might contain **duplicates**, return all possible **unique** permutations in any order.

**Scenario:** The tour operator's landmark list now has repeats (two identical "viewpoint" stops). List every distinct visiting order, never the same order twice.

**Ask first:**
1. Are equal stops interchangeable (so swapping the two viewpoints gives the *same* tour)?
2. May I sort the input?

**Spot it:** #4 plus duplicates. Without handling them, swapping two equal elements would produce the same permutation again. Sort, then use a **twin rule**: among equal values, always take them left to right.

**Brute force:** Generate all `n!` permutations and de-duplicate with a set of tuples: correct, but it generates every repeat first (up to `n!` instead of `n! / (c1! · c2! · ...)`).

**Solve:** ([05-permutations-ii.md](02-permutations-family/05-permutations-ii.md))
```python
def permuteUnique(nums: list[int]) -> list[list[int]]:
    res, n = [], len(nums)
    nums.sort()                                  # equal values become neighbours
    visited = [False] * n

    def bt_dfs(path: list[int]) -> None:
        if len(path) == n:
            res.append(path.copy())
            return
        for i in range(n):
            if visited[i]:
                continue
            if i > 0 and nums[i] == nums[i - 1] and not visited[i - 1]:
                continue                         # an equal twin sits unused to my left: take it first
            visited[i] = True
            path.append(nums[i])
            bt_dfs(path)
            path.pop()
            visited[i] = False

    bt_dfs([])
    return res
```

**Cost:** At most `n!` permutations (fewer with repeats); each call loops `n` positions with `O(1)` checks, and each result is copied at cost `n`, plus `O(n log n)` to sort: `O(n · n!)` time, `O(n)` space.
**Follow-up:** *Why `not visited[i - 1]`?* If the left twin is **not** in use, then taking the right twin first would mean the left twin is placed later: the same arrangement as taking the left first. The rule forces a fixed order among equal values. *Different from #2?* There is no `start` index, so the check uses `visited` instead of `i > start`. *Use a counter map?* Branch on distinct values with remaining counts (no sort needed).

**More scenarios on the same pattern**

**Variant A (crossover: build half, mirror it)**
- **Question:** LC 267 Palindrome Permutation II (premium). Given a string `s`, return all the palindromic permutations (without duplicates) of it, or an empty list if none exist.
- **Scenario:** From a bag of letter tiles, list every distinct word that reads the same in both directions and uses every tile.
- **Pattern and cost:** First check feasibility with letter counts (at most one odd count). Then permute **half** of the letters (with the #5 dedup) and mirror each half around the odd letter. `O((n/2)!)` time instead of `n!`, `O(n)` space. A hash-map check *before* searching is the pruning.

**Variant B (crossover: permutations plus a constraint)**
- **Question:** LC 996 Number of Squareful Arrays. An array is squareful if the sum of every pair of adjacent elements is a perfect square. Given an integer array, return the number of permutations of it that are squareful (two permutations differ if some index differs).
- **Scenario:** A playlist planner wants to count the orderings in which every neighbouring pair of track lengths adds up to a perfect square.
- **Pattern and cost:** #5's dedup (sort, twin rule) plus a **validity prune**: only place a number next to the previous one if their sum is a perfect square. Count at the leaves. Exponential worst case, but heavy pruning; `O(n)` space. A bitmask DP (`dp[mask][last]`) can count in `O(2^n · n²)` instead.

---

### Topic 3. Combination Sum Family

---

### 6. Combination Sum (#6)

**Original question:** LC 39. Given an array of **distinct** integers `candidates` and a target integer `target`, return a list of all **unique combinations** of `candidates` where the chosen numbers sum to `target`. The **same number may be chosen from `candidates` an unlimited number of times**. Two combinations are unique if the frequency of at least one of the chosen numbers is different.

**Scenario:** A cashier must give exactly `target` cents in change using coins of a few given values, with an unlimited supply of each. List every different mix of coins that works (two mixes are the same if they use the same number of each coin).

**Ask first:**
1. Are all coin values positive and distinct? (This is what makes pruning on overshoot safe.)
2. Do you want the mixes themselves, or just how many there are, or the fewest coins?

**Spot it:** "Make a total, **list** every mix, unlimited reuse." Choose a coin, subtract it, and **stay on the same coin** (so it can be reused) or move on. Order doesn't matter, so only move forward.

**Brute force:** Try every sequence of coins and remove repeated mixes: huge and wasteful. The `start` index (never go back) removes re-orderings.

**Solve:** ([06-combination-sum.md](03-combination-sum-family/06-combination-sum.md))
```python
def combinationSum(candidates: list[int], target: int) -> list[list[int]]:
    res = []

    def bt_dfs(start: int, path: list[int]) -> None:
        if sum(path) == target:
            res.append(path.copy())
            return
        if sum(path) > target:                   # overshoot: this branch is doomed
            return
        for i in range(start, len(candidates)):
            path.append(candidates[i])
            bt_dfs(i, path)                      # i, not i + 1: the same coin may be reused
            path.pop()

    bt_dfs(0, [])
    return res

def combinationSumBinary(candidates: list[int], target: int) -> list[list[int]]:
    res, n = [], len(candidates)

    def dfs(i: int, remaining: int, path: list[int]) -> None:
        if remaining == 0:
            res.append(path.copy())
            return
        if i == n or remaining < 0:
            return
        path.append(candidates[i])               # take it, and stay at i (reuse allowed)
        dfs(i, remaining - candidates[i], path)
        path.pop()
        dfs(i + 1, remaining, path)              # skip it for good

    dfs(0, target, [])
    return res
```

**Cost:** The path is at most `T / M` deep (target over the smallest value) with up to `N` children per node: a loose `O(N^(T/M))`. Each `sum(path)` call adds up to `T / M`. Space `O(T / M)`. The binary version carries `remaining` instead of calling `sum(path)`.
**Follow-up:** *Faster prune?* Sort the candidates and `break` as soon as `candidates[i] > remaining`. *Count the mixes only?* DP (Variant A). *Fewest coins?* DP (Variant B). *No reuse?* #7.

**More scenarios on the same pattern**

**Variant A (crossover to DP, a count)**
- **Question:** LC 377 Combination Sum IV. Given distinct positive integers `nums` and a `target`, return the **number** of possible combinations (different sequences count as different) that add up to `target`.
- **Scenario:** How many different ordered payment plans, each step a coin of one of the given values, add up to the target?
- **Pattern and cost:** Only a *count* is asked, and the same remaining amount recurs from many paths, so backtracking is exponential for no reason. DP: `dp[t] = sum(dp[t - x] for x in nums)`. `O(T · N)` time, `O(T)` space (DP repo).

**Variant B (crossover to DP, a best value)**
- **Question:** LC 322 Coin Change. Given coin denominations and an amount, return the **fewest** number of coins needed to make that amount, or `-1`.
- **Scenario:** The cashier wants the smallest number of coins that gives the exact change.
- **Pattern and cost:** "Fewest" is an optimisation, and the state (remaining amount) repeats. Backtracking is exponential; DP is `O(amount · coins)` time, `O(amount)` space. Use backtracking only when asked to *list* the mixes.

---

### 7. Combination Sum II (#7)

**Original question:** LC 40. Given a collection of candidate numbers `candidates` (which may contain **duplicates**) and a target number `target`, find all **unique combinations** in `candidates` where the candidate numbers sum to `target`. Each number in `candidates` may only be used **once** in the combination. The solution set must not contain duplicate combinations.

**Scenario:** A shopper holds a pile of discount vouchers, some with the same value. Each voucher can be used only once. List every distinct set of vouchers that adds up to exactly the bill's discount target.

**Ask first:**
1. Can the same voucher be used twice? (No: each is used once.) Are two vouchers of the same value interchangeable?
2. May I sort the vouchers?

**Spot it:** #6 with **no reuse** (recurse at `i + 1`) and **duplicate values** (the sort-and-skip-equal-siblings trick from #2).

**Brute force:** Try all `2^N` subsets and keep those that hit the target, removing repeats with a set: wasteful. Pruning on overshoot and skipping equal siblings cuts most of it.

**Solve:** ([07-combination-sum-ii.md](03-combination-sum-family/07-combination-sum-ii.md))
```python
def combinationSum2(candidates: list[int], target: int) -> list[list[int]]:
    res = []
    candidates.sort()

    def bt_dfs(start: int, path: list[int]) -> None:
        if sum(path) == target:
            res.append(path.copy())
            return
        if sum(path) > target:
            return
        for i in range(start, len(candidates)):
            if i > start and candidates[i] == candidates[i - 1]:
                continue                         # skip an equal sibling at this level
            path.append(candidates[i])
            bt_dfs(i + 1, path)                  # i + 1: each voucher used at most once
            path.pop()

    bt_dfs(0, [])
    return res
```

**Cost:** About `2^N` calls (fewer with repeats), each running `sum(path)` at up to `N`, plus `O(N log N)` for the sort: `O(N · 2^N)` time, `O(N)` space. A running `remaining` (instead of `sum(path)`) and a `break` on a sorted array are the usual speed-ups.
**Follow-up:** *Why is the dedup `i > start`?* Same reason as #2: it blocks repeats only at the same level, allowing `[1, 1, 6]` for target 8. *Unlimited reuse?* #6. *Binary version?* Take moves to `i + 1`; skip jumps past all copies of the value.

**More scenarios on the same pattern**

**Variant A (crossover: assign items to buckets)**
- **Question:** LC 698 Partition to K Equal Sum Subsets. Given an integer array `nums` and an integer `k`, return `true` if it is possible to divide the array into `k` non-empty subsets whose sums are all equal.
- **Scenario:** A team must split a list of job durations among `k` workers so that every worker has exactly the same total time. Is it possible?
- **Pattern and cost:** Backtracking over *which bucket* gets each item (or fill one bucket at a time up to `total / k`). Prune: sort descending, skip an item that doesn't fit, skip equal-state buckets, return early on success. Exponential in general; a bitmask DP version is `O(2^n · n)`. A yes/no question with an early return.

**Variant B (crossover to DP, yes/no with two groups)**
- **Question:** LC 416 Partition Equal Subset Sum. Given a non-empty array of positive integers, determine if it can be partitioned into two subsets with equal sums.
- **Scenario:** Can a pile of items be split into two piles of exactly equal weight?
- **Pattern and cost:** It reduces to "is there a subset summing to `total / 2`". The state `(index, remaining)` repeats, so DP (0/1 knapsack, `O(n · T)` time) beats backtracking's `O(2^n)` (DP repo). Backtracking is the tool only for *listing* the subsets.

---

### Topic 4. String Partitioning

---

### 8. Palindrome Partitioning (#8)

**Original question:** LC 131. Given a string `s`, partition `s` such that every substring of the partition is a palindrome. Return all possible palindrome partitioning of `s`.

**Scenario:** A label printer must cut a code string into pieces so that every piece reads the same forwards and backwards. List every possible way to cut it.

**Ask first:**
1. Is a single character a valid piece? (Yes, every single character is a palindrome.)
2. How long can the string get? (the number of cuts is up to `2^(n-1)`)

**Spot it:** "Cut into valid pieces, list all ways." At each position, try every **next cut**, recurse on what's left, and keep only pieces that pass the validity test.

**Brute force:** Try all `2^(n-1)` cut patterns and test every piece afterwards. Checking each piece *as soon as it is formed* prunes the whole subtree below an invalid piece.

**Solve:** ([08-palindrome-partitioning.md](04-string-partitioning/08-palindrome-partitioning.md))
```python
def partition(s: str) -> list[list[str]]:
    res, n = [], len(s)

    def bt_dfs(start: int, path: list[str]) -> None:
        if start == n:                           # the whole string is cut up
            res.append(path.copy())
            return
        for end in range(start + 1, n + 1):
            string = s[start:end]
            if string == string[::-1]:           # only recurse on a valid piece
                path.append(string)
                bt_dfs(end, path)
                path.pop()

    bt_dfs(0, [])
    return res
```

**Cost:** Up to `2^(n-1)` partitions (worst case `"aaaa"`); each palindrome test `string[::-1]` costs up to `n`: `O(n · 2^n)` time. Space `O(n)` (depth and `path`). A precomputed palindrome table (DP) makes each test `O(1)`.
**Follow-up:** *Speed up the test?* A table `is_pal[i][j]` built with DP in `O(n²)`. *Only the minimum number of cuts?* Variant A (DP). *No binary version?* Every character belongs to some piece; the choice is *where the next cut lands*. *Why `path.copy()`?* So later un-choosing doesn't empty saved answers.

**More scenarios on the same pattern**

**Variant A (crossover to DP, a minimum)**
- **Question:** LC 132 Palindrome Partitioning II. Return the **minimum** number of cuts needed to partition `s` into palindromes.
- **Scenario:** The label printer wants the fewest cuts, not a list of all ways.
- **Pattern and cost:** Optimisation over overlapping suffixes: DP over the palindrome table, `cuts[i] = min(cuts[j] + 1)` for `s[j+1..i]` palindrome. `O(n²)` time and space. Enumerating all partitions and taking the best would be exponential.

**Variant B (crossover: a yes/no with a fixed number of pieces)**
- **Question:** LC 1745 Palindrome Partitioning IV. Return `true` if it is possible to split `s` into **three** non-empty palindromic substrings.
- **Scenario:** Can the code be split into exactly three mirror-symmetric pieces?
- **Pattern and cost:** Only two cut positions, so no deep search: precompute the palindrome table (`O(n²)`) and test every pair of cuts (`O(n²)`). `O(n²)` time and space. Backtracking is unnecessary because the depth is fixed at 3.

---

### 9. Restore IP Addresses (#9)

**Original question:** LC 93. A valid IP address consists of exactly four integers (each between `0` and `255`, with no leading zeros) separated by single dots. Given a string `s` containing only digits, return all possible valid IP addresses that can be formed by inserting dots into `s`. You are not allowed to reorder or remove any digits.

**Scenario:** A log has lost its dots: `25525511135`. List every way to put three dots back so the result is four valid numbers.

**Ask first:**
1. Are leading zeros allowed in a part (like `01`)? What range is a valid part?
2. Must I use all digits, and keep their order?

**Spot it:** Same as #8, but the number of pieces is **fixed at 4** and each piece has **1 to 3 digits**, so the tree is tiny, and a **feasibility bound** (the remaining digits must fit the remaining parts) kills hopeless branches immediately.

**Brute force:** Try every way to place three dots (`C(n-1, 3)`) and validate: fine for `n ≤ 12`, but the recursion with early checks is cleaner and prunes sooner.

**Solve:** ([09-restore-ip-addresses.md](04-string-partitioning/09-restore-ip-addresses.md))
```python
def restoreIpAddresses(s: str) -> list[str]:
    res, n = [], len(s)
    if n < 4 or n > 12:                          # cannot fit 4 parts of 1 to 3 digits
        return []

    def bt_dfs(start: int, path: list[str]) -> None:
        if len(path) == 4:
            if start == n:                       # valid only if every digit is used
                res.append(".".join(path))
            return
        for length in range(1, 4):               # a part has 1, 2 or 3 digits
            if start + length > n:
                break
            part = s[start : start + length]
            if len(part) > 1 and part[0] == "0": # no leading zeros
                continue
            if int(part) > 255:
                continue
            path.append(part)
            bt_dfs(start + length, path)
            path.pop()

    bt_dfs(0, [])
    return res
```

**Cost:** Depth is fixed at 4 and each level tries at most 3 lengths, so at most `3^4 = 81` paths, and the string is capped at 12: `O(1)` time and space.
**Follow-up:** *Stronger prune?* If `n - start > 3 · (4 - len(path))` or `n - start < 4 - len(path)`, return at once. *IPv6?* Eight groups of up to four hex digits, more rules, same shape. *Just validate an address?* Variant A (parsing, no search).

**More scenarios on the same pattern**

**Variant A (crossover: parsing, not search)**
- **Question:** LC 468 Validate IP Address. Given a string, return whether it is a valid IPv4 address, a valid IPv6 address, or neither.
- **Scenario:** A form field must be classified as IPv4, IPv6, or invalid.
- **Pattern and cost:** No search at all, just split and check each part with the rules (range, leading zeros, hex digits, group count). `O(n)` time, `O(1)` space. The skill is the rule list, not a technique.

**Variant B (backtracking on cuts, with an arithmetic constraint)**
- **Question:** LC 306 Additive Number. A string is additive if its digits can form an additive sequence (at least three numbers, each number after the first two is the sum of the two before it, no leading zeros). Return whether the string is additive.
- **Scenario:** A ticket number might be split into pieces where each piece after the first two is the sum of the previous two. Can it be done?
- **Pattern and cost:** Choose the first two pieces (the lengths of the first and second number) by trying all cuts; after that everything is forced, so check the rest iteratively. `O(n³)` time (`O(n²)` pairs of cuts × `O(n)` verification), `O(n)` space. A yes/no, so return on the first success.

---

### 10. Word Break II (#10)

**Original question:** LC 140. Given a string `s` and a dictionary of strings `wordDict`, add spaces in `s` to construct a sentence where each word is a valid dictionary word. Return all such possible sentences in any order. The same word in the dictionary may be reused multiple times in the segmentation.

**Scenario:** A text has lost its spaces: `catsanddog`. Given a word list, list every sentence you could rebuild by inserting spaces so each word is in the list.

**Ask first:**
1. Can a dictionary word be reused? Is there at least one valid sentence, or might the answer be empty?
2. How long can the string be, and how big is the dictionary?

**Spot it:** Same "try every next cut" as #8, but the **validity test is a dictionary lookup**, and the *same suffix* is reached by many different sets of earlier cuts, so you can **cache the answer for each start position**.

**Brute force:** The plain backtracking below: re-explores dead-end suffixes many times. Memoising by `start` fixes that.

**Solve:** ([10-word-break-ii.md](04-string-partitioning/10-word-break-ii.md))
```python
def wordBreak(s: str, wordDict: list[str]) -> list[str]:
    res, word_set, n = [], set(wordDict), len(s)

    def bt_dfs(start: int, path: list[str]) -> None:
        if start == n:
            res.append(" ".join(path))
            return
        for end in range(start + 1, n + 1):
            word = s[start:end]
            if word in word_set:                 # only cut where a dictionary word ends
                path.append(word)
                bt_dfs(end, path)
                path.pop()

    bt_dfs(0, [])
    return res

def wordBreakMemo(s: str, wordDict: list[str]) -> list[str]:    # the follow-up: solve each suffix once
    word_set, n, memo = set(wordDict), len(s), {}

    def sentences(start: int) -> list[str]:
        if start == n:
            return [""]
        if start in memo:
            return memo[start]
        out = []
        for end in range(start + 1, n + 1):
            word = s[start:end]
            if word in word_set:
                for rest in sentences(end):
                    out.append(word + (" " + rest if rest else ""))
        memo[start] = out
        return out

    return sentences(0)
```

**Cost:** The worst case (`"aaaa"` with words `a, aa, aaa, aaaa`) has `2^(n-1)` sentences, and each `" ".join` costs up to `n`: `O(n · 2^n)` time, `O(n + W)` space (depth plus the word set of total size `W`). Without a memo, dead-end branches are re-explored; with a memo, each suffix is solved once, but the output size still dominates.
**Follow-up:** *Just whether it can be done?* Variant A (DP). *Prune dead ends first?* Run the yes/no DP from #139 first and only recurse where a break exists. *Faster lookups?* Cap the word length, or use a trie. *Why memoise a backtracking problem?* The remaining suffix is an identical sub-problem however you got there (the README's exception).

**More scenarios on the same pattern**

**Variant A (crossover to DP, a yes/no)**
- **Question:** LC 139 Word Break. Given a string `s` and a dictionary, return `true` if `s` can be segmented into a space-separated sequence of dictionary words.
- **Scenario:** Can the spaceless text be rebuilt into dictionary words at all?
- **Pattern and cost:** Only a yes/no, so no need to list sentences: `dp[i]` = can `s[:i]` be broken. `O(n²)` time (with a set), `O(n)` space (DP repo, #06). Backtracking would be exponential for no gain.

**Variant B (crossover: words made of other words)**
- **Question:** LC 472 Concatenated Words. Given an array of unique strings `words`, return all the concatenated words in the list: those that are entirely made of at least two shorter words from the list.
- **Scenario:** From a vocabulary, which entries can be built by joining two or more other entries?
- **Pattern and cost:** For each word, run the Word Break DP (or memoised DFS) against the set of the other words. `O(total length × word length)` with the DP. A hard problem: know that it's "Word Break, once per word".

---

### Topic 5. Grid / Board Backtracking

---

### 11. Word Search (#11)

**Original question:** LC 79. Given an `m x n` grid of characters `board` and a string `word`, return `true` if `word` exists in the grid. The word can be constructed from letters of sequentially adjacent cells (horizontally or vertically neighbouring). The same letter cell may not be used more than once.

**Scenario:** A puzzle app shows a grid of letters. A player claims they can spell a given word by stepping from cell to neighbouring cell (up, down, left, right) without ever stepping on the same cell twice. Is the claim true?

**Ask first:**
1. Are diagonal moves allowed? (Not here.) Can a cell be reused? (No.)
2. May I modify the board temporarily (mark cells in place)?

**Spot it:** "Does a path spelling this word exist?" A path through a grid where *the visited set belongs to the current path*: mark a cell on the way in, **unmark** it on the way out so other paths can use it. And it's a yes/no, so return the moment one path works.

**Brute force:** Generate every path of length `L` from every cell and compare: `O(M · N · 4^L)`. Checking each step against the next letter and refusing to revisit a cell prunes most of it.

**Solve:** ([11-word-search.md](05-grid-board-backtracking/11-word-search.md))
```python
def exist(board: list[list[str]], word: str) -> bool:
    rows, cols = len(board), len(board[0])
    visited = set()

    def dfs(r: int, c: int, i: int) -> bool:
        if i == len(word):                       # every letter matched
            return True
        if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[i] or (r, c) in visited:
            return False
        visited.add((r, c))                      # choose: step onto the cell
        found = (dfs(r + 1, c, i + 1) or dfs(r - 1, c, i + 1)
                 or dfs(r, c + 1, i + 1) or dfs(r, c - 1, i + 1))
        visited.remove((r, c))                   # un-choose: free the cell for other paths
        return found

    for r in range(rows):
        for c in range(cols):
            if dfs(r, c, 0):
                return True
    return False
```

**Cost:** `M · N` start cells; each search goes at most `L` letters deep with at most 3 directions after the first step: `O(M · N · 3^L)` time. `O(L)` space (depth plus the visited cells; the in-place `'#'` marking version drops the set).
**Follow-up:** *Faster pruning?* Check that the board has enough of each letter; if the word's last letter is rarer than its first, search for the reversed word. *Many words at once?* Variant A (trie). *In-place marking?* Replace the cell with `'#'` and restore it. *Why unmark?* Another path may need that cell.

**More scenarios on the same pattern**

**Variant A (crossover to a trie)**
- **Question:** LC 212 Word Search II. Given an `m x n` board of characters and a list of strings `words`, return all words on the board.
- **Scenario:** The app now has a whole dictionary and must list every word that can be traced on the grid.
- **Pattern and cost:** Running #11 once per word is `O(W · M · N · 3^L)`. Build a **trie** of the words and walk the grid and the trie together, pruning a path as soon as no word starts with the current prefix. Roughly `O(M · N · 3^L)` total regardless of `W`, `O(total word length)` space for the trie (a hard problem; Trees repo has tries).

**Variant B (count the paths that visit everything)**
- **Question:** LC 980 Unique Paths III. On a grid with a start cell, an end cell, empty cells and obstacles, return the number of paths from start to end that walk over **every** non-obstacle cell exactly once.
- **Scenario:** A robot vacuum must clean every free cell exactly once, starting at the dock and ending at a given cell. How many different routes are there?
- **Pattern and cost:** The same mark/unmark walk, but **counting** and with the rule "all free cells visited at the end". `O(4^(M·N))` worst case, `O(M·N)` space. Because the count of free cells is tracked, a bitmask DP (`dp[mask][cell]`) is the alternative for small grids.

---

### 12. N-Queens (#12)

**Original question:** LC 51. The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other. Given an integer `n`, return all distinct solutions to the n-queens puzzle. Each solution contains a distinct board configuration of the placement, where `'Q'` and `'.'` both indicate a queen and an empty space.

**Scenario:** A museum has an `n × n` floor and wants to place `n` guards so that no two see each other along a row, a column, or a diagonal. List every possible layout.

**Ask first:**
1. Do I return the boards, or only how many there are (that's #13)?
2. Do rotations and reflections of one layout count as different layouts? (Here: yes.)

**Spot it:** "Place one item per row, with conflict rules against everything placed so far." Put one guard in each row, trying every column, and keep **three sets** (taken columns, and the two diagonal directions) so a conflict is detected in `O(1)`.

**Brute force:** Place guards anywhere and check all pairs at the end: `C(n², n)` placements. One guard per row cuts it to `n^n`; the conflict sets cut it to roughly `n!` or fewer.

**Solve:** ([12-n-queens.md](05-grid-board-backtracking/12-n-queens.md))
```python
def solveNQueens(n: int) -> list[list[str]]:
    col, pos_diag, neg_diag = set(), set(), set()    # columns, r + c, r - c
    res = []
    board = [["."] * n for _ in range(n)]

    def backtrack(r: int) -> None:
        if r == n:                                   # a queen in every row
            res.append(["".join(row) for row in board])
            return
        for c in range(n):
            if c in col or (r + c) in pos_diag or (r - c) in neg_diag:
                continue                             # this square is attacked
            col.add(c); pos_diag.add(r + c); neg_diag.add(r - c)
            board[r][c] = "Q"                        # choose
            backtrack(r + 1)                         # explore the next row
            col.remove(c); pos_diag.remove(r + c); neg_diag.remove(r - c)
            board[r][c] = "."                        # un-choose

    backtrack(0)
    return res
```

**Cost:** Row 0 has `n` choices, row 1 at most `n - 1`, and the diagonals cut deeper: about `O(n!)` nodes. Each solution costs `O(n²)` to copy. Space `O(n²)` for the board plus `O(n)` for the sets and the recursion.
**Follow-up:** *Why `r + c` and `r - c`?* Squares on one `/` diagonal share `r + c`; on one `\` diagonal they share `r - c`. *Just count them?* #13. *Fill a Sudoku board?* Variant A. *No search needed?* Variant B.

**More scenarios on the same pattern**

**Variant A (crossover: a partly filled board)**
- **Question:** LC 37 Sudoku Solver. Write a program to solve a Sudoku puzzle by filling the empty cells, so that each row, column and `3 × 3` box contains the digits `1-9` exactly once.
- **Scenario:** The puzzle app's "solve it for me" button.
- **Pattern and cost:** The same constraint-set idea (a set per row, column and box), but you choose the **next empty cell** and try digits `1-9`. Pick the **most constrained** cell first (fewest legal digits) to prune hard. Exponential worst case, solved instantly in practice. Validity checking is the Arrays-Strings repo's #42.

**Variant B (crossover to math: no constraint, no search)**
- **Question:** Count the ways to place `n` rooks on an `n × n` board so that no two attack each other. (Classic; compare with LC 51.)
- **Scenario:** The museum now only worries about guards seeing along rows and columns, not diagonals.
- **Pattern and cost:** One rook per row and per column means choosing a permutation of the columns: exactly `n!` placements, found with no search. Spotting that dropping the diagonal rule turns the problem into a closed form is the lesson. Listing them is a permutation (#4).

---

### 13. N-Queens II (#13)

**Original question:** LC 52. The n-queens puzzle is the problem of placing `n` queens on an `n x n` chessboard such that no two queens attack each other. Given an integer `n`, return the **number** of distinct solutions to the n-queens puzzle.

**Scenario:** The museum doesn't need the layouts any more: how many valid guard layouts exist for an `n × n` floor?

**Ask first:**
1. Is only the count needed (so I need not store any board)?
2. How large can `n` get? (the search is about `n!`)

**Spot it:** The same search as #12, with a **counter at the leaf** instead of a board copy. No board is needed, only the three conflict sets, so the space drops.

**Brute force:** Run #12 and take `len(result)`: correct, but it builds and copies every board (`O(n²)` per solution).

**Solve:** ([13-n-queens-ii.md](05-grid-board-backtracking/13-n-queens-ii.md))
```python
def totalNQueens(n: int) -> int:
    col, pos_diag, neg_diag = set(), set(), set()
    res = 0

    def backtrack(r: int) -> None:
        nonlocal res
        if r == n:
            res += 1                                 # count, don't copy a board
            return
        for c in range(n):
            if c in col or (r + c) in pos_diag or (r - c) in neg_diag:
                continue
            col.add(c); pos_diag.add(r + c); neg_diag.add(r - c)
            backtrack(r + 1)
            col.remove(c); pos_diag.remove(r + c); neg_diag.remove(r - c)

    backtrack(0)
    return res

def totalNQueensBitmask(n: int) -> int:               # the interview flex
    count = 0
    full_mask = (1 << n) - 1                          # n ones: all columns

    def backtrack(row: int, cols: int, pos_diag: int, neg_diag: int) -> None:
        nonlocal count
        if row == n:
            count += 1
            return
        valid_spots = full_mask & ~(cols | pos_diag | neg_diag)    # 1 bits are safe columns
        while valid_spots:
            bit = valid_spots & -valid_spots                       # the lowest free column
            valid_spots ^= bit
            backtrack(row + 1, cols | bit, (pos_diag | bit) << 1, (neg_diag | bit) >> 1)

    backtrack(0, 0, 0, 0)
    return count
```

**Cost:** The same `O(n!)` search as #12, but no board copy per solution. Space `O(n)` (the sets and recursion depth; no board). The bitmask version visits the same nodes with a much smaller constant (no hashing).
**Follow-up:** *Why shift the diagonal masks?* A diagonal attack moves one column sideways per row down. *Use symmetry?* Solve only the first half of the first row's columns and double (plus the middle column once for odd `n`), nearly halving the work (Variant A). *Is there a formula?* No known closed form.

**More scenarios on the same pattern**

**Variant A (crossover: symmetry)**
- **Question:** Count the n-queens solutions faster by exploiting the left-right symmetry of the board. (Classic optimisation of LC 52.)
- **Scenario:** The museum has a huge floor and wants the count in half the time.
- **Pattern and cost:** Each solution has a mirror image. Place the first-row queen only in columns `0 .. n/2 - 1`, double the count, and for odd `n` add the count with the queen in the middle column. About 2× fewer nodes, still `O(n!)`.

**Variant B (bitmask backtracking on a different problem)**
- **Question:** LC 1239 Maximum Length of a Concatenated String with Unique Characters. Given an array of strings `arr`, a concatenation of a subsequence of `arr` that has unique characters is valid. Return the maximum possible length of such a string.
- **Scenario:** A designer wants to join as many of the given word fragments as possible so that no letter appears twice in the result.
- **Pattern and cost:** Represent each fragment as a 26-bit mask (discard fragments with a repeated letter); backtrack over include/exclude, allowing a fragment only if its mask doesn't overlap the current mask. `O(2^n)` time, `O(n)` space. The same "set as a bitmask" move as the N-Queens bitmask.

---

### Topic 6. Build-a-String Backtracking

---

### 14. Letter Combinations of a Phone Number (#14)

**Original question:** LC 17. Given a string containing digits from `2-9` inclusive, return all possible letter combinations that the number could represent. Return the answer in any order. A mapping of digits to letters (just like on the telephone buttons) is given. `1` does not map to any letters.

**Scenario:** An old phone keypad maps `2` to "abc", `3` to "def", and so on. A user typed a short sequence of digits. List every possible text it could have been.

**Ask first:**
1. Which digits can appear (`2-9` only)? Can the input be empty (return an empty list)?
2. Does the order of the output matter?

**Spot it:** The answer is built **one position at a time**. At position `i`, the options are the letters of one fixed mapping. The depth equals the length of the input, and there is nothing to prune.

**Brute force:** There is no cheaper way to list `∏ (letters per digit)` strings. A nested loop works only if the input length is fixed; recursion handles any length.

**Solve:** ([14-letter-combinations-of-a-phone-number.md](06-build-a-string-backtracking/14-letter-combinations-of-a-phone-number.md))
```python
def letterCombinations(digits: str) -> list[str]:
    res = []
    digit_to_char = {"2": "abc", "3": "def", "4": "ghi", "5": "jkl",
                     "6": "mno", "7": "pqrs", "8": "tuv", "9": "wxyz"}

    def backtrack(index: int, string: str) -> None:
        if len(string) == len(digits):           # one letter chosen per digit
            res.append(string)
            return
        for char in digit_to_char[digits[index]]:
            backtrack(index + 1, string + char)  # a new string per call: un-choose is automatic

    if digits:                                   # guard: empty input returns []
        backtrack(0, "")
    return res
```

**Cost:** At most 4 letters per digit, so at most `4^n` strings, each built by `n` concatenations: `O(n · 4^n)` time. `O(n)` space (depth; the output isn't counted).
**Follow-up:** *Why is "un-choose" automatic?* `string + char` creates a new string; the parent's `string` is untouched. *Iterative?* Variant A. *Why guard `if digits`?* Without it the empty string would be returned as a result. *No binary version?* Every digit contributes exactly one letter.

**More scenarios on the same pattern**

**Variant A (crossover to iteration: a queue / product)**
- **Question:** LC 17 solved **iteratively**, without recursion.
- **Scenario:** The keypad tool is built for a device with an extremely small call stack.
- **Pattern and cost:** Start with `[""]`; for each digit, replace the list by every existing string extended with each of that digit's letters (or use `itertools.product`). `O(n · 4^n)` time and space. The same output with no recursion; the recursion's advantage is only that it scales to other constraints.

**Variant B (crossover to counting with duplicates)**
- **Question:** LC 1079 Letter Tile Possibilities. You have `n` tiles, each with a letter. Return the number of possible non-empty sequences of letters you can make using the letters on those tiles.
- **Scenario:** A word game has a rack of tiles, some with the same letter. How many different strings (of any length) can be spelled?
- **Pattern and cost:** Count distinct sequences: at each level choose any **letter with remaining count** (a map of counts, so repeats are never double counted), and count every node except the root. `O(n · n!)` worst case, `O(n)` space. It combines #5's dedup (by counts) with #14's "build a string".

---

### 15. Generate Parentheses (#15)

**Original question:** LC 22. Given `n` pairs of parentheses, write a function to generate all combinations of well-formed parentheses.

**Scenario:** A formula editor needs every way to arrange `n` pairs of opening and closing marks so that every mark is matched and nothing closes before it opens.

**Ask first:**
1. Only one kind of bracket? Is `n = 0` possible?
2. Does the output order matter?

**Spot it:** The answer is a string of length `2n`, built one character at a time. There are only **two choices** per position, and two **counters** decide which are legal, so almost every dead end is never entered.

**Brute force:** Generate all `2^(2n)` strings of `(` and `)` and keep the valid ones: `O(n · 4^n)`. The counter rules build only valid prefixes.

**Solve:** ([15-generate-parentheses.md](06-build-a-string-backtracking/15-generate-parentheses.md))
```python
def generateParenthesis(n: int) -> list[str]:
    res = []

    def backtrack(open_count: int, closing_count: int, current_str: str) -> None:
        if len(current_str) == 2 * n:
            res.append(current_str)
            return
        if open_count < n:                       # we may still open a mark
            backtrack(open_count + 1, closing_count, current_str + "(")
        if closing_count < open_count:           # a close is legal only if something is open
            backtrack(open_count, closing_count + 1, current_str + ")")

    backtrack(0, 0, "")
    return res
```

**Cost:** Only valid prefixes are built, so the number of results is the `n`-th Catalan number `≈ 4^n / (n·√n)`; each result has length `2n`: `O(4^n / √n)` time. `O(n)` space (recursion depth at most `2n`).
**Follow-up:** *Why is it already binary?* There are only two characters. *Count only?* The Catalan number, by DP or formula. *Several bracket types?* Add a counter per type and a stack of open types. *Remove the fewest brackets to make a string valid?* Variant A.

**More scenarios on the same pattern**

**Variant A (crossover: BFS or backtracking from a broken string)**
- **Question:** LC 301 Remove Invalid Parentheses. Given a string of parentheses and letters, remove the minimum number of invalid parentheses to make it valid; return all possible results.
- **Scenario:** A formula has stray marks. Remove the fewest marks needed to make it well-formed, and list every distinct fixed version.
- **Pattern and cost:** First count how many `(` and `)` must go (one scan), then backtrack over remove/keep with those limits, skipping equal neighbours to avoid duplicate results. Or BFS over strings, removing one mark per level. Exponential worst case; `O(n · 2^n)`.

**Variant B (crossover: divide and conquer with a memo)**
- **Question:** LC 241 Different Ways to Add Parentheses. Given a string of numbers and operators, return all possible results from computing all the different possible ways to group numbers and operators.
- **Scenario:** A calculator wants every value an expression like `2*3-4*5` could take, depending on where the brackets go.
- **Pattern and cost:** Split on each operator, recursively compute all results of the left and right parts, and combine every pair. With a memo on the substring: `O(Catalan(n))` outputs. Not a path-building search: it is divide and conquer returning lists.

---

## Part 5. Common traps to say out loud

Interviewers listen for these. Say the relevant one *before* you code it.

**The template**
- **Save a copy.** `res.append(path.copy())` (or `path[:]`), never `path`. Otherwise every saved answer becomes empty after un-choosing.
- **Un-choose exactly what you chose.** If you add to `path`, mark `used[i]`, add to three sets and write to the board, **all four** must be undone. A forgotten undo gives wrong answers on the *next* branch.
- **Base case first, and spell it out:** `len(path) == k`, `start == n`, `remaining == 0`, `row == n`, `open == close == n`. Say what to do when it's reached (save and return).
- **Subsets save at every node;** combinations and permutations save only at the right length. Mixing these up gives missing or extra answers.
- **Return early only for yes/no questions** (Word Search, Palindrome checks). For "list all", never return early on success.

**Duplicates and ordering**
- **Sort before skipping duplicates.** `if i > start and nums[i] == nums[i - 1]: continue` needs equal values adjacent (#2, #7).
- **`i > start`, not `i > 0`,** for subsets and combinations: the rule blocks an equal sibling at the **same level**, but must allow the same value deeper in a branch (`[1, 2, 2]`).
- **Permutations need a different check:** `i > 0 and nums[i] == nums[i-1] and not used[i-1]` (#5). Using the subset version in permutations gives wrong output.
- **Reuse vs no reuse:** recurse at `i` (reuse allowed, #6) or `i + 1` (each element once, #7). Getting this backwards is the classic bug.
- **A `start` index vs a `used[]` array:** `start` when order doesn't matter, `used[]` when it does.

**Pruning and cost**
- **Prune early, at the top of the call or loop.** Overshoot (`remaining < 0`), feasibility bound (too few characters left), validity (leading zeros, `> 255`, not a palindrome), counters (`close < open`).
- **On a sorted array, `break` instead of `continue`** when `nums[i] > remaining`: every later value is also too big.
- **Don't recompute state.** Pass `remaining` instead of `sum(path)` each call, use a `used[]` array instead of `num in path`, keep counters instead of counting characters.
- **Count questions aren't backtracking.** "How many subsets/paths/ways" is DP or a formula (`2^n`, `n!`, `C(n, k)`, Catalan). Say so.
- **Memoise only when sub-problems repeat** (Word Break II's suffix), not for path-dependent states.

**Problem-specific**
- **Subsets / Combinations:** the empty selection counts in #1. `k > n` returns `[]`. Include `n` in the range (`range(start, n + 1)` for numbers `1..n`).
- **Restore IP:** no leading zeros (except `"0"` itself), each part `0..255`, all digits used, exactly four parts, and an early exit for `n < 4` or `n > 12`.
- **Palindrome / Word Break:** the piece starts at `start` and ends at `end` (exclusive), so loop `end` up to `n + 1`.
- **Word Search:** unmark on the way out; check the bounds **before** indexing the board; the visited set belongs to the current path.
- **N-Queens:** the two diagonals are `r + c` and `r - c`; the board copy needs `join` per row; a count doesn't need a board.
- **Letter Combinations:** guard the empty input. **Generate Parentheses:** the two conditions are `open < n` and `close < open`.

**Python-specific**
- **Recursion depth** is fine for these problems, but say it for long inputs (the default limit is about 1000).
- **Strings are immutable:** `string + char` creates a new string per call. It makes un-choose automatic, but it is `O(n)` per call; for long outputs use a list and `join`.
- **`path = path + [x]`** (new list) avoids the undo step but costs `O(n)` per call; `append`/`pop` is the efficient form.
- **Nested functions that modify an outer integer** (a counter) need `nonlocal`.
- **`sorted()` / `.sort()`** before the search mutates the caller's list (`.sort()`); copy first if that matters.

---

## Part 6. Known gaps: important backtracking problems this repo doesn't cover yet

The repo covers all 15 tracked problems. For scenario questions you should still be able to **recognise** these. Several were named in the variants above.

| Problem | Technique | Why add it |
|---|---|---|
| Sudoku Solver (LC 37) | Placement backtracking with row/column/box sets, most-constrained-first | The natural big sibling of N-Queens; Valid Sudoku is already in the Arrays-Strings repo |
| Word Search II (LC 212) | Grid backtracking + trie | The standard "many words" follow-up of #11 |
| Combination Sum III (LC 216) | Fixed-size combinations with a target | Mixes #3 and #6/#7 |
| Partition to K Equal Sum Subsets (LC 698) | Assign items to buckets with pruning | A very common "yes/no with early return" backtracking question |
| Letter Case Permutation (LC 784), Letter Tile Possibilities (LC 1079) | Binary choice per position; counts with duplicates | Easy reps of branching and dedup |
| Non-decreasing Subsequences (LC 491) | Subsets where sorting is forbidden, dedup with a per-level set | Shows the dedup *idea* without the sort |
| Beautiful Arrangement (LC 526), Matchsticks to Square (LC 473), Unique Paths III (LC 980) | Permutation / bucket / grid backtracking with constraints | Medium reps of constraint pruning |
| Remove Invalid Parentheses (LC 301) | Count the excess first, then backtrack | A Hard that Google has asked in variations |
| Additive Number (LC 306), Expression Add Operators (LC 282) | Backtracking on cut points with an arithmetic constraint | The tracker removed LC 282 as low priority; know the shape |
| Palindrome Partitioning with a DP table (LC 131 follow-up) | Precompute `is_pal[i][j]` | Makes each validity test `O(1)` |
| Gray Code (LC 89), Iterator for Combination (LC 1286) | Bit tricks / generating lazily | When enumeration must be iterative or on demand |
| Count-only versions (Combination Sum IV, Coin Change, Partition Equal Subset Sum) | DP | Knowing when to *stop* using backtracking |

**Notes on the repo's own write-ups** (so you can answer well if asked):
- **#1, #2, #3, #6, #7** each have a **binary include/exclude** alternative in the write-up; **#4, #5, #8-#15** have a "why there's no binary version" note. Know the reason: every element is always used, so the choice is *which one* (or *where*), not *in or out*.
- **#4 Permutations** uses `num in path` (an `O(n)` scan). The write-up points out that a `used[]` array (as in #5) makes it `O(n · n!)`.
- **#6 and #7** call `sum(path)` on each call. A running `remaining` is faster and is used in the binary alternatives.
- **#10 Word Break II** is the one place where memoisation helps backtracking. The write-up notes it as the follow-up; the memoised version above is worth rehearsing.
- **#13 N-Queens II** has a **bitmask** alternative. Be ready to explain `valid_spots & -valid_spots` and why the diagonal masks shift in opposite directions.
- **#11 Word Search** has an in-place version with two prunes (letter frequency, and reversing the word when its last letter is rarer).
- **Tree-shaped backtracking** (root-to-leaf paths) lives in the Trees repo, not here.

**Confidence note:** the LeetCode numbers in the variants were written from memory, in the same spirit as the tracker's own caveat in [backtracking_problems.md](backtracking_problems.md). Before relying on a number, search the title on LeetCode. The techniques, costs and traps are the part to trust and rehearse.
