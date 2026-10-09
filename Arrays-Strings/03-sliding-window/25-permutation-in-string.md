# 567. Permutation in String

**LC 567** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Fixed-size sliding window, frequency array

---

## 1. Intuition

A permutation of `s1` is just "the same letters, same counts, any order." So finding a permutation of `s1`
inside `s2` is really asking: does any window of `s2` with length `len(s1)` have the exact same letter
counts as `s1`? Since the window size never changes, slide it one step at a time — add the new letter
coming in, remove the old letter falling out, and compare counts.

* `c1` is the fixed target: the letter counts of `s1`, built once.
* `c2` is the letter counts of the *current* window in `s2`, always kept at size `len(s1)`.
* The first loop builds the very first window (`s2[0:len(s1)]`) into `c2`.
* `c2[ord(s2[i]) - ord("a")] += 1` adds the incoming letter as the window slides to include `s2[i]`.
* `c2[ord(s2[i - len(s1)]) - ord("a")] -= 1` removes the letter that just fell out of the window's left edge, in the same step — so the window size stays exactly `len(s1)` at all times.
* `if c1 == c2` compares two 26-length arrays; equal counts mean this window is a permutation of `s1`.

**Recall:** keep a fixed-size window using two frequency arrays; add the new letter, remove the one that fell off, compare `c1 == c2`.

---

## 2. Approach

* **Idea:** since the window length is fixed at `len(s1)`, there's no growing or shrinking logic — just "add one, remove one" as the window slides, which keeps each step `O(1)` (26 letters) instead of re-counting the whole window.
* **Data structure / pointers:** `c1` (target counts, built once), `c2` (current window's counts, updated incrementally), `i` is the window's right edge.
* **Invariant:** at every point after the initial window is built, `c2` holds the exact letter counts of `s2[i - len(s1) + 1 : i + 1]` — the last `len(s1)` characters processed.
* **Edge cases:**
  * `len(s1) > len(s2)` → impossible, returns `False` immediately.
  * `s1` is a permutation of the very start of `s2` → caught by the `if c1 == c2` check right after building the initial window, before the sliding loop even runs.
  * No match anywhere → the loop finishes and returns `False`.
  * Repeated letters in `s1` → handled correctly, since counts (not just presence) are compared.

---

## 3. Code

```python
class Solution:

    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False

        c1 = [0] * 26
        c2 = [0] * 26

        for i in range(len(s1)):
            c1[ord(s1[i]) - ord("a")] += 1
            c2[ord(s2[i]) - ord("a")] += 1

        if c1 == c2:
            return True

        for i in range(len(s1), len(s2)):
            c2[ord(s2[i]) - ord("a")] += 1
            c2[ord(s2[i - len(s1)]) - ord("a")] -= 1

            if c1 == c2:
                return True
        return False


if __name__ == "__main__":
    solution = Solution()
    assert solution.checkInclusion("ab", "eidbaooo") is True
    assert solution.checkInclusion("ab", "eidboaoo") is False
    assert solution.checkInclusion("adc", "dcda") is True
    assert solution.checkInclusion("abc", "ab") is False
    print("All tests passed")
```

### Alternative: brute force (why it's too slow)

Check every window by sorting it and comparing to `sorted(s1)`. Correct, but re-does all the counting work
from scratch on every window instead of reusing it.

```python
class BruteForceSolution:

    def checkInclusion(self, s1: str, s2: str) -> bool:
        k = len(s1)
        n = len(s2)

        if k > n:
            return False

        target_sorted = sorted(s1)

        # Check all substrings of length k
        for i in range(n - k + 1):
            sub = s2[i : i + k]
            if sorted(sub) == target_sorted:
                return True

        return False


if __name__ == "__main__":
    brute = BruteForceSolution()
    assert brute.checkInclusion("ab", "eidbaooo") is True
    assert brute.checkInclusion("ab", "eidboaoo") is False
    print("All tests passed")
```

---

## 4. Dry Run

`s1 = "ab"`, `s2 = "eidbaooo"`. Target: `c1` has `'a': 1, 'b': 1` (everything else `0`).

| Step | `i` | Incoming | Outgoing | Window | `c1 == c2`? |
| --- | --- | --- | --- | --- | --- |
| **init** | `0..1` | `'e'`, `'i'` | — | `"ei"` | No |
| **1** | `2` | `'d'` | `'e'` | `"id"` | No |
| **2** | `3` | `'b'` | `'i'` | `"db"` | No |
| **3** | `4` | `'a'` | `'d'` | `"ba"` | **Yes → return `True`** |

---

## 5. Complexity

* **Time:** `O(n)` — `n = len(s2)`; each of the `n` positions does `O(1)` work to update `c2` and an `O(26)` comparison, so total is `O(26n) = O(n)`.
* **Space:** `O(1)` — `c1` and `c2` are fixed-size 26-element arrays, independent of input length.

**Brute force:** `O((n - k + 1) · k log k)` — sorts each of the `~n` windows of length `k = len(s1)` from scratch, which is why it's too slow for large inputs.

---

## 6. Recall (30 seconds)

* **Reframe the question:** "does `s2` contain a permutation of `s1`?" = "does any fixed-size window of `s2` have the same letter counts as `s1`?"
* **Fixed window update:** add `s2[i]`, remove `s2[i - len(s1)]`, in the same step — the window size never changes.
* **Why it beats brute force:** comparing two 26-length arrays is `O(1)`; re-sorting each window from scratch is not.
