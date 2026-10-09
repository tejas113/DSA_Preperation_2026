# 19. Longest Palindromic Substring

**LC 5** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Expand Around Center (with a DP view)

---

## 1. Intuition

Every palindrome is symmetric around a **center**. The center is either a single character (odd length, like `aba`) or the gap between two characters (even length, like `abba`). So try every center and expand outward as long as the two ends match. A string of length `n` has `2n - 1` centers: `n` characters and `n - 1` gaps. Keep the longest palindrome found.

* `expand(left, right)` — starts at a center and moves the two pointers outward while `s[left] == s[right]`.
* `return s[left + 1:right]` — the loop stops one step **past** the palindrome, so the palindrome is `s[left + 1 : right]`.
* `expand(i, i)` — odd-length palindromes, with the center on character `i`.
* `expand(i, i + 1)` — even-length palindromes, with the center in the gap between `i` and `i + 1`.
* `if len(odd) > res_len` — keep only the longest; the strict `>` keeps the earliest one when there is a tie.

**Recall:** for each of the `2n - 1` centers, expand outward while the ends match; keep the longest.

## 2. Template

* **State:** a center, either a character (odd) or the gap between two characters (even)
* **Choice:** expand one step outward on each side while the two characters match
* **Recurrence:** `s[left] == s[right]` → `left -= 1`, `right += 1`
* **Base:** start with `left = right = i` (odd) or `left = i, right = i + 1` (even)
* **Guard:** stop at the string ends, `left >= 0 and right < len(s)`

## 3. Code

**Expand around center** (primary solution). It uses O(1) extra space. It is the DP fact `is_pal(i, j) = s[i] == s[j] and is_pal(i + 1, j - 1)` run from the middle outward, so nothing needs storing.

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        res = ""
        res_len = 0

        def expand(left: int, right: int) -> str:
            while left >= 0 and right < len(s) and s[left] == s[right]:
                left -= 1
                right += 1
            return s[left + 1:right]

        for i in range(len(s)):
            # Odd length palindromes (e.g., "a", "aba")
            odd = expand(i, i)
            if len(odd) > res_len:
                res = odd
                res_len = len(odd)

            # Even length palindromes (e.g., "aa", "abba")
            even = expand(i, i + 1)
            if len(even) > res_len:
                res = even
                res_len = len(even)

        return res
```

### Alternative: DP table (memoization, then tabulation)

Look at every span `s[i..j]` and ask "is it a palindrome?": its two ends must match and the span **inside** must also be a palindrome. That is a 2D DP over `(i, j)`.

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        memo = {}

        def is_pal(i: int, j: int) -> bool:
            # Base: an empty or single-character span is a palindrome
            if i >= j:
                return True
            if (i, j) in memo:
                return memo[(i, j)]

            memo[(i, j)] = s[i] == s[j] and is_pal(i + 1, j - 1)
            return memo[(i, j)]

        res = ""
        for i in range(n):
            for j in range(i, n):
                if j - i + 1 > len(res) and is_pal(i, j):
                    res = s[i:j + 1]

        return res
```

Four moves turn that memo into a table: **cache → array**, **base cases → starting values**, **recursion direction → loop direction**, **calls → lookups**.

| Memoization | Tabulation |
|---|---|
| `memo[(i, j)]` = "is `s[i..j]` a palindrome" | `dp[i][j]`, an `n × n` boolean table |
| `if i >= j: return True` | `dp[i][i] = True`; the `j - i <= 2` shortcut covers lengths 2 and 3, where the inside is empty or one character |
| `s[i] == s[j] and is_pal(i + 1, j - 1)` | `s[i] == s[j] and (j - i <= 2 or dp[i + 1][j - 1])` |
| `is_pal(i, j)` asks for the **inner** span `(i + 1, j - 1)` | `i` goes from `n - 1` down to 0, `j` ascends, so row `i + 1` is already filled |
| the `res` tracking | `start` and `max_len` tracking |

**Loop-order rule:** the memo asks for the shorter span inside, so fill the table with the last rows first (`i` descending).

```python
class Solution:
    def longestPalindrome(self, s: str) -> str:
        n = len(s)
        dp = [[False] * n for _ in range(n)]
        start, max_len = 0, 1

        for i in range(n):
            dp[i][i] = True

        for i in range(n - 1, -1, -1):
            for j in range(i + 1, n):
                if s[i] == s[j] and (j - i <= 2 or dp[i + 1][j - 1]):
                    dp[i][j] = True
                    if j - i + 1 > max_len:
                        start = i
                        max_len = j - i + 1

        return s[start:start + max_len]
```

*Also worth knowing:* Manacher's algorithm finds every palindrome radius in O(n) time by reusing earlier radii; it is rarely needed in an interview.

## 4. Dry Run (`s = "babad"`)

Expansion from every center:

```text
"babad"
center 'b' (i=0)  → "b"
center 'a' (i=1)  → "a" → "bab"      ← best so far (length 3)
center 'b' (i=2)  → "b" → "aba"      (length 3, not longer, so keep "bab")
center 'a' (i=3)  → "a"
center 'd' (i=4)  → "d"
even centers (gaps): no two neighbours match, so nothing expands
```

The answer is `"bab"` (`"aba"` is equally valid).

## 5. Complexity

* **States:** there are `2n - 1` centers, and nothing is stored.
* **Time:** O(n²) — each of the `2n - 1` centers expands at most about `n / 2` steps, and each step is O(1) (the slice at the end costs O(n) once per center).
* **Space:** O(1) beyond the returned substring. The DP table version is O(n²) time and O(n²) space, since it stores one boolean per `(i, j)`.

## 6. Recall (30 seconds)

* **Idea:** every palindrome has a center (a character or a gap), and there are `2n - 1` of them; expand outward while the ends match.
* **Slice:** the loop overshoots by one, so return `s[left + 1:right]`.
* **DP view:** `is_pal(i, j) = s[i] == s[j] and is_pal(i + 1, j - 1)`; the table is O(n²) space, expand-around-center is O(1).
