# 06. Word Break

**LC 139** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** 1D DP / String Segmentation

---

## 1. Intuition

Stand at position `start` (everything before it is already matched) and ask: does some dictionary word begin exactly here? If yes, take it. What remains is the shorter suffix that starts right after that word, and it is the same question again. Reaching the end of the string means everything was matched.

* `dp(start)` — can the suffix `s[start:]` be split into dictionary words?
* `if start == len(s): return True` — nothing is left to match, so the whole string was split successfully.
* `for w in words` with `s[start:start + word_length] == w` — try every word as the **next piece**. It has to fit (`start + word_length <= len(s)`) and match the text that begins at `start`.
* `dp(start+word_length)` — after taking that word, the rest of the string must also be splittable.
* `memo[start] = True` and return on the first success — one valid split is enough, so stop early.
* `memo[start] = False` after the loop — no word led anywhere. Caching `False` too means a dead-end suffix is never retried.

**Recall:** `dp(start)` is true if some word matches at `start` and `dp(start + len(word))` is true.

## 2. Template

* **State:** `dp(start)` = can `s[start:]` be segmented into dictionary words
* **Choice:** which dictionary word is the next piece
* **Recurrence:** `dp(start) = OR over words w that match at start of dp(start + len(w))`
* **Base:** `dp(len(s)) = True`
* **Guard:** check `start + word_length <= len(s)` before slicing

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:

        words = set(wordDict)
        memo = {}
        
        def dp(start):

            if start == len(s):
                return True

            if start in memo:
                return memo[start]

            for w in words:
                word_length = len(w)
                if start + word_length <= len(s) and s[start:start + word_length] == w:
                    if dp(start+word_length):
                        memo[start] = True
                        return memo[start]
            memo[start] = False
            return memo[start]
        return dp(0)
```

### Alternative: Tabulation

Four moves turn the memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo = {}` (keyed by `start`) | `dp = [False] * (n + 1)` (one slot per start position `0..n`) |
| `if start == len(s): return True` | `dp[n] = True` |
| `start + word_length <= len(s) and s[start:start + word_length] == w` | the same condition, now inside the loop |
| `if dp(start+word_length)` | `and dp[start + word_length]` |
| `memo[start] = True` and return | `dp[start] = True` and `break` |
| `dp(start)` asks for **larger** start positions | `for start in range(n - 1, -1, -1)` — fill from the end backward |
| `return dp(0)` | `return dp[0]` |

**Loop-order rule:** the memo asks for later start positions (`start + word_length`), so the table is filled from the back, the same direction as Decode Ways.

```python
class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> bool:
        words = set(wordDict)
        n = len(s)
        dp = [False] * (n + 1)
        dp[n] = True                        # base: reached the end of the string

        for start in range(n - 1, -1, -1):
            for w in words:
                word_length = len(w)
                if start + word_length <= n and s[start:start + word_length] == w and dp[start + word_length]:
                    dp[start] = True
                    break                   # one valid word is enough

        return dp[0]
```

## 4. Dry Run (`s = "leetcode"`, `wordDict = ["leet", "code"]`)

```text
dp(0) = True                                 "leetcode"
├─ word "leet": matches at 0 → dp(4) = True    remaining "code"
│   ├─ word "code": matches at 4 → dp(8) = True    (base: end of string)
│   └─ word "leet": s[4:8] = "code" ≠ "leet" → no
└─ word "code": s[0:4] = "leet" ≠ "code" → no
```

The order the words are tried in doesn't matter; each `dp(start)` returns `True` as soon as any word works.

## 5. Complexity

* **States:** `memo` is keyed by `start`, so at most `n` entries (`dp(len(s))` returns before touching it).
* **Time:** O(n · m · k) — each state loops over the `m` dictionary words, and each check slices and compares up to `k` characters (`k` = longest word).
* **Space:** O(n) — the memo holds about `n` entries and the recursion goes up to `n` deep. Tabulation is O(n) too.

## 6. Recall (30 seconds)

* **State:** `dp(start)` = can `s[start:]` be split into dictionary words.
* **Transition:** some word `w` matches at `start` and `dp(start + len(w))` is true; `dp(len(s)) = True`.
* **Pitfalls:** guard with `start + word_length <= len(s)` before slicing, and cache `False` too.
