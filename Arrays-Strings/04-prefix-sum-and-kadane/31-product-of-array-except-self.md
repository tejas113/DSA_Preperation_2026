# 238. Product of Array Except Self

**LC 238** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Prefix and suffix products

---

## 1. Intuition

`res[i]` needs the product of every number except `nums[i]` — that's exactly "everything to the left of
`i`" times "everything to the right of `i`". Division would compute this in one pass, but it breaks on
zeros, so instead build the left product and the right product separately, in two passes, and multiply them
together.

* Pass 1 fills `res[i]` with the product of everything *before* index `i` — `res[i] = prefix`, then `prefix *= nums[i]` updates it for the *next* index, so `res[i]` never includes `nums[i]` itself.
* Pass 2 walks backward, multiplying each `res[i]` by `suffix` — the product of everything *after* index `i` — using the same before-then-update order, so `suffix` never includes `nums[i]` either.
* Since `res[i]` already holds the left product after pass 1, multiplying by the right product in pass 2 gives the full answer, with no separate output array needed.

**Recall:** left pass fills `res[i]` with the product of everything before `i`; right pass multiplies each `res[i]` by the product of everything after `i`.

---

## 2. Approach

* **Idea:** split "everything except `nums[i]`" into "everything before `i`" and "everything after `i`", and compute each with a simple running product — no division needed, so zeros are never a problem.
* **Data structure / pointers:** `res` doubles as both the output array and the storage for prefix products (an `O(1)`-extra-space trick, since the output array doesn't count against the space bound); `prefix` and `suffix` are the two running products.
* **Invariant:** after pass 1, `res[i]` equals the product of `nums[0:i]`. After processing index `i` in pass 2, `res[i]` equals the product of `nums[0:i] * nums[i+1:n]` — the full answer for that index.
* **Edge cases:**
  * One zero in the array → every index except the zero's own gets `0` in its result (since it multiplies against the zero); the zero's own index gets the product of everything else.
  * Two or more zeros → every result is `0`, since every index's product includes at least one of the zeros.
  * Negative numbers → handled naturally, since multiplication doesn't care about sign.
  * Single-element array → `res = [1]`, since there's nothing else to multiply.

---

## 3. Code

```python
class Solution:

    def productExceptSelf(self, nums: list[int]) -> list[int]:
        n = len(nums)
        res = [1] * n

        # Pass 1: Accumulate Prefix Products (Left to Right)
        prefix = 1
        for i in range(n):
            res[i] = prefix
            prefix *= nums[i]

        # Pass 2: Accumulate Suffix Products (Right to Left)
        suffix = 1
        for i in range(n - 1, -1, -1):
            res[i] *= suffix
            suffix *= nums[i]

        return res


if __name__ == "__main__":
    solution = Solution()
    assert solution.productExceptSelf([1, 2, 3, 4]) == [24, 12, 8, 6]
    assert solution.productExceptSelf([-1, 1, 0, -3, 3]) == [0, 0, 9, 0, 0]
    assert solution.productExceptSelf([1]) == [1]
    print("All tests passed")
```

---

## 4. Dry Run

`nums = [1, 2, 3, 4]`

**Pass 1 (prefix):**

| `i` | `nums[i]` | `res[i] = prefix` (before) | `prefix` after |
| --- | --- | --- | --- |
| `0` | `1` | `1` | `1` |
| `1` | `2` | `1` | `2` |
| `2` | `3` | `2` | `6` |
| `3` | `4` | `6` | `24` |

`res` after pass 1: `[1, 1, 2, 6]`

**Pass 2 (suffix, right to left):**

| `i` | `nums[i]` | `res[i] *= suffix` | `res[i]` after | `suffix` after |
| --- | --- | --- | --- | --- |
| `3` | `4` | `6 * 1` | `6` | `4` |
| `2` | `3` | `2 * 4` | `8` | `12` |
| `1` | `2` | `1 * 12` | `12` | `24` |
| `0` | `1` | `1 * 24` | **`24`** | `24` |

**Return:** `[24, 12, 8, 6]`

---

## 5. Complexity

* **Time:** `O(n)` — two sequential passes over `nums`.
* **Space:** `O(1)` extra — `res` is the required output (doesn't count against the space bound), and only `prefix`/`suffix` are extra scalars.

---

## 6. Recall (30 seconds)

* **Split the product:** `res[i] = (product before i) × (product after i)`.
* **No division needed:** two passes with running products handle zeros safely, which a division-based one-pass approach cannot.
* **In-place trick:** store the prefix products directly in `res`, then multiply in the suffix products during the second pass — no second array required.
