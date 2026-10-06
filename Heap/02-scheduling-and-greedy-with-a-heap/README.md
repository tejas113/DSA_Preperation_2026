# Topic 2 — Scheduling & Greedy with a Heap

## The pattern

Repeatedly take the **biggest (or smallest) remaining item**, do something with it, and put back whatever is left. The heap makes "find the current biggest" cost `O(log n)` instead of a scan.

```python
import heapq

heap = [-count for count in counts.values()]    # Python's heapq is a min-heap → negate for a max-heap
heapq.heapify(heap)
while heap:
    largest = -heapq.heappop(heap)              # take the item with the most remaining
    ...                                         # use it once
    if largest - 1 > 0:
        heapq.heappush(heap, -(largest - 1))    # put the remainder back (or hold it for a cooldown)
```

For **cooldown** and **no-adjacent** problems, the item you just used must sit out for a while: keep it in a holding area (a queue, or one variable) and only push it back into the heap once it is allowed again.

## How to spot this topic

* You repeatedly need the **largest or smallest** remaining thing, and what you do with it changes what's left.
* Words to look for: **"smash the two heaviest"**, **"cooldown of n"**, **"no two adjacent characters the same"**, **"schedule tasks"**, **"most recent k"**.
* Quick test: *at each step, is the greedy choice "take the one with the most remaining"?* If yes, it's this topic.

**Not this topic if:** you want the kth best of a fixed collection (→ Topic 1).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 7 | Last Stone Weight | Pop the two heaviest; push back their difference if it isn't zero |
| 8 | Task Scheduler | Max-heap of counts + a queue of `(ready_time, count)` for tasks cooling down |
| 9 | Reorganize String | Max-heap of counts; place the most frequent letter that isn't the previous one, then push the previous back |
| 10 | Design Twitter | Merge the `k` most recent tweets from followed users with a heap, like merging sorted lists |
