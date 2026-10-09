# 560. Subarray Sum Equals K

**LC 560** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Prefix sum + hash map

---

## 1. Intuition

Sliding window ([[26-minimum-size-subarray-sum]]) needs every number positive so shrinking the window always
shrinks the sum — negatives break that. Instead, track the running sum (`total`) as a prefix sum. Any
subarray's sum is `prefix_sum[i] - prefix_sum[j]` for some earlier `j`, so a subarray summing to `k` exists
exactly when some earlier prefix sum equals `total - k`. Keep a hash map counting how many times each prefix
sum has occurred, and every number becomes an `O(1)` lookup instead of an `O(n)` rescan.

* `sub_num[0] = 1` is the "empty prefix" — it lets a subarray starting at index `0` be counted, since its sum is `total - 0`.
* `total += n` extends the running prefix sum.
* `count += sub_num[total - k]` — every earlier index whose prefix sum equals `total - k` marks the start of a subarray (ending here) that sums to exactly `k`.
* `sub_num[total] += 1` records this position's own prefix sum, *after* the lookup — so a subarray never uses its own ending position as its own start.

**Recall:** `count += sub_num[total - k]`, then `sub_num[total] += 1` — look up before you record, or the current index would count as its own start.

---

## 2. Approach

* **Idea:** turn "does a subarray summing to `k` exist ending here?" into "has the prefix sum `total - k` been seen before?" — a hash map lookup instead of rescanning.
* **Data structure / pointers:** `sub_num` maps a prefix sum value to how many earlier indices produced it; `total` is the running prefix sum; `count` accumulates the answer.
* **Invariant:** at the moment `count += sub_num[total - k]` runs, `sub_num` holds the counts of every prefix sum from index `0` up to (but not including) the current position — so the lookup only matches subarrays that actually end at or before the current index and start strictly after some earlier position.
* **Edge cases:**
  * `k = 0` → `sub_num[0] = 1` is exactly what prevents this from silently double-counting an empty subarray; the look-up-then-record order is what makes `k = 0` safe.
  * All zeros with `k = 0` → correctly counts every contiguous run, since each new `0` matches every previous `0`-sum prefix.
  * Negative numbers → work naturally, since prefix sums can go up or down; there's no assumption of monotonicity.
  * No subarray sums to `k` → `count` stays `0`.
  * A subtlety worth knowing: because `sub_num` is a `defaultdict(int)`, the read `sub_num[total - k]` inserts that key with value `0` if it wasn't already present — harmless for correctness, but if you ever print `sub_num` mid-run, you'll see extra `0`-valued keys that were only touched by a lookup, not a real prefix sum.

---

## 3. Code

```python
from collections import defaultdict


class Solution:

    def subarraySum(self, nums: list[int], k: int) -> int:
        sub_num = defaultdict(int)
        sub_num[0] = 1  # Base case: empty prefix has sum 0
        total = 0
        count = 0

        for n in nums:
            total += n

            # Check if there exists a previous prefix sum equal to (total - k)
            count += sub_num[total - k]

            # Record current prefix sum
            sub_num[total] += 1

        return count


if __name__ == "__main__":
    solution = Solution()
    assert solution.subarraySum([1, 2, 3], 3) == 2
    assert solution.subarraySum([1, 1, 1], 2) == 2
    assert solution.subarraySum([0, 0, 0], 0) == 6
    assert solution.subarraySum([1, -1, 0], 0) == 3
    print("All tests passed")
```

---

## 4. Dry Run

`nums = [1, 2, 3]`, `k = 3`. Start: `sub_num = {0: 1}`, `total = 0`, `count = 0`.

| Step | `n` | `total` | `target = total - k` | matches (`sub_num[target]`) | `count` after | new prefix recorded |
| --- | --- | --- | --- | --- | --- | --- |
| **1** | `1` | `1` | `-2` | `0` | `0` | `sub_num[1] = 1` |
| **2** | `2` | `3` | `0` | `1` | **`1`** (subarray `[1, 2]`) | `sub_num[3] = 1` |
| **3** | `3` | `6` | `3` | `1` | **`2`** (subarray `[3]`) | `sub_num[6] = 1` |

**Return:** `2`

---

## 5. Complexity

* **Time:** `O(n)` — one pass, with `O(1)` average dict lookups and inserts.
* **Space:** `O(n)` — `sub_num` can hold up to `n + 1` distinct prefix sums.

---

## 6. Recall (30 seconds)

* **Reframe the question:** "subarray sums to `k`, ending here" = "has prefix sum `total - k` been seen before?"
* **Base case:** `sub_num[0] = 1` accounts for subarrays starting at index `0`.
* **Order matters:** look up `sub_num[total - k]` *before* recording `sub_num[total] += 1`, or the current index would incorrectly count itself as a valid start (breaks `k = 0` in particular).
