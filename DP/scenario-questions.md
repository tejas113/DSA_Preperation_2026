# DP: Scenario Question Bank (Google L3 style)

Google doesn't say "DP". It gives a short, vague scenario, and **you** have to notice that DP is the tool and work out what the state is.
This file has one scenario per solved problem in this repo, plus two more variants of each, so you practise the *recognition* step and not just the solution.
Problem numbers match [problems.md](problems.md).

**Disguised on purpose:** scenarios never say "subsequence", "knapsack", "dp", "grid path", "adjacent" or "state". Each one has an **Ask first** line (the clarifying questions a good candidate asks, which is how you discover the structure) and a **Spot it** line (the clue that gives DP away).

**How to use:** read only the **Scenario** line, then say out loud: *what is being asked (count / min / max / yes-no)? what do I need to remember about the past? what are my choices at each step?* Only then read the rest. About half of the variants deliberately cross over into a neighbouring pattern (greedy, BFS, backtracking, bitmask...) so you learn where DP stops working.

---

## Part 1. The 5-step "Is this DP?" framework

1. **Smell test: is it DP at all?** All three should be true.
   - It asks for a **count, min, max or yes/no** over many ways to build something. It does **not** ask you to list every solution.
   - A choice now changes what is possible later, but **only through a small summary of the past** (an index, a remaining budget, the last item used, a hold flag), not the full history.
   - A brute-force tree would **solve the same sub-situation more than once**. Draw two levels of the tree and look for repeated nodes.

   Then rule out the neighbours (see Part 2): can a greedy rule never hurt (try a 3 or 4 element counter-example)? Is the whole path part of the answer (backtracking)? Are all moves the same cost in a graph with cycles (BFS)?

2. **Name the state.** Complete this sentence in plain English: *"`dp(...)` = the best / number of ways / whether it is possible, for the part of the problem that is still left, given ..."*
   - Ask: **"what do I have to remember about what I already did, to make the next choice correctly?"** Typical answers: an index `i`; an index plus a running sum or remaining budget; the last item used (`prev`); whether I am holding; a range `(i, j)`; a pair of indexes into two strings.
   - Prefer "from here to the end" (a suffix). The memo then reads like the question.
   - **Every extra thing you remember multiplies the number of states**, so remember the minimum.

3. **List the choices and write the recurrence.** At each state, list every legal move (take / skip, 1 step / 2 steps, which word is next, which item goes last). Combine the children with the operator the question needs: `+` for count, `min`, `max`, or `or` for yes/no. Add the cost or gain of the move itself.

4. **Base case and answer.** A valid end returns what finishes for free (`1` for count, `0` for min/max, `True` for yes/no). A dead end returns what the combine operator ignores (`0`, `inf`, `-inf`, `False`). Then say where the answer lives: `dp(0)`, or the best over **every** cell (Maximal Square, Longest Increasing Path). Handle the **empty input** out loud.

5. **Order, shrink, cost: say it before you code.**
   - **Order of computation:** whatever the recursion asks for must already be filled. Asks for `i + 1`: loop `i` downward. Asks for `i - 1`: loop upward. Interval DP: by increasing length. Irregular (values decide the order): memoised DFS, or sort first.
   - **Can the state be shrunk?** Three tests. (a) Is one index implied by the others (Interleaving: `s3` index is `i + j`)? (b) Is one value derivable from another (remaining = total - sum)? (c) Does row `i` only read row `i + 1`? Then keep one or two rows (`O(n)` instead of `O(m·n)`, `O(1)` instead of `O(n)`).
   - **Cost:** `(number of distinct states) × (work per state)`. Space is the memo plus the recursion depth.

**Say-it-out-loud template:** *"This asks for the [count / min / max / feasibility] of [X]. The only thing the future needs to know about the past is [state]. At each step I choose between [choices]. So `dp([state]) = [combine] of [children]`. Base case is [..]. There are [N] states and [work] per state, so [time]. Row `i` only reads [..], so I can shrink to [..]."*

**Questions to ask the interviewer (cheap and impressive):**
- **Goal:** Do you want the count / min / max, or the actual solution (path, edits, items chosen)? That decides whether I can shrink the table.
- **Sizes:** How big can `n` and the target be? (decides memo vs table, and whether `n × target` is affordable)
- **Values:** Can they be zero, negative or duplicated? Is the answer guaranteed to exist? Should I return `-1`?
- **Reuse:** Can each item be used once or unlimited times? Does order matter ([1,2] vs [2,1])?
- **Edges:** Empty input? A single element? Is the start or end ever blocked?
- **Overflow:** Should the count be returned modulo something? Fits in 64 bits?
- **Mutation:** May I modify the input? (decides `O(1)` space tricks)
- **Repeats:** One query or many on the same data? (decides whether to precompute the table)

---

## Part 2. Signal → pattern cheat sheet

| What the question says | It is really | Pattern | Problems |
|---|---|---|---|
| "how many different ways to reach / make / schedule exactly N", small repeated steps | count sequences of small moves | 1D linear, count (Fibonacci) | 1 |
| "cheapest way to get to the end", each step costs something, jump 1 or 2 | shortest path on a line | 1D linear, min | 2 |
| "pick some, but taking one blocks the next" / "no two ... back to back" | best total with an exclusion rule | 1D take-or-skip | 3 |
| "round table", "ring", "wraps around" | the same line problem, solved twice (drop first / drop last) | 1D + break the circle | 4 |
| "a string of digits / letters with no separators: how many ways to read it" | count cut points | string segmentation, count | 5 |
| "can this text be fully explained by known pieces" | feasibility of cuts | string segmentation, yes/no | 6 |
| "exact total from unlimited items; fewest items" | min count to a target | unbounded knapsack (min) | 7 |
| "how many mixes add up to the total", order ignored | count combinations | unbounded knapsack (count, items outer) | 8 |
| "split into two equal groups", "can we hit exactly half" | subset reaches `total / 2` | 0/1 knapsack, yes/no | 9 |
| "give each item a + or -, count ways to hit T" | count subsets with a computed sum | 0/1 knapsack, count | 10 |
| "best contiguous run" where values can flip sign | keep best and worst ending here | running max and min (Kadane-style) | 11 |
| "pick any items in order, each strictly better than the last", "longest streak / chain / nesting" | longest increasing chain | LIS (`O(n²)` table, `O(n log n)` patience) | 12 |
| "robot moves only right and down", count or cheapest route | each cell is entered from two cells | 2D grid | 13, 14, 15, 16 |
| "largest square / block of good cells" | best block ending here is limited by 3 neighbours | 2D grid, min of three | 17 |
| "move in any of 4 directions, but each step must go uphill" | longest path in a DAG (values give the order) | memoised DFS on a grid | 18 |
| "longest / count of mirror-symmetric stretches" | ends match and the inside is symmetric | palindrome: expand from centres, or `dp[i][j]` | 19, 20 |
| "compare two sequences: keep order, skip some: similarity, fewest edits, can one be woven from two, how many ways to find A inside B" | a fact about prefixes (or suffixes) of both | two-string table | 21–25 |
| "wildcard / pattern with `*`" | fork: use the star zero times or one more time | two-string table with branching | 25 |
| "at most k trades", "cooldown", "fee", "hold or not" | a few modes, one move per day | state machine | 26, 27, 28 |
| "the order of removal changes the payoff", "cost of cutting / merging a range" | pick the item handled **last** in a range | interval DP | 29 |
| "n ≤ 15–20 items, visit / assign / cover all of them" | state = set of used items | bitmask DP | gap (Part 6) |
| "count numbers up to N with a digit property" | state = position, tight flag, summary | digit DP | gap (Part 6) |
| "two players play optimally", "can the first player win", "max margin" | best of me minus best of you on the remaining range | min-max interval DP | gap (Part 6) |
| "a tree, choose nodes but not a node and its parent" | return a pair (take, skip) from each child | tree DP | Trees repo |

**Red flags that you're being tested on DP:** "number of ways", "minimum / maximum cost", "is it possible to make exactly", "longest", "can it be split into", "at most k", and any question where the first brute force you think of is "try everything" and it clearly repeats work.

### DP or greedy?

Greedy is right when one locally best choice can **never** hurt later (usually proven by sorting plus an exchange argument). DP is right when a choice **costs future flexibility**.

- **Test:** write a 3 or 4 element counter-example on the whiteboard. If you find one in 30 seconds, it is DP.
- **Coin Change** `[1, 3, 4]`, amount `6`: greedy takes `4 + 1 + 1` (3 coins), best is `3 + 3` (2 coins). Greedy only works for special coin systems like 1, 5, 10, 25.
- **House Robber** `[4, 5, 4]`: greedy takes the 5 and gets `5`; best is `4 + 4 = 8`.
- **Stocks:** unlimited transactions and no restrictions is **greedy** (add every rise). The moment there is a limit `k`, a cooldown or a fee, it becomes a state machine.
- **Jump Game / minimum jumps** is greedy (track the farthest reach). **Unweighted** interval scheduling is greedy (sort by end). **Weighted** interval scheduling is DP.
- Greedy is usually `O(n log n)` or `O(n)`. If your DP is `O(n²)`, ask the interviewer whether `n` is large, then ask yourself whether a greedy exists.

### DP or backtracking?

- They are the same recursion. **Memoised backtracking is top-down DP.** The only question is whether the memo key is small and repeats.
- **Backtracking** when the output is **every** solution (all subsets, all permutations, Word Break II), or when the future depends on the **whole path** (N-Queens: where every earlier queen is).
- **DP** when you only need a **count, optimum or yes/no**, and the future depends on a **small summary** of the path.
- **If the key needs a visited set**, it's backtracking, or bitmask DP when `n ≤ 20`.

### DP or BFS / Dijkstra?

- A shortest path where every move costs the same and you can go **in all directions** (cycles) is **BFS**. DP needs an order with no cycles: moves only go forward, only go uphill, or carry a step counter.
- Different non-negative costs with cycles is **Dijkstra**. The same cost with only right/down moves is a **DP** sweep.

---

## Part 3. Complexity patterns

Every DP cost is **(number of distinct states) × (work per state)**. Count the parts of the memo key first.

| Pattern | States | Work per state | Time | Space (memo) | Space reduced to (and how) |
|---|---|---|---|---|---|
| 1D, fixed look-back (Climbing Stairs, Min Cost, Robber, Decode Ways) | `n` | O(1) | O(n) | O(n) | **O(1)**: two rolling variables (`dp[i]` reads `i+1`, `i+2`) |
| 1D with a loop over a dictionary (Word Break) | `n` | `m` words × `k` compare | O(n·m·k) | O(n) | stays O(n): it looks at far-away positions |
| Unbounded knapsack (Coin Change I and II) | `n × amount` | O(1) | O(n·amount) | O(n·amount) | **O(amount)**: one array, coins outer, sums in the right direction |
| 0/1 knapsack (Partition, Target Sum) | `n × S` | O(1) | O(n·S) | O(n·S) | **O(S)**: one array; the inner loop direction stops an item being reused |
| LIS as `dp(idx, prev)` | `n²/2` | O(1) | O(n²) | O(n²) | use `dp[i]` = "best ending at i": O(n) space |
| LIS as `dp[i]` | `n` | O(n) (scan earlier) | O(n²) | O(n) | patience sorting: **O(n log n)** time |
| Max Product Subarray | `n` | O(1) | O(n) | O(1) | already two variables |
| Grid sweep (Unique Paths, Min Path Sum, Triangle, Maximal Square) | `m × n` | O(1) | O(m·n) | O(m·n) | **O(n)**: one row (keep the old diagonal in `temp` for Maximal Square); **O(1)** only if you may overwrite the input |
| Memoised DFS on a grid (Longest Increasing Path) | `m × n` | O(4) | O(m·n) | O(m·n) | stack can be `m·n` deep; use a sorted table or Kahn to avoid recursion |
| Two-string table (LCS, Edit Distance, Distinct Subsequences, Interleaving, Regex) | `m × n` | O(1) | O(m·n) | O(m·n) | **O(min(m, n))**: rolling row(s). *Reconstructing the answer needs the full table.* |
| Palindrome by centres | `2n - 1` centres | O(n) expand | O(n²) | O(1) | already O(1) |
| Palindrome table `dp[i][j]` | `n²/2` | O(1) | O(n²) | O(n²) | hard to roll; prefer centres |
| State machine, stocks with `k` trades | `n × 2 × (k+1)` | O(1) | O(n·k) | O(n·k) | **O(k)**: one day's `2 × (k+1)` grid |
| State machine with a fixed number of modes (Cooldown, Fee) | `n × modes` | O(1) | O(n) | O(n) | **O(1)**: one variable per mode |
| Interval DP (Burst Balloons) | `n²/2` ranges | O(n) (try each last `k`) | O(n³) | O(n²) | none: each range reads many shorter ranges |
| Bitmask DP | `2^n × extra` | O(n) | O(2^n · n²) typical | O(2^n · n) | sometimes roll over popcount |
| Digit DP | `digits × tight × summary` | O(10) | O(digits · 10 · summary) | same | roll over the digit position |
| Tree DP | `n` nodes | O(children) | O(n) | O(height) | none needed |

**How to work out complexity (say it in this order):**
1. **Count the parts of the key.** One index: about `n` states. Two indexes: `n × m`. Index + running sum: `n × target`. A range `(i, j)`: about `n²/2`.
2. **Look inside one state.** No loop is O(1). A loop over `k` choices is O(k).
3. **Multiply** for time. **Space** is the memo (every state) plus the recursion stack.
4. **Ask which earlier rows a state reads.** Only the previous row (or one or two values)? Roll it. Reads far back, or you must reconstruct the answer? Keep the table.

**Rules of thumb**
- The state count is often **bigger than the input size**: Coin Change with `amount = 10,000` and 12 coins has about 120,000 states from 12 numbers. The target is the expensive part (it is *pseudo-polynomial*: polynomial in the value of the target, not in the number of digits it takes to write it).
- Top-down and bottom-up have the **same big-O**. Top-down may touch fewer states; bottom-up avoids Python's 1000-deep recursion limit. Say that out loud.
- **Loop direction matters for rolled arrays.** Reuse allowed (unbounded): the loop reads cells already updated *in this pass*. Use once (0/1): it must read cells *not yet* updated. Whether that means "ascending" or "descending" depends on whether your array indexes the sum so far or the sum remaining. Say which you chose.
- Memo dict keys cost hashing. If the interviewer asks for speed, a list-based table is usually 2 to 5 times faster than a dict in Python.

---

## Part 4. The scenarios

Each entry has: **Original question** (the formal LeetCode statement), then **Scenario** (what you'd actually hear), **Ask first**, **Spot it** (the clue that reveals DP), **Model** (state / choices / recurrence / base), **Solve** (the answer from your write-up, top-down and bottom-up), **Cost**, **Follow-up** (what they'd push on), and **two more variants (A and B)** on the same pattern. Each variant gives the formal **Question** first, then the disguised **Scenario**, then **Pattern and cost**. Variants marked **(crossover)** leave the entry's pattern on purpose, to show you where it stops working.

---

### 1. Climbing Stairs (#1)

**Original question:** LC 70. You are climbing a staircase that has `n` steps. Each move climbs 1 or 2 steps. Return the number of distinct ways to reach the top.

**Scenario:** A payment service retries a failed charge, waiting either 1 or 2 minutes between attempts. How many different wait schedules add up to exactly `N` minutes?

**Ask first:**
1. Does the order of the waits matter (1 then 2 versus 2 then 1)?
2. How big can `N` get, and should the count be returned modulo something?

**Spot it:** "How many different ways", and every full schedule ends with either a 1-minute or a 2-minute wait. So the count for `N` is built from the counts for `N - 1` and `N - 2`, which are needed again and again.

**Model:**
- **State:** `dp(i)` = ways to finish the schedule when `i` minutes are already used.
- **Choices:** wait 1, or wait 2.
- **Recurrence:** `dp(i) = dp(i + 1) + dp(i + 2)`.
- **Base:** `dp(n) = 1` (landed exactly on the deadline), `dp(i > n) = 0` (overshot).

**Solve:** ([01-climbing-stairs.md](01-1d-dp-linear-sequences/01-climbing-stairs.md))
```python
# Top-down
def climbStairs(self, n: int) -> int:
    memo = {}
    def dp(i):
        if i == n: return 1
        if i > n: return 0
        if i in memo: return memo[i]
        memo[i] = dp(i + 1) + dp(i + 2)
        return memo[i]
    return dp(0)

# Bottom-up (fill from the top downward, then two variables for O(1) space)
def climbStairs(self, n: int) -> int:
    dp = [0] * (n + 2)
    dp[n] = 1
    for i in range(n - 1, -1, -1):
        dp[i] = dp[i + 1] + dp[i + 2]
    return dp[0]

def climbStairs(self, n: int) -> int:       # O(1) space
    nxt, nxt2 = 1, 0
    for _ in range(n):
        nxt, nxt2 = nxt + nxt2, nxt
    return nxt
```

**Cost:** States = `n` (one per minute mark). Work per state = one addition. Time O(n). Space O(n) for the memo and the recursion; O(1) with two variables.
**Follow-up:** *Space?* Two variables. *Huge N?* Matrix exponentiation gives O(log N). *Steps can be any of a given set?* Loop over the set (see Variant A). *Print the schedules?* That is backtracking now, and the count explodes. *Greedy trap:* none here, there is no "best", only a count.

