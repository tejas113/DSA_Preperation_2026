# 876. Middle of the Linked List

**LC 876** · **Source:** [+] Claude · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Fast / slow pointers (`slow` moves 1, `fast` moves 2)

---

## 1. Intuition

Two people walk down a road, one at normal speed and one at double speed. When the fast one reaches the end, the slow one has covered exactly half the distance, so it is standing in the middle. You never need to count the nodes.

* `slow = slow.next` — moves 1 step per loop.
* `fast = fast.next.next` — moves 2 steps per loop, so it covers the list twice as fast.
* `while fast and fast.next` — stops when `fast` is off the end (odd length) or on the last node (even length). It also guards `fast.next.next` from a `None` crash.
* `return slow` — `slow` has moved about `n / 2` steps, so it is the middle.
* For an even length there are two middles, and this loop ends on the **second** one, which is what LC 876 asks for.

**Recall:** `slow` moves 1, `fast` moves 2; when `fast` runs out, `slow` is the middle.

## 2. Approach

* **Idea:** Move `slow` by 1 and `fast` by 2 until `fast` can't move twice. Return `slow`.
* **Data structure / pointers:**
  * `slow` — tortoise, 1 step per loop; ends on the middle.
  * `fast` — hare, 2 steps per loop; ends at `None` (odd length) or on the last node (even length).
  * Both start at `head`.
* **Invariant:** `fast` has always moved exactly twice as many steps as `slow`. So when the loop ends, `slow` is at index `n // 2` (0-indexed).
* **Edge cases:**
  * One node: the loop doesn't run; returns that node.
  * Two nodes: `slow` moves once and returns the second node (the second middle).
  * Even length `n`: returns the second of the two middles (index `n // 2`).
  * Odd length `n`: returns the exact middle (index `n // 2`).
  * The list always has at least 1 node under the LC constraints. For an empty list the code would return `None`, since `slow` starts at `head`.

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
    def middleNode(self, head: ListNode | None) -> ListNode | None:

        slow = head
        fast = head

        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        return slow


if __name__ == "__main__":
    solution = Solution()
    assert to_list(solution.middleNode(build_list([1, 2, 3, 4, 5]))) == [3, 4, 5]
    assert to_list(solution.middleNode(build_list([1, 2, 3, 4, 5, 6]))) == [4, 5, 6]
    assert to_list(solution.middleNode(build_list([1]))) == [1]
    assert to_list(solution.middleNode(build_list([1, 2]))) == [2]
    print("All tests passed")
```

## 4. Dry Run

`head = 1 → 2 → 3 → 4 → 5 → 6` (even length, so there are two middles, `3` and `4`).

| Step | `slow` | `fast` | Loop check (`fast and fast.next`) |
| --- | --- | --- | --- |
| Start | `1` | `1` | yes |
| 1 | `2` | `3` | yes |
| 2 | `3` | `5` | yes (`5.next` is `6`) |
| 3 | `4` | `None` | no, `fast` is off the end |

Return `slow` = node `4`, so the result is `4 → 5 → 6`: the second middle.

## 5. Complexity

* **Time:** O(n) — `fast` reaches the end after about n / 2 loops, and each loop does O(1) work.
* **Space:** O(1) — only the two pointers `slow` and `fast`.

## 6. Recall (30 seconds)

* `slow` and `fast` both start at `head`; `slow` moves 1, `fast` moves 2.
* Loop `while fast and fast.next`; return `slow` (no length counting needed).
* Odd length → exact middle; even length → the **second** middle. This is the base move for Reorder List, Palindrome and Sort List.
