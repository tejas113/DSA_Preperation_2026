# 3. Longest Substring Without Repeating Characters

**LC 3** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Variable sliding window, hash set

---

## 1. Intuition

Grow a window over the string one character at a time. As long as the new character isn't already inside
the window, the window stays valid and can just keep growing. The moment it repeats a character, the window
has to shrink from the left — one character at a time — until the duplicate is gone, before it can grow
again.

* `seen` is a hash set holding exactly the characters currently inside the window `[left, right]`.
* `while s[right] in seen: seen.remove(s[left]); left += 1` shrinks from the left, one character per step, until `s[right]` is no longer a duplicate. It's a `while`, not an `if`, because more than one character might need to leave before the repeat clears.
* `seen.add(s[right])` — once the window is valid again, the new character joins it.
* `max_length = max(max_length, len(seen))` — `len(seen)` is exactly the window's size, since every character in the window is unique by construction.

**Recall:** grow `right`; while `s[right]` is already in `seen`, remove `s[left]` and advance `left`; then add `s[right]` and update the max.

---

## 2. Approach

* **Idea:** keep the window's characters all distinct at all times, by shrinking from the left whenever the newest character would create a duplicate.
* **Data structure / pointers:** `seen` (hash set of characters currently in the window), `left` and `right` are the window's bounds (`right` is the loop variable).
* **Invariant:** at the end of every iteration of the outer loop, `seen` contains exactly the characters in `s[left:right+1]`, and every one of them is unique.
* **Edge cases:**
  * Empty string → `0` (the loop never runs).
  * All characters the same (`"bbbbb"`) → the window shrinks to size `1` every step, answer is `1`.
  * All characters distinct → the window never shrinks, answer is `len(s)`.
  * A repeat far to the left (`"pwwkew"`) → the `while` loop only removes what's needed, not the whole window; `left` never moves backward.

---

## 3. Code

```python
class Solution:

    def lengthOfLongestSubstring(self, s: str) -> int:
        seen = set()
        left = 0
        max_length = 0

        for right in range(len(s)):
            while s[right] in seen:
                seen.remove(s[left])
                left += 1
            seen.add(s[right])
            max_length = max(max_length, len(seen))
        return max_length


if __name__ == "__main__":
    solution = Solution()
    assert solution.lengthOfLongestSubstring("abcabcbb") == 3
    assert solution.lengthOfLongestSubstring("bbbbb") == 1
    assert solution.lengthOfLongestSubstring("pwwkew") == 3
    assert solution.lengthOfLongestSubstring("") == 0
    print("All tests passed")
```

---

## 4. Dry Run

`s = "pwwkew"`

| Step | `right` | `s[right]` | `left` after | `seen` after | `len(seen)` | `max_length` |
| --- | --- | --- | --- | --- | --- | --- |
| **1** | `0` | `'p'` | `0` | `{'p'}` | `1` | `1` |
| **2** | `1` | `'w'` | `0` | `{'p', 'w'}` | `2` | `2` |
| **3** | `2` | `'w'` | `2` | `{'w'}` (removed `'p'`, then `'w'`) | `1` | `2` |
| **4** | `3` | `'k'` | `2` | `{'w', 'k'}` | `2` | `2` |
| **5** | `4` | `'e'` | `2` | `{'w', 'k', 'e'}` | `3` | **`3`** |
| **6** | `5` | `'w'` | `3` | `{'k', 'e', 'w'}` (removed old `'w'`) | `3` | `3` |

**Return:** `3` (the substrings `"wke"` and `"kew"` both achieve it)

---

## 5. Complexity

* **Time:** `O(n)` — `right` moves `n` times, and `left` moves at most `n` times *in total* across the whole run (it never moves backward), so the nested `while` doesn't make this `O(n²)`.
* **Space:** `O(min(n, m))` — `seen` holds at most one entry per character in the window, bounded by both the string length `n` and the alphabet size `m`.

---

## 6. Recall (30 seconds)

* **Grow, then shrink on repeat:** `while s[right] in seen`, remove from the left until the duplicate clears.
* **Window size = `len(seen)`:** every character inside the window is guaranteed unique.
* **Alternative:** a hash map of `char → last seen index` lets `left` jump directly instead of removing one at a time — same `O(n)` time, fewer individual removals.
