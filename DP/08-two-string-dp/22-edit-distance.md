# 22. Edit Distance

**LC 72** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** 2D DP / Two Strings (Levenshtein)

---

## 1. Intuition

You turn `word1` into `word2` with the fewest inserts, deletes and replaces. Walk both words from the **front** with two pointers. If the current characters match, no edit is needed there: move both pointers forward. If they don't match, you pay 1 for the cheapest of three edits and then continue on what's left.

* `dp(i, j)` — the fewest edits to turn the suffix `word1[i:]` into the suffix `word2[j:]`.
* `if i == len(word1): return len(word2) - j` — `word1` is used up, so insert all `len(word2) - j` remaining characters of `word2`.
* `if j == len(word2): return len(word1) - i` — `word2` is used up, so delete all `len(word1) - i` remaining characters of `word1`.
* `word1[i] == word2[j]` → `dp(i+1, j+1)` — the current characters already match; free, and both pointers advance.
* `insert = dp(i, j+1)` — insert `word2[j]` in front of `word1[i]`, so it now matches; `j` advances, `i` stays.
* `delete = dp(i+1, j)` — delete `word1[i]`; `i` advances, `j` stays.
* `replace = dp(i+1, j+1)` — change `word1[i]` into `word2[j]`; both advance.
* `1 + min(insert,delete,replace)` — pay for one edit, choosing the cheapest.
* `memo[(i,j)]` — many edit sequences reach the same `(i, j)`, so each is solved once.

**Recall:** match → `dp(i + 1, j + 1)`; mismatch → `1 + min(insert, delete, replace)`.

## 2. Template

* **State:** `dp(i, j)` = fewest edits to turn `word1[i:]` into `word2[j:]`
* **Choice:** if the current characters match, pair them; otherwise insert, delete or replace
* **Recurrence:** match → `dp(i + 1, j + 1)`; mismatch → `1 + min(dp(i, j + 1), dp(i + 1, j), dp(i + 1, j + 1))`
* **Base:** `dp(len(word1), j) = len(word2) - j` and `dp(i, len(word2)) = len(word1) - i`
* **Guard:** an index equal to the word's length means that word is used up; both base cases come before the memo check

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def minDistance(self, word1: str, word2: str) -> int:

        memo = {}

        def dp(i, j):
            if i == len(word1):
                return len(word2) - j

            if j == len(word2):
                return len(word1) - i

            if (i, j) in memo:
                return memo[(i, j)]

            if word1[i] == word2[j]:
                memo[(i, j)] = dp(i + 1, j + 1)
            else:
                insert = dp(i, j + 1)
                delete = dp(i + 1, j)
                replace = dp(i + 1, j + 1)

                memo[(i, j)] = 1 + min(insert, delete, replace)

            return memo[(i, j)]

        return dp(0, 0)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**. The memo works on **suffixes** (`word1[i:]`, `word2[j:]`). The usual table is its mirror image on **prefixes**: `dp[i][j]` uses the first `i` chars of `word1` and the first `j` chars of `word2`. It's the same recurrence with the direction flipped, and the answer is the same.

| Memoization (suffixes) | Tabulation (prefixes) |
|---|---|
| `memo` keyed by `(i, j)` | `dp[i][j]` = edits between the first `i` chars of `word1` and the first `j` chars of `word2` |
| `if i == len(word1): return len(word2) - j` (nothing left of `word1`) | first row: `dp[0][j] = j` (insert `j` characters) |
| `if j == len(word2): return len(word1) - i` (nothing left of `word2`) | first column: `dp[i][0] = i` (delete `i` characters) |
| match → `dp(i + 1, j + 1)` | `dp[i][j] = dp[i - 1][j - 1]` |
| mismatch → `1 + min(insert, delete, replace)` | `1 + min(dp[i][j - 1], dp[i - 1][j], dp[i - 1][j - 1])` |
| `dp(i, j)` asks for **larger** indexes | the mirrored table asks for **smaller** ones, so loop `i` and `j` **upward** from 1 |
| `return dp(0, 0)` | `return dp[m][n]` |

**Loop-order rule:** the prefix table asks for smaller indexes, so fill it from the top-left.

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

The table cell `(i, j)` is the edit distance between the first `i` letters of `horse` and the first `j` letters of `ros`. This is the prefix table, so it's the mirror image of the memo. The bottom-right cell is the memo's `dp(0, 0)`:

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

* **State:** `dp(i, j)` = fewest edits to turn `word1[i:]` into `word2[j:]`.
* **Transition:** match → `dp(i + 1, j + 1)`; mismatch → `1 + min(dp(i, j + 1), dp(i + 1, j), dp(i + 1, j + 1))`; bases `len(word2) - j` and `len(word1) - i`.
* **Table:** the usual prefix table is the mirror image; row/column 0 hold the base cases, and loops go upward.
