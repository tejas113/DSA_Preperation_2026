# 11. Maximum Product Subarray

**LC 152** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Running Product / Prefix-Suffix Scan (Kadane-style)

---

## 1. Intuition

Products behave differently from sums: two negatives make a positive, and a zero wipes everything out. Treat the array as runs separated by zeros. In a zero-free run, if the count of negatives is even, the product of the whole run is the best. If it's odd, you must give up **one** negative, and the best you can do is drop everything up to and including the first negative, or everything from the last negative onward. Either way the best subarray is a **prefix or a suffix** of the run, so scanning products from both ends finds it.

* `pre` — the product of the run from the left, since the last zero.
* `suff` — the same product from the right (`nums[n - 1 - i]`).
* why both — with an odd number of negatives, dropping the tail keeps a **prefix** and dropping the head keeps a **suffix**; the best is one of those two.
* `if pre == 0: pre = 1` (and the same for `suff`) — a zero kills every product through it, so start fresh after it.
* `ans = max(ans, pre, suff)` — keep the best product seen from either side. It starts at `-inf` so a lone negative number still counts.

**Recall:** the best subarray is a prefix or suffix of a zero-free run, so scan from both ends and reset at zeros.

## 2. Template

* **State:** `pre` / `suff` = running product from the left / from the right of the current zero-free run
* **Choice:** keep multiplying, or restart from 1 after a zero
* **Recurrence:** `pre *= nums[i]`, `suff *= nums[n - 1 - i]`, `ans = max(ans, pre, suff)`
* **Base:** `pre = suff = 1`, `ans = -inf`
* **Guard:** a zero resets that side's product to 1, since it splits the array into independent runs

## 3. Code

**Prefix-suffix scan** (primary solution). There is no memoization here, because one pass with three variables is enough.

```python
class Solution:
    def maxProduct(self, nums: list[int]) -> int:
        pre = 1
        suff = 1
        ans = float('-inf')
        n = len(nums)

        for i in range(n):
            # Reset prefix/suffix product if previous product was 0
            if pre == 0:
                pre = 1
            if suff == 0:
                suff = 1

            pre *= nums[i]
            suff *= nums[n - 1 - i]

            ans = max(ans, pre, suff)

        return ans
```

### Alternative: Running min/max DP

The DP way to see the same problem: track the **largest and smallest** product of a subarray ending at each index. A negative number flips them, because the smallest (most negative) product times a negative becomes the largest. This is a 1D DP (`dp_max[i]`, `dp_min[i]`) rolled into two variables, so it is already O(1) space.

```python
class Solution:
    def maxProduct(self, nums: list[int]) -> int:
        res = max(nums)
        cur_min, cur_max = 1, 1

        for n in nums:
            if n == 0:
                cur_min, cur_max = 1, 1
                continue
            
            # Store temp before overwriting cur_max
            tmp = cur_max * n
            cur_max = max(n * cur_max, n * cur_min, n)
            cur_min = min(tmp, n * cur_min, n)

            res = max(res, cur_max)

        return res
```

## 4. Dry Run (`nums = [1, 0, -3, 4, -2]`)

| `i` | `nums[i]` | `pre` | `nums[n-1-i]` | `suff` | `ans` |
|---|---|---|---|---|---|
| 0 | 1 | 1 | -2 | -2 | 1 |
| 1 | 0 | 0 | 4 | -8 | 1 |
| 2 | -3 | -3 (reset from 0 first) | -3 | 24 | 24 |
| 3 | 4 | -12 | 0 | 0 | 24 |
| 4 | -2 | 24 | 1 (reset from 0 first) | 1 | 24 |

Both scans find the best run `-3 · 4 · -2 = 24`, `suff` at `i = 2` and `pre` at `i = 4`, from opposite ends.

## 5. Complexity

* **States:** nothing is stored, only the three running variables `pre`, `suff` and `ans`.
* **Time:** O(n) — one loop, and each iteration does two multiplications and one `max`.
* **Space:** O(1) — just those three variables (the min/max DP is O(n) time, O(1) space too).

## 6. Recall (30 seconds)

* **Idea:** with an odd number of negatives the best subarray is a prefix or suffix of a zero-free run, so scan from both ends.
* **Reset:** a zero resets that side's product to 1.
* **Alternative:** track `cur_max` and `cur_min` together, because a negative flips them.
