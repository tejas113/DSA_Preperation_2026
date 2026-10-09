# Topic 1 — Reversal & Pointer Rewiring

## The pattern

Walk the list and flip each node's `next` to point backwards. Use three pointers, and **save `next_node` before you overwrite `curr.next`** — otherwise you lose the rest of the list.

```python
prev, curr = None, head
while curr:
    next_node = curr.next        # 1. remember what comes next
    curr.next = prev             # 2. flip the arrow
    prev, curr = curr, next_node # 3. step forward
return prev                      # prev is the new head
```

For a **range** (Reverse Linked List II) or **groups** (k-Group), reverse just that section, then reconnect the node before it and the node after it.

## How to spot this topic

* The question says **"reverse"**, **"rotate"**, or asks you to **reorder by rewiring `next`** — usually **in place** with **O(1) extra space**.
* Words to look for: **"reverse a sublist"**, **"reverse every k nodes"**, **"rotate right by k"**.
* Quick test: *am I changing the direction of the links, not the values?* If yes, it's this topic.

**Not this topic if:** you need a position (middle, cycle, n-th from the end) → Topic 2, or you're combining two lists → Topic 3.

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 1 | Reverse Linked List | The three-pointer loop above |
| 2 | Reverse Linked List II | Stop at the node before `left`, reverse `right - left + 1` nodes, reconnect both ends |
| 3 | Reverse Nodes in k-Group | Check that `k` nodes remain, reverse them, reconnect, repeat; leave a short last group alone |
| 4 | Rotate List | Find the length, take `k % length`, cut at `length - k` and reconnect the tail to the head |
