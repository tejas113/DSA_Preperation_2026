# 142. Linked List Cycle II

**LC 142** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Floyd's algorithm, two phases (find the meeting point, then reset one pointer to `head`)

---

## 1. Intuition

Phase 1 is the same as Linked List Cycle: `slow` moves 1, `fast` moves 2, and they meet inside the cycle if there is one. Phase 2 is the trick: put `slow` back at `head`, leave `fast` at the meeting point, and move both **1 step at a time**. They meet exactly at the node where the cycle starts.

Why it works, in plain words. Let `F` = steps from `head` to the cycle start, and `a` = steps from the cycle start to the meeting point. `slow` walked `F + a`. `fast` walked twice that, `2(F + a)`, which is also `F + a` plus some whole laps of the cycle. So `F + a` is a whole number of laps. That means walking `F` more steps from the meeting point brings you around to the cycle start, and walking `F` steps from `head` also lands on the cycle start. Both arrive together.

* `while fast and fast.next` + `if slow == fast: break` — phase 1; `break` keeps `fast` at the meeting point.
* `else: return None` — the `while ... else` runs only when the loop ended *without* `break`, i.e. `fast` fell off the end, so there is no cycle.
* `slow = head` — restart `slow` at the head; `fast` stays at the meeting point.
* `while slow != fast: slow = slow.next; fast = fast.next` — both move by 1 until they meet.
* `return slow` — the node where the cycle begins.

**Recall:** meet with 1 and 2 steps; then reset `slow` to `head`; move both 1 step; where they meet is the cycle start.

## 2. Approach

* **Idea:** Phase 1 detects the cycle and finds a meeting point inside it. Phase 2 walks one pointer from `head` and one from the meeting point at the same speed; they meet at the cycle start.
* **Data structure / pointers:**
  * `slow` — 1 step per loop in phase 1; reset to `head` and still 1 step per loop in phase 2.
  * `fast` — 2 steps per loop in phase 1; stays at the meeting point, then moves 1 step per loop in phase 2.
* **Invariant:** In phase 2, the distance from `slow` to the cycle start always equals the distance from `fast` to the cycle start (going around the cycle). So both reach the start on the same step.
* **Edge cases:**
  * Empty list: the `while` doesn't run, so the `else` returns `None`.
  * One node, no cycle: `fast.next` is `None`, returns `None`.
  * One node pointing to itself: the pointers meet at `head`, phase 2 sees `slow == fast` immediately, returns `head`.
  * Cycle starts at `head` (the whole list is a cycle): phase 2 returns `head` without moving, or after a few steps.
  * No cycle: returns `None` (not `False`).

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
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        slow = head
        fast = head

        # Phase 1: Determine if a cycle exists and find the meeting point
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow == fast:
                break
        else:
            # If fast reaches the end (None), there is no cycle
            return None

        # Phase 2: Find the entry point of the cycle
        slow = head
        while slow != fast:
            slow = slow.next
            fast = fast.next

        return slow


if __name__ == "__main__":
    solution = Solution()
    head = build_list([3, 2, 0, -4], pos=1)
    assert solution.detectCycle(head) is head.next  # cycle starts at the node with value 2
    head = build_list([1, 2], pos=0)
    assert solution.detectCycle(head) is head  # cycle starts at the head
    head = build_list([1], pos=0)
    assert solution.detectCycle(head) is head  # self-loop
    assert solution.detectCycle(build_list([1])) is None
    assert solution.detectCycle(build_list([1, 2])) is None
    assert solution.detectCycle(build_list([])) is None
    print("All tests passed")
```

## 4. Dry Run

`head = 3 → 2 → 0 → -4`, where `-4` points back to `2` (`pos = 1`). The cycle starts at `2`.

**Phase 1** (find the meeting point):

| Step | `slow` | `fast` | Equal? |
| --- | --- | --- | --- |
| Start | `3` | `3` | – |
| 1 | `2` | `0` | no |
| 2 | `0` | `2` | no |
| 3 | `-4` | `-4` | **yes → `break`** |

**Phase 2** (reset `slow` to `head`; `fast` stays at `-4`; both move 1 step):

| Step | `slow` | `fast` | Equal? |
| --- | --- | --- | --- |
| Reset | `3` | `-4` | no |
| 1 | `2` | `2` (`-4.next` is `2`) | **yes** |

Return `slow` = node `2`, the start of the cycle.

## 5. Complexity

* **Time:** O(n) — phase 1 takes at most about n steps to meet; phase 2 takes at most `F` steps, and `F` is less than n.
* **Space:** O(1) — only the two pointers `slow` and `fast`.

## 6. Recall (30 seconds)

* Phase 1: `slow` +1, `fast` +2; on meeting, `break`. If `fast` runs out (the `while ... else`), return `None`.
* Phase 2: `slow = head`, leave `fast` at the meeting point, move both +1 until `slow == fast`.
* The meeting node is the cycle start, because `F + a` is a whole number of laps, so `F` steps from the meeting point reach the start.
