# 1. Two Sum

**LC 1** · **Source:** LC150 + NC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Complement lookup (hash map)

---

## 1. Intuition

Checking every pair is `O(n²)`. Instead, for each number ask one question: "what partner would finish
the sum, and have I already seen it?" Keep a notebook of past numbers and where they were, so that
question is a single lookup.

* `complement = target - num` is the partner this number needs.
* `seen = {}` is the notebook: number → index where it appeared.
* `if complement in seen` is the "have I already seen my partner?" check, `O(1)` on average.
* `return [seen[complement], i]` gives the partner's stored index and the current index.
* `seen[num] = i` comes *after* the check, so a number can never pair with itself.

**Recall:** `complement = target - num`; look it up in `seen` first, then store `num`.

---

## 2. Approach

* **Idea:** one pass. For each `num`, compute its `complement` and look it up in `seen`. A hit means the answer; a miss means store `num` and move on.
* **Data structure / pointers:** `seen` maps a number to its index. `i` is the current index, `num` is the current value.
* **Invariant:** at the start of each iteration, `seen` holds every number before index `i` with its index, and no earlier pair added up to `target` (or we would already have returned).
* **Edge cases:**
  * Duplicates such as `[3, 3]`, `target = 6` → works, because the check happens before `seen[num] = i`.
  * The same element cannot be used twice, for the same reason.
  * Negatives and `0` → the formula `target - num` needs no special handling.
  * No valid pair → the loop ends and the function returns `None`; the problem guarantees exactly one answer, so this does not happen.

---

## 3. Code

```python
class Solution:
    def twoSum(self, nums: list[int], target: int) -> list[int]:

        seen = {}

        for i, num in enumerate(nums):
            complement = target - num

            if complement in seen:
                return [seen[complement], i]

            seen[num] = i


if __name__ == "__main__":
    solution = Solution()
    assert solution.twoSum([2, 7, 11, 15], 9) == [0, 1]
    assert solution.twoSum([3, 2, 4], 6) == [1, 2]
    assert solution.twoSum([3, 3], 6) == [0, 1]
    print("All tests passed")
```

---

## 4. Dry Run

`nums = [2, 7, 11, 15]`, `target = 9`

| Index `i` | `num` | `complement` | `complement in seen`? | Action | `seen` after |
| --- | --- | --- | --- | --- | --- |
| `0` | `2` | `7` | `False` | store `seen[2] = 0` | `{2: 0}` |
| `1` | `7` | `2` | `True` | **return `[0, 1]`** | `{2: 0}` |

---

## 5. Complexity

* **Time:** `O(n)` — one pass; each `complement in seen` and `seen[num] = i` is `O(1)` on average.
* **Space:** `O(n)` — `seen` can hold up to `n` numbers before a pair is found.

---

## 6. Recall (30 seconds)

* **Core formula:** `complement = target - num`.
* **Data structure:** `seen = {number: index}` for `O(1)` average lookups.
* **Order matters:** check for the complement *before* storing `num`, so the same element is never used twice.
