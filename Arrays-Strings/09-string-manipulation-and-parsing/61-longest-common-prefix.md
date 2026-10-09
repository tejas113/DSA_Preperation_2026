# 14. Longest Common Prefix

**LC 14** · **Source:** LC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Sort, then compare only the two extremes

---

## 1. Intuition

Sorting the strings lexicographically arranges them so the two *most different* strings end up at the
front and back — any character shared by every string in the list must also be shared by these two most
extreme strings. So instead of comparing all `N` strings character by character, sorting first reduces the
problem to comparing just two strings.

* `strs.sort()` — after sorting, `strs[0]` and `strs[-1]` are the lexicographically smallest and largest strings.
* `first, last = strs[0], strs[-1]` — the common prefix of the *whole list* is guaranteed to be the common prefix of just these two, since any character where they diverge means at least these two strings disagree.
* `while i < len(first) and i < len(last) and first[i] == last[i]: i += 1` walks forward while characters still match, also guarding against running past either string's length.
* `return first[:i]` — the longest matching prefix found.

**Recall:** sort the strings; the longest common prefix of the whole list equals the longest common prefix of just the first and last strings after sorting.

---

## 2. Approach

* **Idea:** sorting collapses an all-strings comparison down to a two-string comparison, since sort order guarantees the first and last strings are the most divergent pair.
* **Data structure / pointers:** `first`/`last` (the two extreme strings after sorting), `i` (how far the match extends).
* **Invariant:** at every step, `first[:i] == last[:i]`, and since every other string in the sorted list lies lexicographically between `first` and `last`, it must also share at least that same prefix.
* **Edge cases:**
  * Empty input list → `""`, guarded explicitly before sorting.
  * A single string → `first == last`, so the whole string matches itself and is returned in full.
  * An empty string among the inputs → sorts to the very front (empty string is lexicographically smallest), so `first = ""` and the `while` condition fails immediately (`i < len(first)` is `0 < 0`), correctly returning `""`.
  * No common prefix at all → the very first character comparison fails, returning `""`.

---

## 3. Code

```python
class Solution:

    def longestCommonPrefix(self, strs: list[str]) -> str:
        if not strs:
            return ""

        # Lexicographically sort the array
        strs.sort()
        first, last = strs[0], strs[-1]

        i = 0
        while i < len(first) and i < len(last) and first[i] == last[i]:
            i += 1

        return first[:i]


if __name__ == "__main__":
    solution = Solution()
    assert solution.longestCommonPrefix(["flower", "flow", "flight"]) == "fl"
    assert solution.longestCommonPrefix(["a"]) == "a"
    assert solution.longestCommonPrefix(["", "b"]) == ""
    assert solution.longestCommonPrefix(["dog", "racecar", "car"]) == ""
    print("All tests passed")
```

### Alternative: vertical scanning — same complexity, no sort needed

Walk character-by-character down the *first* string's length, checking that every other string agrees at
that position. Stops the moment any string mismatches or runs out of characters. Avoids the `O(n log n)`
sort in exchange for comparing against every string at every position.

```python
class SolutionVertical:

    def longestCommonPrefix(self, strs: list[str]) -> str:
        if not strs:
            return ""

        # Use the first string as character reference
        for i in range(len(strs[0])):
            char = strs[0][i]
            for s in strs[1:]:
                # Mismatch or out-of-bounds encountered
                if i == len(s) or s[i] != char:
                    return strs[0][:i]

        return strs[0]


if __name__ == "__main__":
    solution = SolutionVertical()
    assert solution.longestCommonPrefix(["flower", "flow", "flight"]) == "fl"
    assert solution.longestCommonPrefix(["a"]) == "a"
    assert solution.longestCommonPrefix(["", "b"]) == ""
    print("All tests passed")
```

---

## 4. Dry Run

`strs = ["flower", "flow", "flight"]` → after `strs.sort()`: `["flight", "flow", "flower"]`

`first = "flight"`, `last = "flower"`

| `i` | `first[i]` | `last[i]` | Match? | Action |
| --- | --- | --- | --- | --- |
| `0` | `'f'` | `'f'` | True | `i = 1` |
| `1` | `'l'` | `'l'` | True | `i = 2` |
| `2` | `'i'` | `'o'` | **False** | stop |

**Return:** `first[:2] = "fl"`

---

## 5. Complexity

* **Time:** `O(n · m log n)` — `n = len(strs)`, `m` = max string length; dominated by the sort, which compares strings of up to length `m` during each of the `O(n log n)` comparisons.
* **Space:** `O(1)` extra, beyond what Python's sort itself uses internally.

**Vertical scanning alternative:** `O(n · m)` — no sort, but checks up to every character of every string; better than the sorting approach when `n` is large relative to `m`.

---

## 6. Recall (30 seconds)

* **Sort first, then compare only two strings:** the first and last strings after sorting bound every other string's shared prefix.
* **Vertical scanning:** walk down the first string's characters, check every other string at that position — no sort required.
* **Both stop at the first mismatch or exhausted string.**
