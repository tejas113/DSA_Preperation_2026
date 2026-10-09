# 01. Climbing Stairs

**LC 70** · **Source:** LC150 + NC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** 1D DP / Fibonacci

---

## 1. Intuition

You need to climb `n` steps, taking 1 or 2 at a time. Think of `i` as the steps **still remaining**. From `i` remaining, your next move is a 1-step (leaving `i - 1`) or a 2-step (leaving `i - 2`), so the ways to finish from `i` are the ways to finish from each of those, added together. Landing on exactly 0 remaining is one complete way; going below 0 means you overshot.

* `dfs(i)` — the number of distinct ways to climb `i` steps.
* `if i == 0: return 1` — you landed exactly on the top, so that sequence of moves is one complete way.
* `if i < 0: return 0` — you overshot (took a 2-step with only 1 step left), so this is not a valid way.
* `dfs(i-1) + dfs(i-2)` — take a 1-step or a 2-step, then finish the rest; add both counts.
* `memo[i]` — many move sequences leave the same number of steps, so `dfs(i-2)` is asked for again and again. Without the cache the calls double at every level (O(2^n)); with it each value is solved once.

**Recall:** `ways(i) = ways(i - 1) + ways(i - 2)`, with `ways(0) = 1` and `ways(<0) = 0`.

## 2. Template

* **State:** `dfs(i)` = number of distinct ways to climb `i` steps (`i` = steps remaining)
* **Choice:** the next move is a 1-step or a 2-step
* **Recurrence:** `dfs(i) = dfs(i - 1) + dfs(i - 2)`
* **Base:** `dfs(0) = 1` (exactly on the top), `dfs(i < 0) = 0` (overshot)
* **Guard:** the `i < 0` check is needed, because `dfs(1)` calls `dfs(-1)`

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def climbStairs(self, n: int) -> int:

        memo = {}

        def dfs(i):
            if i == 0:
                return 1

            if i < 0:
                return 0
            
            if i in memo:
                return memo[i]

            memo[i] = dfs(i-1) + dfs(i-2)

            return memo[i]

        return dfs(n)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo = {}` (keyed by `i`) | `dp = [0] * (n + 1)` (one slot per `0..n`) |
| `if i == 0: return 1` | `dp[0] = 1` |
| `if i < 0: return 0` | a table has no negative slot, so write `dp[1] = 1` directly (`dfs(1) = dfs(0) + 0`) and start the loop at 2 |
| `dfs(i-1) + dfs(i-2)` | `dp[i] = dp[i - 1] + dp[i - 2]` |
| `dfs(n)` asks for smaller values | `for i in range(2, n + 1)` — smaller values get filled first |
| `return dfs(n)` | `return dp[n]` |

**Loop-order rule:** whatever the memo asks for (`i - 1`, `i - 2`) must already be filled when you reach `i`, so loop upward from the base cases.

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        if n <= 1:
            return 1

        dp = [0] * (n + 1)
        dp[0] = 1
        dp[1] = 1

        for i in range(2, n + 1):
            dp[i] = dp[i - 1] + dp[i - 2]

        return dp[n]
```

**Shrink to O(1) space:** `dp[i]` only reads the previous two slots, so keep just two variables. `one` is the ways for the latest step and `two` is the step before it; each loop slides the pair forward.

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        one, two = 1, 1

        for _ in range(n - 1):
            one, two = one + two, one

        return one
```

## 4. Dry Run (`n = 4`)

```text
dfs(4) = 5
├─ dfs(3) = 3
│   ├─ dfs(2) = 2
│   │   ├─ dfs(1) = 1
│   │   │   ├─ dfs(0) = 1     (base: exactly on the top)
│   │   │   └─ dfs(-1) = 0    (base: overshot)
│   │   └─ dfs(0) = 1         (base: exactly on the top)
│   └─ dfs(1) = 1             (cached — not recomputed)
└─ dfs(2) = 2                 (cached — not recomputed)
```

## 5. Complexity

* **States:** `memo` is keyed by `i`, so at most `n` different values (`1..n`) are ever stored; `dfs(0)` and `dfs(-1)` return before touching it.
* **Time:** O(n) — each value is computed once, and each computation is a single addition (the two recursive calls are base cases or cache hits).
* **Space:** O(n) — the memo holds about `n` entries and the recursion goes `n` deep. Tabulation is O(n) too; the two-variable version is O(1).

## 6. Recall (30 seconds)

* **State:** `dfs(i)` = ways to climb `i` steps.
* **Transition:** `dfs(i-1) + dfs(i-2)`, with `dfs(0) = 1` and `dfs(i < 0) = 0`.
* **Speed:** cache the answers → O(n) time; keep two rolling variables → O(1) space.
