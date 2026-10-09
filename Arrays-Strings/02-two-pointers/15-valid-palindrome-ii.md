# 680. Valid Palindrome II

**LC 680** · **Source:** [+] Claude · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Two pointers, greedy choice on the first mismatch

---

## 1. Intuition

Valid Palindrome ([[14-valid-palindrome]]) only compares the two ends. Here you get one "free" deletion, so
the question becomes: on the *first* mismatch, which side should you drop? You don't know in advance, so
try both and see if either leaves a palindrome.

* `is_pali(left, right)` is a plain two-pointer palindrome check on a range, with no more skips allowed.
* The outer loop moves `left` and `right` inward exactly like Valid Palindrome, while the characters match.
* `if s[left] != s[right]` is the first mismatch — the *only* one this problem allows you to "spend" a skip on.
* `is_pali(left + 1, right) or is_pali(left, right - 1)` tries dropping the left character, then the right character. If either range is a palindrome on its own, one deletion was enough.
* There's no third branch, because after the first mismatch you have no deletions left — the rest of `is_pali` must match exactly.

**Recall:** walk inward like a normal palindrome check; at the first mismatch, try skipping `left` or skipping `right` with a plain palindrome check on the rest.

---

## 2. Approach

* **Idea:** two pointers moving inward. The first time they disagree, branch into two plain palindrome checks — one skipping `s[left]`, one skipping `s[right]` — and accept either.
* **Data structure / pointers:** `left`, `right` in the outer scan; the same roles again, freshly, inside `is_pali`.
* **Invariant:** every pair compared by the outer loop before reaching a mismatch already matched exactly (no skip used); after a mismatch, `is_pali` allows zero further skips.
* **Edge cases:**
  * Already a palindrome → the outer loop runs to completion, returns `True` without ever calling `is_pali`.
  * Empty string or one character → `left < right` is false immediately, returns `True`.
  * Only one valid deletion makes it work, and it can be on either side (`"abca"` works by dropping `'b'` or `'c'`).
  * Two mismatches needed (`"abc"`) → both branches of `is_pali` fail, so it correctly returns `False`.
  * A tricky case like `"eeccccbebaeeabebccceea"` needs more than one deletion, so it correctly returns `False` even though the first mismatch looks fixable — `is_pali` re-checks the *whole* remaining range, not just the character next to the mismatch.

---

## 3. Code

```python
class Solution:

    def validPalindrome(self, s: str) -> bool:
        # Helper function to check standard palindrome in a given range
        def is_pali(left: int, right: int) -> bool:
            while left < right:
                if s[left] != s[right]:
                    return False
                left += 1
                right -= 1
            return True

        left, right = 0, len(s) - 1

        while left < right:
            if s[left] != s[right]:
                # On first mismatch, attempt skipping left or skipping right
                return is_pali(left + 1, right) or is_pali(left, right - 1)

            left += 1
            right -= 1

        return True


if __name__ == "__main__":
    solution = Solution()
    assert solution.validPalindrome("aba") is True
    assert solution.validPalindrome("abca") is True
    assert solution.validPalindrome("abc") is False
    assert solution.validPalindrome("eeccccbebaeeabebccceea") is False
    print("All tests passed")
```

---

## 4. Dry Run

`s = "abca"`, `left = 0` (`'a'`), `right = 3` (`'a'`)

| Step | `left` | `s[left]` | `right` | `s[right]` | Action / branch | Result |
| --- | --- | --- | --- | --- | --- | --- |
| **1** | `0` | `'a'` | `3` | `'a'` | `s[0] == s[3]`; `left += 1`, `right -= 1` | continue |
| **2** | `1` | `'b'` | `2` | `'c'` | `s[1] != s[2]`; try `is_pali(2, 2)` and `is_pali(1, 1)` | both `True` |

Both branches are single-index ranges (`left == right`), which `is_pali` returns `True` for immediately.
`True or True` → **return `True`**.

---

## 5. Complexity

* **Time:** `O(n)` — the outer loop does at most `O(n)` work before the first mismatch (or none at all), and then at most two calls to `is_pali`, each `O(n)`. No string slicing is done, so there's no extra copying cost.
* **Space:** `O(1)` — only index variables; `is_pali` reads directly from `s`.

---

## 6. Recall (30 seconds)

* **One mismatch, one choice:** on the first `s[left] != s[right]`, try `is_pali(left + 1, right)` or `is_pali(left, right - 1)`.
* **No skips after that:** the helper `is_pali` is a plain palindrome check — it does not allow another skip.
* **Generalizes to K deletions** as DP/recursion with memoization; this greedy try-both trick only works because `K = 1`.
