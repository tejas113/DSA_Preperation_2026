# Topic 5 — Intervals

## The pattern

**Sort the intervals first** — by start for merging, or by end for greedy picking. After sorting, every decision only needs to compare the current interval with the **previous** one.

```python
intervals.sort(key=lambda interval: interval[0])      # sort by start
merged = [intervals[0]]
for start, end in intervals[1:]:
    if start <= merged[-1][1]:                         # overlaps the last merged interval
        merged[-1][1] = max(merged[-1][1], end)        # stretch it
    else:
        merged.append([start, end])                    # gap → begin a new one
```

Variants:
* **Sort by end, keep the earliest-ending** — fewest removals, fewest arrows.
* **Sweep line or min-heap of end times** — how many overlap at once (meeting rooms).
* **Two pointers over two sorted lists** — intersections.

## How to spot this topic

* The input is a list of **`[start, end]` pairs**.
* Words to look for: **"merge"**, **"overlap"**, **"insert an interval"**, **"meeting rooms"**, **"minimum number of … to remove / cover"**, **"schedule"**.
* Quick test: *after sorting, can I decide by looking only at the previous interval?* If yes, it's this topic.

**Not this topic if:** the items aren't ranges (→ Topic 1 or 2).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 39 | Merge Intervals | Sort by start; merge when the next start ≤ the last end |
| 40 | Insert Interval | Copy the ones before, merge the overlapping ones, copy the rest |
| 41 | Non-overlapping Intervals | Sort by end; keep the earliest-ending, count the ones you skip |
| 42 | Meeting Rooms II | Sort starts and ends separately (or use a min-heap of end times); count overlaps |
| 43 | Interval List Intersections | Two pointers, one per list; advance the one that ends first |
| 44 | Summary Ranges | One scan; a run ends when the next number isn't `+1` |
| 45 | Minimum Number of Arrows to Burst Balloons | Sort by end; shoot at the earliest end, skip everything it pops |
| 46 | Meeting Rooms | Sort by start; any overlap with the previous means the answer is no |
