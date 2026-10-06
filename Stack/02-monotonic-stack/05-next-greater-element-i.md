# 496. Next Greater Element I

**LC 496** · **Source:** [+] Claude · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Monotonic decreasing stack + hash map lookup

---

## 1. Intuition

For each number in `nums1`, you want the first bigger number to its right inside `nums2`. Walk through `nums2` once. Keep a stack of numbers that are still **waiting** for something bigger. When a bigger number `cur` shows up, every smaller waiting number has just found its answer.

* `stack` holds **values** from `nums2` that have not found their next greater element yet. Bottom is the biggest, top is the smallest, so it is a **decreasing** stack (from bottom to top).
* `while stack and cur > stack[-1]` pops every waiting value that `cur` beats. This is the moment each popped value learns its answer.
* `res[idx] = cur` writes that answer at the value's position in `nums1`. `idx` comes from `nums1_index`, a map `value → position in nums1`.
* `res = [-1] * len(nums1)` is the default. A value that never gets popped has nothing bigger to its right, so it keeps `-1`.
* `if cur in nums1_index: stack.append(cur)` only waits for numbers we are asked about. Other numbers can still pop, but they never need to be popped.

**Recall:** stack of waiting values; a bigger `cur` pops the smaller ones and becomes their answer; unpopped ones stay `-1`.

## 2. Approach

* **Idea:** One pass over `nums2` with a decreasing stack. Each pop records the next greater element for the popped value.
* **Data structure / pointers:** `stack` is a plain list of values (top is `stack[-1]`). `nums1_index` maps each value of `nums1` to its slot in `res`. `res` is the answer. `cur` is the current number in `nums2`.
* **Invariant:** `stack` is strictly decreasing from bottom to top (the values are distinct), and every value on it is still waiting for a bigger number to its right. Anything already popped has its answer written.
* **Why decreasing:** before pushing `cur` we pop everything smaller than it, so what remains below is bigger than `cur`.
* **Edge cases:**
  * **Stack empty when `cur` arrives:** the `while stack and ...` check fails, so nothing is popped and `cur` is just pushed (if it is in `nums1`).
  * **Single element** (`nums1 = [1]`, `nums2 = [1]`): `1` is pushed, never popped, and the result is `[-1]`.
  * **Strictly decreasing `nums2`** (`[4, 3, 2, 1]`): nothing ever pops, so the result is all `-1`.
  * **Strictly increasing `nums2`** (`[1, 2, 3, 4]`): each new number pops the one before it, so each value gets its right neighbor.
  * **Values not in `nums1`** (like `3` in the dry run): they pop smaller values but are never pushed.

## 3. Code

```python
from collections import defaultdict


class Solution:

    def nextGreaterElement(
        self, nums1: list[int], nums2: list[int]
    ) -> list[int]:
        nums1_index = {num: i for i, num in enumerate(nums1)}
        res = [-1] * len(nums1)
        stack = []

        for cur in nums2:
            # While stack top is smaller than current element, `cur` is its next greater element
            while stack and cur > stack[-1]:
                val = stack.pop()
                idx = nums1_index[val]
                res[idx] = cur

            # Only track elements that are present in nums1
            if cur in nums1_index:
                stack.append(cur)

        return res
```

### Alternative: Precompute for all of `nums2`

Instead of filtering while scanning, record the next greater element for every number in `nums2` in a dict `next_greater`, then look up each number of `nums1`.

```python
class SolutionPrecompute:

    def nextGreaterElement(
        self, nums1: list[int], nums2: list[int]
    ) -> list[int]:
        next_greater = {}
        stack = []

        for cur in nums2:
            while stack and cur > stack[-1]:
                next_greater[stack.pop()] = cur
            stack.append(cur)

        return [next_greater.get(num, -1) for num in nums1]


if __name__ == "__main__":
    # Shared tests: run against both Solution and SolutionPrecompute
    for solver in (Solution(), SolutionPrecompute()):
        assert solver.nextGreaterElement([4, 1, 2], [1, 3, 4, 2]) == [-1, 3, -1]
        assert solver.nextGreaterElement([2, 4], [1, 2, 3, 4]) == [3, -1]
        assert solver.nextGreaterElement([1], [1]) == [-1]
        assert solver.nextGreaterElement([1, 2, 3, 4], [4, 3, 2, 1]) == [-1, -1, -1, -1]
        assert solver.nextGreaterElement([1, 2, 3], [1, 2, 3, 4]) == [2, 3, 4]
        assert solver.nextGreaterElement([], [1, 2]) == []
    print("All tests passed")
```

## 4. Dry Run

Input: `nums1 = [4, 1, 2]`, `nums2 = [1, 3, 4, 2]`

Start: `nums1_index = {4: 0, 1: 1, 2: 2}`, `res = [-1, -1, -1]`, `stack = []`

| Step | `cur` | What happens | `res` after | `stack` after |
|---|---|---|---|---|
| 1 | `1` | Stack empty, `1` is in `nums1`, push | `[-1, -1, -1]` | `[1]` |
| 2 | `3` | `3 > 1`: pop `1`, `res[1] = 3`. `3` is not in `nums1`, no push | `[-1, 3, -1]` | `[]` |
| 3 | `4` | Stack empty, push | `[-1, 3, -1]` | `[4]` |
| 4 | `2` | `2 < 4`, no pop. `2` is in `nums1`, push | `[-1, 3, -1]` | `[4, 2]` |

Result: `[-1, 3, -1]`. The values `4` and `2` stay on the stack, so they keep `-1`.

## 5. Complexity

* **Time:** O(m + n), where m is `len(nums1)` and n is `len(nums2)`, because building `nums1_index` is O(m), and the loop over `nums2` pushes and pops each value at most once.
* **Space:** O(m) extra, because `nums1_index` and `stack` hold only values from `nums1`, plus the output `res`. (The alternative uses O(n) for `next_greater`.)

## 6. Recall (30 seconds)

* One pass over `nums2` with a decreasing `stack` of values waiting for a bigger one.
* `while stack and cur > stack[-1]`: pop, and `cur` is that value's answer, written with `nums1_index`.
* Push `cur` only if it is in `nums1`; anything never popped stays `-1`.
