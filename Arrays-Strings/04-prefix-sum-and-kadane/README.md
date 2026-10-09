# Topic 4 — Prefix Sum, Kadane & Running Products

## The pattern

Carry a **running total** while you scan. Any subarray sum is then the difference of two running totals: `sum(nums[i..j]) = prefix[j] − prefix[i−1]`. So instead of trying every subarray, look up an earlier prefix that would make the difference exactly what you want.

```python
# Subarray sum equals k (works with negatives)
prefix = 0
counts = {0: 1}                                   # the empty prefix
for x in nums:
    prefix += x
    answer += counts.get(prefix - k, 0)           # earlier prefixes that make this range sum to k
    counts[prefix] = counts.get(prefix, 0) + 1

# Kadane — best subarray sum ending here
curr = best = nums[0]
for x in nums[1:]:
    curr = max(x, curr + x)                       # extend the previous run, or start fresh
    best = max(best, curr)
```

**Prefix and suffix products:** one pass left-to-right stores "everything before `i`", one pass right-to-left multiplies in "everything after `i`".

## How to spot this topic

* The question asks about **sums or products of subarrays** — the maximum, or how many equal `k`.
* Words to look for: **"subarray sum equals k"**, **"maximum sum subarray"**, **"product of all except self"**, **"range sum"**.
* Quick test: *can I write the answer as (a total up to `j`) minus (a total up to `i`)?* If yes, it's this topic.

**Not this topic if:** every number is positive and you want the longest or shortest subarray (→ Topic 3's sliding window is simpler).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 35 | Product of Array Except Self | Prefix products going right, then suffix products going left — no division |
| 36 | Maximum Subarray | Kadane: at each number, extend the run or start a new one |
| 37 | Subarray Sum Equals K | Running prefix sum + a count map of earlier prefixes; works with negatives |
| 38 | Contiguous Array | Treat `0` as `-1`; the longest subarray with sum 0 is the farthest pair of equal prefix sums (store each prefix's first index) |
