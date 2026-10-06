# Topic 2 — Rotated, Modified & Partition Searches

## The pattern

The array isn't plainly sorted, but a comparison at `mid` (against an end, or a neighbor) still tells you which half to keep.

```python
# Minimum in a rotated array: compare mid with the RIGHT end
lo, hi = 0, len(nums) - 1
while lo < hi:
    mid = (lo + hi) // 2
    if nums[mid] > nums[hi]: lo = mid + 1       # the drop is to the right of mid
    else:                    hi = mid           # mid could be the minimum

# Peak element: move toward the larger neighbor
while lo < hi:
    mid = (lo + hi) // 2
    if nums[mid] < nums[mid + 1]: lo = mid + 1  # uphill to the right
    else:                         hi = mid

# Search in a rotated array: one half is always sorted — check whether the target is inside it
if nums[lo] <= nums[mid]:                       # left half is sorted
    if nums[lo] <= target < nums[mid]: hi = mid - 1
    else:                              lo = mid + 1
```

**Median of two sorted arrays** binary searches the *cut position* in the smaller array, so that everything on the left of both cuts is `<=` everything on the right.

## How to spot this topic

* The array is **rotated**, has a **peak**, or is sorted **except for one twist**.
* Words to look for: **"rotated sorted array"**, **"minimum in rotated"**, **"peak element"**, **"single element"**, **"median of two sorted arrays"**, **O(log n)** even though it isn't plainly sorted.
* Quick test: *does comparing `nums[mid]` with an end or a neighbor tell me where the answer is?* If yes, it's this topic.

**Not this topic if:** the array is fully sorted (→ Topic 1).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 7 | Search in Rotated Sorted Array | One half is always sorted; keep it if the target lies inside it |
| 8 | Find Minimum in Rotated Sorted Array | Compare `nums[mid]` with `nums[hi]`; the minimum is on the side with the drop |
| 9 | Find Peak Element | Compare `nums[mid]` with `nums[mid + 1]`; move toward the larger one |
| 10 | Median of Two Sorted Arrays | Binary search the cut in the smaller array until left halves `<=` right halves |
| 14 *(Extra)* | Single Element in a Sorted Array | Before the single element, pairs start at even indexes; check `nums[mid] == nums[mid ^ 1]` |
