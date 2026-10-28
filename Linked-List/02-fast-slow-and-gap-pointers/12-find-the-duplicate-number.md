# 287. Find the Duplicate Number

**LC 287** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Floyd's cycle detection on an array (treat `nums[i]` as the "next" pointer of index `i`)

---

## 1. Intuition

There are `n + 1` numbers, all between `1` and `n`. Treat the array as a linked list: from index `i`, the next node is index `nums[i]`. Every value is a valid index, so you can always take another step and never fall off the end, which means you must eventually loop. Two indices holding the same value both point to the same next node, so that node has two ways in. That node is where the cycle begins, and its value is the duplicate. Now it is exactly Linked List Cycle II.

* `slow = nums[0]`, `fast = nums[0]` — start both at the first node of the "list" (index 0 is never part of the cycle, because no value is 0).
* `slow = nums[slow]` — one step; `fast = nums[nums[fast]]` — two steps.
* `if slow == fast: break` — phase 1: they meet somewhere inside the cycle. There is no end to the list, so a plain `while True` is safe.
* `slow = nums[0]` — phase 2: put `slow` back at the start, leave `fast` at the meeting point.
* `slow = nums[slow]; fast = nums[fast]` until equal — both move 1 step; they meet at the cycle entrance, which is the duplicate. `return slow`.

**Recall:** array as a linked list (`i → nums[i]`); meet with 1 and 2 steps; reset `slow` to the start; move both 1 step; where they meet is the duplicate.

## 2. Approach

* **Idea:** Run Floyd's cycle detection on the "list" `i → nums[i]`. The cycle entrance is the duplicate value.
* **Data structure / pointers:**
  * `slow` — a value used as an index; 1 step per loop (`nums[slow]`).
  * `fast` — a value used as an index; 2 steps per loop (`nums[nums[fast]]`) in phase 1, then 1 step in phase 2.
  * No extra arrays or sets, and `nums` is never changed.
* **Invariant:** Same as Cycle II: after phase 1, the distance from the start to the cycle entrance equals a whole number of laps minus the distance already walked inside the cycle. So in phase 2, `slow` (from the start) and `fast` (from the meeting point) reach the entrance on the same step.
* **Edge cases:**
  * `[1, 1]` (smallest valid input): the pointers meet at once, and the answer is `1`.
  * The duplicate appears more than twice (e.g. `[3, 3, 3, 3, 3]`): still works; the cycle entrance is that value.
  * The duplicate is `nums[0]` itself: phase 2 still ends on it.
  * Values are always in `1..n`, so `nums[x]` never goes out of range, and index 0 is never reached again after the start.
  * The problem says to use O(1) extra space and not modify the array, which rules out a set, sorting, and negative marking. That is why Floyd's algorithm is used.

## 3. Code

```python
class Solution:
    def findDuplicate(self, nums: list[int]) -> int:
        # Phase 1: Find the intersection point of the two runners in the cycle
        slow = nums[0]
        fast = nums[0]

        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break

        # Phase 2: Find the entrance to the cycle (the duplicate number)
        slow = nums[0]
        while slow != fast:
            slow = nums[slow]
            fast = nums[fast]

        return slow


if __name__ == "__main__":
    solution = Solution()
    assert solution.findDuplicate([1, 3, 4, 2, 2]) == 2
    assert solution.findDuplicate([3, 1, 3, 4, 2]) == 3
    assert solution.findDuplicate([3, 3, 3, 3, 3]) == 3
    assert solution.findDuplicate([1, 1]) == 1
    assert solution.findDuplicate([2, 2, 2, 2, 2]) == 2
    print("All tests passed")
```

## 4. Dry Run

`nums = [1, 3, 4, 2, 2]`. As a list: `0 → 1`, `1 → 3`, `2 → 4`, `3 → 2`, `4 → 2`. So the path from index 0 is `0 → 1 → 3 → 2 → 4 → 2 → 4 → …`; the cycle is `2 ⇄ 4` and it starts at `2`.

**Phase 1:** `slow = fast = nums[0] = 1`.

| Step | `slow = nums[slow]` | `fast = nums[nums[fast]]` | Equal? |
| --- | --- | --- | --- |
| 1 | `nums[1] = 3` | `nums[nums[1]] = nums[3] = 2` | no |
| 2 | `nums[3] = 2` | `nums[nums[2]] = nums[4] = 2` | **yes → `break`** |

**Phase 2:** `slow = nums[0] = 1`, `fast = 2`.

| Step | `slow` | `fast` | Equal? |
| --- | --- | --- | --- |
| Reset | `1` | `2` | no |
| 1 | `nums[1] = 3` | `nums[2] = 4` | no |
| 2 | `nums[3] = 2` | `nums[4] = 2` | **yes** |

Return `slow` = `2`, the duplicate.

## 5. Complexity

* **Time:** O(n) — phase 1 meets within about n steps (the walk is at most `n + 1` nodes long before the cycle is entered and repeated), and phase 2 takes at most that many steps again.
* **Space:** O(1) — only `slow` and `fast`; the array is read, never changed.

## 6. Recall (30 seconds)

* Array as a linked list: from index `i` the next node is `nums[i]`; the duplicate is the cycle entrance.
* Phase 1: `slow = nums[slow]`, `fast = nums[nums[fast]]` until equal. Phase 2: `slow = nums[0]`, both move 1 step until equal.
* Return `slow`. No set, no sorting, no changes to `nums` — O(1) space.
