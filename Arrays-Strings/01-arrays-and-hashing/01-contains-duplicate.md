# 217. Contains Duplicate

**LC 217** · **Source:** NC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Hash set (seen-set)

---

## 1. Intuition

You are checking names at a door with a notebook. For each person, look in the notebook: if the name is
already there, you have found a duplicate and you stop. If not, write the name down and move on.

* `seen = set()` is the notebook. A set answers "have I seen this?" in `O(1)` on average.
* `if num in seen: return True` is the early exit — the first repeat ends the search, so the rest of the list is never read.
* `seen.add(num)` only runs for numbers that were not in `seen`, so `seen` never holds a duplicate.
* `return False` is reached only when the loop finished and no number repeated.
* In the alternative, `len(nums) != len(set(nums))` uses the same idea in one line: a set drops repeats, so a shorter set means something repeated. It has to build the whole set first, so there is no early exit.

**Recall:** keep a `seen` set; if `num in seen`, return `True`, otherwise add it.

---

## 2. Approach

* **Idea:** one pass. For each `num`, check `seen` *before* adding it. A hit means a duplicate.
* **Data structure / pointers:** `seen` is the set of numbers visited so far. `num` is the current element.
* **Invariant:** at the start of each iteration, `seen` holds exactly the numbers before the current position, and all of them are different (if two were equal, we would already have returned `True`).
* **Edge cases:**
  * Empty list → `False` (the loop never runs).
  * One element → `False`.
  * All elements equal → `True` on the second element.
  * Duplicates far apart → still found; the set does not care about distance.
  * Negatives and `0` → fine, any `int` can go in a set.

---

## 3. Code

```python
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        seen = set()

        for num in nums:
            if num in seen:
                return True
            seen.add(num)

        return False


if __name__ == "__main__":
    solution = Solution()
    assert solution.containsDuplicate([1, 2, 3, 1]) is True
    assert solution.containsDuplicate([1, 2, 3, 4]) is False
    assert solution.containsDuplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) is True
    print("All tests passed")
```

### Alternative: Set length comparison

Shorter, but it always builds the whole set — no early exit. Same `O(n)` time and `O(n)` space.

```python
class Solution:
    def containsDuplicate(self, nums: list[int]) -> bool:
        return len(nums) != len(set(nums))


if __name__ == "__main__":
    solution = Solution()
    assert solution.containsDuplicate([1, 2, 3, 1]) is True
    assert solution.containsDuplicate([1, 2, 3, 4]) is False
    assert solution.containsDuplicate([1, 1, 1, 3, 3, 4, 3, 2, 4, 2]) is True
    print("All tests passed")
```

---

## 4. Dry Run

`nums = [1, 2, 3, 1]`

| Index `i` | `num` | `num in seen`? | Action | `seen` after |
| --- | --- | --- | --- | --- |
| `0` | `1` | `False` | add `1` | `{1}` |
| `1` | `2` | `False` | add `2` | `{1, 2}` |
| `2` | `3` | `False` | add `3` | `{1, 2, 3}` |
| `3` | `1` | `True` | **return `True`** | `{1, 2, 3}` |

---

## 5. Complexity

* **Time:** `O(n)` — one pass, and each `num in seen` and `seen.add(num)` is `O(1)` on average. It can stop early at the first repeat.
* **Space:** `O(n)` — `seen` can hold up to `n` numbers when there is no duplicate.

---

## 6. Recall (30 seconds)

* **Core move:** a `seen` set — check `num in seen` first, then `seen.add(num)`.
* **Trade-off:** spend `O(n)` memory to get `O(n)` time; the brute force (compare every pair) is `O(n²)` time and `O(1)` space.
* **Early exit:** the explicit loop stops at the first repeat; `len(nums) != len(set(nums))` always reads all `n` numbers.
