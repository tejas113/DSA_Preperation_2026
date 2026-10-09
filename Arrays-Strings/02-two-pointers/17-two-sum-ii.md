# 167. Two Sum II — Input Array Is Sorted

**LC 167** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Two pointers from opposite ends, on a sorted array

---

## 1. Intuition

Two Sum ([[03-two-sum]]) uses a hash map because the array isn't sorted. Here it is sorted, which means
moving a pointer has a predictable effect: moving `left` right can only *increase* the sum, and moving
`right` left can only *decrease* it. So start from both ends and let the sum tell you which side is wrong.

* `left, right = 0, len(numbers) - 1` start at the smallest and largest values.
* `current_sum < target` means the sum is too small, so `left += 1` reaches for a bigger number.
* `current_sum > target` means the sum is too big, so `right -= 1` reaches for a smaller number.
* `current_sum == target` is the answer; `[left + 1, right + 1]` converts to the 1-indexed positions the problem asks for.

**Recall:** two pointers from the ends; if the sum is too small move `left` up, too big move `right` down, and return 1-indexed positions on a match.

---

## 2. Approach

* **Idea:** because the array is sorted, each pointer move changes the sum in a known direction, so there is never a need to backtrack.
* **Data structure / pointers:** `left` starts at index `0`, `right` at the last index. No extra storage.
* **Invariant:** the true answer's two indices are always still between `left` and `right` (inclusive) — a pointer only ever moves past a value that provably cannot be part of the answer.
* **Edge cases:**
  * Exactly two elements → `left = 0`, `right = 1` is the only pair checked.
  * Negative numbers → the comparisons still hold, since the array is sorted, not necessarily positive.
  * Duplicate values → still works, since the pointers move based on the sum, not on uniqueness.
  * The problem guarantees exactly one solution, so the `return []` at the end is unreachable under the stated constraints, but keeps the function total.

---

## 3. Code

```python
class Solution:

    def twoSum(self, numbers: list[int], target: int) -> list[int]:
        left, right = 0, len(numbers) - 1

        while left < right:
            current_sum = numbers[left] + numbers[right]

            if current_sum == target:
                return [left + 1, right + 1]  # 1-indexed output
            elif current_sum < target:
                left += 1  # Need a larger value
            else:
                right -= 1  # Need a smaller value

        return []


if __name__ == "__main__":
    solution = Solution()
    assert solution.twoSum([2, 7, 11, 15], 9) == [1, 2]
    assert solution.twoSum([2, 3, 4], 6) == [1, 3]
    assert solution.twoSum([-1, 0], -1) == [1, 2]
    print("All tests passed")
```

---

## 4. Dry Run

`numbers = [2, 7, 11, 15]`, `target = 9`

| Iteration | `left` | `numbers[left]` | `right` | `numbers[right]` | `current_sum` | Action |
| --- | --- | --- | --- | --- | --- | --- |
| **1** | `0` | `2` | `3` | `15` | `17` | `17 > 9` → `right -= 1` |
| **2** | `0` | `2` | `2` | `11` | `13` | `13 > 9` → `right -= 1` |
| **3** | `0` | `2` | `1` | `7` | `9` | `9 == 9` → return `[1, 2]` |

---

## 5. Complexity

* **Time:** `O(n)` — `left` only increases and `right` only decreases, so together they take at most `n` steps before crossing.
* **Space:** `O(1)` — only the two pointers and the running sum.

---

## 6. Recall (30 seconds)

* **Why two pointers work here:** the array is sorted, so moving `left` up only raises the sum and moving `right` down only lowers it — no other move could help.
* **Direction rule:** sum too small → `left += 1`; sum too big → `right -= 1`.
* **Don't forget:** the answer is 1-indexed — return `[left + 1, right + 1]`, not `[left, right]`.
