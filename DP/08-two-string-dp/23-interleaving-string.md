# 23. Interleaving String

**LC 97** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** 2D DP / Two Strings (one target)

---

## 1. Intuition

Can `s3` be built by weaving `s1` and `s2` together while keeping each string's own order? Read `s3` from the front. At each step the next character of `s3` must come from the next unused character of `s1` **or** the next unused character of `s2`. The state is just how many characters of each string you have used, `(i, j)`, and the position in `s3` is always `i + j`, so no third index is needed.

* `if len(s1) + len(s2) != len(s3): return False` — the lengths must add up, or it is impossible.
* `dp(i, j)` — can `s1[i:]` and `s2[j:]` be interleaved to form `s3[i + j:]`?
* `if i >= len(s1) and j >= len(s2): return True` — both strings are used up, so `s3` was built completely.
* `if i < len(s1) and s1[i] == s3[i + j]: ans = ans or dp(i + 1, j)` — take the next character from `s1` if it matches `s3`.
* `if j < len(s2) and s2[j] == s3[i + j]: ans = ans or dp(i, j + 1)` — take it from `s2` if it matches.
* `ans or ...` — either source working is enough. Both may match, so both are tried.
* `memo[(i, j)]` — different weaves reach the same `(i, j)`, so each is solved once.

**Recall:** `dp(i, j)` = take from `s1` (if it matches `s3[i + j]`) **or** from `s2`; `s3`'s position is `i + j`.

## 2. Template

* **State:** `dp(i, j)` = can `s1[i:]` and `s2[j:]` interleave into `s3[i + j:]`
* **Choice:** take the next character from `s1`, or from `s2`
* **Recurrence:** `dp(i, j) = (s1[i] == s3[i + j] and dp(i + 1, j)) or (s2[j] == s3[i + j] and dp(i, j + 1))`
* **Base:** `i == len(s1)` and `j == len(s2)` → `True`
* **Guard:** check `len(s1) + len(s2) == len(s3)` first, and bounds-check `i` and `j` before indexing

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        if len(s1) + len(s2) != len(s3):
            return False

        memo = {}

        def dp(i: int, j: int) -> bool:
            # Base Case: Both s1 and s2 are fully traversed
            if i >= len(s1) and j >= len(s2):
                return True

            if (i, j) in memo:
                return memo[(i, j)]

            ans = False

            # Branch 1: Take character from s1
            if i < len(s1) and s1[i] == s3[i + j]:
                ans = ans or dp(i + 1, j)

            # Branch 2: Take character from s2
            if j < len(s2) and s2[j] == s3[i + j]:
                ans = ans or dp(i, j + 1)

            memo[(i, j)] = ans
            return memo[(i, j)]

        return dp(0, 0)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo` keyed by `(i, j)` | `dp[i][j]`, sized `(m + 1) × (n + 1)` |
| `if i >= len(s1) and j >= len(s2): return True` | `dp[m][n] = True` |
| branch 1: `i < len(s1) and s1[i] == s3[i + j]` then `dp(i + 1, j)` | `i < m and s1[i] == s3[k] and dp[i + 1][j]`, with `k = i + j` |
| branch 2: `j < len(s2) and s2[j] == s3[i + j]` then `dp(i, j + 1)` | `j < n and s2[j] == s3[k] and dp[i][j + 1]` |
| `ans = ans or ...` | `dp[i][j] = take_s1 or take_s2` |
| `dp(i, j)` asks for **larger** `i` and `j` | loop `i` and `j` **downward** from `m` and `n` |
| `return dp(0, 0)` | `return dp[0][0]` |

**Loop-order rule:** the memo asks for `(i + 1, j)` and `(i, j + 1)`, so fill from the bottom-right toward the top-left. The length check stays before the loops.

```python
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        m, n = len(s1), len(s2)
        if m + n != len(s3):
            return False

        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[m][n] = True                                   # base: both strings used up

        for i in range(m, -1, -1):
            for j in range(n, -1, -1):
                if i == m and j == n:
                    continue
                k = i + j                                 # position in s3
                take_s1 = i < m and s1[i] == s3[k] and dp[i + 1][j]
                take_s2 = j < n and s2[j] == s3[k] and dp[i][j + 1]
                dp[i][j] = take_s1 or take_s2

        return dp[0][0]
```

**Shrink to one row** (the follow-up asks for O(`len(s2)`) space): row `i` only reads row `i + 1` and its own right neighbour. Before `dp[j]` is overwritten it still holds row `i + 1`, and `dp[j + 1]` already holds row `i`.

```python
class Solution:
    def isInterleave(self, s1: str, s2: str, s3: str) -> bool:
        m, n = len(s1), len(s2)
        if m + n != len(s3):
            return False

        dp = [False] * (n + 1)                            # dp[j]: row i (before it's updated, row i + 1)
        for i in range(m, -1, -1):
            for j in range(n, -1, -1):
                if i == m and j == n:
                    dp[j] = True
                    continue
                k = i + j
                take_s1 = i < m and s1[i] == s3[k] and dp[j]            # dp[j] is still row i + 1
                take_s2 = j < n and s2[j] == s3[k] and dp[j + 1]        # dp[j + 1] is already row i
                dp[j] = take_s1 or take_s2

        return dp[0]
```

## 4. Dry Run (`s1 = "aab"`, `s2 = "axy"`, `s3 = "aaxaby"`)

The memo's values `dp(i, j)`. Rows are suffixes of `s1`, columns are suffixes of `s2`:

```text
              j=0     j=1    j=2    j=3
             "axy"   "xy"    "y"    ""
i=0  "aab"     T       T      F      F
i=1  "ab"      T       T      T      F
i=2  "b"       F       F      T      F
i=3  ""        F       F      T      T
```

`dp(0, 0) = True`, so `"aaxaby"` can be woven from `"aab"` and `"axy"`.

## 5. Complexity

* **States:** `memo` is keyed by `(i, j)`, so at most `(m + 1) × (n + 1)` entries. The `s3` position is `i + j`, so it adds no dimension.
* **Time:** O(m × n) — each `(i, j)` is solved once, and each solve is two O(1) checks.
* **Space:** O(m × n) — the memo plus recursion up to `m + n` deep. The one-row table is O(n).

## 6. Recall (30 seconds)

* **State:** `dp(i, j)` = can `s1[i:]` and `s2[j:]` weave into `s3[i + j:]`; the `s3` index is always `i + j`.
* **Transition:** `(s1[i] == s3[i + j] and dp(i + 1, j)) or (s2[j] == s3[i + j] and dp(i, j + 1))`.
* **Guard:** return `False` immediately if `len(s1) + len(s2) != len(s3)`.
