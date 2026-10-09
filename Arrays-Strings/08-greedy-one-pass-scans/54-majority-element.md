# 169. Majority Element

**LC 169** · **Source:** LC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Boyer-Moore voting

---

## 1. Intuition

The majority element appears more than half the time, so if you paired up every majority occurrence with a
non-majority occurrence and cancelled them out, at least one majority instance would always survive. That's
exactly what a running `count` simulates: every match with the current `candidate` adds a vote, every
mismatch cancels one out, and because the majority element outnumbers everything else combined, it can never
be fully cancelled away.

* `candidate` is the current guess for the majority element; `count` tracks its "net votes" so far.
* `if count == 0: candidate = num` — whenever the running tally hits zero, the current candidate has been fully cancelled out, so start fresh with whatever number is next.
* `if num == candidate: count += 1 else: count -= 1` — a match adds a vote, a mismatch removes one, treating every non-candidate number as "opposition."
* The problem guarantees a majority element exists, so whatever `candidate` holds when the loop ends is guaranteed correct — no verification pass is needed.

**Recall:** track a `candidate` and a `count`; reset the candidate whenever `count` hits `0`; `+1` on a match, `-1` on a mismatch.

---

## 2. Approach

* **Idea:** simulate cancelling out one majority vote against one non-majority vote at a time — since the majority element outnumbers everything else combined, it's mathematically guaranteed to survive every round of cancellation.
* **Data structure / pointers:** just `candidate` and `count`, both scalars.
* **Invariant:** whenever `count > 0`, the number of times `candidate` has appeared so far, minus the number of times anything else has appeared so far (since `candidate` was last reset), equals `count` — so `candidate` can never be eliminated before the true majority element would be.
* **Edge cases:**
  * Single element → `candidate` is set on the first (and only) iteration, `count` becomes `1`, returned directly.
  * Majority element appears in an alternating pattern (`[3,1,3,1,3]`) → count oscillates between `0` and `1`, but the extra occurrence at the end means `3` is what survives.
  * The algorithm never checks whether `candidate` is *actually* the majority — it relies entirely on the problem's guarantee that one exists; without that guarantee, this would need a second pass to verify.

---

## 3. Code

```python
class Solution:

    def majorityElement(self, nums: list[int]) -> int:
        count = 0
        candidate = None

        for num in nums:
            # Pick a new candidate when counter hits zero
            if count == 0:
                candidate = num

            # Increment count for matches, decrement for mismatches
            if num == candidate:
                count += 1
            else:
                count -= 1

        return candidate


if __name__ == "__main__":
    solution = Solution()
    assert solution.majorityElement([2, 2, 1, 1, 1, 2, 2]) == 2
    assert solution.majorityElement([1]) == 1
    assert solution.majorityElement([3, 1, 3, 1, 3]) == 3
    assert solution.majorityElement([1, 1, 1, 2, 2]) == 1
    print("All tests passed")
```

---

## 4. Dry Run

`nums = [2, 2, 1, 1, 1, 2, 2]`

| `num` | `count` before | Action | `candidate` after | `count` after |
| --- | --- | --- | --- | --- |
| `2` | `0` | new candidate `2`, match | `2` | `1` |
| `2` | `1` | match | `2` | `2` |
| `1` | `2` | mismatch | `2` | `1` |
| `1` | `1` | mismatch | `2` | `0` |
| `1` | `0` | new candidate `1`, match | `1` | `1` |
| `2` | `1` | mismatch | `1` | `0` |
| `2` | `0` | new candidate `2`, match | `2` | `1` |

**Return:** `2`

---

## 5. Complexity

* **Time:** `O(n)` — a single pass, `O(1)` work per element.
* **Space:** `O(1)` — only `candidate` and `count`.

---

## 6. Recall (30 seconds)

* **Cancellation intuition:** each mismatch cancels one vote for `candidate`; the true majority element can never be fully cancelled, since it outnumbers everything else combined.
* **Reset rule:** `count == 0` → pick a fresh candidate.
* **Extension — Majority Element II (LC 229):** find elements appearing more than `n/3` times using the same idea, generalized to *two* candidates and *two* counters.
