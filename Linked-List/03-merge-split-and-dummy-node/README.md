# Topic 3 — Merge, Split & Dummy-Node Construction

## The pattern

Put a **dummy node** in front, keep a `tail` pointer, and append onto `tail`. Because the dummy already exists, you never have to special-case "is this the first node?". At the end, the answer is `dummy.next`.

```python
dummy = tail = ListNode(0)
while a and b:
    if a.val <= b.val:
        tail.next, a = a, a.next
    else:
        tail.next, b = b, b.next
    tail = tail.next
tail.next = a or b               # attach whichever list still has nodes
return dummy.next
```

The same skeleton handles **adding numbers with a carry**, **removing nodes** (skip them instead of appending), **partitioning** (two dummy lists, joined at the end) and **merge sort**.

## How to spot this topic

* You're **building a new list** from one or more lists, or **removing nodes** where the **head itself might go**.
* Words to look for: **"merge"**, **"add two numbers"**, **"remove duplicates"**, **"partition"**, **"sort the list"**, **"k sorted lists"**.
* Quick test: *would it be simpler if there were always a node before the head?* If yes, use a dummy — it's this topic.

**Not this topic if:** you're flipping links in place (→ Topic 1) or finding a position (→ Topic 2).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 13 | Merge Two Sorted Lists | The dummy + tail template above |
| 14 | Add Two Numbers | Walk both lists with a `carry`; keep going while either list or the carry remains |
| 15 | Remove Duplicates from Sorted List II | Dummy before the head; when a value repeats, skip every node with that value |
| 16 | Merge k Sorted Lists | Min-heap of the current heads, or merge lists in pairs (divide and conquer) |
| 17 | Partition List | Build a "less than x" list and a "greater or equal" list, then join them |
| 18 | Sort List | Merge sort: find the middle, cut the list, sort each half, merge |
