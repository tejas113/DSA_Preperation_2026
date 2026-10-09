# 05. Decode Ways

**LC 91** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** 1D DP / String Counting

---

## 1. Intuition

Digits map to letters (`1 → A` ... `26 → Z`). Standing at position `i`, you can read **one digit** (if it isn't `0`) or **two digits** (if they form 10–26), then decode whatever is left. So the ways to decode `s[i:]` are the ways after each possible reading, added together.

* `dp(i)` — the number of ways to decode the suffix `s[i:]`.
* `if i == len(s): return 1` — the whole string has been consumed, which is one complete decoding.
* `if s[i] == "0": return 0` — a `0` cannot start a code, so this path is dead. (A `0` is only valid as the second digit of `10` or `20`, and the previous step already consumed it.)
* `ans = dp(i+1)` — read one digit, then decode the rest.
* the `if i + 1 < len(s) and (...)` line — read two digits when they form 10–26 (`"1"` followed by anything, or `"2"` followed by `0–6`), then add `dp(i+2)` to `ans`.
* `memo[i]` — different readings can land on the same index, so each suffix is solved once.

**Recall:** `dp(i) = dp(i + 1) + dp(i + 2)`, where the second term counts only if `s[i:i+2]` is 10–26.

## 2. Template

* **State:** `dp(i)` = number of ways to decode `s[i:]`
* **Choice:** read one digit, or read two digits
* **Recurrence:** `dp(i) = dp(i + 1) + dp(i + 2)`, the second term only when the two digits form 10–26
* **Base:** `dp(len(s)) = 1`; `dp(i) = 0` when `s[i] == "0"`
* **Guard:** the two-digit read needs `i + 1 < len(s)`

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def numDecodings(self, s: str) -> int:

        memo = {}

        def dp(i):
            if i == len(s):
                return 1

            if s[i] == "0":
                return 0

            if i in memo:
                return memo[i]

            ans = dp(i+1)

            if i + 1 < len(s) and (s[i] == "1" or (s[i] =="2" and s[i+1] <= "6")):
                ans = ans + dp(i+2)

            memo[i] = ans 

            return memo[i]

        return dp(0)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo = {}` (keyed by `i`) | `dp = [0] * (n + 1)` (one slot per position `0..n`) |
| `if i == len(s): return 1` | `dp[n] = 1` |
| `if s[i] == "0": return 0` | `dp[i] = 0` and move on |
| `ans = dp(i+1)` | `dp[i] = dp[i + 1]` |
| `ans = ans + dp(i+2)` (when valid) | `dp[i] += dp[i + 2]` |
| `dp(i)` asks for **larger** positions | `for i in range(n - 1, -1, -1)` — fill from the end backward |
| `return dp(0)` | `return dp[0]` |

**Loop-order rule:** this time the memo asks for larger indexes (`i + 1`, `i + 2`), so the table is filled from the back, the opposite direction from Climbing Stairs. The rule is the same: fill what the recursion asks for first.

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        n = len(s)
        dp = [0] * (n + 1)
        dp[n] = 1                          # base: end of string = one way

        for i in range(n - 1, -1, -1):
            if s[i] == "0":
                dp[i] = 0                  # a leading zero cannot be decoded
                continue
            dp[i] = dp[i + 1]              # take 1 digit
            if i + 1 < n and (s[i] == "1" or (s[i] == "2" and s[i + 1] <= "6")):
                dp[i] += dp[i + 2]         # take 2 digits

        return dp[0]
```

**Shrink to O(1) space:** `dp[i]` only reads `dp[i + 1]` and `dp[i + 2]`, so keep two variables (`nxt` and `nxt2`) and slide them backward.

```python
class Solution:
    def numDecodings(self, s: str) -> int:
        nxt, nxt2 = 1, 0                   # dp[i + 1], dp[i + 2]  (dp[n] = 1)

        for i in range(len(s) - 1, -1, -1):
            if s[i] == "0":
                cur = 0
            else:
                cur = nxt
                if i + 1 < len(s) and (s[i] == "1" or (s[i] == "2" and s[i + 1] <= "6")):
                    cur += nxt2
            nxt2, nxt = nxt, cur

        return nxt
```

## 4. Dry Run (`s = "226"`)

```text
dp(0) = 3                                 "226"
├─ take "2"  → dp(1) = 2
│   ├─ take "2"  → dp(2) = 1
│   │   └─ take "6"  → dp(3) = 1        (base: end of string)
│   └─ take "26" → dp(3) = 1            (base: end of string)
└─ take "22" → dp(2) = 1                (cached — not recomputed)
```

The three decodings: `2|2|6`, `2|26`, `22|6`.

## 5. Complexity

* **States:** `memo` is keyed by the index `i`, so at most `n` entries.
* **Time:** O(n) — each index is solved once, and each solve makes at most two calls and a couple of O(1) checks.
* **Space:** O(n) — the memo holds about `n` entries and the recursion goes `n` deep. Tabulation is O(n) too; the two-variable version is O(1).

## 6. Recall (30 seconds)

* **State:** `dp(i)` = ways to decode `s[i:]`.
* **Transition:** `dp(i + 1)` (one digit) plus `dp(i + 2)` (two digits, only if 10–26); `dp(n) = 1`.
* **Pitfall:** a `0` can't stand alone, so `s[i] == "0"` means 0 ways (`"06"` → 0).
