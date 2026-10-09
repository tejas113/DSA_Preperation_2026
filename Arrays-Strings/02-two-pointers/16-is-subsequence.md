# 392. Is Subsequence

**LC 392** · **Source:** LC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Two pointers, greedy matching

---

## 1. Intuition

`s` is a subsequence of `t` if you can find its characters inside `t`, in order, but not necessarily
next to each other. Walk `t` once. Every time the current character of `t` matches the character of `s`
you still need, take it and move on to the next character of `s`. If you run out of `s` before running
out of `t`, every character was found.

* `i` tracks how much of `s` has been matched so far; `j` scans through `t`.
* `if s[i] == t[j]: i += 1` only advances `i` on a match — this is the "take it" step.
* `j += 1` runs every time, matched or not, because `t` is scanned once regardless.
* `return i == len(s)` — if `i` reached the end of `s`, every character was found in order.

**Recall:** scan `t` with `j`; whenever `s[i] == t[j]`, advance `i` too; done when `i == len(s)`.

---

## 2. Approach

* **Idea:** greedily match `s` against `t` left to right — always take the *earliest* possible match for each character of `s`, since taking it later can never help and might cost you room for the rest.
* **Data structure / pointers:** `i` is the pointer into `s` (how many characters matched), `j` is the pointer into `t` (how far scanned).
* **Invariant:** at every point, `s[:i]` has already been matched, in order, using only characters from `t[:j]`.
* **Edge cases:**
  * `s = ""` → `i == len(s) == 0` immediately, returns `True`.
  * `t = ""`, `s` non-empty → the loop never runs (`j < len(t)` fails), `i` stays `0`, returns `False`.
  * `s` longer than `t` → cannot be a subsequence; the loop runs out of `t` before `i` catches up, correctly returns `False`.
  * `s == t` → every character matches in step, returns `True`.
  * Repeated characters in `t` → greedy still works, since taking the first available match never blocks a later one.

---

## 3. Code

```python
class Solution:

    def isSubsequence(self, s: str, t: str) -> bool:
        i = 0  # Pointer for s
        j = 0  # Pointer for t

        while i < len(s) and j < len(t):
            if s[i] == t[j]:
                i += 1  # Matched s[i], move to next character in s
            j += 1  # Always advance through t

        return i == len(s)


if __name__ == "__main__":
    solution = Solution()
    assert solution.isSubsequence("abc", "ahbgdc") is True
    assert solution.isSubsequence("axc", "ahbgdc") is False
    assert solution.isSubsequence("", "") is True
    assert solution.isSubsequence("a", "") is False
    print("All tests passed")
```

### Alternative: many queries against a fixed `t`

If the same `t` is checked against millions of different `s` strings, re-scanning `t` for every query is
wasteful. Preprocess `t` once into a map of character → sorted list of indices, then binary-search for the
next usable index per character of `s`:

```python
from collections import defaultdict
from bisect import bisect_right

def build_positions(t: str) -> dict[str, list[int]]:
    pos = defaultdict(list)
    for index, char in enumerate(t):
        pos[char].append(index)
    return pos

def is_subsequence_fast(s: str, pos: dict[str, list[int]]) -> bool:
    last_index = -1
    for char in s:
        indices = pos.get(char)
        if not indices:
            return False
        k = bisect_right(indices, last_index)
        if k == len(indices):
            return False
        last_index = indices[k]
    return True


if __name__ == "__main__":
    t = "ahbgdc"
    positions = build_positions(t)
    assert is_subsequence_fast("abc", positions) is True
    assert is_subsequence_fast("axc", positions) is False
    print("All tests passed")
```

---

## 4. Dry Run

`s = "abc"`, `t = "ahbgdc"`

| Step | `i` | `s[i]` | `j` | `t[j]` | Match? | Action |
| --- | --- | --- | --- | --- | --- | --- |
| **1** | `0` | `'a'` | `0` | `'a'` | Yes | `i = 1`, `j = 1` |
| **2** | `1` | `'b'` | `1` | `'h'` | No | `j = 2` |
| **3** | `1` | `'b'` | `2` | `'b'` | Yes | `i = 2`, `j = 3` |
| **4** | `2` | `'c'` | `3` | `'g'` | No | `j = 4` |
| **5** | `2` | `'c'` | `4` | `'d'` | No | `j = 5` |
| **6** | `2` | `'c'` | `5` | `'c'` | Yes | `i = 3`, `j = 6` |

The loop ends because `i == len(s) == 3` → return `True`.

---

## 5. Complexity

* **Time:** `O(t)` — `j` scans `t` once (`t = len(t)`), and `i` only ever moves forward too, up to `len(s) ≤ len(t)` times.
* **Space:** `O(1)` — only the two index variables.

**Follow-up (many `s` against a fixed `t`):** `O(t)` once to build `pos`, then `O(s log t)` per query — binary search per character instead of a full rescan of `t`. Worth it when `s` is much shorter than `t` and there are many queries.

---

## 6. Recall (30 seconds)

* **Two pointers, greedy:** advance `i` only on a match; always advance `j`.
* **Done check:** `i == len(s)` at the end — everything in `s` was found in order.
* **Follow-up:** many `s` against one fixed `t` → preprocess `t` into `{char: sorted indices}`, binary-search with `bisect_right` per character, `O(s log t)` per query.
