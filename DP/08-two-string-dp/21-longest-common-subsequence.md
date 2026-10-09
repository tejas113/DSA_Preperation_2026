# 21. Longest Common Subsequence

**LC 1143** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** 2D DP / Two Strings

---

## 1. Intuition

Compare the two strings from the front, one pair of characters at a time. If the current characters **match**, that character can safely be part of the answer: count it and move both pointers forward. If they **don't match**, they can't both be used at this step, so drop one of them (move either pointer) and take whichever choice gives the longer result.

* `dp(i, j)` — the LCS length of `text1[i:]` and `text2[j:]`.
* `if i == len(text1) or j == len(text2): return 0` — one string is used up, so nothing more is in common.
* `text1[i] == text2[j]` → `1 + dp(i + 1, j + 1)` — matching characters are paired: +1, and both pointers advance.
* else `max(dp(i + 1, j), dp(i, j + 1))` — skip a character from `text1` or from `text2`, and keep the better result.
* `memo[(i, j)]` — many skip sequences reach the same `(i, j)`, so each pair is solved once.

**Recall:** match → `1 + dp(i + 1, j + 1)`; mismatch → `max(dp(i + 1, j), dp(i, j + 1))`.

## 2. Template

* **State:** `dp(i, j)` = LCS length of `text1[i:]` and `text2[j:]`
* **Choice:** if the characters match, pair them; if not, skip one from either string
* **Recurrence:** match → `1 + dp(i + 1, j + 1)`; mismatch → `max(dp(i + 1, j), dp(i, j + 1))`
* **Base:** `dp(len(text1), ·) = dp(·, len(text2)) = 0`
* **Guard:** none — the base case stops both pointers at the string ends

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        memo = {}

        def dp(i: int, j: int) -> int:
            if i == len(text1) or j == len(text2):
                return 0

            if (i, j) in memo:
                return memo[(i, j)]

            if text1[i] == text2[j]:
                memo[(i, j)] = 1 + dp(i + 1, j + 1)
            else:
                memo[(i, j)] = max(dp(i + 1, j), dp(i, j + 1))

            return memo[(i, j)]

        return dp(0, 0)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo` keyed by `(i, j)` | `dp[i][j]`, sized `(m + 1) × (n + 1)` |
| `if i == len(text1) or j == len(text2): return 0` | the last row and last column stay `0` |
| match → `1 + dp(i + 1, j + 1)` | `dp[i][j] = 1 + dp[i + 1][j + 1]` |
| mismatch → `max(dp(i + 1, j), dp(i, j + 1))` | `dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])` |
| `dp(i, j)` asks for **larger** `i` and `j` | loop `i` and `j` **downward** from `m - 1` and `n - 1` |
| `return dp(0, 0)` | `return dp[0][0]` |

**Loop-order rule:** the memo asks for larger indexes (`i + 1`, `j + 1`), so fill the table from the bottom-right toward the top-left.

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]       # last row and column stay 0 (the base case)

        for i in range(m - 1, -1, -1):
            for j in range(n - 1, -1, -1):
                if text1[i] == text2[j]:
                    dp[i][j] = 1 + dp[i + 1][j + 1]
                else:
                    dp[i][j] = max(dp[i + 1][j], dp[i][j + 1])

        return dp[0][0]
```

**Shrink to two rows:** row `i` only reads row `i + 1` and its own right neighbour, so keep just `prev` (row `i + 1`) and `curr` (row `i`).

```python
class Solution:
    def longestCommonSubsequence(self, text1: str, text2: str) -> int:
        m, n = len(text1), len(text2)
        prev = [0] * (n + 1)                              # row i + 1

        for i in range(m - 1, -1, -1):
            curr = [0] * (n + 1)                          # row i
            for j in range(n - 1, -1, -1):
                if text1[i] == text2[j]:
                    curr[j] = 1 + prev[j + 1]
                else:
                    curr[j] = max(prev[j], curr[j + 1])
            prev = curr

        return prev[0]
```

The space is O(n); put the **shorter** string as `text2` to get O(min(m, n)). The textbook version builds the same table from the front (`dp[i][j]` = LCS of the first `i` and `j` characters, loops upward); it is a mirror image with the same answer.

## 4. Dry Run (`text1 = "abcde"`, `text2 = "ace"`)

The memo's values `dp(i, j)` for every pair. Each row is a suffix of `text1` and each column a suffix of `text2`:

```text
              a   c   e   ""
     a  [     3   2   1   0 ]
     b  [     2   2   1   0 ]
     c  [     2   2   1   0 ]
     d  [     1   1   1   0 ]
     e  [     1   1   1   0 ]
    ""  [     0   0   0   0 ]
```

`dp(0, 0) = 3`: `'a'` matches (`1 + dp(1, 1)`), and the LCS is `"ace"`.

## 5. Complexity

* **States:** `memo` is keyed by `(i, j)`, so at most `m × n` entries.
* **Time:** O(m × n) — each pair is solved once, and each solve is O(1): a comparison and at most one `max`.
* **Space:** O(m × n) — the memo plus recursion up to `m + n` deep (for long strings use the table, since Python's default recursion limit is 1000). The two-row table is O(n).

## 6. Recall (30 seconds)

* **State:** `dp(i, j)` = LCS of `text1[i:]` and `text2[j:]`.
* **Transition:** match → `1 + dp(i + 1, j + 1)`; mismatch → `max(dp(i + 1, j), dp(i, j + 1))`.
* **Table:** loops go **downward**, and you only need the previous row for O(n) space.
