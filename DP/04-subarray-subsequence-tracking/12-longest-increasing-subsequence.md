# 12. Longest Increasing Subsequence

**LC 300** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** 1D DP / Take-or-Skip, Patience Sorting

---

## 1. Intuition

Walk through the array once, deciding for each element: **skip it**, or **take it** if it is strictly bigger than the last element you kept. The only thing you need to remember about the past is *which element you kept last*, so the state is the current index plus that "previous" index.

* `dp(i, prev_idx)` — the best increasing-subsequence length obtainable from `nums[i:]`, when the last element kept is at `prev_idx` (`-1` means nothing kept yet).
* `if i == len(nums): return 0` — no elements left, so nothing more can be added.
* `skip = dp(i + 1, prev_idx)` — leave `nums[i]` out; the last kept element is unchanged.
* `if prev_idx == -1 or nums[i] > nums[prev_idx]` — we may only take `nums[i]` if nothing is kept yet, or it is strictly larger than the last kept value.
* `take = 1 + dp(i + 1, i)` — count it, and now `i` is the last kept element.
* `max(skip, take)` — keep the better choice.
* `memo[(i, prev_idx)]` — many skip/take histories end at the same (index, last kept) pair, so each is solved once.

**Recall:** at each element, `max(skip, take)`, where take needs `nums[i] > nums[prev_idx]`.

## 2. Template

* **State:** `dp(i, prev_idx)` = best length from `nums[i:]` given the last kept index
* **Choice:** skip `nums[i]`, or take it (only if it beats the last kept value)
* **Recurrence:** `dp(i, prev) = max(dp(i + 1, prev), 1 + dp(i + 1, i))`, where the take is allowed only if `nums[i] > nums[prev]`
* **Base:** `dp(len(nums), ·) = 0`
* **Guard:** `prev_idx == -1` means nothing has been taken yet, so the first element is always allowed

## 3. Code

**Top-down with memoization** (primary solution).

```python
class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        memo = {}

        def dp(i: int, prev_idx: int) -> int:
            # Base Case: Reached end of array
            if i == len(nums):
                return 0

            # Check cache
            if (i, prev_idx) in memo:
                return memo[(i, prev_idx)]

            # Choice 1: Skip current element
            skip = dp(i + 1, prev_idx)

            # Choice 2: Take current element (only if strictly greater than previous taken)
            take = 0
            if prev_idx == -1 or nums[i] > nums[prev_idx]:
                take = 1 + dp(i + 1, i)

            memo[(i, prev_idx)] = max(skip, take)
            return memo[(i, prev_idx)]

        # Start at index 0 with no previous element chosen (-1)
        return dp(0, -1)
```

### Alternative: Tabulation

The memo carries `prev_idx` in its state, which gives about `n²` states. A table can use a smaller state: **"the last kept element is `i`"**. So `dp[i]` = the length of the longest increasing subsequence that **ends at** `i`.

| Memoization | Tabulation |
|---|---|
| `memo[(i, prev_idx)]` | `dp[i]` — one variable instead of two |
| base: a single element is a subsequence of length 1 | `dp = [1] * n` |
| `take = 1 + dp(i + 1, i)` with `nums[i] > nums[prev_idx]` | `dp[i] = max(dp[i], dp[j] + 1)` for each earlier `j` with `nums[j] < nums[i]` |
| skip | do nothing — `dp[i]` keeps its current value |
| `return dp(0, -1)` | `return max(dp)` — the best subsequence may end anywhere |

**Loop-order rule:** `dp[i]` reads earlier `dp[j]` (`j < i`), so loop `i` upward and inner `j` from `0` to `i - 1`.

```python
class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        n = len(nums)
        dp = [1] * n                       # every element alone is a subsequence of length 1

        for i in range(n):
            for j in range(i):
                if nums[j] < nums[i]:
                    dp[i] = max(dp[i], dp[j] + 1)

        return max(dp)
```

### Alternative: Patience sorting (O(N log N))

Keep `sub`, where `sub[k]` is the **smallest possible last element** of an increasing subsequence of length `k + 1`. For each `x`, `bisect_left` finds where it belongs: past the end means it extends the longest subsequence (append), otherwise it replaces the first tail `>= x` (a smaller tail is better for future elements). `sub` itself is not the answer sequence, but `len(sub)` is the LIS length.

```python
import bisect

class Solution:
    def lengthOfLIS(self, nums: list[int]) -> int:
        sub = []

        for x in nums:
            # Find insertion index to maintain sorted order in `sub`
            idx = bisect.bisect_left(sub, x)

            # If x is strictly larger than all elements in sub, append it
            if idx == len(sub):
                sub.append(x)
            else:
                # Replace the first element >= x to keep tails as small as possible
                sub[idx] = x

        return len(sub)
```

## 4. Dry Run (`nums = [1, 2, 3]`)

```text
dp(0,-1) = 3
├─ skip 1 → dp(1,-1) = 2
│   ├─ skip 2 → dp(2,-1) = 1
│   └─ take 2 → 1 + dp(2,1) = 2
└─ take 1 → 1 + dp(1,0) = 3
    ├─ skip 2 → dp(2,0) = 1
    └─ take 2 → 1 + dp(2,1) = 2      (dp(2,1) cached — not recomputed)
```

The leaves `dp(3, ·) = 0` (end of the array) are left out to keep the tree short. The best subsequence is `1, 2, 3`.

## 5. Complexity

* **States:** `memo` is keyed by `(i, prev_idx)`, where `prev_idx` is `-1` or any index below `i`, so about `n² / 2` entries.
* **Time:** O(n²) — each state does one skip call and at most one take call, both O(1) beyond the recursion.
* **Space:** O(n²) for the memo, plus recursion depth `n`. The `dp[i]` table is O(n²) time but only O(n) space, and patience sorting is O(n log n) time, O(n) space.

## 6. Recall (30 seconds)

* **State:** `dp(i, prev_idx)` = best length from `nums[i:]`, given the last kept index (`-1` = none).
* **Transition:** `max(skip, take)`; take (`1 + dp(i + 1, i)`) only if `nums[i] > nums[prev_idx]`.
* **Faster:** table `dp[i]` = LIS ending at `i` (O(n²) time, O(n) space); patience sorting with `bisect_left` (O(n log n)).
