# 383. Ransom Note

**LC 383** · **Source:** LC150 · **Difficulty:** Easy · **Priority:** Stretch · **Pattern:** Frequency count (supply vs. demand)

---

## 1. Intuition

Cutting letters out of a magazine to build a note: the magazine is your supply, the note is your demand.
Count how many of each letter the magazine has. Then, for each letter the note needs, take one from the
pile. If the pile for that letter is empty, the note cannot be built. This is the same counting idea as
Valid Anagram, but you only need "enough", not "exactly equal".

* `count = defaultdict(int)` is the supply pile: letter → how many the magazine has. A missing letter reads as `0`.
* `count[char] = count[char] + 1` fills the pile from `magazine`.
* `if count[char] <= 0: return False` means the note needs a letter that is missing or already used up.
* `count[char] -= 1` takes one copy of the letter out of the pile.
* `return True` is reached only if every letter of the note found a copy.

**Recall:** count the magazine, then subtract each note letter; if any count would go below zero, return `False`.

---

## 2. Approach

* **Idea:** build the supply counts from `magazine`, then spend them one letter at a time while reading `ransomNote`.
* **Data structure / pointers:** `count` is a `defaultdict(int)` from character to how many copies are still available. `char` is the current letter.
* **Invariant:** while reading `ransomNote`, `count[c]` is the number of copies of `c` in `magazine` that the note has not used yet, and it is never negative.
* **Edge cases:**
  * Empty `ransomNote` → `True` (the second loop never runs).
  * Empty `magazine` with a non-empty note → `False`.
  * Note longer than the magazine → `False`, found naturally when a count runs out.
  * A letter used more times than the magazine has (`"aa"` from `"ab"`) → `False`.
  * Each magazine letter can be used only once, which is why we subtract.

---

## 3. Code

```python
from collections import defaultdict

class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:
        
        count = defaultdict(int)

        for char in magazine:
            count[char] = count[char] + 1

        for char in ransomNote:
            if count[char] <= 0:
                return False
            count[char] -= 1
        
        return True


if __name__ == "__main__":
    solution = Solution()
    assert solution.canConstruct("a", "b") is False
    assert solution.canConstruct("aa", "ab") is False
    assert solution.canConstruct("aa", "aab") is True
    print("All tests passed")
```

---

## 4. Dry Run

`ransomNote = "aa"`, `magazine = "aab"`

Setup: build the supply from `magazine`, so `count = {'a': 2, 'b': 1}`.

| Step | `char` | `count[char]` before | `count[char] <= 0`? | `count` after |
| --- | --- | --- | --- | --- |
| **1** | `'a'` | `2` | `False` | `{'a': 1, 'b': 1}` |
| **2** | `'a'` | `1` | `False` | `{'a': 0, 'b': 1}` |

The loop finishes → return `True`.

---

## 5. Complexity

* **Time:** `O(m + n)` — one pass over `magazine` (`m` letters) and one over `ransomNote` (`n` letters), each step `O(1)` on average.
* **Space:** `O(k)` — `count` has one entry per distinct letter in `magazine` (plus any note letter looked up), so `k ≤ 26` for lowercase letters, which is `O(1)`.

---

## 6. Recall (30 seconds)

* **Supply then demand:** count `magazine` first, then subtract for each letter of `ransomNote`.
* **Stop rule:** `if count[char] <= 0: return False` — the letter is missing or used up.
* **Extras:** `Counter(ransomNote) <= Counter(magazine)` checks the same thing in one line (Python 3.10+). You could also return `False` early when `len(ransomNote) > len(magazine)`, but the code above does not need it.
