# Topic 7 — In-Place Array Manipulation

## The pattern

Change the array **without a second array**. The main tool is two indices: a **read** pointer that scans every element, and a **write** pointer that marks where the next kept element goes. Everything left of `write` is already "done".

```python
write = 0
for read in range(len(nums)):
    if <keep nums[read]>:                 # e.g. nums[read] != val, or differs from the last kept one
        nums[write] = nums[read]
        write += 1
return write                              # the new length
```

Other in-place moves in this topic:
* **Fill from the back** (merge sorted arrays) so you never overwrite something you still need.
* **Reverse in pieces** (rotate an array = reverse all, reverse the first `k`, reverse the rest).
* **Swap from the right** (next permutation: find the pivot, swap it with the next larger value, reverse the tail).

## How to spot this topic

* The question says **"in place"**, **"O(1) extra space"**, or **"return the new length"**.
* Words to look for: **"remove"**, **"merge into the first array"**, **"rotate"**, **"move all zeroes"**, **"next permutation"**.
* Quick test: *am I rearranging or filtering the array itself, keeping it the same array?* If yes, it's this topic.

**Not this topic if:** you're allowed a new array and the goal is a count or lookup (→ Topic 1).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 53 | Merge Sorted Array | Fill `nums1` from the back, taking the larger of the two ends |
| 54 | Remove Element | Read / write pointers; write only the values you keep |
| 55 | Remove Duplicates from Sorted Array | Read / write; keep a value only if it differs from the last kept one |
| 56 | Rotate Array | Reverse everything, then reverse the first `k` and the rest |
| 57 | Next Permutation | Find the pivot from the right, swap it with the next larger value, reverse the tail |
| 58 | Plus One | Add from the right and carry; if the carry survives, add a leading 1 |
| 59 | Move Zeroes | Read / write pointers; fill the rest with zeroes |
| 60 | Remove Duplicates from Sorted Array II | Read / write; keep a value if it differs from `nums[write - 2]` |
| 61 | First Missing Positive | Put each value `v` at index `v - 1`, then scan for the first misplaced slot |