**More scenarios on the same pattern**

**Variant A (crossover to unbounded knapsack, order matters)**
- **Question:** LC 377 Combination Sum IV. Given distinct positive integers `nums` and a `target`, return the number of sequences (order matters) of numbers from `nums` that add up to `target`.
- **Scenario:** A delivery robot can be loaded with 1, 3 or 4 parcels per trip. How many different trip-by-trip plans deliver exactly `N` parcels? A 1-then-3 plan and a 3-then-1 plan are different plans.
- **Pattern and cost:** `dp[i] = sum(dp[i - x] for x in nums if x <= i)`, `dp[0] = 1`. States `N`, work `k` (number of sizes), so O(N·k) time, O(N) space. The **target is the outer loop** here. In Coin Change II the coins are the outer loop (combinations). Swapping the loops swaps "sequences" and "mixes".

**Variant B (crossover to a hidden state machine)**
- **Question:** Count binary strings of length `n` with no two consecutive `1`s. (LC 600 is the harder "integers up to `n`" version, a digit-DP problem.)
- **Scenario:** An on-call rota covers `n` days. Each day a person is either on call or off, and nobody is on call two days running. How many valid rotas exist?
- **Pattern and cost:** It is Fibonacci again, but the way to see it is by the **last day's value**: `ends_off[i] = ends_off[i-1] + ends_on[i-1]`, `ends_on[i] = ends_off[i-1]`. That is a two-mode state machine, the same idea as the stock problems. O(n) time, O(1) space.

---

### 2. Min Cost Climbing Stairs (#2)

**Original question:** LC 746. Given `cost[i]`, the price of standing on step `i`, you may start on step 0 or step 1 and climb 1 or 2 steps at a time. Return the minimum total cost to reach the top (one position past the last step).

**Scenario:** A hiker follows a trail with `n` huts in a row. Staying at hut `i` costs `fee[i]`. Each day they move on by one or two huts. They may begin at either of the first two huts and must get past the last one. What is the least they can pay in total?

**Ask first:**
1. Is the fee paid for huts you *pass over* (jump across), or only for huts you stop at?
2. Can fees be zero or negative?

**Spot it:** "Cheapest way to get to the end" with two possible last moves. The best total to finish from a hut depends only on the next two huts' best totals.

**Model:**
- **State:** `dp(i)` = cheapest total from hut `i` to the end, including `fee[i]`.
- **Choices:** move 1 hut or 2 huts.
- **Recurrence:** `dp(i) = fee[i] + min(dp(i + 1), dp(i + 2))`.
- **Base:** `dp(i >= n) = 0`. **Answer:** `min(dp(0), dp(1))` (two possible starts).

**Solve:** ([02-min-cost-climbing-stairs.md](01-1d-dp-linear-sequences/02-min-cost-climbing-stairs.md))
```python
# Top-down
def minCostClimbingStairs(self, cost: list[int]) -> int:
    n = len(cost)
    memo = {}
    def dp(i):
        if i >= n: return 0
        if i in memo: return memo[i]
        memo[i] = cost[i] + min(dp(i + 1), dp(i + 2))
        return memo[i]
    return min(dp(0), dp(1))

# Bottom-up, O(1) space
def minCostClimbingStairs(self, cost: list[int]) -> int:
    nxt, nxt2 = 0, 0
    for i in range(len(cost) - 1, -1, -1):
        cur = cost[i] + min(nxt, nxt2)
        nxt2, nxt = nxt, cur
    return min(nxt, nxt2)
```

**Cost:** States = `n`. Work = one `min`. Time O(n), space O(n) (O(1) rolled).
**Follow-up:** *Print the route?* Keep the full table, then walk it from the start choosing the smaller neighbour. *Jump up to `k` huts?* Work per state becomes `k`, O(n·k), or O(n) with a sliding-window minimum. *Greedy trap:* "always step to the cheaper of the next two" fails: a cheap next hut can lead to an expensive one.

**More scenarios on the same pattern**

**Variant A (crossover to greedy)**
- **Question:** LC 45 Jump Game II. `nums[i]` is the maximum jump length from position `i`. Return the minimum number of jumps to reach the last index (it is always reachable).
- **Scenario:** A message must be relayed along a row of signal towers. Tower `i` can forward it to any tower up to `p[i]` towers ahead. What is the fewest relays needed to reach the last tower?
- **Pattern and cost:** DP works: `dp[i] = 1 + min(dp[j] for j in reach of i)`, O(n²). But a **greedy** is O(n): sweep once, track the farthest reach of the current "jump level", and add a jump when you pass its end. This is the "DP exists but greedy is expected" case.

**Variant B (crossover to a sliding-window optimisation)**
- **Question:** LC 1696 Jump Game VI. From index `i` you may jump to any index in `[i + 1, i + k]`. Each visited index adds `nums[i]` (can be negative). Return the maximum score on a path from index 0 to the last index.
- **Scenario:** A game character crosses `n` platforms with point values (some negative). It can leap forward by at most `k` platforms. What is the best total it can collect arriving at the last platform?
- **Pattern and cost:** `dp[i] = nums[i] + max(dp[i-k .. i-1])`. Naive is O(n·k). A **monotonic deque** holding the window maximum makes it O(n) time, O(k) space.

---

### 3. House Robber (#3)

**Original question:** LC 198. Given `nums[i]`, the money in house `i`, return the maximum you can rob without robbing two adjacent houses.

**Scenario:** A conference has `n` talks in a row, each with an expected audience size. A sponsor may fund any talks, but a funded talk takes over the room for set-up of the following slot, so the following talk cannot be funded. Maximise the total audience the sponsor reaches.

**Ask first:**
1. Can audience sizes be zero? Is an empty selection allowed?
2. Do you want only the total, or which talks to fund?

**Spot it:** "Maximise a total" where picking one thing rules out another thing right after it. Each talk is either picked or skipped, and the best from slot `i` onward depends on only two later answers.

**Model:**
- **State:** `dp(i)` = best total from talks `i..n-1`.
- **Choices:** fund talk `i` (then jump to `i + 2`) or skip it (go to `i + 1`).
- **Recurrence:** `dp(i) = max(nums[i] + dp(i + 2), dp(i + 1))`.
- **Base:** `dp(i >= n) = 0`.

**Solve:** ([03-house-robber.md](01-1d-dp-linear-sequences/03-house-robber.md))
```python
# Top-down
def rob(self, nums: list[int]) -> int:
    n = len(nums)
    memo = {}
    def dp(i):
        if i >= n: return 0
        if i in memo: return memo[i]
        rob = nums[i] + dp(i + 2)
        not_rob = dp(i + 1)
        memo[i] = max(rob, not_rob)
        return memo[i]
    return dp(0)

# Bottom-up, O(1) space
def rob(self, nums: list[int]) -> int:
    nxt, nxt2 = 0, 0
    for i in range(len(nums) - 1, -1, -1):
        cur = max(nums[i] + nxt2, nxt)
        nxt2, nxt = nxt, cur
    return nxt
```

**Cost:** States = `n`. Work = one `max`. Time O(n). Space O(n) memo plus stack; O(1) rolled.
**Follow-up:** *Which talks?* Keep the full table and walk it: if `dp[i] == dp[i+1]` skip, else take. *Round-table / wrap-around?* See #4. *Must fund at least `k`?* Add a count to the state (n × k). *Greedy trap:* "take the biggest, then the next biggest that fits" fails on `[4, 5, 4]` (greedy gets 5, best is 8).

**More scenarios on the same pattern**

**Variant A (crossover: bucket first, then the same recurrence)**
- **Question:** LC 740 Delete and Earn. Choosing a number `x` from `nums` earns `x` points for every copy of `x` but deletes every `x - 1` and `x + 1`. Return the maximum points.
- **Scenario:** In a loyalty game, you have a pile of tokens, each marked with a number. Picking a number collects every token with that number, but destroys all tokens marked one higher or one lower. What is the most you can collect?
- **Pattern and cost:** Add up the points per value into `gain[v]`, then run **House Robber over the value axis** (picking `v` blocks `v + 1`). O(n + maxV) time, O(maxV) space. The skill: turning a "blocks neighbours by value" rule into a line.

**Variant B (crossover to tree DP)**
- **Question:** LC 337 House Robber III. The houses form a binary tree; you cannot rob a house and its direct child. Return the maximum money.
- **Scenario:** A company chart shows who manages whom. HR picks employees for a bonus scheme, but no one may be chosen if their direct manager is also chosen. Maximise the total productivity score of the chosen group.
- **Pattern and cost:** Each node returns a **pair** `(best if taken, best if skipped)`. `take = val + left.skip + right.skip`; `skip = max(left) + max(right)`. O(n) time, O(h) space. Lives in the Trees repo.

---

### 4. House Robber II (#4)

**Original question:** LC 213. The houses are arranged in a circle (the first and last are adjacent). Return the maximum you can rob without robbing two adjacent houses.

**Scenario:** A venue rents out `n` time slots that repeat every day, so after the last slot of the day comes the first slot of the next day. A booking uses the slot's room and also the changeover time of the slot right after it. Choose bookings to maximise revenue.

**Ask first:**
1. Is the schedule really circular (last slot blocks the first)?
2. What if there is only one slot?

**Spot it:** The same pick-or-skip problem, but "after the last comes the first". That breaks the line into two cases.

**Model:**
- **Reduce:** the first and last house are never both robbed, so the answer is `max(solve(nums[:-1]), solve(nums[1:]))`. Each is House Robber.
- **State:** `dp(i)` = best from slots `i..` of *this* line (fresh memo per line).
- **Recurrence:** `dp(i) = max(dp(i + 1), lis[i] + dp(i + 2))`.
- **Base:** `dp(i >= length) = 0`; `n == 1` returns `nums[0]` before slicing.

**Solve:** ([04-house-robber-ii.md](01-1d-dp-linear-sequences/04-house-robber-ii.md))
```python
# Top-down
def rob(self, nums: list[int]) -> int:
    n = len(nums)
    if n == 1:
        return nums[0]
    def solve(lis):
        length = len(lis)
        memo = {}
        def dp(i):
            if i >= length: return 0
            if i in memo: return memo[i]
            skip_current = dp(i + 1)
            rob_current = lis[i] + dp(i + 2)
            memo[i] = max(skip_current, rob_current)
            return memo[i]
        return dp(0)
    return max(solve(nums[:-1]), solve(nums[1:]))

# Bottom-up, two variables per line
def rob(self, nums: list[int]) -> int:
    if len(nums) == 1:
        return nums[0]
    def solve(lis):
        nxt, nxt2 = 0, 0
        for i in range(len(lis) - 1, -1, -1):
            cur = max(nxt, lis[i] + nxt2)
            nxt2, nxt = nxt, cur
        return nxt
    return max(solve(nums[:-1]), solve(nums[1:]))
```

**Cost:** States ≈ `n - 1` per line, two lines. Time O(n). Space O(n) (the slice copies); pass `(lo, hi)` bounds to get O(1).
**Follow-up:** *Avoid the slice copies?* Pass bounds. *Why not one pass?* Because "first taken" must be remembered: that's the extra state you are splitting away. *k-fold wrap-around?* Not DP-friendly. *Greedy trap:* none; it is the same as #3.

**More scenarios on the same pattern**

**Variant A (crossover to Kadane)**
- **Question:** LC 918 Maximum Sum Circular Subarray. Given a circular array, return the maximum sum of a non-empty contiguous subarray (it may wrap around the end).
- **Scenario:** A circular conveyor belt has `n` bins with profit or loss values. Pick one continuous stretch, which may pass the belt's join point, to maximise the total.
- **Pattern and cost:** Answer = `max(kadane_max, total - kadane_min)`: a wrapping stretch is "everything except a middle run". Watch the all-negative case (then `total - kadane_min` is 0, which is wrong, so return `kadane_max`). O(n) time, O(1) space.

**Variant B (same 1D family, richer last-element state)**
- **Question:** LC 276 Paint Fence. Paint `n` posts with `k` colours so that no more than two adjacent posts share a colour. Return the number of ways.
- **Scenario:** A mural has `n` panels in a row and `k` paint colours. No three panels in a row may have the same colour. How many designs are possible?
- **Pattern and cost:** Track two counts: `same[i]` (panel `i` copies panel `i-1`) and `diff[i]`. `same[i] = diff[i-1]`, `diff[i] = (same[i-1] + diff[i-1]) * (k - 1)`. O(n) time, O(1) space. Same shape as #3, but the state is the "run so far".

---

### 5. Decode Ways (#5)

**Original question:** LC 91. A message of digits is decoded using `1 → A ... 26 → Z`. Given a digit string `s`, return the number of ways to decode it.

**Scenario:** An old telemetry log stores event codes from 1 to 26 written one after another with no separators, like `11106`. Without the original recorder, how many different code sequences could have produced the log?

**Ask first:**
1. Can the string start with 0, or contain a standalone 0 (for example "06")? What do we return then?
2. How long can it be, and is the answer taken modulo something?

**Spot it:** "How many ways can this string be read", where at each point there are only two possible readings (one digit or two). The rest of the string after a given cut is a smaller copy of the same question.

**Model:**
- **State:** `dp(i)` = ways to decode `s[i:]`.
- **Choices:** read one digit (if not `0`), or two digits (if 10 to 26).
- **Recurrence:** `dp(i) = dp(i + 1) + (dp(i + 2) if s[i:i+2] is 10..26)`.
- **Base:** `dp(n) = 1`; `dp(i) = 0` if `s[i] == "0"`.

**Solve:** ([05-decode-ways.md](02-string-counting-dp/05-decode-ways.md))
```python
# Top-down
def numDecodings(self, s: str) -> int:
    n = len(s)
    memo = {}
    def dp(i):
        if i == n: return 1
        if s[i] == "0": return 0
        if i in memo: return memo[i]
        ans = dp(i + 1)
        if i + 1 < n and (s[i] == "1" or (s[i] == "2" and s[i + 1] <= "6")):
            ans = dp(i + 1) + dp(i + 2)
        memo[i] = ans
        return memo[i]
    return dp(0)

# Bottom-up, O(1) space
def numDecodings(self, s: str) -> int:
    n = len(s)
    nxt, nxt2 = 1, 0
    for i in range(n - 1, -1, -1):
        if s[i] == "0":
            cur = 0
        else:
            cur = nxt
            if i + 1 < n and (s[i] == "1" or (s[i] == "2" and s[i + 1] <= "6")):
                cur += nxt2
        nxt2, nxt = nxt, cur
    return nxt
```

**Cost:** States = `n` (one per start index). Work = O(1) (two checks). Time O(n). Space O(n); O(1) rolled.
**Follow-up:** *Space?* Two variables. *Return the decodings?* Backtracking, output can be exponential. *Wildcard digits?* See Variant A. *Trap:* a `0` can only be the second digit of `10` or `20`; the check `s[i] == "0"` is what stops `"06"`.

**More scenarios on the same pattern**

**Variant A (same pattern, bigger case analysis)**
- **Question:** LC 639 Decode Ways II. The string may also contain `*`, which stands for any digit 1 to 9. Return the number of ways to decode, modulo 10^9 + 7.
- **Scenario:** The same telemetry log, but a few characters got smudged and could be any digit from 1 to 9. Count the possible original code sequences.
- **Pattern and cost:** Same `dp(i)`; the transition multiplies by how many digits a `*` can be (9 for one digit; 9, 6 or 15 for two-digit combos). O(n) time, O(1) space. The lesson is to enumerate the cases cleanly.

**Variant B (crossover to backtracking)**
- **Question:** LC 140 Word Break II. Given a string and a dictionary, return all sentences you can form by inserting spaces so that each piece is a dictionary word.
- **Scenario:** A search box receives text with all spaces stripped. List every way to put spaces back so that each piece is a product in the catalogue.
- **Pattern and cost:** The yes/no DP from #6 tells you whether any solution exists, but listing them is **memoised backtracking**: `dp(i)` returns the list of sentences for `s[i:]`. Cost is output-sensitive, up to O(2^n) sentences. Use the feasibility DP first to prune dead branches.

---

### 6. Word Break (#6)

**Original question:** LC 139. Given a string `s` and a dictionary `wordDict`, return `true` if `s` can be segmented into a space-separated sequence of one or more dictionary words (words may be reused).

**Scenario:** A log parser has a registry of known command tokens. A line arrives written with no separators. Can the entire line be explained as a run of known tokens?

**Ask first:**
1. Can a token be used more than once? How large is the registry, and how long can a token be?
2. Is the match case-sensitive? Can the registry contain an empty token?

**Spot it:** "Can the whole thing be covered by pieces from a set". The remainder after a chosen first piece is the same question on a shorter suffix, and different first pieces can land on the same cut point.

**Model:**
- **State:** `dp(start)` = can `s[start:]` be fully segmented.
- **Choices:** which dictionary word starts here (it must match).
- **Recurrence:** `dp(start) = any(dp(start + len(w)) for w in words if s.startswith(w, start))`.
- **Base:** `dp(n) = True`. Cache `False` as well.

