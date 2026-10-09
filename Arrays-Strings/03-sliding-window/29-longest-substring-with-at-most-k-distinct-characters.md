# 340. Longest Substring with At Most K Distinct Characters

**LC 340** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Variable sliding window, "invalid when too many distinct characters"

---

## 1. Intuition

A window is valid as long as it doesn't use more than `k` different characters. Grow the window one
character at a time; the moment it introduces a `(k+1)`-th distinct character, shrink from the left — one
character at a time — until a whole distinct character is removed from the window entirely, not just
reduced in count.

* `char_count` maps each character in the window to how many times it appears. `len(char_count)` is exactly the number of *distinct* characters currently in the window.
* `char_count[s[r]] += 1` grows the window; a brand-new character adds a new key.
* `while len(char_count) > k` is the shrink condition — the window has one too many distinct characters.
* `char_count[s[l]] -= 1; if char_count[s[l]] == 0: del char_count[s[l]]` shrinks by one character. The `del` is essential: without it, a character that's dropped to count `0` would still count toward `len(char_count)`, making the distinct-count check wrong.
* `max_len = max(max_len, r - l + 1)` only runs after the window is valid again.

**Recall:** window is valid when `len(char_count) <= k`; grow `r`, and while `len(char_count) > k`, shrink `l` — deleting a character from the map entirely once its count hits `0`.

---

## 2. Approach

* **Idea:** the answer is the largest window whose set of *distinct* characters never exceeds `k` — track that count directly via the size of a frequency map, rather than recomputing it from scratch each step.
* **Data structure / pointers:** `char_count` (character → count in the current window), `l`/`r` (window bounds).
* **Invariant:** after each outer loop iteration, `char_count` holds exactly the characters and counts of `s[l:r+1]`, with every key having a strictly positive count — so `len(char_count)` always equals the true number of distinct characters in the window.
* **Edge cases:**
  * `k = 0` → no substring can have `0` distinct characters and non-zero length, so return `0` immediately (guarded explicitly).
  * Empty string → `0` immediately.
  * `k >= number of distinct characters in s` → the window never needs to shrink, answer is `len(s)`.
  * All the same character → `len(char_count)` never exceeds `1`, so as long as `k >= 1` the whole string qualifies.
  * Forgetting the `del` when a count hits `0` is the classic bug here — without it, `len(char_count)` overcounts distinct characters and the window shrinks too aggressively (or the validity check never resolves correctly).

---

## 3. Code

```python
from collections import defaultdict


class Solution:

    def lengthOfLongestSubstringKDistinct(self, s: str, k: int) -> int:
        if k == 0 or not s:
            return 0

        char_count = defaultdict(int)
        l = 0
        max_len = 0

        for r in range(len(s)):
            char_count[s[r]] += 1

            # Shrink window if distinct character count exceeds k
            while len(char_count) > k:
                char_count[s[l]] -= 1
                if char_count[s[l]] == 0:
                    del char_count[s[l]]
                l += 1

            max_len = max(max_len, r - l + 1)

        return max_len


if __name__ == "__main__":
    solution = Solution()
    assert solution.lengthOfLongestSubstringKDistinct("eceba", 2) == 3
    assert solution.lengthOfLongestSubstringKDistinct("aa", 1) == 2
    assert solution.lengthOfLongestSubstringKDistinct("", 2) == 0
    assert solution.lengthOfLongestSubstringKDistinct("abc", 0) == 0
    print("All tests passed")
```

---

## 4. Dry Run

`s = "eceba"`, `k = 2`

| `r` | `s[r]` | `l` after | `char_count` after | distinct count | window | `max_len` |
| --- | --- | --- | --- | --- | --- | --- |
| `0` | `'e'` | `0` | `{e:1}` | `1` | `"e"` | `1` |
| `1` | `'c'` | `0` | `{e:1, c:1}` | `2` | `"ec"` | `2` |
| `2` | `'e'` | `0` | `{e:2, c:1}` | `2` | `"ece"` | **`3`** |
| `3` | `'b'` | `2` | `{e:1, b:1}` (deleted `'c'`) | `2` | `"eb"` | `3` |
| `4` | `'a'` | `3` | `{b:1, a:1}` (deleted `'e'`) | `2` | `"ba"` | `3` |

**Return:** `3` — the substring `"ece"`.

---

## 5. Complexity

* **Time:** `O(n)` — `r` moves `n` times, and `l` only ever moves forward, so its total movement across the run is at most `n`.
* **Space:** `O(k)` — `char_count` never holds more than `k + 1` distinct keys at once (it's caught and shrunk back to `k` the moment it exceeds that).

---

## 6. Recall (30 seconds)

* **Validity rule:** `len(char_count) <= k` — count of *distinct* characters, not total characters.
* **The `del` matters:** a character whose count drops to `0` must be removed from the map entirely, or `len(char_count)` lies about how many distinct characters are really in the window.
* **Generalizes:** this is the same technique behind "at most 2 distinct characters" and "Fruit Into Baskets" — just swap `k`.
