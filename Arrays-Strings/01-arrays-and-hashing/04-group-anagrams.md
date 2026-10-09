# 49. Group Anagrams

**LC 49** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Canonical key (sorted string) in a hash map

---

## 1. Intuition

Anagrams are the same letters in a different order. If you sort the letters of each word, every anagram
in a group turns into the *same* string. That sorted string is a label all of them share, so use it as a
dictionary key and drop each word into the bucket with its label.

* `sorted(s)` puts the letters in order, so `"eat"`, `"tea"` and `"ate"` all become `a, e, t`.
* `"".join(sorted(s))` turns that list of letters into a string, because a list cannot be a dict key but a string can.
* `ans = defaultdict(list)` creates an empty bucket the first time a key appears, so there is no "does this key exist yet?" check.
* `ans[sorted_key].append(s)` files the original word (not the sorted one) into its bucket.
* `list(ans.values())` returns just the buckets; the keys were only labels.

**Recall:** sort each word to get its key; group the words by that key.

---

## 2. Approach

* **Idea:** compute a canonical key for each word (its letters, sorted) and group words that share a key.
* **Data structure / pointers:** `ans` maps `sorted_key` → list of the original words with that key. `s` is the current word.
* **Invariant:** every word seen so far sits in the list under its own `sorted_key`, and two words are in the same list exactly when they are anagrams.
* **Edge cases:**
  * Empty list → `[]`.
  * A list holding one empty string `[""]` → `[[""]]` (the key is `""`).
  * One word → one group of one.
  * All words are anagrams → a single group.
  * No two words are anagrams → every word is its own group.
  * Order of the groups, and of the words inside a group, does not matter to the problem.

---

## 3. Code

```python
from collections import defaultdict

class Solution:
    def groupAnagrams(self, strs: list[str]) -> list[list[str]]:

        ans = defaultdict(list)

        for s in strs:
            sorted_key = "".join(sorted(s))
            ans[sorted_key].append(s)

        return list(ans.values())


if __name__ == "__main__":
    solution = Solution()

    def normalize(groups: list[list[str]]) -> list[list[str]]:
        return sorted(sorted(group) for group in groups)

    assert normalize(solution.groupAnagrams(["eat", "tea", "tan", "ate", "nat", "bat"])) == normalize(
        [["bat"], ["nat", "tan"], ["ate", "eat", "tea"]]
    )
    assert normalize(solution.groupAnagrams([""])) == [[""]]
    assert normalize(solution.groupAnagrams(["a"])) == [["a"]]
    print("All tests passed")
```

---

## 4. Dry Run

`strs = ["eat", "tea", "tan", "ate", "nat", "bat"]`

| String `s` | `sorted_key` | Action | `ans` after |
| --- | --- | --- | --- |
| `"eat"` | `"aet"` | append to `"aet"` | `{"aet": ["eat"]}` |
| `"tea"` | `"aet"` | append to `"aet"` | `{"aet": ["eat", "tea"]}` |
| `"tan"` | `"ant"` | append to `"ant"` | `{"aet": ["eat", "tea"], "ant": ["tan"]}` |
| `"ate"` | `"aet"` | append to `"aet"` | `{"aet": ["eat", "tea", "ate"], "ant": ["tan"]}` |
| `"nat"` | `"ant"` | append to `"ant"` | `{"aet": ["eat", "tea", "ate"], "ant": ["tan", "nat"]}` |
| `"bat"` | `"abt"` | append to `"abt"` | `{"aet": [...], "ant": [...], "abt": ["bat"]}` |

**Return:** `[["eat", "tea", "ate"], ["tan", "nat"], ["bat"]]`

---

## 5. Complexity

* **Time:** `O(n · k log k)` — `n` words, and sorting one word of length `k` costs `O(k log k)`; the dict append is `O(1)` on average (`k` = longest word).
* **Space:** `O(n · k)` — `ans` stores every word once in its bucket, plus one sorted key per group.

---

## 6. Recall (30 seconds)

* **Core trick:** anagrams have the same sorted string, so `"".join(sorted(s))` is the group key.
* **Data structure:** `defaultdict(list)` — `sorted_key` → list of original words; return `list(ans.values())`.
* **Faster key:** a tuple of 26 letter counts as the key gives `O(n · k)` time, but the sorted key is shorter to write and fine for typical word lengths.
