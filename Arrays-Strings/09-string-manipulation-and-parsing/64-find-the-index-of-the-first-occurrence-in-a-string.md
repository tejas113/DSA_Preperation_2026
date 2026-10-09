# 28. Find the Index of the First Occurrence in a String

**LC 28** · **Source:** LC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Fixed-size window, direct substring comparison

---

## 1. Intuition

Finding the first occurrence of `needle` in `haystack` just means checking every possible starting position
for a match — a fixed-size window of length `len(needle)` slid across `haystack`, comparing at each step.

* `if m > n: return -1` — `needle` can't possibly fit if it's longer than `haystack`, so this is checked once up front.
* `range(n - m + 1)` — the last valid starting position is `n - m`, since starting any later wouldn't leave enough characters for `needle` to fit.
* `if haystack[i : i + m] == needle: return i` — a direct slice comparison at each position; the first match found is returned immediately, since we want the *first* occurrence.
* `return -1` — reached only if every position was checked and none matched.

**Recall:** slide a window of `needle`'s length across `haystack`, from `0` to `n - m`, comparing the slice directly; return the first matching index, or `-1`.

---

## 2. Approach

* **Idea:** direct substring comparison at every valid starting position — simple to reason about, though it can re-examine overlapping characters on repeated near-misses.
* **Data structure / pointers:** `i` is the current starting position; `n`, `m` are the lengths of `haystack` and `needle`.
* **Invariant:** by the time index `i` is checked, every starting position before `i` has already been confirmed not to produce a match.
* **Edge cases:**
  * `needle` longer than `haystack` (`"a"`, `"aa"`) → caught by the `m > n` guard, returns `-1` immediately without ever reaching the loop.
  * Exact-length match (`haystack == needle`) → the loop runs exactly once (`range(0, 1)`), checking `i = 0`.
  * Single-character `needle` → the window is just one character, scanning until the first match.
  * Worst case (`haystack = "aaaaaaaaab"`, `needle = "aaaa"`) → every window nearly matches before failing at the last character, giving `O((n-m+1) · m)` — the case KMP is designed to avoid.

---

## 3. Code

```python
class Solution:

    def strStr(self, haystack: str, needle: str) -> int:
        n, m = len(haystack), len(needle)

        # Optimization: needle cannot fit if haystack is shorter
        if m > n:
            return -1

        for i in range(n - m + 1):
            if haystack[i : i + m] == needle:
                return i

        return -1


if __name__ == "__main__":
    solution = Solution()
    assert solution.strStr("sadbutsad", "sad") == 0
    assert solution.strStr("leetcode", "leeto") == -1
    assert solution.strStr("a", "aa") == -1
    assert solution.strStr("abc", "abc") == 0
    print("All tests passed")
```

### Alternative: Knuth-Morris-Pratt (KMP) — O(n + m) time

Precomputes a Longest Prefix Suffix (LPS) array for `needle`, so on a mismatch the search can skip ahead
using already-known information instead of re-comparing from scratch — avoids the sliding window's
worst-case re-examination of overlapping characters.

```python
class SolutionKMP:

    def strStr(self, haystack: str, needle: str) -> int:
        if not needle:
            return 0
        if len(needle) > len(haystack):
            return -1

        # 1. Build Longest Prefix Suffix (LPS) array for needle
        lps = [0] * len(needle)
        prevLPS, i = 0, 1

        while i < len(needle):
            if needle[i] == needle[prevLPS]:
                lps[i] = prevLPS + 1
                prevLPS += 1
                i += 1
            elif prevLPS == 0:
                lps[i] = 0
                i += 1
            else:
                prevLPS = lps[prevLPS - 1]

        # 2. Search needle in haystack using LPS
        i, j = 0, 0  # i -> haystack, j -> needle
        while i < len(haystack):
            if haystack[i] == needle[j]:
                i += 1
                j += 1
            else:
                if j == 0:
                    i += 1
                else:
                    j = lps[j - 1]

            if j == len(needle):
                return i - len(needle)

        return -1


if __name__ == "__main__":
    solution = SolutionKMP()
    assert solution.strStr("sadbutsad", "sad") == 0
    assert solution.strStr("leetcode", "leeto") == -1
    assert solution.strStr("aaaaaaaaab", "aaab") == 6
    print("All tests passed")
```

---

## 4. Dry Run

**Match found immediately (`haystack = "sadbutsad"`, `needle = "sad"`, `n=9`, `m=3`):**

| `i` | `haystack[i:i+3]` | `== "sad"`? | Action |
| --- | --- | --- | --- |
| `0` | `"sad"` | **True** | **return `0`** |

**No match anywhere (`haystack = "leetcode"`, `needle = "leeto"`, `n=8`, `m=5`):**

| `i` | `haystack[i:i+5]` | `== "leeto"`? |
| --- | --- | --- |
| `0` | `"leetc"` | False |
| `1` | `"eetco"` | False |
| `2` | `"etcod"` | False |
| `3` | `"tcode"` | False |

Loop ends (range was `0` to `3`). **Return:** `-1`

---

## 5. Complexity

* **Time:** `O((n - m + 1) · m)` worst case, though `O(n)` on average for typical (non-adversarial) inputs.
* **Space:** `O(1)` — Python string slicing does allocate a temporary substring of length `m` per comparison, but no structure grows with the input beyond that.

**KMP alternative:** `O(n + m)` time — guaranteed linear regardless of input; `O(m)` space for the LPS array.

---

## 6. Recall (30 seconds)

* **Slide a fixed window, compare directly:** `haystack[i:i+m] == needle` for each valid `i`.
* **Range bound:** `range(n - m + 1)` — no point starting later than `n - m`.
* **KMP's edge:** the LPS array lets a mismatch skip ahead instead of restarting the comparison from scratch, avoiding the sliding window's worst case.
