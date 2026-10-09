# 25. Regular Expression Matching

**LC 10** · **Source:** NC150 · **Difficulty:** Hard · **Priority:** Core · **Pattern:** 2D DP / Two Strings (wildcard branching)

---

## 1. Intuition

Everything is ordinary two-string DP (`s` vs. the pattern `p`) except one thing: **`*` is bound to the character before it** and means "zero or more copies of it". So whenever the pattern character we stand on is **followed by `*`**, we face a real fork:

1. **Zero copies:** drop the whole `x*` pair and keep matching the rest of the pattern against the same spot in `s`, which is `dp(i, j + 2)`.
2. **One or more copies:** if the current character of `s` matches `x` (or `x` is `.`), consume that one character but **stay on the same `x*`** so it can match more, which is `dp(i + 1, j)`.

If the pattern character is **not** followed by `*`, it's a plain single-character match: the characters must match (or the pattern has `.`), then both pointers advance.

* `dp(i, j)` — does the suffix `s[i:]` fully match the suffix `p[j:]`?
* `if j == len(p): return i == len(s)` — the pattern is used up, so it matches only if `s` is used up too. (Returning `True` here without checking `s` is a classic bug.)
* `first_match = i < len(s) and p[j] in (s[i], '.')` — does the current character of `s` fit the current pattern character? The `i < len(s)` check guards the end of `s`.
* `if j + 1 < len(p) and p[j + 1] == '*'` — is the current pattern character followed by a star?
* `dp(i, j + 2) or (first_match and dp(i + 1, j))` — the fork: skip the `x*` pair, **or** eat one character and stay put.
* `first_match and dp(i + 1, j + 1)` — the no-star case: both pointers advance.
* `memo[(i, j)]` — many paths reach the same `(i, j)`, so each is solved once.

This "jump two places in the pattern" step is what no other two-string problem here has (LCS and Edit Distance only ever step by one).

**Recall:** with a `*` next: `dp(i, j + 2)` **or** `first_match and dp(i + 1, j)`; otherwise `first_match and dp(i + 1, j + 1)`.

## 2. Template

* **State:** `dp(i, j)` = does `s[i:]` fully match `p[j:]`
* **Choice:** if `p[j]` is followed by `*`, use it zero times or one more time; otherwise match one character
* **Recurrence:** star → `dp(i, j + 2) or (first_match and dp(i + 1, j))`; no star → `first_match and dp(i + 1, j + 1)`
* **Base:** `j == len(p)` → `i == len(s)`
* **Guard:** `first_match` includes `i < len(s)`, so `s[i]` is never read past the end

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        memo = {}

        def dp(i: int, j: int) -> bool:
            # Base Case: pattern exhausted -> match only if the string is exhausted too
            if j == len(p):
                return i == len(s)

            if (i, j) in memo:
                return memo[(i, j)]

            # Does the current character of s match the current pattern character?
            first_match = i < len(s) and p[j] in (s[i], '.')

            if j + 1 < len(p) and p[j + 1] == '*':
                # Fork: zero occurrences of p[j], OR one more occurrence (stay on the same x*)
                ans = dp(i, j + 2) or (first_match and dp(i + 1, j))
            else:
                # Plain single-character match: both pointers advance
                ans = first_match and dp(i + 1, j + 1)

            memo[(i, j)] = ans
            return ans

        return dp(0, 0)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo` keyed by `(i, j)` | `dp[i][j]`, sized `(m + 1) × (n + 1)` |
| `if j == len(p): return i == len(s)` | last column: `dp[m][n] = True` and `dp[i][n] = False` for `i < m` (already the default) |
| `first_match = i < len(s) and p[j] in (s[i], '.')` | the same expression, with `m` |
| star fork: `dp(i, j + 2) or (first_match and dp(i + 1, j))` | `dp[i][j + 2] or (first_match and dp[i + 1][j])` |
| no star: `first_match and dp(i + 1, j + 1)` | `first_match and dp[i + 1][j + 1]` |
| `dp(i, j)` asks for **larger** `i` and `j` | `i` from `m` down to `0`, `j` from `n - 1` down to `0` |
| `return dp(0, 0)` | `return dp[0][0]` |

**Loop-order rule:** the memo asks for `(i, j + 2)`, `(i + 1, j)` and `(i + 1, j + 1)`, so fill from the bottom-right toward the top-left. Columns that start on a `*` are never asked for and simply stay `False`.

```python
class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        m, n = len(s), len(p)
        dp = [[False] * (n + 1) for _ in range(m + 1)]
        dp[m][n] = True                                   # base: both used up

        for i in range(m, -1, -1):
            for j in range(n - 1, -1, -1):
                first_match = i < m and p[j] in (s[i], '.')
                if j + 1 < n and p[j + 1] == '*':
                    dp[i][j] = dp[i][j + 2] or (first_match and dp[i + 1][j])
                else:
                    dp[i][j] = first_match and dp[i + 1][j + 1]

        return dp[0][0]
```

The textbook version builds the same table from the front (prefix orientation) and needs a special row-0 initialisation for patterns like `a*b*` (an empty string can match them). The suffix version above needs no such special case.

## 4. Dry Run (`s = "aab"`, `p = "c*a*b"`)

The memo's values `dp(i, j)`. Rows are suffixes of `s`, columns are suffixes of `p`:

```text
                j=0       j=1      j=2     j=3    j=4    j=5
              "c*a*b"   "*a*b"    "a*b"   "*b"   "b"    ""
i=0  "aab"       T         F        T       F      F      F
i=1  "ab"        T         F        T       F      F      F
i=2  "b"         T         F        T       F      T      F
i=3  ""          F         F        F       F      F      T
```

`dp(0, 0) = True`. Reading it: `c*` is used **zero** times (`dp(0, 0) = dp(0, 2)`); then `a*` eats both `a`s (`dp(0, 2)` needs `dp(1, 2)`, which needs `dp(2, 2)`); finally `dp(2, 2)` uses `a*` zero times and reaches `dp(2, 4)`, where `b` matches `b`.

## 5. Complexity

* **States:** `memo` is keyed by `(i, j)`, so at most `(m + 1) × (n + 1)` entries.
* **Time:** O(m × n) — each pair is solved once, and each solve makes at most two recursive calls plus O(1) work.
* **Space:** O(m × n) — the memo plus recursion up to `m + n` deep. The table is O(m × n) too.

## 6. Recall (30 seconds)

* **State:** `dp(i, j)` = does `s[i:]` match `p[j:]`.
* **Star fork:** `dp(i, j + 2)` (zero copies) **or** `first_match and dp(i + 1, j)` (one more copy, stay on the same `x*`).
* **Base / pitfall:** pattern used up means `i == len(s)`; a `*` binds to the character **before** it.
