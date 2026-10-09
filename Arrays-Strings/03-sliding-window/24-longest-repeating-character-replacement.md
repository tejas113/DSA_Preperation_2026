# 424. Longest Repeating Character Replacement

**LC 424** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Variable sliding window, "invalid when replacements > k"

---

## 1. Intuition

To turn a window into one repeated character, every character that *isn't* the most common one in that
window has to be replaced. So a window is usable exactly when `window length - max_freq <= k` — the number
of "wrong" characters fits your budget of `k` replacements. Grow the window, and only shrink it when that
budget is blown.

* `count[s[r]] += 1` and `max_freq = max(max_freq, count[s[r]])` track the most frequent character's count inside the current window.
* `while (r - l + 1) - max_freq > k` is the validity check — `window length - max_freq` is exactly how many replacements this window would need.
* `count[s[l]] -= 1; l += 1` shrinks the window from the left when it needs too many replacements.
* `res = max(res, r - l + 1)` records the window's length only *after* it's back to valid.

**Recall:** window is valid when `length - max_freq <= k`; grow `r`, shrink `l` while that's violated, track `max_freq` as you go.

---

## 2. Approach

* **Idea:** the answer is the largest window where "everything except the most frequent character" fits inside the replacement budget `k`.
* **Data structure / pointers:** `count` (frequency of each character in the current window), `max_freq` (highest count seen for any character, in any window this size or smaller), `l` and `r` are the window bounds.
* **Invariant:** `max_freq` is never decreased, even as the window shrinks — it's not "the max frequency in the *current* window," it's "the highest max-frequency seen so far in *any* window at least this big." That's safe because the answer can never shrink below what's already been found — see the Recall note on why this doesn't produce a wrong (too large) answer.
* **Edge cases:**
  * `k = 0` → no replacements allowed; the window can only be a single repeated character.
  * `k >= len(s)` → the whole string is replaceable, so the answer is `len(s)`.
  * Empty string → `0`.
  * All same character → the window never needs to shrink, answer is `len(s)`.

---

## 3. Code

```python
from collections import defaultdict


class Solution:

    def characterReplacement(self, s: str, k: int) -> int:
        count = defaultdict(int)
        l = 0
        max_freq = 0
        res = 0

        for r in range(len(s)):
            count[s[r]] += 1
            max_freq = max(max_freq, count[s[r]])

            # Shrink window if replacements needed exceed k
            while (r - l + 1) - max_freq > k:
                count[s[l]] -= 1
                l += 1

            res = max(res, r - l + 1)

        return res


if __name__ == "__main__":
    solution = Solution()
    assert solution.characterReplacement("AABABBA", 1) == 4
    assert solution.characterReplacement("ABAB", 2) == 4
    assert solution.characterReplacement("", 0) == 0
    assert solution.characterReplacement("AAAA", 0) == 4
    print("All tests passed")
```

---

## 4. Dry Run

`s = "AABABBA"`, `k = 1`

| `r` | `s[r]` | `count` | `max_freq` | `l` after | window length | `length - max_freq` | `res` |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `0` | `'A'` | `{A:1}` | `1` | `0` | `1` | `0` | `1` |
| `1` | `'A'` | `{A:2}` | `2` | `0` | `2` | `0` | `2` |
| `2` | `'B'` | `{A:2, B:1}` | `2` | `0` | `3` | `1` | `3` |
| `3` | `'A'` | `{A:3, B:1}` | `3` | `0` | `4` | `1` | **`4`** |
| `4` | `'B'` | `{A:2, B:2}` | `3` | `1` (shrunk once) | `4` | `1` | `4` |
| `5` | `'B'` | `{A:1, B:3}` | `3` | `2` (shrunk once) | `4` | `1` | `4` |
| `6` | `'A'` | `{A:2, B:2}` | `3` | `3` (shrunk once) | `4` | `1` | `4` |

**Return:** `4` — the window `"AABA"` (indices 0–3), turning the one `'B'` into an `'A'`, uses exactly 1 replacement.

---

## 5. Complexity

* **Time:** `O(n)` — `r` moves `n` times, and `l` only ever moves forward, so its total movement across the whole run is at most `n`.
* **Space:** `O(1)` — `count` holds at most 26 entries for uppercase English letters.

---

## 6. Recall (30 seconds)

* **Validity rule:** `window length - max_freq <= k`.
* **`max_freq` never decreases:** it's not recalculated when the window shrinks, and that's fine — a window this size or smaller was already shown invalid unless it hits at least that `max_freq`, so the recorded `res` never gets credited for a window that wasn't actually achievable.
* **Shrink, don't reset:** `l` only ever moves forward, one step at a time, keeping the whole scan `O(n)`.