**Solve:** ([06-word-break.md](02-string-counting-dp/06-word-break.md))
```python
# Top-down
def wordBreak(self, s: str, wordDict: list[str]) -> bool:
    words = set(wordDict)
    memo = {}
    n = len(s)
    def dp(start):
        if start == n: return True
        if start in memo: return memo[start]
        for word in words:
            word_length = len(word)
            if start + word_length <= n and s[start:start + word_length] == word:
                if dp(start + word_length):
                    memo[start] = True
                    return memo[start]
        memo[start] = False
        return memo[start]
    return dp(0)

# Bottom-up
def wordBreak(self, s: str, wordDict: list[str]) -> bool:
    words = set(wordDict)
    n = len(s)
    dp = [False] * (n + 1)
    dp[n] = True
    for start in range(n - 1, -1, -1):
        for word in words:
            word_length = len(word)
            if start + word_length <= n and s[start:start + word_length] == word and dp[start + word_length]:
                dp[start] = True
                break
    return dp[0]
```

**Cost:** States = `n`. Work = loop over `m` words, each comparison up to `k` characters. Time O(n·m·k). Space O(n).
**Follow-up:** *Speed it up?* Put the words in a trie, or only try prefix lengths up to the longest word, so work per state is `O(k²)` with a hash set. *List all segmentations?* Variant B of #5. *Shortest segmentation?* Change `or` to `min`. *Trap:* cache `False`, or a dead suffix is retried many times.

**More scenarios on the same pattern**

**Variant A (same pattern, applied to each item)**
- **Question:** LC 472 Concatenated Words. Given a list of unique words, return all words that are a concatenation of at least two shorter words from the list.
- **Scenario:** From a list of product names, find every name that could be built entirely by gluing together two or more other names from the same list.
- **Pattern and cost:** Run Word Break for each word against the set of the *other* words (skip the word itself, or require at least 2 pieces). O(total characters × L) with a set. Sorting by length lets you add each word to the set after testing it.

**Variant B (crossover: yes/no becomes min)**
- **Question:** LC 2707 Extra Characters in a String. Break `s` into non-overlapping dictionary words; characters not in any chosen word are "extra". Return the minimum number of extra characters.
- **Scenario:** A text must be tiled with entries from a phrasebook. Letters not covered by any entry are wasted. Minimise the wasted letters.
- **Pattern and cost:** `dp[i] = min(dp[i+1] + 1, min(dp[i + len(w)] for w that matches))`, `dp[n] = 0`. Same states and work as #6: O(n·m·k). Only the combine operator changed (`or` became `min`).

---

### 7. Coin Change (#7)

**Original question:** LC 322. Given coin denominations and an `amount`, return the fewest coins that make up exactly `amount`, or `-1` if impossible. Each coin can be used any number of times.

**Scenario:** A kiosk's cash drawer holds an unlimited supply of a few bill sizes. A customer is owed an exact amount. What is the fewest bills the kiosk can hand over, or can't it be done at all?

**Ask first:**
1. Is the supply of each bill really unlimited? Can the amount be 0?
2. Are the bill sizes arbitrary (not guaranteed to work like 1, 5, 10, 25)?

**Spot it:** "Fewest items to hit an exact total, reuse allowed". Greedy *looks* right but fails on odd denominations, which is the signal to use DP.

**Model:**
- **State:** `dp(i, current_sum)` = fewest more coins to reach `amount` using coins from index `i` on, having already reached `current_sum`.
- **Choices:** pick coin `i` (and **stay on `i`**, reuse allowed), or skip to coin `i + 1`.
- **Recurrence:** `dp(i, s) = min(1 + dp(i, s + coins[i]), dp(i + 1, s))`.
- **Base:** `s == amount` → `0`; out of coins or `s > amount` → `inf`. Return `-1` if the result is `inf`.

**Solve:** ([07-coin-change.md](03-knapsack-dp/07-coin-change.md))
```python
# Top-down (pick / not-pick)
def coinChange(self, coins: list[int], amount: int) -> int:
    memo = {}
    def dp(i, current_sum):
        if current_sum == amount: return 0
        if i >= len(coins) or current_sum > amount: return float('inf')
        if (i, current_sum) in memo: return memo[(i, current_sum)]
        pick = 1 + dp(i, current_sum + coins[i])
        not_pick = dp(i + 1, current_sum)
        memo[(i, current_sum)] = min(pick, not_pick)
        return memo[(i, current_sum)]
    ans = dp(0, 0)
    return ans if ans != float('inf') else -1

# Bottom-up (one array; coins outer, sums descending so a coin can repeat)
def coinChange(self, coins: list[int], amount: int) -> int:
    dp = [float('inf')] * (amount + 1)
    dp[amount] = 0
    for c in coins:
        for s in range(amount - c, -1, -1):
            dp[s] = min(dp[s], 1 + dp[s + c])
    return dp[0] if dp[0] != float('inf') else -1
```
Leaner memo with a single index (the coin order cannot change a "fewest" answer): `dp(curr_amount) = min(1 + dp(curr_amount + c) for c in coins)`, so only `amount` states.

