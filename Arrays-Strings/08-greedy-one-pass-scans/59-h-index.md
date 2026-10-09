# 274. H-Index

**LC 274** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Sort, then find where "papers remaining" drops to meet citations

---

## 1. Intuition

The h-index is the largest `h` where at least `h` papers each have at least `h` citations. Sorting the
citations ascending turns this into a simple positional fact: after sorting, the number of papers with *at
least* `citations[i]` citations is exactly `n - i` — everything from index `i` to the end. So walk forward
looking for the first spot where a paper's own citation count is enough to cover all the papers that remain
from there on.

* `citations.sort()` orders papers from fewest to most citations.
* `papers_remaining = n - i` is how many papers (including this one) have at least `citations[i]` citations, since everything from `i` onward is `>= citations[i]` after sorting.
* `if citations[i] >= papers_remaining` — this paper's own citation count is high enough to be one of the `papers_remaining` papers needed for an h-index of `papers_remaining`; that value is the answer.
* `return 0` only triggers if no index satisfies the condition, meaning even the paper with the most citations doesn't have enough citations to justify any positive h-index alongside the rest.

**Recall:** sort ascending; the first `i` where `citations[i] >= n - i` gives the answer `n - i`.

---

## 2. Approach

* **Idea:** sorting turns "how many papers have at least X citations" into a direct index calculation (`n - i`), so the h-index condition becomes a single comparison per position instead of a fresh count each time.
* **Data structure / pointers:** just the sorted array and the loop index `i`; no extra structure needed.
* **Invariant:** for any index `i` in the sorted array, `n - i` papers (this one and everything after it) are guaranteed to have at least `citations[i]` citations — that's a direct consequence of ascending sort order.
* **Edge cases:**
  * All citations `0` → the condition never holds (even at `i = 0`, `0 >= n` fails for any `n > 0`), correctly returns `0`.
  * All citations very high, exceeding `n` → the very first index already satisfies `citations[0] >= n`, returning `n` (the h-index can never exceed the total paper count).
  * Empty list → the loop never runs, returns `0`.
  * A single paper → h-index is either `0` (no citations) or `1` (any citation), decided by the same single comparison.

---

## 3. Code

```python
class Solution:

    def hIndex(self, citations: list[int]) -> int:
        citations.sort()
        n = len(citations)

        for i in range(n):
            papers_remaining = n - i
            if citations[i] >= papers_remaining:
                return papers_remaining

        return 0


if __name__ == "__main__":
    solution = Solution()
    assert solution.hIndex([3, 0, 6, 1, 5]) == 3
    assert solution.hIndex([0, 0, 0]) == 0
    assert solution.hIndex([100, 200, 300]) == 3
    assert solution.hIndex([]) == 0
    print("All tests passed")
```

### Alternative: counting sort — O(n) time, O(n) space

The h-index can never exceed `n` (the total number of papers), so cap every citation count at `n` and bucket
by citation count. Scanning buckets from the top down and accumulating a running paper total finds the
h-index in linear time, avoiding the `O(n log n)` sort.

```python
class SolutionBucket:

    def hIndex(self, citations: list[int]) -> int:
        n = len(citations)
        buckets = [0] * (n + 1)

        # Populate frequency buckets (cap citations > n at n)
        for c in citations:
            if c >= n:
                buckets[n] += 1
            else:
                buckets[c] += 1

        total_papers = 0
        # Iterate backwards to find maximum h-index
        for h in range(n, -1, -1):
            total_papers += buckets[h]
            if total_papers >= h:
                return h

        return 0


if __name__ == "__main__":
    solution = SolutionBucket()
    assert solution.hIndex([3, 0, 6, 1, 5]) == 3
    assert solution.hIndex([0, 0, 0]) == 0
    assert solution.hIndex([100, 200, 300]) == 3
    print("All tests passed")
```

---

## 4. Dry Run

`citations = [3, 0, 6, 1, 5]` → sorted: `[0, 1, 3, 5, 6]`, `n = 5`

| `i` | `citations[i]` | `papers_remaining = n - i` | `citations[i] >= papers_remaining`? | Action |
| --- | --- | --- | --- | --- |
| `0` | `0` | `5` | `0 >= 5` → False | continue |
| `1` | `1` | `4` | `1 >= 4` → False | continue |
| `2` | `3` | `3` | `3 >= 3` → **True** | **return `3`** |

---

## 5. Complexity

* **Time:** `O(n log n)` — dominated by the sort; the scan afterward is `O(n)`.
* **Space:** `O(1)` extra, beyond what Python's sort itself uses internally.

**Bucket alternative:** `O(n)` time and space — one pass to bucket, one pass backward to find `h`, at the cost of an `O(n)`-sized array.

---

## 6. Recall (30 seconds)

* **After sorting, `n - i` is a free count:** it's exactly how many papers have at least `citations[i]` citations.
* **Stop rule:** first `i` where `citations[i] >= n - i` → answer is `n - i`.
* **Extension — H-Index II (LC 275):** input already sorted → binary search finds the answer in `O(log n)`.
