# Topic 2 — Fast & Slow (and Gap) Pointers

## The pattern

Two pointers walk the same list. Either they move at **different speeds** (`slow` by 1, `fast` by 2), or they keep a **fixed gap** between them. That lets you find a position in one pass, without knowing the length.

```python
# Middle / cycle
slow = fast = head
while fast and fast.next:
    slow = slow.next
    fast = fast.next.next
    if slow is fast:             # they can only meet if there's a cycle
        ...
# no cycle: when the loop ends, slow is at the middle

# n-th from the end: gap of n
fast = head
for _ in range(n): fast = fast.next
slow = dummy                     # dummy → so slow ends up BEFORE the node to remove
while fast:
    slow, fast = slow.next, fast.next
```

**Cycle start:** after `slow` and `fast` meet, put one pointer back at `head` and move both one step at a time — they meet at the start of the cycle.

## How to spot this topic

* You need something from the **middle or the end**, or need to detect a **cycle**, in **one pass**.
* Words to look for: **"middle"**, **"cycle"**, **"n-th node from the end"**, **"palindrome"**, **"reorder"**, **"intersection"**.
* Quick test: *would this be easy if I knew the length, and can two pointers at different speeds stand in for that?* If yes, it's this topic.

**Not this topic if:** you're flipping links (→ Topic 1) or building a new list (→ Topic 3).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 5 | Middle of the Linked List | `fast` moves 2 per step; when it ends, `slow` is at the middle |
| 6 | Linked List Cycle | If `fast` ever meets `slow`, there is a cycle |
| 7 | Linked List Cycle II | After they meet, reset one pointer to `head` and move both by 1 — they meet at the cycle start |
| 8 | Remove Nth Node From End of List | Gap of `n` between the pointers, using a dummy so the head can be removed |
| 9 | Reorder List | Find the middle, reverse the second half, then interleave the two halves |
| 10 | Intersection of Two Linked Lists | Each pointer switches to the other list's head at the end; they meet at the intersection |
| 11 | Palindrome Linked List | Find the middle, reverse the second half, compare the two halves |
| 12 | Find the Duplicate Number | Treat `nums[i]` as a `next` pointer; the duplicate is where the cycle starts |