**Cost:** States = `len(coins) × amount` (or just `amount` in the single-index version). Work = O(1) (or `len(coins)` in the single-index version). Time O(amount × len(coins)). Space O(amount × len(coins)) memo, O(amount) with the array.
**Follow-up:** *Space?* One array. *Which coins?* Keep a `parent[s]` coin. *Each coin only once?* Change the loop direction (0/1, like #9). *Greedy trap:* coins `[1, 3, 4]`, amount `6`: greedy gives 3 coins, best is `3 + 3`. *Recursion depth?* Up to `amount` for a coin worth 1, so use the table for big amounts.

**More scenarios on the same pattern**

**Variant A (same pattern, hidden denominations)**
- **Question:** LC 279 Perfect Squares. Return the least number of perfect square numbers (1, 4, 9, ...) that sum to `n`.
- **Scenario:** A flooring company sells only square tiles with whole-number side lengths (1×1, 2×2, 3×3, ...). A room has `n` unit cells to cover exactly. What is the fewest tiles needed?
- **Pattern and cost:** Coin Change where the "coins" are all squares up to `n`. `dp[i] = 1 + min(dp[i - k²])`. O(n√n) time, O(n) space. (Lagrange's four-square theorem bounds the answer by 4.)

**Variant B (crossover: the index is a calendar)**
- **Question:** LC 983 Minimum Cost For Tickets. You travel on given days of the year. A 1-day pass costs `c1`, a 7-day pass `c2`, a 30-day pass `c3`. Return the minimum cost to cover every travel day.
- **Scenario:** A commuter knows the days they will travel this year. Day, week and month passes have different prices. What is the cheapest way to cover all the trips?
- **Pattern and cost:** `dp[d]` = cheapest cost from day `d`, three choices per travel day. O(365) time and space (or O(number of travel days)). The cheapest-per-day pass is a greedy trap; a month pass bought for one trip can be wasted.

---

### 8. Coin Change II (#8)

**Original question:** LC 518. Given coin denominations and an `amount`, return the number of combinations that make up that amount (unlimited supply of each coin). `[1, 2]` and `[2, 1]` count as one.

**Scenario:** A charity accepts pledges only in a few fixed sizes, any number of each. How many different pledge mixes add up to exactly the campaign goal? Two pledges of 5 and one of 10 is the same mix however the pledges arrived.

**Ask first:**
1. Does the order of arrival matter, or only how many of each size?
2. Could the goal be 0 (the answer is then 1, the empty mix)? Is the answer modulo something?

**Spot it:** "How many mixes" with unlimited reuse, and order is explicitly ignored. That is why the coin index goes in the state, or coins form the outer loop.

**Model:**
- **State:** `dp(i, current_sum)` = ways to reach `amount` from `current_sum` using coins `i` onward.
- **Choices:** pick coin `i` (stay on `i`) or move to coin `i + 1`.
- **Recurrence:** `dp(i, s) = dp(i, s + coins[i]) + dp(i + 1, s)`.
- **Base:** `s == amount` → `1`; out of coins or `s > amount` → `0`.

**Solve:** ([08-coin-change-ii.md](03-knapsack-dp/08-coin-change-ii.md))
```python
# Top-down
def change(self, amount: int, coins: list[int]) -> int:
    memo = {}
    def dp(i, current_sum):
        if current_sum == amount: return 1
        if i >= len(coins) or current_sum > amount: return 0
        if (i, current_sum) in memo: return memo[(i, current_sum)]
        pick = dp(i, current_sum + coins[i])
        not_pick = dp(i + 1, current_sum)
        memo[(i, current_sum)] = pick + not_pick
        return memo[(i, current_sum)]
    return dp(0, 0)

# Bottom-up (coins outer; sums descending in this orientation)
def change(self, amount: int, coins: list[int]) -> int:
    dp = [0] * (amount + 1)
    dp[amount] = 1
    for c in coins:
        for s in range(amount - c, -1, -1):
            dp[s] += dp[s + c]
    return dp[0]
```
(Your other orientation counts remaining amount upward: `dp[0] = 1`, then `for coin in coins: for i in range(coin, amount + 1): dp[i] += dp[i - coin]`.)

**Cost:** States = `len(coins) × amount`. Work = O(1). Time O(amount × len(coins)). Space O(amount × len(coins)) memo, O(amount) array.
**Follow-up:** *Order should matter?* Swap the loops (target outer): that's LC 377, Variant A of #1. *Each coin once?* Switch to the 0/1 loop direction. *Big answers?* Use modulo. *Trap:* coins outer for combinations; the loop order is the whole difference.

**More scenarios on the same pattern**

**Variant A (crossover: grouped choices)**
- **Question:** LC 1155 Number of Dice Rolls With Target Sum. You have `n` dice, each with `k` faces numbered 1 to `k`. Return the number of ways the sum of the faces equals `target`, modulo 10^9 + 7.
- **Scenario:** A board game rolls `n` identical dice each showing 1 to `k`. How many different outcomes (dice are distinguishable) total exactly `T`?
- **Pattern and cost:** State `(dice left, sum)`; each die chooses one of `k` faces. This is a group knapsack: exactly one item from each group. O(n·T·k) time, O(T) space rolled by dice. With a prefix sum over the window it drops to O(n·T).

**Variant B (crossover to bounded supply)**
- **Question:** Same as Coin Change II, but coin `i` has only `cnt[i]` copies. Count the combinations.
- **Scenario:** A cashier has only so many bills of each size in the till. How many different bundles of bills make exactly the change owed?
- **Pattern and cost:** State `(i, sum)`, but now try `0..cnt[i]` copies of coin `i` and move on: `dp[i][s] = sum(dp[i+1][s - c*coin[i]] for c in 0..cnt[i])`. O(amount × Σ cnt) time, or O(amount × n) with a sliding window or binary splitting. The change from the unbounded version is "stay on `i`" becomes "move on after taking up to `cnt` copies".

---

### 9. Partition Equal Subset Sum (#9)

**Original question:** LC 416. Given an integer array `nums`, return `true` if it can be partitioned into two subsets with equal sums.

**Scenario:** Two warehouse crews must unload a truck of crates with known weights. Can the crates be shared out so that both crews carry exactly the same total weight?

**Ask first:**
1. Are weights positive integers? What is the largest total weight?
2. Does every crate have to go to one of the two crews?

**Spot it:** "Two equal halves" means one half must reach exactly `total / 2`. That turns it into "can some selection hit this exact number", where each crate is taken or left.

**Model:**
- **Reduce:** odd total → `False`. Otherwise `k = total // 2`.
- **State:** `dp(i, current_sum)` = can crates `i..` bring the running sum from `current_sum` to exactly `k`.
- **Choices:** take crate `i` or skip it. Each is used once, so both moves go to `i + 1`.
- **Recurrence:** `dp(i, s) = dp(i + 1, s + nums[i]) or dp(i + 1, s)`.
- **Base:** `s == k` → `True`; `s > k` or `i >= len(nums)` → `False`.

**Solve:** ([09-partition-equal-subset-sum.md](03-knapsack-dp/09-partition-equal-subset-sum.md))
```python
# Top-down
def canPartition(self, nums: list[int]) -> bool:
    total_sum = sum(nums)
    if total_sum % 2 != 0:
        return False
    memo = {}
    k = total_sum // 2
    def dp(i, current_sum):
        if current_sum == k: return True
        if current_sum > k or i >= len(nums): return False
        if (i, current_sum) in memo: return memo[(i, current_sum)]
        pick = dp(i + 1, current_sum + nums[i])
        not_pick = dp(i + 1, current_sum)
        memo[(i, current_sum)] = pick or not_pick
        return memo[(i, current_sum)]
    return dp(0, 0)

# Bottom-up (one array; numbers outer; sums ASCENDING so dp[s + num] is still the old value)
def canPartition(self, nums: list[int]) -> bool:
    total_sum = sum(nums)
    if total_sum % 2 != 0:
        return False
    k = total_sum // 2
    dp = [False] * (k + 1)
    dp[k] = True
    for num in nums:
        for s in range(0, k - num + 1):
            dp[s] = dp[s] or dp[s + num]
    return dp[0]
```

**Cost:** States = `n × k`. Work = O(1). Time O(n·k). Space O(n·k) memo, O(k) array. This is *pseudo-polynomial*: it depends on the size of the weights, not just on `n`.
**Follow-up:** *Which crates go to which crew?* Keep the full table and walk it. *Huge weights?* Then `k` is too big; meet-in-the-middle (`2^(n/2)`) or a bitset (`bits |= bits << num`) are the usual answers. *Three crews?* See Variant B. *Trap:* the inner loop direction. Ascending here (this array indexes the sum so far); with the other orientation (sum still needed) it is descending. If you get it wrong, one crate is used twice.

**More scenarios on the same pattern**

**Variant A (crossover: from "exactly half" to "closest to half")**
- **Question:** LC 1049 Last Stone Weight II. Stones are smashed in pairs; the final stone has weight `|x - y|` repeatedly. Return the smallest possible weight left. (It reduces to splitting the stones into two groups with the smallest weight difference.)
- **Scenario:** The same two crews, but an even split is not always possible. How small can the difference between their loads be made?
- **Pattern and cost:** Compute every reachable subset sum up to `total / 2` (the same table as #9), take the largest reachable `s`, and answer `total - 2s`. O(n·total) time, O(total) space.

**Variant B (crossover to bitmask DP)**
- **Question:** LC 698 Partition to K Equal Sum Subsets. Return `true` if `nums` can be divided into `k` non-empty subsets of equal sum.
- **Scenario:** Instead of two crews there are `k` crews (and at most 16 crates). Can everyone carry exactly the same weight?
- **Pattern and cost:** One `k`-way split is too big for a simple `(i, sum)` state. Use a **bitmask** of used crates: `dp[mask]` = the partial load of the crew currently being filled (or `-1` if unreachable). O(2^n · n) time, O(2^n) space. This is where the knapsack idea stops working and the state becomes "which items are used".

---

### 10. Target Sum (#10)

**Original question:** LC 494. Given `nums` and a `target`, build expressions by placing `+` or `-` before every number. Return the number of expressions that evaluate to `target`.

**Scenario:** An accountant has a list of `n` adjustments. Each one must be booked as either a credit or a debit. In how many different ways can they be booked so that the final balance is exactly `T`?

**Ask first:**
1. Can the numbers be zero? (each zero doubles the count)
2. How large can the sum of the numbers be?

**Spot it:** A binary choice for every item, and only the final running total matters. Many different choice histories reach the same (item, total) pair.

**Model:**
- **State:** `dp(i, current_sum)` = ways to sign `nums[i:]` so the final total is `target`, starting from `current_sum`.
- **Choices:** `+nums[i]` or `-nums[i]`.
- **Recurrence:** `dp(i, s) = dp(i + 1, s + nums[i]) + dp(i + 1, s - nums[i])`.
- **Base:** `i == len(nums)` → `1` if `current_sum == target` else `0`. No pruning, because the sum may go negative and zeros must be counted.

**Solve:** ([10-target-sum.md](03-knapsack-dp/10-target-sum.md))
```python
# Top-down
def findTargetSumWays(self, nums: list[int], target: int) -> int:
    memo = {}
    def dp(i, current_sum):
        if i == len(nums):
            return 1 if current_sum == target else 0
        if (i, current_sum) in memo: return memo[(i, current_sum)]
        add = dp(i + 1, current_sum + nums[i])
        substract = dp(i + 1, current_sum - nums[i])
        memo[(i, current_sum)] = add + substract
        return memo[(i, current_sum)]
    return dp(0, 0)

# Bottom-up via the subset-sum reduction: sum(P) = (target + total) / 2
def findTargetSumWays(self, nums: list[int], target: int) -> int:
    total_sum = sum(nums)
    if abs(target) > total_sum or (target + total_sum) % 2 != 0:
        return 0
    p_target = (target + total_sum) // 2
    dp = [0] * (p_target + 1)
    dp[0] = 1
    for num in nums:
        for j in range(p_target, num - 1, -1):
            dp[j] += dp[j - num]
    return dp[p_target]
```
(The write-up also has the two-row table over sums `-total..total` with an `offset`.)

**Cost:** States = `n × (2S + 1)` where `S = sum(nums)`. Work = O(1). Time O(n·S). Space O(n·S) memo; the reduction gives O(P), `P = (target + S) / 2`.
**Follow-up:** *Space?* The reduction to a single array. *Why the parity check?* `sum(P) = (target + total)/2` must be an integer. *Zeros?* Each zero doubles the count; this falls out of the DP, but a `dp[0] = 1` special case is a common bug. *Which expressions?* That is backtracking (Variant B).

**More scenarios on the same pattern**

**Variant A (crossover: two capacities)**
- **Question:** LC 474 Ones and Zeroes. Given binary strings and integers `m` and `n`, return the size of the largest subset of strings having at most `m` zeros and `n` ones in total.
- **Scenario:** A rocket can carry at most `m` kg of fuel and `n` kg of oxygen. Each of several mission packages needs a known amount of each. How many packages can be shipped at most?
- **Pattern and cost:** 0/1 knapsack with **two** capacities: `dp[a][b] = max(dp[a][b], 1 + dp[a - zeros][b - ones])`, looping `a`, `b` downward per package. O(L·m·n) time, O(m·n) space.

**Variant B (crossover to backtracking)**
- **Question:** LC 282 Expression Add Operators. Given a digit string and a `target`, insert `+`, `-` or `*` between digits (or nothing) so the expression evaluates to `target`. Return **all** expressions.
- **Scenario:** A calculator toy gets a string of digits and a goal value. List every way to place plus, minus and times signs between the digits so that it works out to the goal.
- **Pattern and cost:** You need every expression, and `*` makes the value depend on the previous term, so the summary state is awkward. Use **backtracking** carrying `(value so far, last term)`. O(4^n) time. A good example of "the output is the whole path, so DP cannot compress it".

---

### 11. Maximum Product Subarray (#11)

**Original question:** LC 152. Given an integer array `nums`, find a contiguous non-empty subarray with the largest product, and return the product.

**Scenario:** A signal passes through a chain of stages. Each stage multiplies the strength by a factor that may be negative (phase flip), zero (dead stage) or a fraction. Pick one continuous run of stages to get the largest overall gain.

**Ask first:**
1. Can the factors be zero or negative? Fractions or only integers?
2. Is the run required to be non-empty? Could the answer overflow?

**Spot it:** "Best continuous run" like a sum problem, but the sign can flip. So the best run ending here might come from the **worst** run ending at the previous position.

**Model:**
- **State:** `cur_max`, `cur_min` = largest and smallest product of a run ending at `i`.
- **Choices:** extend the previous run, or start fresh at `i`.
- **Recurrence:** `cur_max = max(x, cur_max·x, cur_min·x)`, `cur_min = min(x, cur_max·x, cur_min·x)` (using the old values).
- **Base:** reset at a zero. Track the best `cur_max`.

**Solve:** ([11-maximum-product-subarray.md](04-subarray-subsequence-tracking/11-maximum-product-subarray.md))
```python
# Primary: prefix / suffix scan (no memo needed)
def maxProduct(self, nums: list[int]) -> int:
    pre = 1
    suff = 1
    max_product = float('-inf')
    n = len(nums)
    for i in range(n):
        if pre == 0: pre = 1
        if suff == 0: suff = 1
        pre *= nums[i]
        suff *= nums[n - 1 - i]
        max_product = max(max_product, pre, suff)
    return max_product

# DP view: running min and max
def maxProduct(self, nums: list[int]) -> int:
    res = max(nums)
    cur_min, cur_max = 1, 1
    for n in nums:
        if n == 0:
            cur_min, cur_max = 1, 1
            continue
        tmp = cur_max * n
        cur_max = max(n * cur_max, n * cur_min, n)
        cur_min = min(tmp, n * cur_min, n)
        res = max(res, cur_max)
    return res
```

**Cost:** States = `n` (two numbers each). Work = O(1). Time O(n), space O(1).
**Follow-up:** *Why both max and min?* A negative flips them. *Return the subarray?* Remember start indexes. *Trap:* save `cur_max * n` in a temp before overwriting `cur_max`; reset on zero; initialise the answer to `max(nums)`, not 0 (a single negative number).

**More scenarios on the same pattern**

**Variant A (crossover to Kadane's sum)**
- **Question:** LC 53 Maximum Subarray. Return the largest sum of a contiguous non-empty subarray.
- **Scenario:** A shop has the net cash flow for each day of the quarter. Which continuous stretch of days made the most money in total?
- **Pattern and cost:** With sums there is no sign flip, so one variable is enough: `cur = max(x, cur + x)`. O(n) time, O(1) space. Product needs a min as well; sum does not.

**Variant B (same two-variable idea, different quantity)**
- **Question:** LC 1567 Maximum Length of Subarray With Positive Product. Return the length of the longest subarray whose product is positive.
- **Scenario:** The same chain of stages. What is the longest continuous run whose overall effect is a positive gain, not zero and not inverted?
- **Pattern and cost:** Track `pos` = longest run ending here with positive product and `neg` = with negative product. A negative number swaps them; a zero resets both. O(n) time, O(1) space.

---

### 12. Longest Increasing Subsequence (#12)

**Original question:** LC 300. Given an integer array `nums`, return the length of the longest strictly increasing subsequence.

**Scenario:** A fitness app wants the longest "improvement streak" a user could claim. They may choose any days, in order, as long as each chosen day has a strictly higher step count than the previous chosen day. Days in between are ignored.

**Ask first:**
1. Strictly higher, or equal allowed too?
2. Only the length, or the actual days? How many days can there be (`n` = 10^5 needs `O(n log n)`)?

**Spot it:** "Longest chain where each pick must beat the last pick, with gaps allowed". The only thing the future needs from the past is **the last value kept**.

**Model:**
- **State (memo):** `dp(idx, prev_idx)` = best length from `nums[idx:]` given the last kept index (`-1` = none).
- **State (table):** `dp[i]` = length of the longest chain **ending at** `i`.
- **Choices:** skip `nums[idx]`, or take it (only if it beats `nums[prev_idx]`).
- **Recurrence:** `dp(idx, prev) = max(dp(idx + 1, prev), 1 + dp(idx + 1, idx))`; table: `dp[i] = max(dp[j] + 1 for j < i if nums[j] < nums[i])`.
- **Base:** `dp(len(nums), ·) = 0`; table starts at `[1] * n`; answer is `max(dp)`.

**Solve:** ([12-longest-increasing-subsequence.md](04-subarray-subsequence-tracking/12-longest-increasing-subsequence.md))
```python
# Top-down
def lengthOfLIS(self, nums: list[int]) -> int:
    memo = {}
    def dp(idx, prev_idx):
        if idx == len(nums): return 0
        if (idx, prev_idx) in memo: return memo[(idx, prev_idx)]
        skip = dp(idx + 1, prev_idx)
        take = 0
        if prev_idx == -1 or nums[idx] > nums[prev_idx]:
            take = 1 + dp(idx + 1, idx)
        memo[(idx, prev_idx)] = max(skip, take)
        return memo[(idx, prev_idx)]
    return dp(0, -1)

# Bottom-up (smaller state: best ending at i)
def lengthOfLIS(self, nums: list[int]) -> int:
    n = len(nums)
    dp = [1] * n
    for i in range(n):
        for j in range(i):
            if nums[j] < nums[i]:
                dp[i] = max(dp[i], dp[j] + 1)
    return max(dp)

# O(n log n): patience sorting
import bisect
def lengthOfLIS(self, nums: list[int]) -> int:
    sub = []
    for x in nums:
        idx = bisect.bisect_left(sub, x)
        if idx == len(sub): sub.append(x)
        else: sub[idx] = x
    return len(sub)
```

**Cost:** Memo: `n²/2` states, O(1) each, so O(n²) time and space. Table: `n` states, O(n) each, so O(n²) time, O(n) space. Patience: O(n log n) time, O(n) space.
**Follow-up:** *Faster?* Patience sorting. `sub` is not the answer sequence, only its length counts. *Print one?* Store parent pointers in the table version. *Non-decreasing?* Use `bisect_right`. *Count how many LIS?* Add a `count[i]` array (LC 673). *Trap:* the table answer is `max(dp)`, not `dp[-1]`.

**More scenarios on the same pattern**

**Variant A (crossover: two dimensions down to one)**
- **Question:** LC 354 Russian Doll Envelopes. Envelopes have `(width, height)`. One fits inside another only if both dimensions are strictly smaller. Return the maximum number that can be nested.
- **Scenario:** A packaging team has boxes with a width and a height. A box can go inside another only if it is strictly smaller in both. What is the longest nesting chain?
- **Pattern and cost:** Sort by width ascending and, for equal widths, height **descending** (so equal widths can't chain), then take the LIS of the heights. O(n log n) time, O(n) space. The tie-break is the whole trick.

**Variant B (crossover to greedy)**
- **Question:** LC 646 Maximum Length of Pair Chain. Given pairs `[left, right]`, a pair `p2` can follow `p1` if `p1.right < p2.left`. Return the length of the longest chain.
- **Scenario:** A room-booking system has requests with start and end times. What is the largest number of requests it can accept so that each starts strictly after the previous one ends?
- **Pattern and cost:** An `O(n²)` LIS-style DP works, but **sort by end time and take greedily** is O(n log n). It is the classic unweighted interval scheduling. If requests had different values, it would be DP again (weighted scheduling).

---

### 13. Unique Paths (#13)

**Original question:** LC 62. A robot is on the top-left of an `m × n` grid and can only move right or down. Return the number of unique paths to the bottom-right corner.

**Scenario:** A warehouse robot starts at the north-west dock of an `m` by `n` floor and must reach the south-east dock, moving only east or south one tile at a time. How many different routes are there?

**Ask first:**
1. Are any tiles blocked? Can the robot ever move west or north?
2. How large can `m` and `n` be (overflow, and is a closed formula allowed)?

**Spot it:** "How many routes" where each tile is entered from exactly two tiles. The number of routes into a tile is the sum of the routes into those two.

**Model:**
- **State:** `dp(r, c)` = number of paths from `(0, 0)` to `(r, c)`.
- **Choices:** the last move came from above or from the left.
- **Recurrence:** `dp(r, c) = dp(r - 1, c) + dp(r, c - 1)`.
- **Base:** top row or left column → `1`.

**Solve:** ([13-unique-paths.md](05-grid-path-dp/13-unique-paths.md))
```python
# Top-down
def uniquePaths(self, m: int, n: int) -> int:
    memo = {}
    def dp(r: int, c: int) -> int:
        if r == 0 or c == 0: return 1
        if (r, c) in memo: return memo[(r, c)]
        memo[(r, c)] = dp(r - 1, c) + dp(r, c - 1)
        return memo[(r, c)]
    return dp(m - 1, n - 1)

# Bottom-up (full table, then one row)
def uniquePaths(self, m: int, n: int) -> int:
    dp = [[0] * n for _ in range(m)]
    for r in range(m): dp[r][0] = 1
    for c in range(n): dp[0][c] = 1
    for r in range(1, m):
        for c in range(1, n):
            dp[r][c] = dp[r - 1][c] + dp[r][c - 1]
    return dp[m - 1][n - 1]

def uniquePaths(self, m: int, n: int) -> int:        # O(n) space
    row = [1] * n
    for r in range(1, m):
        new_row = [1] * n
        for c in range(1, n):
            new_row[c] = new_row[c - 1] + row[c]
        row = new_row
    return row[-1]
```
Closed form: `math.comb(m + n - 2, m - 1)` (choose which of the `m + n - 2` moves are "down").

**Cost:** States = `m × n`. Work = one addition. Time O(m·n). Space O(m·n) memo, O(n) one row, O(min(m, n)) for the formula.
**Follow-up:** *Blocked tiles?* #14. *Cheapest instead of count?* #15. *Space?* One row. *Count of routes through a required waypoint?* Multiply two counts. *Trap:* the base case is the whole first row **and** column; with obstacles that stops being true.

**More scenarios on the same pattern**

**Variant A (crossover to backtracking: the whole path matters)**
- **Question:** LC 980 Unique Paths III. A grid has a start, an end, empty squares and obstacles. Return the number of 4-directional walks from start to end that visit **every** empty square exactly once.
- **Scenario:** A cleaning robot must start at the charging dock, cover every free tile exactly once, and finish at the exit. How many routes can it take?
- **Pattern and cost:** The robot can go in all directions and the future depends on **which tiles are used already**, so the "small summary" is gone. Use **backtracking** (or bitmask DP when there are at most ~20 free tiles). O(3^(free tiles)) time. DP's cheap `(r, c)` state no longer works.

**Variant B (crossover: reverse the direction)**
- **Question:** LC 174 Dungeon Game. A knight moves right or down through a grid of rooms with health changes (negative = damage). Return the minimum initial health needed so that health never drops to 0 or below.
- **Scenario:** A courier crosses a city map moving only east or south. Each block adds or deducts money from a balance that must never fall below 1. What is the smallest starting balance that makes the trip possible?
- **Pattern and cost:** A forward DP fails (cheapest-so-far is not enough; you need the *remaining* requirement). Compute **backwards** from the destination: `need[r][c] = max(1, min(need[r+1][c], need[r][c+1]) - cell)`. O(m·n) time, O(n) space. The skill: choosing the direction of the recurrence.

---

### 14. Unique Paths II (#14)

**Original question:** LC 63. Same robot as #13, but the grid has obstacles (`1`) and empty cells (`0`). Return the number of unique paths from the top-left to the bottom-right avoiding obstacles.

**Scenario:** The same warehouse, but some tiles are occupied by pallets that cannot be crossed. How many routes from the north-west dock to the south-east dock now?

**Ask first:**
1. Can the starting or finishing tile itself be blocked? (then the answer is 0)
2. Is the pallet layout known in advance, or does it change?

**Spot it:** Same counting idea, but an unreachable tile just contributes **zero** to everything that depends on it.

**Model:**
- **State:** `dp(r, c)` = paths from `(0, 0)` to `(r, c)`; a blocked cell has 0.
- **Choices:** from above or from the left.
- **Recurrence:** `dp(r, c) = dp(r - 1, c) + dp(r, c - 1)` for open cells.
- **Base:** off-grid or obstacle → `0` (check this **before** the start check); `(0, 0)` → `1`.

**Solve:** ([14-unique-paths-ii.md](05-grid-path-dp/14-unique-paths-ii.md))
```python
# Top-down
def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
    m, n = len(obstacleGrid), len(obstacleGrid[0])
    memo = {}
    def dp(r: int, c: int) -> int:
        if r < 0 or c < 0 or obstacleGrid[r][c] == 1: return 0
        if r == 0 and c == 0: return 1
        if (r, c) in memo: return memo[(r, c)]
        memo[(r, c)] = dp(r - 1, c) + dp(r, c - 1)
        return memo[(r, c)]
    return dp(m - 1, n - 1)

# Bottom-up, one row
def uniquePathsWithObstacles(self, obstacleGrid: list[list[int]]) -> int:
    m, n = len(obstacleGrid), len(obstacleGrid[0])
    dp = [0] * n
    dp[0] = 1 if obstacleGrid[0][0] == 0 else 0
    for r in range(m):
        for c in range(n):
            if obstacleGrid[r][c] == 1:
                dp[c] = 0
            elif c > 0:
                dp[c] += dp[c - 1]
    return dp[-1]
```

**Cost:** States = `m × n`. Work = O(1). Time O(m·n). Space O(m·n) memo, O(n) one row.
**Follow-up:** *Count modulo?* Add it. *Pallets that can be removed (up to `k`)?* Add a dimension (see Variant B). *Trap:* don't set the first row and column to 1; an obstacle blocks everything after it in that row or column.

**More scenarios on the same pattern**

**Variant A (three predecessors, any start column)**
- **Question:** LC 931 Minimum Falling Path Sum. For an `n × n` matrix, a falling path starts at any element of the first row and moves to the next row, to a column differing by at most 1. Return the minimum sum.
- **Scenario:** A marble is dropped into any slot at the top of a pegboard. At each row it rolls straight down or one slot left or right, paying that peg's penalty. What is the lowest total penalty reaching the bottom?
- **Pattern and cost:** `dp[r][c] = m[r][c] + min(dp[r-1][c-1], dp[r-1][c], dp[r-1][c+1])`. The answer is the minimum over the last row, not one corner. O(n²) time, O(n) space.

**Variant B (crossover to BFS)**
- **Question:** LC 1293 Shortest Path in a Grid with Obstacles Elimination. Move in 4 directions on a grid of 0s and 1s, and you may remove at most `k` obstacles. Return the minimum number of steps from the top-left to the bottom-right, or `-1`.
- **Scenario:** A drone flies across a floor plan in any direction, one tile per move, and may break through up to `k` walls. What is the fewest moves to the far corner?
- **Pattern and cost:** All four directions means cycles, and every move costs 1, so it is a **BFS over `(r, c, walls_left)`**: O(m·n·k) time and space. A row-by-row DP cannot be used because there is no fixed order. Same "tile + extra counter" idea, different tool.

---

### 15. Minimum Path Sum (#15)

**Original question:** LC 64. Given an `m × n` grid of non-negative numbers, find a path from top-left to bottom-right (moving only right or down) that minimises the sum of the numbers along it.

**Scenario:** A hiker crosses a rectangular trail map from the north-west trailhead to the south-east lodge, always heading east or south. Each square has an energy cost. What is the least total energy for the trip?

**Ask first:**
1. Can costs be negative or zero? Is it only east/south, or can the hiker backtrack?
2. Do you want just the cost, or the route?

**Spot it:** "Cheapest way to the corner" with only two entry directions. The cheapest way into a square is the cheaper of two earlier answers plus the square's own cost.

**Model:**
- **State:** `dp(r, c)` = minimum path sum from `(0, 0)` to `(r, c)`, including `grid[r][c]`.
- **Choices:** arrive from above or from the left.
- **Recurrence:** `dp(r, c) = grid[r][c] + min(dp(r - 1, c), dp(r, c - 1))`.
- **Base:** `dp(0, 0) = grid[0][0]`; off-grid → `inf`.

**Solve:** ([15-minimum-path-sum.md](05-grid-path-dp/15-minimum-path-sum.md))
```python
# Top-down
def minPathSum(self, grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    memo = {}
    def dp(r: int, c: int) -> int:
        if r == 0 and c == 0: return grid[0][0]
        if r < 0 or c < 0: return float('inf')
        if (r, c) in memo: return memo[(r, c)]
        memo[(r, c)] = grid[r][c] + min(dp(r - 1, c), dp(r, c - 1))
        return memo[(r, c)]
    return dp(m - 1, n - 1)

# Bottom-up, one row (inf seed makes the first row and column fall out of the same formula)
def minPathSum(self, grid: list[list[int]]) -> int:
    m, n = len(grid), len(grid[0])
    dp = [float('inf')] * n
    dp[0] = 0
    for r in range(m):
        for c in range(n):
            if c == 0:
                dp[c] += grid[r][c]
            else:
                dp[c] = grid[r][c] + min(dp[c], dp[c - 1])
    return dp[-1]
```

**Cost:** States = `m × n`. Work = one `min`. Time O(m·n). Space O(m·n) memo, O(n) one row, O(1) if you may overwrite the input.
**Follow-up:** *Print the route?* Keep the table and walk back choosing the smaller predecessor. *Any direction allowed?* Variant A. *Greedy trap:* "always step to the cheaper next square" fails: a cheap square can lead into an expensive region.

**More scenarios on the same pattern**

**Variant A (crossover to Dijkstra)**
- **Question:** LC 1631 Path With Minimum Effort. Move in 4 directions; the effort of a path is the maximum absolute height difference between consecutive cells. Return the minimum effort from top-left to bottom-right.
- **Scenario:** A hiker may walk in any direction on a height map. The strain of a route is its single steepest step. Find the route with the gentlest steepest step.
- **Pattern and cost:** Moves go back and forth, so there is no sweep order. This is **Dijkstra with `max`** (or binary search on the answer plus BFS). O(m·n log(m·n)) time, O(m·n) space. Compare with #15: moves only go forward, so a plain sweep is enough.

**Variant B (crossover: two walkers at once)**
- **Question:** LC 741 Cherry Pickup. Walk from `(0, 0)` to `(n-1, n-1)` moving right or down, then back to `(0, 0)` moving left or up, collecting cherries (each picked once). Return the maximum cherries.
- **Scenario:** Two couriers leave the north-west depot together, both head east or south to the south-east depot, and each parcel on a tile can only be collected once. What is the most parcels the pair can collect?
- **Pattern and cost:** A round trip equals two walkers moving down/right simultaneously. State `(step, r1, r2)` (their columns are `step - r`). O(n³) time, O(n²) rolling. Taking the single best forward path first and then the best return path is a **greedy trap** and gives the wrong answer.

---

### 16. Triangle (#16)

**Original question:** LC 120. Given a triangle array, return the minimum path sum from top to bottom. At each step you may move to an adjacent number on the row below (index `i` or `i + 1`).

**Scenario:** A tower has 1 room on the top floor, 2 on the next, 3 on the next, and so on. From a room a guest can walk down to the room directly below or the one below and to the right. Each room has an entry fee. What is the cheapest descent to the ground floor?

**Ask first:**
1. Can fees be negative? Can I modify the input to save memory?
2. How many floors, and do you want only the cost or also the route?

**Spot it:** Same "cheapest way to the end" idea, but the shape is a triangle. Two different rooms above share a room below, so work is shared.

**Model:**
- **State:** `dp(r, c)` = min path sum from `(r, c)` down to the bottom row (a "finish from here" state).
- **Choices:** go to `(r + 1, c)` or `(r + 1, c + 1)`.
- **Recurrence:** `dp(r, c) = triangle[r][c] + min(dp(r + 1, c), dp(r + 1, c + 1))`.
- **Base:** last row → the cell itself.

**Solve:** ([16-triangle.md](05-grid-path-dp/16-triangle.md))
```python
# Top-down
def minimumTotal(self, triangle: list[list[int]]) -> int:
    n = len(triangle)
    memo = {}
    def dp(r: int, c: int) -> int:
        if r == n - 1: return triangle[r][c]
        if (r, c) in memo: return memo[(r, c)]
        down = dp(r + 1, c)
        diag = dp(r + 1, c + 1)
        memo[(r, c)] = triangle[r][c] + min(down, diag)
        return memo[(r, c)]
    return dp(0, 0)

# Bottom-up (start from the bottom row, go up; one row)
def minimumTotal(self, triangle: list[list[int]]) -> int:
    dp = triangle[-1][:]
    for r in range(len(triangle) - 2, -1, -1):
        for c in range(r + 1):
            dp[c] = triangle[r][c] + min(dp[c], dp[c + 1])
    return dp[0]
```

**Cost:** States = `n(n+1)/2 ≈ n²/2`. Work = one `min`. Time O(n²). Space O(n²) memo, O(n) one row (the number of floors, not the number of rooms).
**Follow-up:** *Why bottom-up?* No boundary checks and the answer sits in `dp[0]`. *O(1) extra?* Overwrite the input. *Route?* Keep the table and trace it. *Trap:* in-place update is safe only because `c` ascends (`dp[c + 1]` is still the row below).

**More scenarios on the same pattern**

**Variant A (counting instead of min)**
- **Question:** LC 119 Pascal's Triangle II. Return row `k` of Pascal's triangle, where each number is the sum of the two numbers directly above it. Use `O(k)` extra space.
- **Scenario:** In the same tower, visitors enter at the top and at each floor split evenly into the two rooms below. How many distinct routes lead to each room on floor `k`?
- **Pattern and cost:** Counting version of #16. Update one row from right to left so you don't overwrite what you still need. O(k²) time, O(k) space. (Closed form: binomial coefficients.)

**Variant B (crossover: transition from every column)**
- **Question:** LC 1937 Maximum Number of Points with Cost. In each row you pick one cell for points; moving from column `c1` to `c2` between rows costs `|c1 - c2|`. Return the maximum points.
- **Scenario:** In a game board, you choose one square per row to score, but each time you change column between rows you lose points equal to the distance moved. What is the best total?
- **Pattern and cost:** `dp[r][c] = pts[r][c] + max over c' of (dp[r-1][c'] - |c - c'|)`. Naive is O(m·n²). Precompute left-to-right and right-to-left running maxima, so each cell is O(1): O(m·n) time, O(n) space. The skill: speeding up a "from any column" transition.

---

### 17. Maximal Square (#17)

**Original question:** LC 221. Given an `m × n` binary matrix of `'0'` and `'1'`, find the largest square containing only `'1'`s and return its **area**.

**Scenario:** A solar installer has a roof map where each tile is either usable or shaded. What is the area of the largest square array of panels that fits entirely on usable tiles?

**Ask first:**
1. Square only, or any rectangle? Return the side or the area?
2. Is the map stored as characters or numbers, and can I overwrite it?

**Spot it:** "Biggest block of good cells ending at this cell is limited by the blocks ending at the neighbouring cells." Every cell could be the bottom-right corner, so the answer is a max over all cells.

**Model:**
- **State:** `dp(r, c)` = side of the largest all-`1` square whose bottom-right corner is `(r, c)`.
- **Choices:** none; it is decided by the three neighbouring squares (left, up, up-left).
- **Recurrence:** `dp(r, c) = 1 + min(dp(r, c-1), dp(r-1, c), dp(r-1, c-1))` for a `'1'`, else `0`.
- **Base:** off-grid or `'0'` → `0`. Answer: `max_side * max_side`, with `max_side` the max over all cells.

**Solve:** ([17-maximal-square.md](05-grid-path-dp/17-maximal-square.md))
```python
# Top-down
def maximalSquare(self, matrix: list[list[str]]) -> int:
    m = len(matrix)
    n = len(matrix[0])
    max_side = 0
    memo = {}
    def dp(r, c):
        nonlocal max_side
        if r < 0 or c < 0 or matrix[r][c] == '0': return 0
        if (r, c) in memo: return memo[(r, c)]
        left = dp(r, c - 1)
        up = dp(r - 1, c)
        vertical = dp(r - 1, c - 1)
        memo[(r, c)] = 1 + min(left, up, vertical)
        max_side = max(max_side, memo[(r, c)])
        return memo[(r, c)]
    for i in range(m):
        for j in range(n):
            dp(i, j)
    return max_side * max_side

# Bottom-up, one row (temp keeps the old dp[c] so it can become the next cell's diagonal)
def maximalSquare(self, matrix: list[list[str]]) -> int:
    m, n = len(matrix), len(matrix[0])
    dp = [0] * (n + 1)
    max_side = 0
    for r in range(1, m + 1):
        prev_diag = 0
        for c in range(1, n + 1):
            temp = dp[c]
            if matrix[r - 1][c - 1] == '1':
                dp[c] = 1 + min(dp[c], dp[c - 1], prev_diag)
                max_side = max(max_side, dp[c])
            else:
                dp[c] = 0
            prev_diag = temp
    return max_side * max_side
```

**Cost:** States = `m × n`. Work = one `min` of three. Time O(m·n). Space O(m·n) memo and stack, O(n) one row.
**Follow-up:** *Space?* One row plus the saved diagonal. *Position of the square?* Record the corner when the max updates. *Rectangles?* Variant A. *Trap:* return the **area** (`side²`), and ask for every cell, not only the last.

**More scenarios on the same pattern**

**Variant A (crossover to a monotonic stack)**
- **Question:** LC 85 Maximal Rectangle. Given a binary matrix, find the largest rectangle containing only `1`s and return its area.
- **Scenario:** The same roof, but the installer can use a panel array of any rectangular shape. What is the largest area?
- **Pattern and cost:** The "min of three neighbours" rule does not work for rectangles. Treat each row as a **histogram** of consecutive `1`s above it and find the largest rectangle in the histogram with a monotonic stack. O(m·n) time, O(n) space. It shows where the square DP stops.

**Variant B (same recurrence, different answer)**
- **Question:** LC 1277 Count Square Submatrices with All Ones. Return the number of square submatrices that have all ones.
- **Scenario:** For the same roof, the installer wants to know how many different square patches of usable tiles exist, of every size and position.
- **Pattern and cost:** Same `dp[r][c]`. A cell with value `k` is the corner of exactly `k` squares (sizes 1 to `k`), so the answer is the **sum** of all cells, not the max. O(m·n) time, O(n) space.

---

### 18. Longest Increasing Path in a Matrix (#18)

**Original question:** LC 329. Given an `m × n` integer matrix, return the length of the longest strictly increasing path. From each cell you can move in 4 directions, not diagonally or outside the grid.

**Scenario:** A delivery drone flies over a terrain-height map. From any tile it can move to the tile directly north, south, east or west, but only if the ground there is strictly higher. Starting anywhere, how long can its longest flight be?

**Ask first:**
1. Strictly higher, or equal heights allowed too?
2. Can the drone start anywhere? How large can the map be (recursion depth)?

**Spot it:** Moves go in all directions, but "strictly higher" means you can **never come back**. So there are no cycles, and each tile's best flight from it is 1 plus the best of its higher neighbours.

**Model:**
- **State:** `dfs(r, c)` = length of the longest increasing path **starting** at `(r, c)`.
- **Choices:** which strictly larger neighbour to step to (up to 4).
- **Recurrence:** `dfs(r, c) = 1 + max(dfs(nr, nc) for larger neighbours)`, or `1` if none.
- **Base:** no larger neighbour → `1`. No visited set needed. Answer: max over all cells.

**Solve:** ([18-longest-increasing-path-in-a-matrix.md](06-memoized-dfs-on-grid/18-longest-increasing-path-in-a-matrix.md))
```python
# Top-down memoised DFS
def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
    if not matrix or not matrix[0]: return 0
    m, n = len(matrix), len(matrix[0])
    memo = {}
    max_path = 0
    def dfs(r, c):
        nonlocal max_path
        if (r, c) in memo: return memo[(r, c)]
        val = matrix[r][c]
        up = dfs(r - 1, c) if r - 1 >= 0 and matrix[r - 1][c] > val else 0
        down = dfs(r + 1, c) if r + 1 < m and matrix[r + 1][c] > val else 0
        left = dfs(r, c - 1) if c - 1 >= 0 and matrix[r][c - 1] > val else 0
        right = dfs(r, c + 1) if c + 1 < n and matrix[r][c + 1] > val else 0
        memo[(r, c)] = 1 + max(up, down, left, right)
        max_path = max(max_path, memo[(r, c)])
        return memo[(r, c)]
    for i in range(m):
        for j in range(n):
            dfs(i, j)
    return max_path

# Bottom-up: process cells from the largest value to the smallest
def longestIncreasingPath(self, matrix: list[list[int]]) -> int:
    rows, cols = len(matrix), len(matrix[0])
    dp = [[1] * cols for _ in range(rows)]
    cells = sorted(((matrix[r][c], r, c) for r in range(rows) for c in range(cols)), reverse=True)
    for _, r, c in cells:
        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and matrix[nr][nc] > matrix[r][c]:
                dp[r][c] = max(dp[r][c], 1 + dp[nr][nc])
    return max(max(row) for row in dp)
```

**Cost:** States = `m × n`. Work = 4 neighbour checks, O(1). Time O(m·n) (O(m·n log(m·n)) for the sorted table). Space O(m·n); the recursion can be `m·n` deep on a snake-shaped map, so raise Python's recursion limit or use the sorted table or Kahn's topological sort.
**Follow-up:** *No recursion?* Sort by value, or Kahn (peel cells with no smaller neighbour; the number of layers is the answer). *Why no visited set?* Strict increase makes cycles impossible. *Trap:* with `>=` (equal allowed) cycles appear and this memo breaks.

**More scenarios on the same pattern**

**Variant A (crossover: cycles are fine because a counter is added)**
- **Question:** LC 576 Out of Boundary Paths. A ball starts at `(startRow, startColumn)` on an `m × n` grid and can be moved up, down, left or right, at most `maxMove` times. Return the number of paths that take it out of the grid, modulo 10^9 + 7.
- **Scenario:** A drone sits on a field and makes at most `N` one-tile moves in any compass direction. In how many different ways can it fly off the edge of the field?
- **Pattern and cost:** Moves can return to the same tile, but the remaining-moves counter strictly decreases, so `(r, c, moves_left)` forms a DAG. O(N·m·n) time, O(m·n) space rolled by move. The extra dimension replaces the "strictly higher" rule.

**Variant B (max becomes a sum)**
- **Question:** LC 2328 Number of Increasing Paths in a Grid. Return the number of strictly increasing paths (of any length, starting and ending anywhere) in the grid, modulo 10^9 + 7.
- **Scenario:** For the same terrain map, how many different uphill flights exist in total, counting every start and every length?
- **Pattern and cost:** Same DAG memo: `dfs(r, c) = 1 + sum(dfs(larger neighbour))`; the answer is the sum over all cells. O(m·n) time and space. Only `max` became `+`, the structure is identical.

---

### 19. Longest Palindromic Substring (#19)

**Original question:** LC 5. Given a string `s`, return the longest palindromic substring (reads the same forwards and backwards).

**Scenario:** A text editor wants to highlight the longest stretch of a document that reads the same forwards and backwards.

**Ask first:**
1. If there is a tie, which one do I return? Is the comparison case- or punctuation-sensitive?
2. How long can the text be (`n²` fine, or need `O(n)`)?

**Spot it:** A mirror-symmetric stretch is symmetric around a **centre**, and a longer one is a shorter one with matching ends. So the facts about a stretch come from the stretch just inside it.

**Model:**
- **State (centres):** a centre (a letter, or the gap between two letters): `2n - 1` of them.
- **State (table):** `is_pal(i, j)` = is `s[i..j]` a palindrome.
- **Choices:** expand one step outward while the two ends match.
- **Recurrence:** `is_pal(i, j) = s[i] == s[j] and is_pal(i + 1, j - 1)`.
- **Base:** `i >= j` → `True` (empty or single letter).

**Solve:** ([19-longest-palindromic-substring.md](07-palindrome-dp/19-longest-palindromic-substring.md))
```python
# Primary: expand around centres, O(1) extra space
def longestPalindrome(self, s: str) -> str:
    res_len = 0
    res = ""
    def expand(left, right):
        while left >= 0 and right < len(s) and s[left] == s[right]:
            left -= 1
            right += 1
        return s[left + 1:right]
    for i in range(len(s)):
        p1 = expand(i, i)
        if len(p1) > res_len:
            res_len = len(p1)
            res = p1
        p2 = expand(i, i + 1)
        if len(p2) > res_len:
            res_len = len(p2)
            res = p2
    return res

# DP view: top-down memo
def longestPalindrome(self, s: str) -> str:
    n = len(s)
    memo = {}
    def is_pal(i: int, j: int) -> bool:
        if i >= j: return True
        if (i, j) in memo: return memo[(i, j)]
        memo[(i, j)] = s[i] == s[j] and is_pal(i + 1, j - 1)
        return memo[(i, j)]
    res = ""
    for i in range(n):
        for j in range(i, n):
            if j - i + 1 > len(res) and is_pal(i, j):
                res = s[i:j + 1]
    return res

# DP view: bottom-up (i descending so row i + 1 is ready)
def longestPalindrome(self, s: str) -> str:
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    start, max_len = 0, 1
    for i in range(n):
        dp[i][i] = True
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            if s[i] == s[j] and (j - i <= 2 or dp[i + 1][j - 1]):
                dp[i][j] = True
                if j - i + 1 > max_len:
                    start = i
                    max_len = j - i + 1
    return s[start:start + max_len]
```

**Cost:** Centres: `2n - 1` centres, each expands up to about `n / 2` steps: O(n²) time, O(1) space. Table: `n²/2` states, O(1) each: O(n²) time, O(n²) space.
**Follow-up:** *Faster?* Manacher's algorithm, O(n). *Longest palindromic subsequence?* Variant A. *Trap:* the loop overshoots by one, so return `s[left + 1:right]`; remember both odd and even centres.

**More scenarios on the same pattern**

**Variant A (crossover to interval DP)**
- **Question:** LC 516 Longest Palindromic Subsequence. Return the length of the longest palindromic subsequence of `s` (characters may be skipped).
- **Scenario:** A text may be trimmed by deleting any characters, without reordering the rest. What is the longest mirror-symmetric text that can be left?
- **Pattern and cost:** `dp[i][j] = 2 + dp[i+1][j-1]` if `s[i] == s[j]`, else `max(dp[i+1][j], dp[i][j-1])`. Equivalent to the LCS of `s` and its reverse. O(n²) time, O(n²) space (O(n) rolled). Expand-around-centre no longer works because skipped characters break the "contiguous" idea.

**Variant B (crossover: partition DP on top of a palindrome table)**
- **Question:** LC 132 Palindrome Partitioning II. Return the minimum cuts needed to split `s` so that every part is a palindrome.
- **Scenario:** A serial number must be cut into pieces, each of which reads the same forwards and backwards. What is the fewest cuts?
- **Pattern and cost:** First build `is_pal[i][j]` (O(n²)), then `cuts[i] = min(cuts[j] + 1 for j < i if is_pal[j][i-1])`. O(n²) time, O(n²) space. Two DPs chained.

---

### 20. Palindromic Substrings (#20)

**Original question:** LC 647. Given a string `s`, return the number of palindromic substrings in it (substrings at different positions count separately even if they have the same characters).

**Scenario:** A spam filter scores a message by how many of its contiguous fragments read the same forwards and backwards. Fragments at different positions count separately, even if the text is the same. Compute the score.

**Ask first:**
1. Count by position or only distinct fragments? Does a single letter count?
2. How long can the message be?

**Spot it:** Same mirror structure as #19, but "how many" instead of "longest". Every successful expansion step around a centre is one more.

**Model:**
- **State:** a centre (`2n - 1` of them); or `is_pal(i, j)`.
- **Choices:** expand one step while the ends match.
- **Recurrence:** each successful expansion adds 1. Or count all `(i, j)` where `s[i] == s[j] and is_pal(i + 1, j - 1)`.
- **Base:** start with `left = right = i` (odd) and `left = i, right = i + 1` (even).

**Solve:** ([20-palindromic-substrings.md](07-palindrome-dp/20-palindromic-substrings.md))
```python
# Primary: expand around centres
def countSubstrings(self, s: str) -> int:
    n = len(s)
    total_palindromes = 0
    def expand(left, right):
        count = 0
        while left >= 0 and right < n and s[left] == s[right]:
            count += 1
            left -= 1
            right += 1
        return count
    for i in range(n):
        total_palindromes += expand(i, i)
        total_palindromes += expand(i, i + 1)
    return total_palindromes

# DP view: bottom-up table
def countSubstrings(self, s: str) -> int:
    n = len(s)
    dp = [[False] * n for _ in range(n)]
    count = 0
    for i in range(n):
        dp[i][i] = True
        count += 1
    for i in range(n - 1, -1, -1):
        for j in range(i + 1, n):
            if s[i] == s[j]:
                if j - i <= 2 or dp[i + 1][j - 1]:
                    dp[i][j] = True
                    count += 1
    return count
```

**Cost:** Centres: O(n²) time, O(1) space. Table: O(n²) time and space. (The answer itself can be about `n²/2`, so you can't beat O(n²) by listing; Manacher counts them in O(n).)
**Follow-up:** *Only distinct ones?* Variant A. *Many range queries?* Variant B. *Trap:* count each expansion step, and include both odd and even centres.

**More scenarios on the same pattern**

**Variant A (crossover: dedupe breaks the counting)**
- **Question:** Count the **distinct** palindromic substrings of `s`. (A classic; for example solved with hashing, or a palindromic tree in O(n).)
- **Scenario:** The same filter, but if the same fragment appears twice in different places it should be scored only once.
- **Pattern and cost:** The `dp[i][j]` count adds one per position and cannot tell duplicates apart. Collect each palindrome into a **set** (or hash it), O(n²) time and up to O(n²) space, or use a palindromic tree for O(n). Shows where "count by position" stops being the question.

**Variant B (precompute once, answer many)**
- **Question:** Given `s` and `q` queries `(l, r)`, answer for each whether `s[l..r]` is a palindrome.
- **Scenario:** An audit tool will be asked thousands of times whether a given range of a log reads the same forwards and backwards.
- **Pattern and cost:** Build the `n × n` table once (O(n²) time and space), then each query is O(1). Without it, each query costs O(length). If `n` is large and queries are few, use hashing (forward and reverse prefix hashes) for O(1) per query after O(n) setup.

---

### 21. Longest Common Subsequence (#21)

**Original question:** LC 1143. Given two strings `text1` and `text2`, return the length of their longest common subsequence (characters in order but not necessarily contiguous), or `0` if there is none.

**Scenario:** A code-review tool compares two versions of a file, each a list of lines. How many lines survive in the same relative order in both versions?

**Ask first:**
1. Do you want only the count or the lines themselves?
2. How large can each version be (`m × n` memory)?

**Spot it:** Two sequences, order preserved, skipping allowed. After looking at the first element of each, you are left with a smaller copy of the same question.

**Model:**
- **State:** `dp(i, j)` = LCS length of `text1[i:]` and `text2[j:]`.
- **Choices:** if the characters match, pair them; if not, skip one from either side.
- **Recurrence:** match → `1 + dp(i + 1, j + 1)`; mismatch → `max(dp(i + 1, j), dp(i, j + 1))`.
- **Base:** either string used up → `0`.

**Solve:** ([21-longest-common-subsequence.md](08-two-string-dp/21-longest-common-subsequence.md))
```python
# Top-down
def longestCommonSubsequence(self, text1: str, text2: str) -> int:
    memo = {}
    def dp(i, j):
        if i == len(text1) or j == len(text2): return 0
        if (i, j) in memo: return memo[(i, j)]
        if text1[i] == text2[j]:
            memo[(i, j)] = 1 + dp(i + 1, j + 1)
        else:
            memo[(i, j)] = max(dp(i + 1, j), dp(i, j + 1))
        return memo[(i, j)]
    return dp(0, 0)

# Bottom-up, two rows (loops go DOWNWARD because the memo asks for larger indexes)
def longestCommonSubsequence(self, text1: str, text2: str) -> int:
    m, n = len(text1), len(text2)
    prev = [0] * (n + 1)
    for i in range(m - 1, -1, -1):
        curr = [0] * (n + 1)
        for j in range(n - 1, -1, -1):
            if text1[i] == text2[j]:
                curr[j] = 1 + prev[j + 1]
            else:
                curr[j] = max(prev[j], curr[j + 1])
        prev = curr
    return prev[0]
```

**Cost:** States = `m × n`. Work = O(1). Time O(m·n). Space O(m·n) memo and stack, O(n) two rows (put the shorter string as `text2` for O(min(m, n))).
**Follow-up:** *Print the common lines?* Needs the full table (or Hirschberg's divide-and-conquer for O(min) space). *Three strings?* Add a dimension, `m·n·p`. *Greedy trap:* "take every match you see" fails; a match now can block a longer chain later.

**More scenarios on the same pattern**

**Variant A (LCS plus reconstruction)**
- **Question:** LC 1092 Shortest Common Supersequence. Return the shortest string that has both `str1` and `str2` as subsequences.
- **Scenario:** Two playlists each list songs in a fixed order. Merge them into the shortest combined playlist that still plays each original in its own order.
- **Pattern and cost:** The length is `m + n - LCS`. To build the string, walk the LCS table: emit the shared character once, otherwise emit the character from the side you moved away from. O(m·n) time and space (the full table is needed to reconstruct).

**Variant B (crossover: contiguous instead of in-order)**
- **Question:** LC 718 Maximum Length of Repeated Subarray. Given two integer arrays, return the maximum length of a subarray that appears in both.
- **Scenario:** Two server logs: what is the longest unbroken run of identical events that appears in both?
- **Pattern and cost:** `dp[i][j] = dp[i-1][j-1] + 1` if equal, **else `0`** (a mismatch breaks the run). Answer is the max cell, not the corner. O(m·n) time, O(n) space with one row. Only the mismatch rule changed from LCS.

---

### 22. Edit Distance (#22)

**Original question:** LC 72. Given two strings `word1` and `word2`, return the minimum number of operations (insert, delete, replace a character) to convert `word1` into `word2`.

**Scenario:** A search engine's "did you mean" feature ranks candidates by the fewest single-letter changes (add a letter, remove a letter, or swap one letter) needed to turn the typed query into the candidate.

**Ask first:**
1. Do all three operations cost the same? Are swaps of two neighbouring letters (transposition) allowed?
2. How long can the strings be, and do you need the list of edits?

**Spot it:** Turning one sequence into another with small local edits. At the first mismatch there are a few ways to fix it, and each leaves a smaller copy of the problem.

**Model:**
- **State:** `dp(i, j)` = fewest edits to turn `word1[i:]` into `word2[j:]`.
- **Choices:** match → free; else insert, delete or replace (cost 1).
- **Recurrence:** match → `dp(i + 1, j + 1)`; mismatch → `1 + min(dp(i, j + 1), dp(i + 1, j), dp(i + 1, j + 1))`.
- **Base:** `dp(len(word1), j) = len(word2) - j`, `dp(i, len(word2)) = len(word1) - i` (the end base is not always 0).

**Solve:** ([22-edit-distance.md](08-two-string-dp/22-edit-distance.md))
```python
# Top-down
def minDistance(self, word1: str, word2: str) -> int:
    memo = {}
    def dp(i, j):
        if i == len(word1): return len(word2) - j
        if j == len(word2): return len(word1) - i
        if (i, j) in memo: return memo[(i, j)]
        if word1[i] == word2[j]:
            memo[(i, j)] = dp(i + 1, j + 1)
        else:
            insert = dp(i, j + 1)
            delete = dp(i + 1, j)
            replace = dp(i + 1, j + 1)
            memo[(i, j)] = 1 + min(insert, delete, replace)
        return memo[(i, j)]
    return dp(0, 0)

# Bottom-up on prefixes (mirror image), one row
def minDistance(self, word1: str, word2: str) -> int:
    m, n = len(word1), len(word2)
    dp = list(range(n + 1))
    for i in range(1, m + 1):
        prev = dp[0]
        dp[0] = i
        for j in range(1, n + 1):
            temp = dp[j]
            if word1[i - 1] == word2[j - 1]:
                dp[j] = prev
            else:
                dp[j] = 1 + min(dp[j - 1], dp[j], prev)
            prev = temp
    return dp[n]
```

**Cost:** States = `m × n`. Work = one `min` of three. Time O(m·n). Space O(m·n) memo, O(n) one row.
**Follow-up:** *List the edits?* Full table and trace back. *Different costs per operation?* Add them in the recurrence. *Transpositions (Damerau)?* Add a fourth case. *Trap:* the base cases are `len - j` and `len - i`, not `0`.

**More scenarios on the same pattern**

**Variant A (delete only, crossover to LCS)**
- **Question:** LC 583 Delete Operation for Two Strings. Return the minimum number of steps to make `word1` and `word2` the same, where each step deletes one character from either string.
- **Scenario:** Two config files must be made identical, but the only allowed change is removing lines from either. What is the fewest removals?
- **Pattern and cost:** Without insert or replace the kept part is a common subsequence: answer = `m + n - 2·LCS`. O(m·n) time, O(n) space.

**Variant B (crossover: DP is overkill)**
- **Question:** LC 161 One Edit Distance. Return `true` if `s` and `t` are exactly one edit apart (one insert, delete or replace).
- **Scenario:** A signup form must tell whether a typed username is exactly one keystroke away from an existing username.
- **Pattern and cost:** No table needed. Compare from the front until the first mismatch, then check the rest by length case (equal length: rest equal after skipping one; different by one: rest equal after skipping one in the longer). O(min(m, n)) time, O(1) space. The skill: noticing that "exactly one" removes the need for DP.

---

### 23. Interleaving String (#23)

**Original question:** LC 97. Given strings `s1`, `s2` and `s3`, return `true` if `s3` is formed by interleaving `s1` and `s2` (keeping the relative order of each string's characters).

**Scenario:** Two cashiers each print their receipt lines in a fixed order. A combined audit log shows lines from both registers mixed together. Could this log have come from these two receipts, with neither register's lines being reordered?

**Ask first:**
1. Do the lengths have to add up? Can lines repeat (ambiguous matches)?
2. Two registers only, or more?

**Spot it:** Reading the combined log left to right, each next line must come from one of two places. When **both** could match, you cannot decide greedily, which means trying both and sharing repeated work.

**Model:**
- **State:** `dp(i, j)` = can `s1[i:]` and `s2[j:]` interleave to form `s3[i + j:]`. (The `s3` index is implied by `i + j`, so no third dimension.)
- **Choices:** take the next character from `s1`, or from `s2`.
- **Recurrence:** `(s1[i] == s3[i+j] and dp(i+1, j)) or (s2[j] == s3[i+j] and dp(i, j+1))`.
- **Base:** both used up → `True`; return `False` first if `len(s1) + len(s2) != len(s3)`.

**Solve:** ([23-interleaving-string.md](08-two-string-dp/23-interleaving-string.md))
```python
# Top-down
def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
    if len(s1) + len(s2) != len(s3):
        return False
    memo = {}
    def dp(i, j):
        if i >= len(s1) and j >= len(s2): return True
        if (i, j) in memo: return memo[(i, j)]
        match_s1 = (i < len(s1) and s1[i] == s3[i + j]) and dp(i + 1, j)
        match_s2 = (j < len(s2) and s2[j] == s3[i + j]) and dp(i, j + 1)
        memo[(i, j)] = match_s1 or match_s2
        return memo[(i, j)]
    return dp(0, 0)

# Bottom-up, one row (j downward; dp[j] is still row i+1 until overwritten)
def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
    m, n = len(s1), len(s2)
    if m + n != len(s3):
        return False
    dp = [False] * (n + 1)
    for i in range(m, -1, -1):
        for j in range(n, -1, -1):
            if i == m and j == n:
                dp[j] = True
                continue
            k = i + j
            take_s1 = i < m and s1[i] == s3[k] and dp[j]
            take_s2 = j < n and s2[j] == s3[k] and dp[j + 1]
            dp[j] = take_s1 or take_s2
    return dp[0]
```

**Cost:** States = `(m+1) × (n+1)` (the `s3` position adds nothing). Work = two O(1) checks. Time O(m·n). Space O(m·n) memo, O(n) one row.
**Follow-up:** *Space?* One row (the standard follow-up). *Three sources?* The state becomes `(i, j, k)`, so O(m·n·p). *Trap:* check the lengths first, and bounds-check `i`, `j` before indexing. Greedy "take from whichever matches" fails: `s1 = "aab"`, `s2 = "axy"`, `s3 = "aaxaby"`.

**More scenarios on the same pattern**

**Variant A (weights on the two-string table)**
- **Question:** LC 712 Minimum ASCII Delete Sum for Two Strings. Return the lowest ASCII sum of deleted characters needed to make two strings equal.
- **Scenario:** Two codes must be made identical by removing characters from either, but removing a character costs its character code. Minimise the total cost.
- **Pattern and cost:** `dp(i, j)`: match → `dp(i+1, j+1)`; else `min(ord(s1[i]) + dp(i+1, j), ord(s2[j]) + dp(i, j+1))`; bases are the sum of the remaining characters. O(m·n) time, O(n) space.

**Variant B (crossover to greedy / index lookup)**
- **Question:** LC 392 Is Subsequence, with the follow-up: there are billions of strings `s` to test against one long string `t`.
- **Scenario:** A security scanner checks whether a short signature appears in order inside a very long stream of events, for billions of different signatures.
- **Pattern and cost:** One pass with two pointers is O(n). For many queries, preprocess `t` into a list of positions per character and **binary search** the next position for each character: O(|s| log |t|) per query. No table: the single-string version needs no DP. It shows where the two-string table is not the right tool.

---

### 24. Distinct Subsequences (#24)

**Original question:** LC 115. Given two strings `s` and `t`, return the number of distinct subsequences of `s` that equal `t`.

**Scenario:** A monitoring tool looks for an incident signature, a short list of events that must happen in a given order but may have other events in between, inside a long event stream. In how many different ways can the signature be found in the stream?

**Ask first:**
1. Are two ways different if they use different positions even for the same letters (yes in this problem)?
2. Is the result modulo something? What if the signature is empty?

**Spot it:** "How many ways to find A inside B in order". When two characters match, you have two choices: use it, or skip it and look for a later one.

**Model:**
- **State:** `dp(i, j)` = ways `t[j:]` appears as a subsequence of `s[i:]`.
- **Choices:** on a match, use `s[i]` for `t[j]` **or** skip it; on a mismatch, skip it.
- **Recurrence:** match → `dp(i + 1, j + 1) + dp(i + 1, j)`; mismatch → `dp(i + 1, j)`.
- **Base:** `j == len(t)` → `1` (**check this first**); `i == len(s)` → `0`.

**Solve:** ([24-distinct-subsequences.md](08-two-string-dp/24-distinct-subsequences.md))
```python
# Top-down
def numDistinct(self, s: str, t: str) -> int:
    m = len(s)
    n = len(t)
    memo = {}
    def dp(i, j):
        if j == n: return 1
        if i == m: return 0
        if (i, j) in memo: return memo[(i, j)]
        if s[i] == t[j]:
            memo[(i, j)] = dp(i + 1, j + 1) + dp(i + 1, j)
        else:
            memo[(i, j)] = dp(i + 1, j)
        return memo[(i, j)]
    return dp(0, 0)

# Bottom-up on prefixes, one row (j DOWNWARD so dp[j - 1] still holds the previous row)
def numDistinct(self, s: str, t: str) -> int:
    m, n = len(s), len(t)
    if n > m:
        return 0
    dp = [0] * (n + 1)
    dp[0] = 1
    for i in range(1, m + 1):
        for j in range(n, 0, -1):
            if s[i - 1] == t[j - 1]:
                dp[j] = dp[j] + dp[j - 1]
    return dp[n]
```

**Cost:** States = `m × n`. Work = one addition. Time O(m·n). Space O(m·n) memo, O(n) one row.
**Follow-up:** *Big answers?* Modulo. *Why check `j == n` before `i == m`?* An empty target is one way even if `s` is empty. *Trap:* the one-row loop must run `j` downward, or `dp[j - 1]` is already the current row.

**More scenarios on the same pattern**

**Variant A (crossover: many patterns at once)**
- **Question:** LC 792 Number of Matching Subsequences. Given a string `s` and an array of words, return how many words are subsequences of `s`.
- **Scenario:** A scanner has a long event stream and a list of thousands of signatures. How many of them appear, in order, somewhere in the stream?
- **Pattern and cost:** Instead of a table per word, scan `s` once and keep, for each letter, a bucket of "words waiting for this letter". Advance each word by one position per letter seen. O(|s| + total word length) time. A one-pass bucket method beats running DP per word.

**Variant B (single-string counting with de-duplication)**
- **Question:** LC 940 Distinct Subsequences II. Return the number of distinct non-empty subsequences of `s`, modulo 10^9 + 7.
- **Scenario:** How many different event signatures can be formed from a single recorded session by dropping any events and keeping the order? Two signatures with the same events count once.
- **Pattern and cost:** `dp[i] = 2·dp[i-1] - dp[last[c] - 1]` (counting the empty one; subtract 1 at the end), where `last[c]` is the previous index of character `c`: doubling counts every old signature with and without `c`, and the subtraction removes the duplicates already created the last time `c` was added. O(n) time, O(1) space with a 26-slot array.

---

### 25. Regular Expression Matching (#25)

**Original question:** LC 10. Given an input string `s` and a pattern `p`, implement regular expression matching with support for `.` (any single character) and `*` (zero or more of the **preceding** element). The matching must cover the **entire** input string.

**Scenario:** A routing rule is written with two wildcards: `.` stands for any single character, and `x*` stands for any number of `x` (including none). Does a request path match the whole rule, from the first character to the last?

**Ask first:**
1. Can `*` appear first in the rule, or twice in a row? (assume it always follows a character)
2. Must the whole path match, or just a part of it?

**Spot it:** Two sequences compared left to right, with one rule that creates a **fork**: a starred character can be used zero times or one more time. Forks that rejoin at the same positions are exactly what a memo is for.

**Model:**
- **State:** `dp(i, j)` = does `s[i:]` fully match `p[j:]`.
- **Choices:** if `p[j+1] == '*'`: skip the whole `x*` pair, or eat one matching character and **stay** on the same `x*`. Otherwise match one character and advance both.
- **Recurrence:** star → `dp(i, j+2) or (first_match and dp(i+1, j))`; no star → `first_match and dp(i+1, j+1)`, with `first_match = i < len(s) and p[j] in (s[i], '.')`.
- **Base:** `j == len(p)` → `i == len(s)`.

**Solve:** ([25-regular-expression-matching.md](08-two-string-dp/25-regular-expression-matching.md))
```python
# Top-down
def isMatch(self, s: str, p: str) -> bool:
    memo = {}
    def dp(i: int, j: int) -> bool:
        if j == len(p):
            return i == len(s)
        if (i, j) in memo: return memo[(i, j)]
        first_match = i < len(s) and p[j] in (s[i], '.')
        if j + 1 < len(p) and p[j + 1] == '*':
            ans = dp(i, j + 2) or (first_match and dp(i + 1, j))
        else:
            ans = first_match and dp(i + 1, j + 1)
        memo[(i, j)] = ans
        return ans
    return dp(0, 0)

# Bottom-up (suffix orientation; i and j both downward)
def isMatch(self, s: str, p: str) -> bool:
    m, n = len(s), len(p)
    dp = [[False] * (n + 1) for _ in range(m + 1)]
    dp[m][n] = True
    for i in range(m, -1, -1):
        for j in range(n - 1, -1, -1):
            first_match = i < m and p[j] in (s[i], '.')
            if j + 1 < n and p[j + 1] == '*':
                dp[i][j] = dp[i][j + 2] or (first_match and dp[i + 1][j])
            else:
                dp[i][j] = first_match and dp[i + 1][j + 1]
    return dp[0][0]
```

**Cost:** States = `(m+1) × (n+1)`. Work = at most two calls plus O(1). Time O(m·n). Space O(m·n); two rows are enough for the table.
**Follow-up:** *Wildcards `?` and `*` meaning "any run"?* Variant A. *Why `i < len(s)` inside `first_match`?* A starred pair can still be skipped when `s` is used up (e.g. `a*b*` matches `""`). *Trap:* returning `True` when `j == len(p)` without checking `i == len(s)`; and remembering that `*` binds to the character **before** it.

**More scenarios on the same pattern**

**Variant A (crossover to greedy)**
- **Question:** LC 44 Wildcard Matching. `?` matches any single character, `*` matches any sequence (including empty). Return whether the pattern matches the whole string.
- **Scenario:** A file search lets users type `?` for any one letter and `*` for any run of letters (even none). Does a given file name match the query exactly?
- **Pattern and cost:** The same `(i, j)` table: `*` → `dp(i, j+1) or dp(i+1, j)`; else compare. O(m·n) time. Because `*` is independent of the previous character, a **greedy two-pointer** that remembers the last `*` and retries is O(m·n) worst case but typically O(m + n).

**Variant B (crossover to interval DP)**
- **Question:** LC 87 Scramble String. A string is scrambled by splitting it into two non-empty parts, optionally swapping them, and recursing on each part. Return whether `s2` is a scrambled form of `s1`.
- **Scenario:** A document is reorganised by repeatedly splitting a section in two and optionally swapping the halves, again and again inside each half. Could this second version have come from the first?
- **Pattern and cost:** State `(i, j, length)`: do `s1[i:i+len]` and `s2[j:j+len]` scramble into each other; try every split, swapped or not. O(n³) states × O(n) splits = O(n⁴) time, O(n³) space. Here the state is a pair of equal-length windows, not a prefix pair.

---

### 26. Best Time to Buy and Sell Stock III (#26)

**Original question:** LC 123. Given daily `prices`, return the maximum profit using at most **two** transactions. You may not hold more than one share at a time (you must sell before buying again).

**Scenario:** A reseller can hold at most one unit of a product at a time, and a licence lets them complete at most two buy-then-resell rounds this season. Given the price for each day, what is the best total profit?

**Ask first:**
1. Can I buy and sell on the same day? Are there fees or a cooldown?
2. May I hold more than one unit? Is doing nothing allowed (profit 0)?

**Spot it:** Every day you are in one of a few modes (holding or not) and have a limited number of rounds left. The best result from tomorrow depends only on those two facts.

**Model:**
- **State:** `dp(i, holding, transactions)` = best profit from day `i` onward.
- **Choices:** do nothing, or the one allowed move (buy if not holding, sell if holding).
- **Recurrence:** holding → `max(dp(i+1, 1, t), prices[i] + dp(i+1, 0, t-1))`; not holding → `max(dp(i+1, 0, t), -prices[i] + dp(i+1, 1, t))`.
- **Base:** `i == n` or `transactions == 0` → `0`. Count the transaction on the **sell**.

**Solve:** ([26-best-time-to-buy-and-sell-stock-iii.md](09-state-machine-dp-stocks/26-best-time-to-buy-and-sell-stock-iii.md))
```python
# Top-down
def maxProfit(self, prices: list[int]) -> int:
    n = len(prices)
    memo = {}
    def dp(i: int, holding: int, transactions: int) -> int:
        if i == n or transactions == 0: return 0
        if (i, holding, transactions) in memo: return memo[(i, holding, transactions)]
        skip = dp(i + 1, holding, transactions)
        if holding:
            sell = prices[i] + dp(i + 1, 0, transactions - 1)
            memo[(i, holding, transactions)] = max(skip, sell)
        else:
            buy = -prices[i] + dp(i + 1, 1, transactions)
            memo[(i, holding, transactions)] = max(skip, buy)
        return memo[(i, holding, transactions)]
    return dp(0, 0, 2)

# Bottom-up, one day's 2 x 3 grid at a time (O(1) space)
def maxProfit(self, prices: list[int]) -> int:
    n = len(prices)
    nxt = [[0] * 3 for _ in range(2)]
    for i in range(n - 1, -1, -1):
        cur = [[0] * 3 for _ in range(2)]
        for tx in range(1, 3):
            cur[0][tx] = max(nxt[0][tx], -prices[i] + nxt[1][tx])
            cur[1][tx] = max(nxt[1][tx], prices[i] + nxt[0][tx - 1])
        nxt = cur
    return nxt[0][2]

# Four variables, read forward in time
def maxProfit(self, prices: list[int]) -> int:
    first_buy = float('-inf')
    first_sell = 0
    second_buy = float('-inf')
    second_sell = 0
    for price in prices:
        first_buy = max(first_buy, -price)
        first_sell = max(first_sell, first_buy + price)
        second_buy = max(second_buy, first_sell - price)
        second_sell = max(second_sell, second_buy + price)
    return second_sell
```

**Cost:** States = `n × 2 × 3 = 6n`. Work = O(1). Time O(n). Space O(n) memo (and recursion); O(1) rolled or with the four variables.
**Follow-up:** *k trades?* #27. *Unlimited trades?* Greedy (Variant B). *Cooldown or fee?* Change one transition (#28, Variant A). *Trap:* count the transaction on the sell, so you can still buy when one is left; for large `n` the memo hits Python's recursion limit.

**More scenarios on the same pattern**

**Variant A (state machine, no counter)**
- **Question:** LC 714 Best Time to Buy and Sell Stock with Transaction Fee. Unlimited transactions, but each one costs a fixed `fee`. Return the maximum profit.
- **Scenario:** A reseller can trade as often as they like, but the marketplace charges a flat fee per completed round. What is the best profit?
- **Pattern and cost:** Two modes only: `hold = max(hold, free - price)`, `free = max(free, hold + price - fee)`. O(n) time, O(1) space. No transaction count in the state because there is no limit.

**Variant B (crossover to greedy)**
- **Question:** LC 122 Best Time to Buy and Sell Stock II. Unlimited transactions, no fee, one share at a time. Return the maximum profit.
- **Scenario:** A reseller may trade as often as they like with no fees. What is the best possible profit over the season?
- **Pattern and cost:** Add up every price rise between consecutive days: `sum(max(0, p[i] - p[i-1]))`. O(n) time, O(1) space. With nothing restricting the trades, the state machine collapses into a simple greedy. This is also why Stock IV has a `k >= n // 2` shortcut.

---

### 27. Best Time to Buy and Sell Stock IV (#27)

**Original question:** LC 188. Given an integer `k` and daily `prices`, return the maximum profit using at most `k` transactions.

**Scenario:** The same reseller, but the licence now allows up to `k` buy-then-resell rounds, where `k` can be anywhere from 1 to a few hundred and the season can have thousands of days.

**Ask first:**
1. How do `k` and the number of days compare? (if `k` is at least half the days, the limit stops mattering)
2. Hold one unit at a time? Any fees?

**Spot it:** The same as #26, with the "rounds left" count turned into a parameter. That count multiplies the state size, so now it matters for cost.

**Model:**
- **State:** `dp(i, holding, transactions)` = best profit from day `i` onward.
- **Choices:** do nothing, buy (if not holding) or sell (if holding).
- **Recurrence:** exactly as #26, started with `transactions = k`.
- **Base:** `i == n` or `transactions == 0` → `0`.

**Solve:** ([27-best-time-to-buy-and-sell-stock-iv.md](09-state-machine-dp-stocks/27-best-time-to-buy-and-sell-stock-iv.md))
```python
# Top-down: same as #26, but return dp(0, 0, k)
def maxProfit(self, k: int, prices: list[int]) -> int:
    n = len(prices)
    memo = {}
    def dp(i: int, holding: int, transactions: int) -> int:
        if i == n or transactions == 0: return 0
        if (i, holding, transactions) in memo: return memo[(i, holding, transactions)]
        skip = dp(i + 1, holding, transactions)
        if holding:
            sell = prices[i] + dp(i + 1, 0, transactions - 1)
            memo[(i, holding, transactions)] = max(skip, sell)
        else:
            buy = -prices[i] + dp(i + 1, 1, transactions)
            memo[(i, holding, transactions)] = max(skip, buy)
        return memo[(i, holding, transactions)]
    return dp(0, 0, k)

# Bottom-up, one day's 2 x (k+1) grid (O(k) space)
def maxProfit(self, k: int, prices: list[int]) -> int:
    n = len(prices)
    nxt = [[0] * (k + 1) for _ in range(2)]
    for i in range(n - 1, -1, -1):
        cur = [[0] * (k + 1) for _ in range(2)]
        for tx in range(1, k + 1):
            cur[0][tx] = max(nxt[0][tx], -prices[i] + nxt[1][tx])
            cur[1][tx] = max(nxt[1][tx], prices[i] + nxt[0][tx - 1])
        nxt = cur
    return nxt[0][k]
```
Shortcut from the write-up: if `k >= n // 2`, the limit never binds, so `sum(max(prices[i] - prices[i-1], 0))`.

**Cost:** States = `n × 2 × (k+1)`. Work = O(1). Time O(n·k). Space O(n·k) memo, O(k) rolled.
**Follow-up:** *Huge `k`?* The greedy shortcut. *Space?* Roll over days. *Trap:* with `k` large, the memo's `n·k` states blow up if you don't take the shortcut.

**More scenarios on the same pattern**

**Variant A (state = last choice made)**
- **Question:** LC 256 Paint House. Each of `n` houses is painted one of three colours with a known cost matrix; no two neighbouring houses share a colour. Return the minimum total cost.
- **Scenario:** A developer must repaint a row of `n` buildings in one of three brand colours. Costs differ per building and colour, and a building can't reuse the colour of the one before it. What is the cheapest plan?
- **Pattern and cost:** State `(i, last_colour)`; `dp[i][c] = cost[i][c] + min(dp[i-1][c'] for c' != c)`. O(n·3·3) = O(n) time, O(1) space. It is the same "few modes, one move per step" shape as the stock problems, with colours as modes. (With `k` colours, track the best two previous values to stay O(n·k).)

**Variant B (state machine on a subarray)**
- **Question:** LC 1186 Maximum Subarray Sum with One Deletion. Return the maximum sum of a non-empty subarray, where you may delete at most one element from it.
- **Scenario:** A shop picks a continuous stretch of days to report, but is allowed to leave out one bad day inside it. What is the best achievable total?
- **Pattern and cost:** Two modes ending at `i`: `no_del[i] = max(x, no_del[i-1] + x)` and `one_del[i] = max(no_del[i-1], one_del[i-1] + x)`. Answer is the best of all. O(n) time, O(1) space.

---

### 28. Best Time to Buy and Sell Stock with Cooldown (#28)

**Original question:** LC 309. You may trade as many times as you like, but after you sell you cannot buy on the next day (a one-day cooldown). Return the maximum profit.

**Scenario:** A reseller can trade as often as they like, but after each resale the marketplace freezes their account for one day before they can buy again. What is the best profit over the season?

**Ask first:**
1. Does the freeze apply only after a sale (not after a purchase)?
2. May I hold more than one unit? Is there a fee as well?

**Spot it:** A rule about what is allowed the day **after** a certain action, so the mode must remember "just sold". The fix is to jump past the frozen day, or to add a mode.

**Model:**
- **State:** `dp(i, holding)` = best profit from day `i` onward.
- **Choices:** skip; buy (if not holding); sell (if holding), after which the next day is skipped.
- **Recurrence:** holding → `max(dp(i+1, 1), prices[i] + dp(i+2, 0))`; not holding → `max(dp(i+1, 0), -prices[i] + dp(i+1, 1))`.
- **Base:** `i >= n` → `0` (`>=` because a sell jumps to `i + 2`).

**Solve:** ([28-best-time-to-buy-and-sell-stock-with-cooldown.md](09-state-machine-dp-stocks/28-best-time-to-buy-and-sell-stock-with-cooldown.md))
```python
# Top-down
def maxProfit(self, prices: list[int]) -> int:
    n = len(prices)
    memo = {}
    def dp(i: int, holding: int) -> int:
        if i >= n: return 0
        if (i, holding) in memo: return memo[(i, holding)]
        skip = dp(i + 1, holding)
        if holding:
            sell = prices[i] + dp(i + 2, 0)
            memo[(i, holding)] = max(skip, sell)
        else:
            buy = -prices[i] + dp(i + 1, 1)
            memo[(i, holding)] = max(skip, buy)
        return memo[(i, holding)]
    return dp(0, 0)

# Bottom-up (two spare rows cover i + 1 and i + 2 past the end)
def maxProfit(self, prices: list[int]) -> int:
    n = len(prices)
    dp = [[0, 0] for _ in range(n + 2)]
    for i in range(n - 1, -1, -1):
        dp[i][0] = max(dp[i + 1][0], -prices[i] + dp[i + 1][1])
        dp[i][1] = max(dp[i + 1][1], prices[i] + dp[i + 2][0])
    return dp[0][0]

# State machine, three variables, read forward in time
def maxProfit(self, prices: list[int]) -> int:
    if not prices:
        return 0
    held = float('-inf')
    sold = float('-inf')
    reset = 0
    for price in prices:
        prev_sold = sold
        held = max(held, reset - price)
        sold = held + price
        reset = max(reset, prev_sold)
    return max(sold, reset)
```

**Cost:** States = `2n`. Work = O(1). Time O(n). Space O(n) memo; O(1) with three variables.
**Follow-up:** *Cooldown of `c` days?* Jump to `i + c + 1` after a sell. *Add a fee?* Subtract it on the sell. *Trap:* the base is `i >= n`, not `==`; selling on day `n - 1` jumps to `n + 1`.

**More scenarios on the same pattern**

**Variant A (crossover to weighted interval scheduling)**
- **Question:** LC 1235 Maximum Profit in Job Scheduling. Jobs have `startTime`, `endTime`, `profit`. Return the maximum profit from non-overlapping jobs.
- **Scenario:** A freelancer has a list of gigs, each with a start, an end and a payment, and can only do one at a time. What is the most they can earn?
- **Pattern and cost:** Sort by end time. `dp[i] = max(dp[i-1], profit_i + dp[last job ending before start_i])`, with the last compatible job found by **binary search**. O(n log n) time, O(n) space. The unweighted version (#12 Variant B) is greedy; with payments the greedy rule fails, so it becomes DP.

**Variant B (counting through a small automaton)**
- **Question:** LC 552 Student Attendance Record II. Count the length-`n` attendance strings over `A` (absent), `L` (late), `P` (present) that have fewer than 2 `A`s and never 3 or more consecutive `L`s, modulo 10^9 + 7.
- **Scenario:** A school logs each day as present, late or absent. A record is "good" if there are fewer than two absences and never three late days in a row. How many good records of length `n` exist?
- **Pattern and cost:** State `(absences so far in {0,1}, current late streak in {0,1,2})`, so 6 modes; each day moves between modes. O(6·3·n) time, O(1) space rolled. A counting version of the state machine.

---

### 29. Burst Balloons (#29)

**Original question:** LC 312. There are `n` balloons with values `nums[i]`. Bursting balloon `i` earns `nums[i-1] * nums[i] * nums[i+1]` coins (out-of-range neighbours count as 1). Return the maximum coins from bursting all the balloons.

**Scenario:** A demolition crew removes a row of buildings one at a time. Removing a building pays its height times the height of whatever is still standing immediately to its left and to its right (treat the ends as height 1). In what order should they demolish everything to earn the most?

**Ask first:**
1. What value do the missing neighbours at the ends take? (1)
2. How many buildings, and do you want the order, or just the total payout?

**Spot it:** The payout of one removal depends on **which buildings are still standing**, which depends on the earlier removals. Thinking "which first?" tangles everything. Flip it: pick the one removed **last** in a range, and the rest of the range is already gone, so the two sides become independent.

**Model:**
- **Pad:** `A = [1] + nums + [1]`.
- **State:** `dp(i, j)` = max coins from bursting every balloon in `A[i..j]`, with `A[i-1]` and `A[j+1]` staying as the outer neighbours.
- **Choices:** which balloon `k` in `[i, j]` is burst **last**.
- **Recurrence:** `dp(i, j) = max over k of A[i-1]·A[k]·A[j+1] + dp(i, k-1) + dp(k+1, j)`.
- **Base:** `i > j` → `0`. Answer: `dp(1, len(nums))`.

**Solve:** ([29-burst-balloons.md](10-interval-partition-dp/29-burst-balloons.md))
```python
# Top-down
def maxCoins(self, nums: list[int]) -> int:
    A = [1] + nums + [1]
    memo = {}
    def dp(i: int, j: int) -> int:
        if i > j: return 0
        if (i, j) in memo: return memo[(i, j)]
        max_coins = 0
        for k in range(i, j + 1):
            coins = A[i - 1] * A[k] * A[j + 1]
            total = coins + dp(i, k - 1) + dp(k + 1, j)
            max_coins = max(max_coins, total)
        memo[(i, j)] = max_coins
        return memo[(i, j)]
    return dp(1, len(nums))

# Bottom-up: fill ranges by increasing length
def maxCoins(self, nums: list[int]) -> int:
    A = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * (n + 2) for _ in range(n + 2)]
    for length in range(1, n + 1):
        for i in range(1, n - length + 2):
            j = i + length - 1
            for k in range(i, j + 1):
                dp[i][j] = max(dp[i][j], A[i - 1] * A[k] * A[j + 1] + dp[i][k - 1] + dp[k + 1][j])
    return dp[1][n]
```

**Cost:** States = about `n²/2` ranges. Work = a loop over up to `n` choices of `k`. Time O(n³). Space O(n²).
**Follow-up:** *Print the order?* Store the best `k` per range and unwind. *Space?* Can't roll; each range reads many shorter ranges. *Trap:* choosing the **first** balloon to burst makes the neighbours depend on history; choosing the **last** is what makes the halves independent. Also: pad the array with 1s.

**More scenarios on the same pattern**

**Variant A (same "choose the last" idea)**
- **Question:** LC 1547 Minimum Cost to Cut a Stick. A stick of length `n` must be cut at the positions in `cuts`; each cut costs the length of the piece being cut. Return the minimum total cost over all cut orders.
- **Scenario:** A carpenter has a plank and a list of places where it must be sawn. Each saw cut costs as much as the length of the piece being cut. In what order should the cuts be made to pay the least?
- **Pattern and cost:** Sort the cuts and add the two ends. `dp[i][j] = (pos[j] - pos[i]) + min over k of dp[i][k] + dp[k][j]`, where `k` is the **first** cut made in that piece (it costs the whole piece, then the two halves are independent). Unlike Burst Balloons, you pick the first, not the last, because the cost depends on the piece length at the time of the cut. O(c³) time, O(c²) space, where `c` is the number of cuts.

**Variant B (crossover: split a polygon)**
- **Question:** LC 1039 Minimum Score Triangulation of Polygon. A convex polygon has vertex values `values[i]`. Triangulate it; the score of a triangle is the product of its three vertex values. Return the minimum total score.
- **Scenario:** A plot of land with `n` corners (each with a known value) is divided into triangular lots by non-crossing boundary lines. A lot's cost is the product of its three corner values. What is the cheapest way to divide it?
- **Pattern and cost:** For the edge `(i, j)`, choose the third corner `k` of the triangle that sits on it: `dp[i][j] = min over k of dp[i][k] + dp[k][j] + v[i]·v[k]·v[j]`. O(n³) time, O(n²) space. The same "pick the middle one, split into two independent ranges" idea as Burst Balloons.

---

## Part 5. Common traps to say out loud

Say the relevant one out loud *before* the interviewer has to point it out. It shows you know where these problems usually go wrong.

**Base cases and boundaries**
- **Off-by-one in the base case.** A jump of 2 can overshoot by one, so use `i >= n`, not `i == n` (Climbing Stairs, House Robber, Cooldown). Say: "which indexes can the recursion actually reach?"
- **The end base is not always 0.** Edit Distance returns `len(word2) - j` when `word1` is used up. Say: "what does it cost to finish from here?"
- **Wrong dead-end value.** A dead end must return what the combine operator ignores: `inf` for `min` (Coin Change), `-inf` for `max`, `0` for `+`, `False` for `or`. Returning `0` in a `min` makes the dead end look like the best answer.
- **Prefix vs suffix indexes.** A prefix table shifts everything by one (`word1[i - 1]`). Suffix tables loop **downward** because the recursion asks for larger indexes.
- **Check order matters.** Distinct Subsequences: check `j == len(t)` before `i == len(s)`. Coin Change: check `current_sum == amount` before "out of coins". Unique Paths II: obstacle check before the start check.

**Order of computation**
- **Wrong iteration order or direction.** Rolled 0/1 knapsack and unbounded knapsack need *opposite* loop directions (use once: read cells not yet updated; reuse: read cells already updated). Say which way your array indexes the sum.
- **Combinations vs permutations.** Coins outer loop counts combinations (Coin Change II); target outer loop counts sequences (Combination Sum IV). Reading the question for "does order matter?" is the whole difference.
- **Interval DP order.** Fill by increasing length, never by `i` alone. **Pick vs skip:** reuse stays on index `i`; use-once moves to `i + 1`.
- **Rolling-array overwrite.** Keep the old diagonal in `temp` (Maximal Square, Edit Distance). In-place Triangle is only safe because `c` ascends.

**Empty and tiny inputs**
- **Forgetting the empty case.** Empty string, empty dictionary, `amount = 0`, `target = 0`, `n = 1` (House Robber II slices to empty), `k = 0` (Stock IV), empty prices. Say: "n = 0 and n = 1 first."
- **Impossible answer.** Coin Change must return `-1`, not `inf`. Decode Ways with a leading `0` returns `0`, not an error.

**State, memo and answer**
- **Memo key missing a variable.** If two calls with the same key can give different answers, a variable is missing (the `holding` flag, the transaction count, `prev_idx`). Equally, an extra variable that never changes the future only wastes states.
- **Forgetting to cache `False`.** Word Break retries dead suffixes without it.
- **Shared memo.** House Robber II needs a fresh memo per slice. A memo shared across test cases or kept as a default argument returns stale values.
- **Answer in the wrong place.** Maximal Square and Longest Increasing Path need the best over **all** cells. LIS answer is `max(dp)`, not `dp[-1]`. Return the **area**, not the side.

**Greedy that looks right but isn't** (find a counter-example, say it aloud)
- Coin Change `[1, 3, 4]`, amount `6`: largest-first gives 3 coins, best is 2.
- House Robber `[4, 5, 4]`: take-the-biggest gives 5, best is 8.
- Min Path Sum: stepping to the cheaper next square can lead into an expensive region.
- LCS / Interleaving: taking every match you see (or the first source that matches) can block a longer answer later.
- Cherry Pickup: best forward path, then best return path, is not the best pair.
- Stock with a limit, cooldown or fee: "buy every dip, sell every peak" is only right when there is no restriction (Stock II).
- *And the reverse:* don't write a DP when a sort + greedy works (Pair Chain, Jump Game II, Stock II). Ask "is there a simpler rule?" once.

**Mutating the input**
- Writing running sums into the grid (Min Path Sum, Triangle) gives `O(1)` space but **destroys the input**. Ask first, and say you are doing it.
- Don't sort an array whose order is the problem (LIS, Max Product Subarray, House Robber). Sorting is fine for Russian Dolls and Job Scheduling, where the sort is the trick.
- Slicing (`nums[:-1]`) copies; pass `(lo, hi)` bounds to stay `O(1)` space.
- Memo dict keys must be hashable: tuples, not lists.

**Cost and practicalities**
- **Pseudo-polynomial.** Knapsack time depends on the *value* of the target. With huge targets it is not feasible; name meet-in-the-middle or a bitset.
- **Recursion limit.** Python allows about 1000 frames. Say "I'd switch to the table here" when `n` is in the thousands.
- **Reconstruction needs the table.** A rolled array gives the value but not the route. Ask whether they want the route before you roll.
- **Overflow and modulo.** Counting problems often want `% 1_000_000_007`. Ask.

---

## Part 6. Known gaps

DP problems this repo does not cover yet, in the order I'd add them. Some are covered as variants in Part 4 (marked **V**) but have no write-up with the six sections. Likelihood is my judgement, as in problems.md: there is **no verified Google data** behind it.

**Check the sibling repos first.** Jump Game / Jump Game II, Maximum Subarray (Kadane) and Stock I / II are already in `Arrays-Strings` (as greedy, not DP). Word Break II is in `Backtracking`. House Robber III, Diameter and Max Path Sum are in `Trees`. They are not repeated here.

| Gap | Pattern it teaches | Closest problem here | Why add it | Likelihood |
|---|---|---|---|---|
| Longest Palindromic Subsequence (LC 516) **V** | interval DP on a subsequence (equals LCS with the reverse) | #19, #21 | listed in problems.md as a deliberate omission; the contiguous-vs-subsequence contrast is a favourite follow-up | Medium |
| Unique Binary Search Trees (LC 96) / Catalan | split a range, multiply the two sides (`×` when counting) | #29 | `patterns.md` mentions it but there is no write-up | Medium |
| Perfect Squares (LC 279) **V** | unbounded knapsack with implicit coins | #7 | very common warm-up; one extra rep | Medium |
| Combination Sum IV (LC 377) **V** | permutations vs combinations | #1 A, #8 | referenced in patterns.md; the loop-order trap | Medium |
| Delete and Earn (LC 740) **V** | reduce to House Robber after bucketing | #3 | tests spotting the reduction | Medium |
| Stone Game (LC 877) / Predict the Winner (LC 486) / Guess Number Higher or Lower II (LC 375) | two-player min-max on a range | #29 | "can the first player win" scenarios are a natural Google-style prompt; the state is `(i, j)` with a negation | **High** |
| Bitmask: Partition to K Equal Sum Subsets (LC 698) **V**, Can I Win (LC 464), Shortest Path Visiting All Nodes (LC 847) | state = set of used items, `n ≤ 20` | #9 B | the one pattern with no coverage at all; recognising "n ≤ 16" is the clue | Medium |
| Digit DP: Numbers At Most N Given Digit Set (LC 902), Count Numbers with Unique Digits (LC 357), Non-negative Integers without Consecutive Ones (LC 600) | state = (position, tight, summary) | none | "count numbers up to N with a property" is easy to miss without a prior rep | Low |
| Knight Probability in Chessboard (LC 688), New 21 Game (LC 837) | probability / expected value DP | #18 A | the DP is the same; the combine operator is a weighted sum | Low |
| Minimum Cost For Tickets (LC 983) **V**, Paint House (LC 256) **V** | day-indexed and colour-state machines | #7 B, #27 A | good for "few modes, one move per step" recognition outside stocks | Medium |
| Ones and Zeroes (LC 474) **V** | 0/1 knapsack with two capacities | #10 | the first time the table needs two budgets | Medium |
| Dungeon Game (LC 174) **V**, Minimum Falling Path Sum (LC 931) **V**, Cherry Pickup (LC 741) **V** | grid DP where the direction, the start or the number of walkers changes | #13 to #16 | shows grid DP is more than "top-left to bottom-right" | Medium |
| Maximal Rectangle (LC 85) **V** / Largest Rectangle in Histogram (LC 84) | where the square DP stops; monotonic stack | #17 | frequent follow-up to Maximal Square | Medium |
| Wildcard Matching (LC 44) **V** | two-string table with greedy alternative | #25 | simpler sibling of Regex; the greedy two-pointer comparison is a good talking point | Medium |
| Russian Doll Envelopes (LC 354) **V**, Number of LIS (LC 673), Largest Divisible Subset (LC 368), Longest String Chain (LC 1048) | LIS with a sort, with counts, or with reconstruction | #12 | many "sort, then LIS" disguises | Medium |
| Palindrome Partitioning II (LC 132) **V** | palindrome table plus partition DP | #19 | two DPs chained | Low |
| Minimum Cost to Cut a Stick (LC 1547) **V**, Strange Printer (LC 664), Minimum Score Triangulation (LC 1039) **V**, Remove Boxes (LC 546) | more interval DP reps | #29 | burst balloons is the only interval rep in the repo | Low |
| Integer Break (LC 343), Ugly Number II (LC 264), Counting Bits (LC 338) | small 1D DPs with a twist | #1 | easy to blank on under pressure | Low |
| Maximum Profit in Job Scheduling (LC 1235) **V** | weighted interval scheduling: sort plus binary search | #12 B, #28 A | the "greedy fails once there are weights" lesson | Medium |
| Student Attendance Record II (LC 552) **V**, Knight Dialer (LC 935) | counting through a small automaton | #28 | counting state machines with modulo | Low |

**Closing the gaps, in order:** (1) game / min-max DP, (2) Longest Palindromic Subsequence, (3) one bitmask problem, (4) Unique BSTs, (5) Ones and Zeroes, (6) Maximal Rectangle, (7) one digit-DP problem. Everything else in the table is already practised as a variant in Part 4.
