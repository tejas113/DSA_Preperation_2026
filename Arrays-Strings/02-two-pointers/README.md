# Topic 2 — Two Pointers

## The pattern

Put one pointer at each end (or both at the start) and look at the values they point to. Those values tell you **which pointer to move**, so you never need a nested loop.

```python
left, right = 0, len(nums) - 1
while left < right:
    total = nums[left] + nums[right]
    if total == target:            # found it: record or return
        ...
    elif total < target:           # too small → the only way to grow is to move the left pointer up
        left += 1
    else:                          # too big → move the right pointer down
        right -= 1
```

Variants: **two ends moving inward** (palindromes, sorted pairs, water), **one pointer per string** (subsequence), and **three pointers** that partition an array (`low`, `mid`, `high`).

## How to spot this topic

* The input is **sorted**, or the structure is **symmetric** (a palindrome).
* You need a **pair or triplet** that meets a condition, or you must compare **both ends**.
* Words to look for: **"sorted array"**, **"pair that sums to"**, **"palindrome"**, **"subsequence"**, **"in place"**, **"O(1) extra space"**.
* Quick test: *from the two current values, can I tell which pointer to move without checking anything else?* If yes, it's this topic.

**Not this topic if:** the array is unsorted and you can use extra space (→ Topic 1's hash map), or the answer is a window whose size changes (→ Topic 3).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 14 | Valid Palindrome | Compare the ends, skipping non-alphanumeric characters |
| 15 | Valid Palindrome II | On the first mismatch, try skipping the left character or the right one |
| 16 | Is Subsequence | One pointer per string; advance the pattern pointer when characters match |
| 17 | Two Sum II | Sorted array: sum too small → `left += 1`, too big → `right -= 1` |
| 18 | 3Sum | Sort, fix one number, run two pointers on the rest, skip repeats |
| 19 | Container With Most Water | Always move the shorter wall; the taller one can't do better with it |
| 20 | Trapping Rain Water | Move the lower side inward, tracking the tallest wall seen on each side |
| 21 | Sort Colors | Three pointers: `low` (next 0), `mid` (scanner), `high` (next 2) |
| 22 | Backspace String Compare | Walk both strings from the back, skipping characters a `#` cancels, and compare what's left (`O(1)` space) |
| 23 | One Edit Distance | Find the first mismatch; the rest must match after a replace, insert or delete (lengths differ by at most 1) |
