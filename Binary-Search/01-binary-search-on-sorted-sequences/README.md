# Topic 1 — Binary Search on a Sorted Sequence

## The pattern

Keep a range `[lo, hi]`. Look at `mid`, decide which half can't contain the answer, and discard it. There are two forms — pick by what you're looking for.

```python
# Exact target
lo, hi = 0, len(nums) - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if nums[mid] == target: return mid
    if nums[mid] < target:  lo = mid + 1
    else:                   hi = mid - 1
return -1

# Boundary: the FIRST index where a condition is true (insert position, first bad version, first/last position)
lo, hi = 0, len(nums)
while lo < hi:
    mid = (lo + hi) // 2
    if <condition true at mid>: hi = mid          # mid might be the answer — keep it
    else:                       lo = mid + 1
return lo
```

## How to spot this topic

* The input is **sorted**, and you need a **value, a position, or a floor/ceiling**.
* Words to look for: **"sorted"**, **"find the target"**, **"insert position"**, **"first / last occurrence"**, **"closest"**, **"at or before time t"**, **O(log n)**.
* Quick test: *does one comparison at `mid` let me throw away half the array?* If yes, it's this topic.

**Not this topic if:** the array is **rotated or has a peak** (→ Topic 2), or you're searching for the **best value of something** with a yes/no test (→ Topic 3).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 1 | Binary Search | The plain exact-match loop |
| 2 | Search Insert Position | Boundary: the first index with `nums[i] >= target` |
| 3 | Find First and Last Position | Two boundary searches: first `>= target`, and first `> target` minus one |
| 4 | Search a 2D Matrix | Treat it as one sorted list: `row = mid // cols`, `col = mid % cols` |
| 5 | Find K Closest Elements | Binary search the window start in `[0, n - k]`; compare the distance to each end |
| 6 | Time Based Key-Value Store | One sorted list of timestamps per key; find the latest timestamp `<=` the query |
| 13 *(Extra)* | First Bad Version | Boundary: the first version where `isBadVersion` is true |
