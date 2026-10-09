# 125. Valid Palindrome

**LC 125** · **Source:** LC150 + NC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Two pointers moving inward

---

## 1. Intuition

A palindrome reads the same forwards and backwards, so check it from both ends at once and meet in the
middle. Punctuation, spaces and case don't count, so skip over them instead of comparing them.

* `left = 0`, `right = len(s) - 1` start at the two ends and walk toward each other.
* `while left < right and not s[left].isalnum()` moves `left` past anything that isn't a letter or digit.
* `while left < right and not s[right].isalnum()` does the same for `right`, from the other end.
* `if s[left].lower() != s[right].lower()` compares the two valid characters, ignoring case; a mismatch means it's not a palindrome.
* `left += 1; right -= 1` steps both pointers inward for the next pair, once the current pair matches.

**Recall:** two pointers from both ends; skip non-alphanumeric characters, compare lowercased, meet in the middle.

---

## 2. Approach

* **Idea:** compare characters from the outside in, skipping anything that isn't alphanumeric, without building a cleaned copy of the string.
* **Data structure / pointers:** `left` and `right` are indices into `s`; no extra storage is needed.
* **Invariant:** every pair of alphanumeric characters compared before `left` and after `right` (relative to the current pointers) already matched, case-insensitively.
* **Edge cases:**
  * Empty string, or a string with no alphanumeric characters (`",,"`) → `left` and `right` cross or meet without a mismatch, so it returns `True`.
  * One character → `left == right`, the loop never runs, returns `True`.
  * All punctuation/spaces around a single valid core (`"0P"`) → still compared correctly.
  * Mixed case (`"Aa"`) → matched via `.lower()`.
  * The inner `while` loops both check `left < right`, so `left` and `right` can never cross while skipping.

---

## 3. Code

```python
class Solution:

    def isPalindrome(self, s: str) -> bool:
        left = 0
        right = len(s) - 1

        while left < right:
            # Skip non-alphanumeric characters from the left
            while left < right and not s[left].isalnum():
                left += 1

            # Skip non-alphanumeric characters from the right
            while left < right and not s[right].isalnum():
                right -= 1

            # Compare lowercased valid alphanumeric characters
            if s[left].lower() != s[right].lower():
                return False

            left += 1
            right -= 1

        return True


if __name__ == "__main__":
    solution = Solution()
    assert solution.isPalindrome("A man, a plan, a canal: Panama") is True
    assert solution.isPalindrome("race a car") is False
    assert solution.isPalindrome(" ") is True
    assert solution.isPalindrome(".,") is True
    print("All tests passed")
```

---

## 4. Dry Run

`s = "A man, a plan, a canal: Panama"` (length 30, so `right` starts at `29`)

| `left` | `s[left]` | `right` | `s[right]` | Action / Comparison | Result |
| --- | --- | --- | --- | --- | --- |
| `0` | `'A'` | `29` | `'a'` | compare `'a' == 'a'` | match |
| `2` | `'m'` | `28` | `'m'` | skip space at `1`, compare `'m' == 'm'` | match |
| `3` | `'a'` | `27` | `'a'` | compare `'a' == 'a'` | match |
| `4` | `'n'` | `26` | `'n'` | compare `'n' == 'n'` | match |
| `7` | `'a'` | `25` | `'a'` | skip `,` and space, compare | match |
| `9` | `'p'` | `24` | `'P'` | skip space, compare (case-insensitive) | match |
| `10` | `'l'` | `21` | `'l'` | skip `,`, space, `a` from the right side, compare | match |
| `11`–`17` | `'a','n','a','c'` | `20`–`17` | `'a','n','a','c'` | pointers keep closing in, all match | match |
| `17` | `'c'` | `17` | `'c'` | `left == right`, loop ends | — |

**Return:** `True`

---

## 5. Complexity

* **Time:** `O(n)` — `left` and `right` only move inward, so together they visit each character at most once across the outer loop and both inner skip loops.
* **Space:** `O(1)` — only the two index variables are used; no copy of the string is built.

---

## 6. Recall (30 seconds)

* **Two pointers, inward:** `left` from the start, `right` from the end.
* **Skip, then compare:** skip non-alphanumeric characters on each side first, then compare `.lower()` of what's left.
* **Why not filter first:** building `[c.lower() for c in s if c.isalnum()]` also works, but costs `O(n)` extra space; the two-pointer scan does it in `O(1)`.
