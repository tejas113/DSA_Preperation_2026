# 189. Rotate Array

**LC 189** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Three reversals

---

## 1. Intuition

Rotating right by `k` moves the last `k` elements to the front and shifts everything else right — awkward to
do directly without extra space. But three reversals accomplish exactly that: reverse each of the two
pieces individually first (which puts each piece's *own* elements in the wrong order), then reverse the
whole array (which flips both the piece order *and* undoes each piece's internal reversal, landing every
element in its final correct position and order).

* `k = k % n` — rotating by a full array length changes nothing, so any `k >= n` collapses to its remainder.
* `reverse(0, n - k - 1)` reverses the first `n - k` elements (the part that moves to the *back* after rotation).
* `reverse(n - k, n - 1)` reverses the last `k` elements (the part that moves to the *front*).
* `reverse(0, n - 1)` reverses everything — this swaps the two pieces' positions *and* un-reverses each piece internally, since reversing an already-reversed sequence restores its original order.

**Recall:** reverse the first `n-k` elements, reverse the last `k` elements, then reverse the whole array.

---

## 2. Approach

* **Idea:** two reversals scramble each piece's internal order on purpose; the final whole-array reversal both relocates the pieces and un-scrambles them, in one pass.
* **Data structure / pointers:** a single in-place `reverse(start, end)` helper, called three times with different ranges.
* **Invariant:** after the first two reversals, each of the two pieces holds its correct final elements but in reverse order; the third reversal is what restores the correct order within each piece while also swapping which piece comes first.
* **Edge cases:**
  * `k = 0` or `k = n` → `k % n == 0`; the first reversal covers the whole array, the second does nothing (`reverse(n, n-1)` has `start > end`), and the third reversal restores the original order — net effect: no change.
  * `k > n` → normalized by `k % n`, so it behaves identically to a smaller equivalent `k`.
  * Single-element array → `k % 1 == 0` always, so nothing happens regardless of `k`.
  * `k` exactly `n - 1` or `1` → still handled correctly; the reversal ranges just become very unbalanced (one piece of size `1`, one of size `n-1`).

---

## 3. Code

```python
class Solution:

    def rotate(self, nums: list[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        k = k % n  # Handle cases where k >= n

        def reverse(start: int, end: int) -> None:
            while start < end:
                nums[start], nums[end] = nums[end], nums[start]
                start += 1
                end -= 1

        # Step 1: Reverse first n - k elements
        reverse(0, n - k - 1)
        # Step 2: Reverse remaining k elements
        reverse(n - k, n - 1)
        # Step 3: Reverse the entire array
        reverse(0, n - 1)


if __name__ == "__main__":
    solution = Solution()

    nums = [1, 2, 3, 4, 5, 6, 7]
    solution.rotate(nums, 3)
    assert nums == [5, 6, 7, 1, 2, 3, 4]

    single = [1]
    solution.rotate(single, 5)
    assert single == [1]

    no_rotation = [1, 2, 3]
    solution.rotate(no_rotation, 0)
    assert no_rotation == [1, 2, 3]

    print("All tests passed")
```

### Alternative: brute force, shift by 1 repeated k times — O(k · n), TLEs on large inputs

```python
class SolutionBrute:

    def rotate(self, nums: list[int], k: int) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        n = len(nums)
        k %= n

        # Rotate right by 1 step, repeated k times
        for _ in range(k):
            previous = nums[-1]  # Store last element
            for i in range(n):
                nums[i], previous = previous, nums[i]


if __name__ == "__main__":
    solution = SolutionBrute()
    nums = [1, 2, 3, 4, 5, 6, 7]
    solution.rotate(nums, 3)
    assert nums == [5, 6, 7, 1, 2, 3, 4]
    print("All tests passed")
```

### Alternative: slice reassignment — O(n) time, O(n) space

```python
class SolutionSlice:

    def rotate(self, nums: list[int], k: int) -> None:
        n = len(nums)
        k %= n
        # Re-assign slice in-place
        nums[:] = nums[n - k :] + nums[: n - k]


if __name__ == "__main__":
    solution = SolutionSlice()
    nums = [1, 2, 3, 4, 5, 6, 7]
    solution.rotate(nums, 3)
    assert nums == [5, 6, 7, 1, 2, 3, 4]
    print("All tests passed")
```

---

## 4. Dry Run

`nums = [1, 2, 3, 4, 5, 6, 7]`, `k = 3` (so `n - k = 4`)

| Step | Range | Segment before | Segment after | Full array after |
| --- | --- | --- | --- | --- |
| `reverse(0, 3)` | `0` to `n-k-1` | `[1, 2, 3, 4]` | `[4, 3, 2, 1]` | `[4, 3, 2, 1, 5, 6, 7]` |
| `reverse(4, 6)` | `n-k` to `n-1` | `[5, 6, 7]` | `[7, 6, 5]` | `[4, 3, 2, 1, 7, 6, 5]` |
| `reverse(0, 6)` | `0` to `n-1` | `[4, 3, 2, 1, 7, 6, 5]` | `[5, 6, 7, 1, 2, 3, 4]` | `[5, 6, 7, 1, 2, 3, 4]` |

**Return (in-place):** `[5, 6, 7, 1, 2, 3, 4]`

---

## 5. Complexity

* **Time:** `O(n)` — three reversals, together touching each element a constant number of times (roughly `2n` swaps total).
* **Space:** `O(1)` — all swaps happen in place.

**Alternatives:** brute force is `O(k · n)` (TLEs for large `k`, `n`); slice reassignment is `O(n)` time but `O(n)` space, since it builds a new list before reassigning.

---

## 6. Recall (30 seconds)

* **Three reversals:** first `n-k` elements, last `k` elements, then the whole array.
* **Why it works:** reversing each piece first, then reversing everything, both relocates the pieces *and* restores their internal order in one combined operation.
* **Always normalize first:** `k = k % n` handles `k >= n` and `k = 0` uniformly.
