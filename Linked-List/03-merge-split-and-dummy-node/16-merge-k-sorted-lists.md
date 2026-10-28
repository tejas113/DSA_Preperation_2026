# 23. Merge k Sorted Lists

**LC 23** · **Source:** NC150 · **Difficulty:** Hard · **Priority:** Core · **Pattern:** Min-heap of the current head of each list + dummy node and tail

---

## 1. Intuition

This is Merge Two Sorted Lists, but with `k` lists. With two lists you compare two fronts. With `k` lists you need the smallest of `k` fronts, and a min-heap gives you that in O(log k). Keep exactly one node per list in the heap (its current front). Pop the smallest, append it to the answer, and push the next node from the same list.

* `HeapNode.__lt__` — `heapq` only needs `<`; this compares `node.val`, so two equal values never make Python compare the `ListNode` objects (which would raise an error).
* The first `for l in lists` loop — pushes the head of every non-empty list, so the heap starts with at most `k` entries. `None` lists are skipped.
* `dummy` / `curr` — the usual dummy node and tail for building the result.
* `heapq.heappop(min_heap)` — the smallest front among all lists; append it with `curr.next = node`.
* `if node.next: heapq.heappush(...)` — the next node of that same list becomes its new front, so the heap always holds one front per list.

**Recall:** heap of list fronts; pop the smallest, append it, push its `next`; `dummy` + `curr` build the answer.

## 2. Approach

* **Idea:** Keep a min-heap with the current front node of each list. Repeatedly pop the smallest, attach it to the result, and push the node after it.
* **Data structure / pointers:**
  * `min_heap` — heap of `HeapNode` wrappers, one per non-exhausted list; smallest `node.val` on top.
  * `HeapNode.node` — the actual `ListNode`.
  * `dummy` — fake node before the answer.
  * `curr` — tail of the answer.
  * Alternative to the wrapper class: push `(node.val, index, node)` tuples. The unique `index` is the tie-breaker so two equal values never compare the nodes.
* **Invariant:** The heap always holds the current front of every list that still has nodes. So the heap's minimum is the smallest unused node overall, and the answer built so far is sorted and contains only values at most that minimum.
* **Edge cases:**
  * `lists` is empty (`[]`): the heap stays empty, returns `None`.
  * `lists` contains only empty lists (`[[]]` or `[None, None]`): same, returns `None`.
  * Some lists empty, some not: the empty ones are skipped.
  * One list only: the result is that list.
  * Equal values across lists: handled by `__lt__` using only `val`.
  * The last node appended always has `next = None`, because a node with a `next` is never the last one pushed.

## 3. Code

```python
from typing import Optional
import heapq


class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def build_list(values: list[int]) -> Optional[ListNode]:
    dummy = ListNode(0)
    tail = dummy
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
    return dummy.next


def to_list(head: Optional[ListNode]) -> list[int]:
    values = []
    while head:
        values.append(head.val)
        head = head.next
    return values


class Solution:
    def mergeKLists(self, lists: list[ListNode | None]) -> ListNode | None:
        # Custom wrapper for ListNode to handle custom comparison in heapq
        # in case node values are equal (prevents object comparison errors)
        class HeapNode:
            def __init__(self, node: ListNode):
                self.node = node
            def __lt__(self, other):
                return self.node.val < other.node.val

        min_heap = []

        # Initialize the heap with the head node of each non-empty list
        for l in lists:
            if l:
                heapq.heappush(min_heap, HeapNode(l))

        dummy = ListNode(0)
        curr = dummy

        # Extract the minimum node, append it to result, and push its next node into the heap
        while min_heap:
            heap_node = heapq.heappop(min_heap)
            node = heap_node.node

            curr.next = node
            curr = curr.next

            if node.next:
                heapq.heappush(min_heap, HeapNode(node.next))

        return dummy.next


if __name__ == "__main__":
    solution = Solution()
    lists = [build_list([1, 4, 5]), build_list([1, 3, 4]), build_list([2, 6])]
    assert to_list(solution.mergeKLists(lists)) == [1, 1, 2, 3, 4, 4, 5, 6]
    assert to_list(solution.mergeKLists([])) == []
    assert to_list(solution.mergeKLists([None])) == []
    assert to_list(solution.mergeKLists([None, None])) == []
    assert to_list(solution.mergeKLists([build_list([1, 2, 3])])) == [1, 2, 3]
    assert to_list(solution.mergeKLists([None, build_list([2]), None, build_list([1])])) == [1, 2]
    print("All tests passed")
```

## 4. Dry Run

`lists = [A: 1 → 4 → 5, B: 1 → 3 → 4, C: 2 → 6]`. The heap starts with the fronts `1(A), 1(B), 2(C)`.

| Step | Pop (smallest) | Push (its `next`) | Heap after (value, list) | Result so far |
| --- | --- | --- | --- | --- |
| 1 | `1` (A) | `4` (A) | `1(B), 2(C), 4(A)` | `1` |
| 2 | `1` (B) | `3` (B) | `2(C), 3(B), 4(A)` | `1 → 1` |
| 3 | `2` (C) | `6` (C) | `3(B), 4(A), 6(C)` | `1 → 1 → 2` |
| 4 | `3` (B) | `4` (B) | `4(A), 4(B), 6(C)` | `1 → 1 → 2 → 3` |
| 5 | `4` (A) | `5` (A) | `4(B), 5(A), 6(C)` | `… → 3 → 4` |
| 6 | `4` (B) | none | `5(A), 6(C)` | `… → 4 → 4` |
| 7 | `5` (A) | none | `6(C)` | `… → 4 → 5` |
| 8 | `6` (C) | none | empty | `1 → 1 → 2 → 3 → 4 → 4 → 5 → 6` |

(In steps 1, 2, 5 and 6 two entries have equal values; which one comes out first doesn't change the result.)

## 5. Complexity

* **Time:** O(N log k) — each of the N nodes is pushed and popped once, and each heap operation costs O(log k) because the heap holds at most k nodes.
* **Space:** O(k) — the heap holds at most one node per list. The result reuses the existing nodes, so no O(N) output is allocated.
* Merging the lists one after another instead would cost O(N · k).

## 6. Recall (30 seconds)

* Heap of the current front of each list (skip empty lists); `__lt__` compares `node.val` only.
* Loop: pop the smallest, `curr.next = node`, `curr = curr.next`, push `node.next` if it exists.
* `dummy` + `curr`, return `dummy.next`. Time O(N log k), space O(k). Empty `lists` returns `None`.
