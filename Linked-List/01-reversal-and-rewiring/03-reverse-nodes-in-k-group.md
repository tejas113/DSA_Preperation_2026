# 25. Reverse Nodes in k-Group

**LC 25** · **Source:** LC150 + NC150 · **Difficulty:** Hard · **Priority:** Core · **Pattern:** Repeated sublist reversal with a dummy node (`leftPrev`, `cur`, `prev`, `tail`)

---

## 1. Intuition

This is Reverse Linked List II repeated. First count the nodes, so you know exactly how many *full* groups of `k` exist and never reverse a short group at the end. Then, group by group: reverse `k` nodes, stitch the flipped group back between its neighbours, and move on.

* `groups = length // k` — the number of full groups; the leftover `length % k` nodes are never touched.
* `dummy` / `leftPrev` — `leftPrev` is the node just before the current group, and the dummy lets the first group start from the head.
* `while count > 0` — the usual three-pointer reversal, run exactly `k` times.
* `tail = leftPrev.next` — still the old first node of the group; after reversal it's the group's tail.
* `tail.next = cur` — the flipped group's tail points to what comes next (the next group or the leftover).
* `leftPrev.next = prev` and `leftPrev = tail` — link the previous part to the new group head, then the tail becomes `leftPrev` for the next group.

**Recall:** count → `groups = length // k`; per group: reverse `k`, `tail.next = cur`, `leftPrev.next = prev`, `leftPrev = tail`.

## 2. Approach

* **Idea:** Count the length, compute the number of full groups, then reverse each group in place and reconnect.
* **Data structure / pointers:**
  * `dummy` — fake node before `head`, so the head can change.
  * `leftPrev` — last node of the already-finished part, just before the current group.
  * `cur` — the node being reversed; after a group it points at the first node after that group.
  * `prev` — head of the reversed group so far; after a group it is the group's new head.
  * `tmpNext` — saved `cur.next`.
  * `tail` — the old first node of the group, which becomes the group's tail.
* **Invariant:** Before each group, everything up to `leftPrev` is final (reversed groups in order), and `cur` is the first node of the next unprocessed group.
* **Edge cases:**
  * `k = 1`: nothing to change, returns `head` immediately.
  * Empty list: returns `head` (`None`).
  * `k` equals the length: the whole list is one group and gets reversed.
  * `k` greater than the length: `groups = 0`, the list is returned unchanged.
  * Leftover nodes (length not a multiple of `k`): they stay in the original order, because the loop runs only `groups` times.

## 3. Code

```python
from typing import Optional


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

    def reverseKGroup(
        self, head: ListNode | None, k: int
    ) -> ListNode | None:
        if not head or k == 1:
            return head

        # Step 1: Compute total length of list
        length = 0
        curr = head
        while curr:
            length += 1
            curr = curr.next

        groups = length // k

        dummy = ListNode(0, head)
        leftPrev = dummy
        cur = head

        # Step 2: Reverse each k-group
        for _ in range(groups):
            prev = None
            count = k

            while count > 0:
                tmpNext = cur.next
                cur.next = prev
                prev = cur
                cur = tmpNext
                count -= 1

            # Step 3: Reconnect boundary pointers
            tail = leftPrev.next  # Old group head -> new group tail
            tail.next = cur  # Connect tail to next group/remainder
            leftPrev.next = prev  # Connect leftPrev to new group head
            leftPrev = tail  # Advance leftPrev for next iteration

        return dummy.next


if __name__ == "__main__":
    solution = Solution()
    assert to_list(solution.reverseKGroup(build_list([1, 2, 3, 4, 5]), 2)) == [2, 1, 4, 3, 5]
    assert to_list(solution.reverseKGroup(build_list([1, 2, 3, 4, 5]), 3)) == [3, 2, 1, 4, 5]
    assert to_list(solution.reverseKGroup(build_list([1, 2, 3]), 3)) == [3, 2, 1]
    assert to_list(solution.reverseKGroup(build_list([1, 2, 3]), 1)) == [1, 2, 3]
    assert to_list(solution.reverseKGroup(build_list([1, 2]), 5)) == [1, 2]
    assert to_list(solution.reverseKGroup(build_list([1]), 1)) == [1]
    print("All tests passed")
```

## 4. Dry Run

`head = 1 → 2 → 3 → 4 → 5`, `k = 2`. `length = 5`, so `groups = 2`. Start: `leftPrev = dummy`, `cur = 1`.

| Group | `leftPrev` | Reverse `k` nodes | `prev` (new head) | `tail` | `cur` after | After reconnect |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `dummy` | `1, 2` | `2` | `1` | `3` | `dummy → 2 → 1 → 3 → 4 → 5` |
| 2 | `1` | `3, 4` | `4` | `3` | `5` | `dummy → 2 → 1 → 4 → 3 → 5` |

Each reconnect does `tail.next = cur`, then `leftPrev.next = prev`, then `leftPrev = tail`. The loop ends after 2 groups; node `5` is the leftover and stays put. Return `2 → 1 → 4 → 3 → 5`.

## 5. Complexity

* **Time:** O(n) — one pass to count the length, then at most one more pass in which each node is reversed once.
* **Space:** O(1) — only pointers (`dummy`, `leftPrev`, `cur`, `prev`, `tail`, `tmpNext`) and counters; links are changed in place, with no recursion.

## 6. Recall (30 seconds)

* Count the length, `groups = length // k`; `dummy` before `head`, `leftPrev = dummy`.
* Per group: reverse exactly `k` nodes with `prev` / `cur` / `tmpNext`; the leftover tail is never touched.
* Reconnect in order: `tail = leftPrev.next`, `tail.next = cur`, `leftPrev.next = prev`, `leftPrev = tail`.
