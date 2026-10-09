# 76. Minimum Window Substring

**LC 76** · **Source:** LC150 + NC150 · **Difficulty:** Hard · **Priority:** Core · **Pattern:** Variable sliding window, "cover a required multiset" via have/need

---

## 1. Intuition

The window is valid once it contains *at least* as many of each character as `t` needs — not just which
characters, but how many. Instead of comparing two full frequency maps on every step (slow), track a single
number: how many of `t`'s distinct characters currently have *enough* copies in the window. Once every
required character is satisfied, shrink from the left as far as possible before that stops being true.

* `t_freq` is what the window needs; `need = len(t_freq)` is how many *distinct* characters must be satisfied.
* `have` counts how many of those distinct characters currently meet their required count — not their raw count, just "enough or not."
* `if char in t_freq and s_freq[char] == t_freq[char]: have += 1` — the moment a character's count in the window reaches *exactly* what's needed, that requirement flips from unmet to met. (It only increments once per character reaching the threshold, not on every excess copy.)
* `while have == need` — every requirement is currently satisfied, so record the window and try to shrink it.
* `if left_char in t_freq and s_freq[left_char] < t_freq[left_char]: have -= 1` — removing this character just made its count fall *below* what's needed, so this requirement is now unmet, and the shrink loop must stop.

**Recall:** `have == need` means the window is valid; shrink while that holds, and only decrement `have` when a removed character's count drops below what `t` needs.

---

## 2. Approach

* **Idea:** avoid ever comparing two full frequency maps — a single counter (`have` vs `need`) tells you instantly whether the window is valid, updated incrementally as characters enter and leave.
* **Data structure / pointers:** `t_freq` (fixed target counts), `s_freq` (current window's counts), `have`/`need` (validity counter), `l`/`r` (window bounds), `res`/`res_len` (best answer so far).
* **Invariant:** at every point where the `while` loop checks its condition, `s_freq` exactly reflects the counts of `s[l:r+1]`, and `have` exactly equals the number of distinct characters in `t_freq` whose count in `s_freq` is `>=` required — no full-map comparison ever needed to know this.
* **Edge cases:**
  * No valid window exists → `res_len` stays `float("inf")`, returns `""`.
  * `t` longer than `s` → no window can ever satisfy every requirement, correctly returns `""`.
  * `t` guaranteed non-empty per the problem's constraints — with an empty `t`, `need = 0` and the shrink loop would never find a reason to stop, since this path is outside the guaranteed input space, it's not something the code needs to defend against here.
  * Repeated characters in `t` (like `"AABC"`) → handled correctly, since `t_freq` and the `==`/`<` checks compare counts, not just presence.
  * A single valid window found once and never beaten → still returned correctly, since `res` only updates on a strict improvement (`<`).

---

## 3. Code

```python
from collections import Counter, defaultdict


class Solution:

    def minWindow(self, s: str, t: str) -> str:
        t_freq = Counter(t)
        s_freq = defaultdict(int)

        have, need = 0, len(t_freq)
        res, res_len = [-1, -1], float("inf")
        l = 0

        for r in range(len(s)):
            char = s[r]
            s_freq[char] += 1

            if char in t_freq and s_freq[char] == t_freq[char]:
                have += 1

            while have == need:
                if (r - l + 1) < res_len:
                    res_len = r - l + 1
                    res = [l, r]

                left_char = s[l]
                s_freq[left_char] -= 1

                if (
                    left_char in t_freq
                    and s_freq[left_char] < t_freq[left_char]
                ):
                    have -= 1

                l += 1
        l, r = res
        return s[l : r + 1] if res_len != float("inf") else ""


if __name__ == "__main__":
    solution = Solution()
    assert solution.minWindow("ADOBECODEBANC", "ABC") == "BANC"
    assert solution.minWindow("a", "a") == "a"
    assert solution.minWindow("a", "aa") == ""
    print("All tests passed")
```

---

## 4. Dry Run

`s = "ADOBECODEBANC"`, `t = "ABC"` → `t_freq = {A:1, B:1, C:1}`, `need = 3`

Indices: `A(0) D(1) O(2) B(3) E(4) C(5) O(6) D(7) E(8) B(9) A(10) N(11) C(12)`

| `r` | `s[r]` | `have` reaches `need`? | Shrink from `l` | Best window found | `res_len` |
| --- | --- | --- | --- | --- | --- |
| `0–5` | `A,D,O,B,E,C` | Yes, at `r=5` (all of A,B,C now present) | `l: 0→1` (removes `'A'`, drops `have`, loop stops) | `"ADOBEC"` (`[0,5]`) | `6` |
| `6–9` | `O,D,E,B` | No — the removed `'A'` isn't back yet | — | — | `6` |
| `10` | `A` | Yes again | shrinks `l: 1→2→3→4→5` (removing `D,O,B,E` — the *other* `B` at index 9 keeps `have` satisfied), stops when removing `'C'` at `l=5` drops `have` | `"CODEBA"` at `l=5` never beats `6` | `6` (no improvement) |
| `11` | `N` | No | — | — | `6` |
| `12` | `C` | Yes again | shrinks `l: 6→7→8→9`, checking a new window at each step | `"EBANC"` (`[8,12]`, len `5`) improves, then `"BANC"` (`[9,12]`, len `4`) improves again | **`4`** |

**Return:** `s[9:13] = "BANC"`

> Note: the window shrinks all the way through several non-improving steps before *and after* finding
> `"EBANC"` — the answer doesn't jump straight from length 6 to length 4 in one step; length 5 is found
> first, then length 4 immediately after, both during the same `r = 12` shrink sequence.

---

## 5. Complexity

* **Time:** `O(m + n)` — `m = len(s)`, `n = len(t)`. Building `t_freq` is `O(n)`; `r` and `l` each move forward through `s` at most `m` times total, with `O(1)` work per step (thanks to `have`/`need` avoiding full map comparisons).
* **Space:** `O(m + n)` — `t_freq` holds up to `n` distinct characters, `s_freq` up to `m`.

---

## 6. Recall (30 seconds)

* **`have` vs `need`:** `need` is fixed (distinct characters in `t`); `have` counts how many of those are currently satisfied in the window.
* **Shrink while valid:** `while have == need`, record the window, then try to shrink — stop the instant removing a character breaks a requirement.
* **Why it's fast:** `have == need` is a single integer comparison, replacing what would otherwise be a full frequency-map comparison on every step.
