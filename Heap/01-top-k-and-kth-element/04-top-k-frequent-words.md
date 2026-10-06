# 692. Top K Frequent Words

**LC 692** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Fixed-size min-heap with a custom tie-break (count, then alphabet)

---

## 1. Intuition

This is Kth Largest again, with one twist. We keep the `k` best words, and "best" means higher count first. When two words have the same count, the alphabetically smaller word is better ("i" beats "love"). The heap must therefore always evict the worst word: the lowest count and, among equal counts, the alphabetically largest.

* `freq_map = Counter(words)` counts each word once, so the heap only ever sees unique words.
* `min_heap` is a min-heap whose root is the **worst** word kept so far, the first one to evict.
* `Pair.__lt__` says which word is "smaller" (worse). Lower `count` is worse. On equal counts, the word that is **larger** alphabetically (`self.word > other.word`) is worse. That inverted comparison is the whole trick.
* `if len(min_heap) > k: heappop` evicts that worst word.
* The heap pops worst-first, so `res[::-1]` flips the list into best-first order.

**Recall:** min-heap of `Pair(count, word)` with `__lt__` meaning "worse"; pop when the size goes above `k`, then reverse.

---

## 2. Approach

* **Idea:** Count the words, push each unique word into a size-`k` heap, evict the worst word whenever the heap is too big, then reverse the pops to get best-first order.
* **Data structure / pointers:**
  * `freq_map`: a `Counter` of word to count.
  * `min_heap`: a **min-heap** of `Pair` objects, capped at `k`. The root is the worst kept word.
  * `Pair`: a custom class used instead of a tuple, kept as written. A tuple `(count, word)` would break the tie the wrong way, because it would evict the alphabetically smaller word first. The tie-break is that **larger word = worse**, so `__lt__` is `count` ascending, then `word` descending.
  * Words are unique in the heap, so two `Pair`s never compare as completely equal.
* **Invariant:** After each unique word, `min_heap` holds the `k` best words seen so far (by count, then alphabet), and its root is the worst of them.
* **Edge cases:**
  * All counts equal (`["day", "is", "sunny"]`, `k = 2`): the tie-break evicts the alphabetically largest, "sunny", and the answer is `["day", "is"]`.
  * `k` equals the number of unique words: nothing is evicted, and the reversal returns every word in the required order.
  * One word: it is returned.
  * The result is already ordered, so there is no need to sort afterwards.

---

## 3. Code

```python
from collections import Counter
import heapq


class Pair:

    def __init__(self, count: int, word: str):
        self.count = count
        self.word = word

    def __lt__(self, other: "Pair") -> bool:
        # Primary sort: lower frequency has higher priority for eviction
        if self.count != other.count:
            return self.count < other.count
        # Secondary sort: larger word lexicographically has higher priority for eviction
        return self.word > other.word


class Solution:

    def topKFrequent(self, words: list[str], k: int) -> list[str]:
        freq_map = Counter(words)
        min_heap = []

        for word, count in freq_map.items():
            heapq.heappush(min_heap, Pair(count, word))
            if len(min_heap) > k:
                heapq.heappop(min_heap)

        # Extract elements and reverse to get highest frequency & lowest lexicographical order first
        res = []
        while min_heap:
            res.append(heapq.heappop(min_heap).word)

        return res[::-1]


if __name__ == "__main__":
    solution = Solution()
    assert solution.topKFrequent(["i", "love", "leetcode", "i", "love", "coding"], 2) == ["i", "love"]
    assert solution.topKFrequent(
        ["the", "day", "is", "sunny", "the", "the", "the", "sunny", "is", "is"], 4
    ) == ["the", "is", "sunny", "day"]
    assert solution.topKFrequent(["day", "is", "sunny"], 2) == ["day", "is"]
    assert solution.topKFrequent(["a"], 1) == ["a"]
    print("All tests passed")
```

---

## 4. Dry Run

`words = ["i", "love", "leetcode", "i", "love", "coding"]`, `k = 2`

`freq_map = {"i": 2, "love": 2, "leetcode": 1, "coding": 1}`

| Word | Pushed | `min_heap` after push | Evicted | `min_heap` after |
| --- | --- | --- | --- | --- |
| `"i"` | `Pair(2, "i")` | `[(2,i)]` | - | `[(2,i)]` |
| `"love"` | `Pair(2, "love")` | `[(2,love), (2,i)]` | - | `[(2,love), (2,i)]` |
| `"leetcode"` | `Pair(1, "leetcode")` | `[(1,leetcode), (2,i), (2,love)]` | `(1,leetcode)` | `[(2,love), (2,i)]` |
| `"coding"` | `Pair(1, "coding")` | `[(1,coding), (2,i), (2,love)]` | `(1,coding)` | `[(2,love), (2,i)]` |

`(2,love)` is the root because with equal counts "love" is alphabetically larger, so it is the worse word.

Extraction: pop gives `"love"`, then `"i"`, so `res = ["love", "i"]`. `res[::-1]` gives `["i", "love"]`.

---

## 5. Complexity

* **Time:** O(n + u log k), which is at most O(n log k). Here `n` is the number of words and `u` is the number of unique words. `Counter` is one O(n) pass, then each of the `u` unique words does one push and at most one pop on a heap of at most `k + 1` items. The final pops are O(k log k).
* **Space:** O(u). `freq_map` holds one entry per unique word, and the heap and `res` hold at most `k`.

---

## 6. Recall (30 seconds)

* Count with `Counter`, then keep a size-`k` min-heap of `Pair(count, word)`. The root is the worst word.
* `__lt__`: lower count is worse, and on a tie the alphabetically larger word is worse (`self.word > other.word`).
* Pop everything into `res`, then return `res[::-1]` for best-first order.
