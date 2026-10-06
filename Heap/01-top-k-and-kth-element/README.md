# Topic 1 — Top-K & Kth Element

## The pattern

Keep a heap of size `k` holding the **best `k` items seen so far**. The root of the heap is the worst of those `k` — which is exactly the kth best. Anything worse than the root can be ignored.

```python
import heapq

heap = []                                   # min-heap holding the k LARGEST values so far
for x in nums:
    heapq.heappush(heap, x)
    if len(heap) > k:
        heapq.heappop(heap)                 # drop the smallest of the k + 1
return heap[0]                              # the kth largest

# Python's heapq is a min-heap → for the k SMALLEST (or "closest"), push the negative:
#   heapq.heappush(heap, -distance);  if len(heap) > k: heapq.heappop(heap)
```

## How to spot this topic

* The question asks for the **kth** something, or the **top / bottom `k`**, without sorting everything.
* Words to look for: **"kth largest"**, **"k closest"**, **"top k"**, **"k smallest"**, **"in a stream"**.
* Quick test: *do I only care about the best `k`, so the rest can be thrown away as I go?* If yes, it's this topic.

**Not this topic if:** you need the **median** (→ Topic 3), or you're repeatedly simulating a process with the biggest item (→ Topic 2).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 1 | Kth Largest Element in a Stream | Min-heap of size `k`; each `add` pushes, trims to `k`, and returns the root |
| 2 | Kth Largest Element in an Array | The same size-`k` min-heap (Quickselect is the `O(n)` follow-up) |
| 3 | K Closest Points to Origin | Max-heap of size `k` keyed on the squared distance (push `-distance`) |
| 4 | Top K Frequent Words | Heap on `(-count, word)` so ties break alphabetically |
| 5 | Kth Smallest Element in a Sorted Matrix | Min-heap seeded with the first column; pop, then push the next item in that row |
| 6 | Find K Pairs with Smallest Sums | Min-heap seeded with `(nums1[i] + nums2[0], i, 0)`; pop, then push the next `j` |
