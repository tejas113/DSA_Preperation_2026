# 242. Valid Anagram

**LC 242** · **Source:** LC150 + NC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Frequency count (hash map)

---

## 1. Intuition

Two words are anagrams when they are built from the same letters, the same number of times. So don't
compare the order — count how many times each letter appears in each word and compare the two tallies.

* `if len(s) != len(t): return False` is a free early exit — different lengths can never be anagrams.
* `Counter(s)` is the tally for `s`: each character mapped to how many times it appears.
* `Counter(t)` is the same tally for `t`.
* `==` on two `Counter`s is `True` only when every character has the same count in both. Order does not matter.

**Recall:** check the lengths, then compare `Counter(s) == Counter(t)`.

---

## 2. Approach

* **Idea:** count the characters of each string and compare the counts.
* **Data structure / pointers:** two `Counter`s (hash maps from character → count), one per string.
* **Invariant:** none to maintain — each `Counter` is built in one pass and only compared at the end.
* **Edge cases:**
  * Different lengths → `False` straight away.
  * Empty strings → both `Counter`s are empty, so `True`.
  * Same letters but different counts (`"aab"` vs `"abb"`) → the counts differ, so `False`.
  * Unicode characters → works unchanged; dict keys can be any character. Space grows to the number of distinct characters, not 26.

---

## 3. Code

```python
from collections import Counter

class Solution:
    def isAnagram(self, s: str, t: str) -> bool:
        if len(s) != len(t):
            return False
        
        return Counter(s) == Counter(t)


if __name__ == "__main__":
    solution = Solution()
    assert solution.isAnagram("anagram", "nagaram") is True
    assert solution.isAnagram("rat", "car") is False
    print("All tests passed")
```

---

## 4. Dry Run

`s = "anagram"`, `t = "nagaram"`

1. **Length check:** `len(s) == 7` and `len(t) == 7`, so continue.
2. **`Counter(s)`:** `{'a': 3, 'n': 1, 'g': 1, 'r': 1, 'm': 1}`
3. **`Counter(t)`:** `{'n': 1, 'a': 3, 'g': 1, 'r': 1, 'm': 1}`
4. **Compare:** the two maps hold the same counts (key order does not matter), so return `True`.

---

## 5. Complexity

* **Time:** `O(n)` — each `Counter` reads its string once (`n = len(s)`), and comparing two counters costs `O(k)`, which is at most `n`.
* **Space:** `O(k)` — the two `Counter`s hold one entry per distinct character; `k ≤ 26` for lowercase letters, so it is `O(1)` there.

---

## 6. Recall (30 seconds)

* **Guard first:** `if len(s) != len(t): return False`.
* **Core move:** `Counter(s) == Counter(t)` — same characters, same counts.
* **Unicode:** no change needed; hash map keys handle any character.
