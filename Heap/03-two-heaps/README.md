# Topic 3 — Two Heaps

## The pattern

Split the data in half. A **max-heap** holds the smaller half (its root is the biggest of the small numbers), and a **min-heap** holds the larger half (its root is the smallest of the big numbers). The middle of the data is always at the two roots.

```python
import heapq

lower_half = []     # max-heap (store negatives)
upper_half = []     # min-heap

def add(num):
    heapq.heappush(lower_half, -num)                          # 1. push into the lower half
    heapq.heappush(upper_half, -heapq.heappop(lower_half))    # 2. move the lower half's largest up
    if len(upper_half) > len(lower_half):                     # 3. keep lower_half the same size or 1 bigger
        heapq.heappush(lower_half, -heapq.heappop(upper_half))

def median():
    if len(lower_half) > len(upper_half):
        return -lower_half[0]
    return (-lower_half[0] + upper_half[0]) / 2
```

## How to spot this topic

* You need the **median (or another middle point)** of data that **keeps changing**.
* Words to look for: **"median from a data stream"**, **"maximize capital"** (choosing between two pools).
* Quick test: *do I need quick access to both the largest of the small half and the smallest of the large half?* If yes, it's this topic.

**Not this topic if:** the data is fixed and sorted (→ just index the middle).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 11 | Find Median from Data Stream | Max-heap for the lower half, min-heap for the upper half, kept balanced |
| 12 | IPO | Min-heap of projects by capital to unlock them; max-heap of unlocked profits to pick the best |
