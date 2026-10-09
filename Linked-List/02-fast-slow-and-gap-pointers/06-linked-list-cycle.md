# 141. Linked List Cycle

**LC 141** · **Source:** LC150 + NC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Fast / slow pointers (Floyd's tortoise and hare)

---

## 1. Intuition

Two runners on a track: one walks, one runs at double speed. On a straight road the fast one just reaches the end. On a circular track the fast one laps the slow one and they meet.

* `slow = slow.next` — moves 1 step.
* `fast = fast.next.next` — moves 2 steps.
* `while fast and fast.next` — if `fast` falls off the end, there is no cycle. It also guards `fast.next.next` from a `None` crash.
* `if slow == fast` — inside a cycle `fast` gains exactly 1 node per step, so it can't jump over `slow`. They must land on the same node.
* `return False` — the loop ended because `fast` reached `None`.

**Recall:** slow moves 1, fast moves 2; they meet if and only if there's a cycle.

## 2. Approach

* **Idea:** Move `slow` by 1 and `fast` by 2. If they ever point to the same node, there is a cycle. If `fast` reaches `None`, there isn't.
* **Data structure / pointers:**
  * `slow` — tortoise, 1 step per loop.
  * `fast` — hare, 2 steps per loop.
  * Both start at `head`.
* **Invariant:** `fast` is always ahead of (or equal to) `slow`. If there is a cycle, once both are inside it the gap shrinks by 1 each step until it is 0.
* **Edge cases:**
  * Empty list: the loop never runs, returns `False`.
  * One node, no cycle: `fast.next` is `None`, returns `False`.
  * One node pointing to itself: after one step both are that node, returns `True`.
  * Two nodes, no cycle: `fast` becomes `None` after one step, returns `False`.
  * Cycle includes the head: still detected, since the pointers meet somewhere in the cycle.

## 3. Code

```python
from typing import Optional


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def build_list(values: list[int], pos: int = -1) -> Optional[ListNode]:
    """Build a list; if pos >= 0, the last node points back to the node at index pos."""
    dummy = ListNode(0)
    tail = dummy
    nodes = []
    for value in values:
        tail.next = ListNode(value)
        tail = tail.next
        nodes.append(tail)
    if pos >= 0:
        tail.next = nodes[pos]
    return dummy.next


class Solution:

    def hasCycle(self, head: Optional[ListNode]) -> bool:
        slow = head
        fast = head

        while fast and fast.next:
            slow = slow.next  # Move 1 step
            fast = fast.next.next  # Move 2 steps

            if slow == fast:  # Pointers meet -> cycle detected
                return True

        return False  # End reached -> no cycle


if __name__ == "__main__":
    solution = Solution()
    assert solution.hasCycle(build_list([3, 2, 0, -4], pos=1)) is True
    assert solution.hasCycle(build_list([1, 2], pos=0)) is True
    assert solution.hasCycle(build_list([1], pos=0)) is True
    assert solution.hasCycle(build_list([1])) is False
    assert solution.hasCycle(build_list([1, 2])) is False
    assert solution.hasCycle(build_list([])) is False
    print("All tests passed")
```

## 4. Dry Run

`head = 3 → 2 → 0 → -4`, where `-4` points back to `2` (`pos = 1`).

| Step | `slow` | `fast` | `slow == fast`? |
| --- | --- | --- | --- |
| Start | `3` | `3` | – |
| 1 | `2` | `0` | No |
| 2 | `0` | `2` (`0 → -4 → 2`) | No |
| 3 | `-4` | `-4` (`2 → 0 → -4`) | **Yes → return `True`** |

## 5. Complexity

* **Time:** O(n) — with no cycle, `fast` reaches the end in about n/2 loops. With a cycle, `slow` takes at most n steps to get in and `fast` closes the gap by 1 per step, so it takes at most about one more lap.
* **Space:** O(1) — only the two pointers `slow` and `fast`.

## 6. Recall (30 seconds)

* `slow` and `fast` both start at `head`; `slow` moves 1, `fast` moves 2.
* Loop condition `while fast and fast.next` — it protects `fast.next.next` and also means "no cycle" when it fails.
* Meet (`slow == fast`) → `True`; loop ends → `False`.
