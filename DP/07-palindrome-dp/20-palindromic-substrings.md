# 20. Palindromic Substrings

**LC 647** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Expand Around Center (with a DP view)

---

## 1. Intuition

Same idea as Longest Palindromic Substring, with a different question: instead of keeping the **longest** palindrome, **count every one**. Every palindrome has a center (a character, or the gap between two), and each step of a successful expansion is one more palindrome around that center.

* `expand(left, right)` — starts at a center and, each time `s[left] == s[right]`, counts one more palindrome (`count += 1`) before stepping outward.
* why each step counts — `s[left..right]` is a palindrome exactly when its ends match and everything inside already matched, so every successful step is a new palindrome.
* `expand(i, i)` — odd-length palindromes (`"a"`, `"aba"`, ...).
* `expand(i, i + 1)` — even-length palindromes (`"aa"`, `"abba"`, ...).
* `total_palindromes += ...` — sum the counts over all `2n - 1` centers.

**Recall:** for every center, count each successful expansion step.

## 2. Template

* **State:** a center, either a character (odd) or the gap between two characters (even)
* **Choice:** expand one step outward on each side while the two characters match
* **Recurrence:** each time `s[left] == s[right]`, `count += 1`, then `left -= 1` and `right += 1`
* **Base:** start with `left = right = i` (odd) or `left = i, right = i + 1` (even)
* **Guard:** stop at the string ends, `left >= 0 and right < n`

## 3. Code

**Expand around center** (primary solution).

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        total_palindromes = 0

        def expand(left: int, right: int) -> int:
            count = 0
            while left >= 0 and right < n and s[left] == s[right]:
                count += 1
                left -= 1
                right += 1
            return count

        for i in range(n):
            # Odd length palindromes (e.g., "a", "aba")
            total_palindromes += expand(i, i)
            # Even length palindromes (e.g., "aa", "abba")
            total_palindromes += expand(i, i + 1)

        return total_palindromes
```

### Alternative: DP table (memoization, then tabulation)

The DP view is the same as in Longest Palindromic Substring: a span `s[i..j]` is a palindrome when its ends match and the span inside is one too. Here you count every `(i, j)` that comes out true.

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        memo = {}

        def is_pal(i: int, j: int) -> bool:
            if i >= j:
                return True
            if (i, j) in memo:
                return memo[(i, j)]

            memo[(i, j)] = s[i] == s[j] and is_pal(i + 1, j - 1)
            return memo[(i, j)]

        return sum(is_pal(i, j) for i in range(n) for j in range(i, n))
```

The conversion to a table is the same four moves as in Longest Palindromic Substring: `memo[(i, j)]` becomes `dp[i][j]`, `i >= j → True` becomes `dp[i][i] = True` (plus the `j - i <= 2` shortcut), and the memo asks for the inner span `(i + 1, j - 1)`, so `i` runs downward and `j` upward. The only change is a counter.

```python
class Solution:
    def countSubstrings(self, s: str) -> int:
        n = len(s)
        dp = [[False] * n for _ in range(n)]
        count = 0

        # Base case: Single character substrings are palindromes
        for i in range(n):
            dp[i][i] = True
            count += 1

        # Fill DP table bottom-up
        for i in range(n - 1, -1, -1):
            for j in range(i + 1, n):
                if s[i] == s[j]:
                    if j - i <= 2 or dp[i + 1][j - 1]:
                        dp[i][j] = True
                        count += 1

        return count
```

## 4. Dry Run (`s = "aaa"`)

Expansion from every center:

```text
"aaa"  →  6 palindromic substrings
i=0:  odd → "a" (1)             even → "aa" (1)
i=1:  odd → "a", "aaa" (2)      even → "aa" (1)
i=2:  odd → "a" (1)             even → none (0)
total = 1 + 1 + 2 + 1 + 1 + 0 = 6
```

## 5. Complexity

* **States:** there are `2n - 1` centers, and nothing is stored.
* **Time:** O(n²) — each of the `2n - 1` centers expands at most about `n / 2` steps, and each step is O(1).
* **Space:** O(1) — just the counters. The DP table version is O(n²) time and O(n²) space, one boolean per `(i, j)`.

## 6. Recall (30 seconds)

* **Idea:** same `2n - 1` centers as Longest Palindromic Substring; count **every** successful expansion step instead of keeping the longest.
* **Formula:** `total = sum of expand(i, i) + expand(i, i + 1)` over all `i`.
* **DP view:** count the true cells of `is_pal(i, j) = s[i] == s[j] and is_pal(i + 1, j - 1)`.
