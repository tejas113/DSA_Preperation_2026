# 24. Distinct Subsequences

**LC 115** · **Source:** NC150 · **Difficulty:** Hard · **Priority:** Stretch · **Pattern:** 2D DP / Two Strings (counting)

---

## 1. Intuition

Count how many different ways `t` can be picked out of `s` as a subsequence. Compare the **last** characters. If `s[i]` can't match `t[j]`, that character of `s` is useless, so skip it. If they **do** match, you have two options: use this `s[i]` to match `t[j]` (both shrink), or skip it anyway and hope an earlier character matches `t[j]` (only `s` shrinks). Add the two counts.

* `dp(i, j)` — the number of ways `t[:j + 1]` appears as a subsequence of `s[:i + 1]`.
* `if j < 0: return 1` — all of `t` has been matched: that is exactly one way.
* `if i < 0: return 0` — `s` ran out before `t` was fully matched: no way.
* `s[i] == t[j]` → `dp(i - 1, j - 1) + dp(i - 1, j)` — **use** `s[i]` for `t[j]`, plus **skip** `s[i]`; both count.
* else `dp(i - 1, j)` — no match, so `s[i]` has to be skipped.
* `memo[(i, j)]` — many skip/use histories reach the same `(i, j)`, so each is solved once.

**Recall:** match → `dp(i - 1, j - 1) + dp(i - 1, j)`; mismatch → `dp(i - 1, j)`.

## 2. Template

* **State:** `dp(i, j)` = number of ways `t[:j + 1]` is a subsequence of `s[:i + 1]`
* **Choice:** on a match, use `s[i]` for `t[j]` or skip it; on a mismatch, skip it
* **Recurrence:** match → `dp(i - 1, j - 1) + dp(i - 1, j)`; mismatch → `dp(i - 1, j)`
* **Base:** `dp(·, -1) = 1` (all of `t` matched), `dp(-1, j ≥ 0) = 0` (`s` used up)
* **Guard:** check `j < 0` **before** `i < 0`, because an empty `t` counts as one way even when `s` is also empty

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        memo = {}

        def dp(i: int, j: int) -> int:
            # Base Case 1: Target string t is fully matched
            if j < 0:
                return 1

            # Base Case 2: Source string s is exhausted before t is matched
            if i < 0:
                return 0

            if (i, j) in memo:
                return memo[(i, j)]

            if s[i] == t[j]:
                memo[(i, j)] = dp(i - 1, j - 1) + dp(i - 1, j)
            else:
                memo[(i, j)] = dp(i - 1, j)

            return memo[(i, j)]

        return dp(len(s) - 1, len(t) - 1)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**. As in Edit Distance, the memo uses `-1` for "used up", so shift every index by one: **memo index `i` is table row `i + 1`**, and row/column `0` means "empty".

| Memoization | Tabulation |
|---|---|
| `memo` keyed by `(i, j)` | `dp[i][j]` = ways the first `j` chars of `t` appear in the first `i` chars of `s` |
| `if j < 0: return 1` | first column: `dp[i][0] = 1` (empty target: one way) |
| `if i < 0: return 0` | first row: `dp[0][j] = 0` for `j > 0` (already the default) |
| match → `dp(i - 1, j - 1) + dp(i - 1, j)` | `dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]` |
| mismatch → `dp(i - 1, j)` | `dp[i][j] = dp[i - 1][j]` |
| `dp(i, j)` asks for **smaller** indexes | loop `i` and `j` **upward** from 1 |
| `return dp(len(s) - 1, len(t) - 1)` | `return dp[m][n]` |

**Loop-order rule:** the memo asks for smaller indexes, so fill the table from the top-left.

```python
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        m, n = len(s), len(t)
        # Base case guard: If t is longer than s, it's impossible to form t
        if n > m:
            return 0

        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Base Case: An empty target string t (j = 0) can be formed in exactly 1 way (by deleting all chars in s)
        for i in range(m + 1):
            dp[i][0] = 1

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if s[i - 1] == t[j - 1]:
                    # Match: dp[i-1][j-1] (use s[i-1]) + dp[i-1][j] (skip s[i-1])
                    dp[i][j] = dp[i - 1][j - 1] + dp[i - 1][j]
                else:
                    # Mismatch: dp[i-1][j] (skip s[i-1])
                    dp[i][j] = dp[i - 1][j]

        return dp[m][n]
```

**Shrink to one row:** row `i` only reads row `i - 1` at `j - 1` and `j`. Loop `j` **downward** so `dp[j - 1]` is still the old row when it is used.

```python
class Solution:
    def numDistinct(self, s: str, t: str) -> int:
        m, n = len(s), len(t)
        if n > m:
            return 0

        # dp[j] stores the number of ways to form t[0...j-1]
        dp = [0] * (n + 1)
        dp[0] = 1  # Base Case: Empty target string t has 1 way

        for i in range(1, m + 1):
            # Iterate backwards to avoid overwriting values needed for the current iteration
            for j in range(n, 0, -1):
                if s[i - 1] == t[j - 1]:
                    dp[j] = dp[j] + dp[j - 1]

        return dp[n]
```

## 4. Dry Run (`s = "babgbag"`, `t = "bag"`)

Table cell `(i, j)`: the number of ways the first `j` letters of `bag` appear in the first `i` letters of `babgbag`. It equals the memo's `dp(i - 1, j - 1)`.

```text
          ""   b   a   g
   ""      1   0   0   0
   b       1   1   0   0
   a       1   1   1   0
   b       1   2   1   0
   g       1   2   1   1
   b       1   3   1   1
   a       1   3   4   1
   g       1   3   4   5
```

The answer is `5`. For example, the last `g` matches `t[2]`, so the count is `4` (using it, from `"ba"` inside the first six letters) plus `1` (skipping it).

## 5. Complexity

* **States:** `memo` is keyed by `(i, j)`, so at most `m × n` entries.
* **Time:** O(m × n) — each pair is solved once, and each solve is one addition of two known values.
* **Space:** O(m × n) — the memo plus recursion up to `m + n` deep (for long strings use the table, since Python's default recursion limit is 1000). The one-row table is O(n).

## 6. Recall (30 seconds)

* **State:** `dp(i, j)` = ways `t[:j + 1]` appears as a subsequence of `s[:i + 1]`.
* **Transition:** match → `dp(i - 1, j - 1) + dp(i - 1, j)`; mismatch → `dp(i - 1, j)`; `dp(·, -1) = 1`, `dp(-1, ·) = 0`.
* **One-row table:** loop `j` **downward** so `dp[j - 1]` still holds the previous row.
