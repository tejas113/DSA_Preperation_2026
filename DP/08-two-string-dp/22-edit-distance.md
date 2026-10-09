# 22. Edit Distance

**LC 72** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** 2D DP / Two Strings (Levenshtein)

---

## 1. Intuition

You turn `word1` into `word2` with the fewest inserts, deletes and replaces. Line the two words up and compare their **last** characters. If they match, no edit is needed there: shrink both words. If they don't match, you pay 1 for the cheapest of three edits and then continue on what's left.

* `dp(i, j)` — the fewest edits to turn `word1[:i + 1]` into `word2[:j + 1]`.
* `if i < 0: return j + 1` — `word1` is used up, so insert all `j + 1` remaining characters of `word2`.
* `if j < 0: return i + 1` — `word2` is used up, so delete all `i + 1` remaining characters of `word1`.
* `word1[i] == word2[j]` → `dp(i - 1, j - 1)` — the last characters already match; free, and both words shrink.
* `insert = dp(i, j - 1)` — insert `word2[j]` at the end of `word1`, so it now matches; then `word2` shrinks by one.
* `delete = dp(i - 1, j)` — delete `word1[i]`; then `word1` shrinks by one.
* `replace = dp(i - 1, j - 1)` — change `word1[i]` into `word2[j]`; both shrink by one.
* `1 + min(...)` — pay for one edit, choosing the cheapest.
* `memo[(i, j)]` — many edit sequences reach the same `(i, j)`, so each is solved once.

**Recall:** match → `dp(i - 1, j - 1)`; mismatch → `1 + min(insert, delete, replace)`.

## 2. Template

* **State:** `dp(i, j)` = fewest edits to turn `word1[:i + 1]` into `word2[:j + 1]`
* **Choice:** if the last characters match, pair them; otherwise insert, delete or replace
* **Recurrence:** match → `dp(i - 1, j - 1)`; mismatch → `1 + min(dp(i, j - 1), dp(i - 1, j), dp(i - 1, j - 1))`
* **Base:** `dp(-1, j) = j + 1` and `dp(i, -1) = i + 1`
* **Guard:** an index of `-1` means that word is used up

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        memo = {}

        def dp(i, j):
            # Base Case 1: word1 exhausted -> insert remaining characters of word2
            if i < 0:
                return j + 1
            
            # Base Case 2: word2 exhausted -> delete remaining characters of word1
            if j < 0:
                return i + 1

            if (i, j) in memo:
                return memo[(i, j)]

            if word1[i] == word2[j]:
                memo[(i, j)] = dp(i - 1, j - 1)
            else:
                insert = dp(i, j - 1)
                delete = dp(i - 1, j)
                replace = dp(i - 1, j - 1)

                memo[(i, j)] = 1 + min(insert, delete, replace)

            return memo[(i, j)]

        return dp(len(word1) - 1, len(word2) - 1)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**. One detail: the memo uses `-1` for "used up", but a table can't have index `-1`. So shift every index by one: **memo index `i` is table row `i + 1`**, and row/column `0` means "empty word".

| Memoization | Tabulation |
|---|---|
| `memo` keyed by `(i, j)` | `dp[i][j]` = edits between the first `i` chars of `word1` and the first `j` chars of `word2` |
| `if i < 0: return j + 1` | first row: `dp[0][j] = j` (insert `j` characters) |
| `if j < 0: return i + 1` | first column: `dp[i][0] = i` (delete `i` characters) |
| match → `dp(i - 1, j - 1)` | `dp[i][j] = dp[i - 1][j - 1]` |
| mismatch → `1 + min(insert, delete, replace)` | `1 + min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])` |
| `dp(i, j)` asks for **smaller** indexes | loop `i` and `j` **upward** from 1 |
| `return dp(len(word1) - 1, len(word2) - 1)` | `return dp[m][n]` |

**Loop-order rule:** the memo asks for smaller indexes, so fill the table from the top-left.

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        dp = [[0] * (n + 1) for _ in range(m + 1)]

        # Base Cases: Empty string comparisons
        for i in range(m + 1):
            dp[i][0] = i  # Deletions
        for j in range(n + 1):
            dp[0][j] = j  # Insertions

        for i in range(1, m + 1):
            for j in range(1, n + 1):
                if word1[i - 1] == word2[j - 1]:
                    dp[i][j] = dp[i - 1][j - 1]
                else:
                    dp[i][j] = 1 + min(
                        dp[i][j - 1],     # Insert
                        dp[i - 1][j],     # Delete
                        dp[i - 1][j - 1]  # Replace
                    )

        return dp[m][n]
```

**Shrink to one row:** row `i` only reads row `i - 1` and its own left neighbour. Keep one array; `prev` remembers the top-left value that the update is about to overwrite.

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:
        m, n = len(word1), len(word2)
        dp = list(range(n + 1))  # Equivalent to dp[0][j] = j

        for i in range(1, m + 1):
            prev = dp[0]  # Stores dp[i-1][j-1] (top-left element)
            dp[0] = i     # Base case dp[i][0] = i

            for j in range(1, n + 1):
                temp = dp[j]  # Current dp[i-1][j] before overwrite
                if word1[i - 1] == word2[j - 1]:
                    dp[j] = prev
                else:
                    dp[j] = 1 + min(dp[j - 1], dp[j], prev)
                prev = temp

        return dp[n]
```

## 4. Dry Run (`word1 = "horse"`, `word2 = "ros"`)

The table cell `(i, j)` is the edit distance between the first `i` letters of `horse` and the first `j` letters of `ros`, which equals the memo's `dp(i - 1, j - 1)`:

```text
          ""   r   o   s
   ""      0   1   2   3
   h       1   1   2   3
   o       2   2   1   2
   r       3   2   2   2
   s       4   3   3   2
   e       5   4   4   3
```

The answer is `3`: `horse → rorse` (replace `h`), `rorse → rose` (delete `r`), `rose → ros` (delete `e`).

## 5. Complexity

* **States:** `memo` is keyed by `(i, j)`, so at most `m × n` entries.
* **Time:** O(m × n) — each pair is solved once, and each solve is a comparison and one `min` of three known values.
* **Space:** O(m × n) — the memo plus recursion up to `m + n` deep (for long words use the table, since Python's default recursion limit is 1000). The one-row table is O(n).

## 6. Recall (30 seconds)

* **State:** `dp(i, j)` = fewest edits to turn `word1[:i + 1]` into `word2[:j + 1]`.
* **Transition:** match → `dp(i - 1, j - 1)`; mismatch → `1 + min(insert, delete, replace)`; bases `j + 1` and `i + 1`.
* **Table:** indexes shift by one (memo `i` = table row `i + 1`), and row/column 0 hold the base cases.
