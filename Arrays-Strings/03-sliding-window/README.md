# Topic 3 — Sliding Window

## The pattern

Keep a window `[left, right]` over a contiguous part of the input. **Grow** it by moving `right`. Whenever it becomes invalid, **shrink** it by moving `left` until it is valid again. Record the best window as you go.

```python
left = 0
for right in range(len(s)):
    add s[right] to the window state          # e.g. counts[s[right]] += 1
    while <window is invalid>:
        remove s[left] from the window state  # e.g. counts[s[left]] -= 1
        left += 1
    best = max(best, right - left + 1)        # the window [left, right] is valid here
```

**Fixed-size window (size `k`):** add `s[right]`, and once `right >= k`, remove `s[right - k]`.

## How to spot this topic

* The answer is a **contiguous** substring or subarray.
* Words to look for: **"longest / shortest substring (or subarray) that …"**, **"at most k distinct"**, **"contains all of"**, **"window of size k"**, **"maximum in every window"**.
* Quick test: *if I extend the window, does validity change in a predictable direction (only gets worse, or only gets better)?* If yes, it's this topic.

**Not this topic if:** the array has **negative numbers** and the condition is a sum (→ Topic 4's prefix sum + hash map — shrinking a window doesn't fix a negative sum), or the answer isn't contiguous.

## Why it isn't O(n²)

`right` moves `n` times, and `left` also moves at most `n` times in total. The inner `while` loop looks nested, but it never moves `left` backwards, so the whole thing is `O(n)`.

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 24 | Best Time to Buy and Sell Stock | Track the lowest price so far; profit = today − lowest |
| 25 | Longest Substring Without Repeating Characters | Shrink the window while the new character is already inside it |
| 26 | Longest Repeating Character Replacement | Window is valid while `size - max_freq <= k` |
| 27 | Permutation in String | Fixed window the size of the pattern; compare letter counts |
| 28 | Minimum Size Subarray Sum | All positive: shrink from the left while the sum is still enough |
| 29 | Minimum Window Substring | Track how many required characters are still missing; shrink once none are |
| 30 | Sliding Window Maximum | Monotonic deque holds the indices of candidates in decreasing order |
| 31 | Longest Substring with At Most K Distinct Characters | Count map of the window; shrink while distinct > k |
| 32 | Find All Anagrams in a String | Permutation in String, but record every start index |
| 33 | Substring with Concatenation of All Words | Sliding window that moves by whole-word steps |
| 34 | Max Consecutive Ones III | Window is valid while it holds at most `k` zeros; shrink from the left otherwise |
