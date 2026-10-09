# 347. Top K Frequent Elements

**LC 347** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Frequency count + bucket by frequency

---

## 1. Intuition

Count how often each number appears. Then, instead of sorting the numbers by count, use the count
itself as a shelf number: put each number on the shelf that matches its count. A number can appear at
most `len(nums)` times, so there are only `len(nums) + 1` shelves. Walk the shelves from the fullest
end down and pick numbers until you have `k`.

* `count[n] = 1 + count.get(n, 0)` builds the tally: number → how many times it appears.
* `freq = [[] for i in range(len(nums) + 1)]` makes the shelves. `freq[c]` will hold every number that appears exactly `c` times. The size is `len(nums) + 1` because the highest possible count is `len(nums)`.
* `freq[c].append(n)` puts each number on the shelf for its count.
* `range(len(freq) - 1, 0, -1)` walks from the highest frequency down to `1`. Index `0` is never used, since every counted number appears at least once.
* `if len(res) == k: return res` stops as soon as we have `k` numbers, so we never look at the low shelves.

**Recall:** count each number, shelve it at `freq[count]`, then read the shelves from the top down until you have `k`.

---

## 2. Approach

* **Idea:** count, bucket by count, then collect from the highest count downward. This avoids sorting, so it is `O(n)` instead of `O(n log n)`.
* **Data structure / pointers:** `count` maps number → frequency. `freq` is a list of lists where the index is the frequency. `res` collects the answer. `i` is the current shelf, moving down from `len(freq) - 1` to `1`.
* **Invariant:** while walking down, everything already in `res` has a frequency at least as high as anything not yet visited — we always read higher shelves first.
* **Edge cases:**
  * One element (`[1]`, `k = 1`) → `[1]`.
  * All numbers equal → a single number sits on shelf `len(nums)`.
  * Ties in frequency → the numbers share a shelf and either order is fine; the problem guarantees the answer is unique.
  * Negatives and `0` → fine, they are only dict keys.
  * `k` equals the number of distinct values → the loop returns all of them.
  * `k` is always valid (`1` to the number of distinct values); if it were larger, the function would end without returning and give `None`.

---

## 3. Code

```python
class Solution:
    def topKFrequent(self, nums: list[int], k: int) -> list[int]:

        count = {}
        freq = [[] for i in range(len(nums) + 1)]

        for n in nums:
            count[n] = 1 + count.get(n, 0)

        for n, c in count.items():
            freq[c].append(n)

        res = []
        for i in range(len(freq) - 1, 0, -1):
            for n in freq[i]:
                res.append(n)
                if len(res) == k:
                    return res


if __name__ == "__main__":
    solution = Solution()
    assert sorted(solution.topKFrequent([1, 1, 1, 2, 2, 3], 2)) == [1, 2]
    assert sorted(solution.topKFrequent([1], 1)) == [1]
    assert sorted(solution.topKFrequent([1, 2, 1, 2, 1, 2, 3, 1, 3, 2], 2)) == [1, 2]
    print("All tests passed")
```

---

## 4. Dry Run

`nums = [1, 1, 1, 2, 2, 3]`, `k = 2`

Setup: `count = {1: 3, 2: 2, 3: 1}`, then `freq = [[], [3], [2], [1], [], [], []]` (length `7`, index = frequency).

| Shelf `i` | `freq[i]` | `res` after | `len(res) == k`? |
| --- | --- | --- | --- |
| `6`, `5`, `4` | `[]` | `[]` | `False` |
| `3` | `[1]` | `[1]` | `False` |
| `2` | `[2]` | `[1, 2]` | **`True`** → return `[1, 2]` |

---

## 5. Complexity

* **Time:** `O(n)` — counting is one pass, filling the shelves loops over at most `n` distinct numbers, and the reverse walk touches `n + 1` shelves and at most `n` stored numbers.
* **Space:** `O(n)` — `count` holds up to `n` entries and `freq` holds `n + 1` lists with up to `n` numbers in total.

---

## 6. Recall (30 seconds)

* **Count, then shelve:** `count[n]` is the frequency; `freq[c]` holds every number that appears `c` times (`freq` has length `len(nums) + 1`).
* **Read from the top:** loop `i` from `len(freq) - 1` down to `1` and append until `len(res) == k`.
* **Why it wins:** no sorting, so it is linear `O(n)` — better than the `O(n log n)` sort or heap.
