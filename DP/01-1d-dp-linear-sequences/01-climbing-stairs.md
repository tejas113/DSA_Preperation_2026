# 01. Climbing Stairs

**LC 70** · **Source:** LC150 + NC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** 1D DP / Fibonacci

---

## 1. Intuition

You need to climb `n` steps, taking 1 or 2 at a time. Think of `i` as the step you are **standing on**, starting at the bottom (`0`). From step `i` your next move is a 1-step (to `i + 1`) or a 2-step (to `i + 2`), so the ways to reach the top from `i` are the ways from each of those, added together. Landing exactly on step `n` is one complete way; going past it means you overshot.

* `dp(i)` — the number of distinct ways to reach the top (step `n`) when you are standing on step `i`.
* `if i == n: return 1` — you landed exactly on the top, so that sequence of moves is one complete way.
* `if i > n: return 0` — you overshot (took a 2-step from step `n - 1`), so this is not a valid way.
* `dp(i+1) + dp(i+2)` — take a 1-step or a 2-step, then finish the rest; add both counts.
* `memo[i]` — many move sequences land on the same step, so `dp(i+2)` is asked for again and again. Without the cache the calls double at every level (O(2^n)); with it each step is solved once.

**Recall:** `ways(i) = ways(i + 1) + ways(i + 2)`, with `ways(n) = 1` and `ways(> n) = 0`.

## 2. Template

* **State:** `dp(i)` = number of distinct ways to reach step `n` from step `i`
* **Choice:** the next move is a 1-step or a 2-step
* **Recurrence:** `dp(i) = dp(i + 1) + dp(i + 2)`
* **Base:** `dp(n) = 1` (exactly on the top), `dp(i > n) = 0` (overshot)
* **Guard:** the `i > n` check is needed, because `dp(n - 1)` calls `dp(n + 1)`

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        memo = {}

        def dp(i):

            if i == n:
                return 1

            if i > n:
                return 0
            
            if i in memo:
                return memo[i]

            memo[i] = dp(i + 1) + dp(i + 2)
            return memo[i]

        return dp(0)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo = {}` (keyed by `i`) | `dp = [0] * (n + 2)` (one slot per step `0..n`, plus slot `n + 1` for the overshoot) |
| `if i == n: return 1` | `dp[n] = 1` |
| `if i > n: return 0` | `dp[n + 1]` stays `0` |
| `dp(i+1) + dp(i+2)` | `dp[i] = dp[i + 1] + dp[i + 2]` |
| `dp(i)` asks for **larger** steps | `for i in range(n - 1, -1, -1)` — fill from the top downward |
| `return dp(0)` | `return dp[0]` |

**Loop-order rule:** whatever the memo asks for (`i + 1`, `i + 2`) must already be filled when you reach `i`, so loop downward from the top.

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        dp = [0] * (n + 2)
        dp[n] = 1                          # base: standing on the top = one way

        for i in range(n - 1, -1, -1):
            dp[i] = dp[i + 1] + dp[i + 2]

        return dp[0]
```

**Shrink to O(1) space:** `dp[i]` only reads the next two slots, so keep just two variables. `nxt` is `dp[i + 1]` and `nxt2` is `dp[i + 2]`; each loop slides the pair down one step.

```python
class Solution:
    def climbStairs(self, n: int) -> int:
        nxt, nxt2 = 1, 0                   # dp[n] = 1, dp[n + 1] = 0

        for _ in range(n):
            nxt, nxt2 = nxt + nxt2, nxt

        return nxt
```

## 4. Dry Run (`n = 4`)

```text
dp(0) = 5
├─ dp(1) = 3
│   ├─ dp(2) = 2
│   │   ├─ dp(3) = 1
│   │   │   ├─ dp(4) = 1     (base: exactly on the top)
│   │   │   └─ dp(5) = 0     (base: overshot)
│   │   └─ dp(4) = 1         (base: exactly on the top)
│   └─ dp(3) = 1             (cached — not recomputed)
└─ dp(2) = 2                 (cached — not recomputed)
```

## 5. Complexity

* **States:** `memo` is keyed by `i`, so at most `n` different values (`0..n - 1`) are ever stored; `dp(n)` and `dp(n + 1)` return before touching it.
* **Time:** O(n) — each step is computed once, and each computation is a single addition (the two recursive calls are base cases or cache hits).
* **Space:** O(n) — the memo holds about `n` entries and the recursion goes `n` deep. Tabulation is O(n) too; the two-variable version is O(1).

## 6. Recall (30 seconds)

* **State:** `dp(i)` = ways to reach step `n` from step `i`.
* **Transition:** `dp(i+1) + dp(i+2)`, with `dp(n) = 1` and `dp(i > n) = 0`; start at `dp(0)`.
* **Speed:** cache the answers → O(n) time; keep two rolling variables → O(1) space.
