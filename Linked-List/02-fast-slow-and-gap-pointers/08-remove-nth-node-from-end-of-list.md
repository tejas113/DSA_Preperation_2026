# 19. Remove Nth Node From End of List

**LC 19** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Gap pointers (`fast` is `n` ahead) + dummy node

---

## 1. Intuition

You can't count back from the end of a singly linked list, but you can make two people walk with a fixed gap. Send `fast` ahead by `n` steps, then walk both together. When `fast` falls off the end, `slow` is exactly in front of the node to delete. A dummy node in front handles "delete the head".

* `dummyNode = ListNode(0, head)` and `slow = dummyNode` — `slow` starts one node before `head`, so it can stand *before* the target even when the target is the head.
* `while n > 0 and fast` — moves `fast` `n` steps ahead of `head`; this creates the gap.
* `while fast: slow = slow.next; fast = fast.next` — the gap never changes, so when `fast` is `None`, `slow` is the node just before the one to remove.
* `slow.next = slow.next.next` — skips (deletes) the target node.
* `return dummyNode.next` — correct even if the old head was removed.

**Recall:** dummy; `fast` goes `n` ahead; move both until `fast` is `None`; `slow.next = slow.next.next`.

## 2. Approach

* **Idea:** Create a gap of `n` between `slow` and `fast`, move them together until `fast` reaches the end, then unlink the node after `slow`. One pass, no length count.
* **Data structure / pointers:**
  * `dummyNode` — fake node before `head`, so removing the head needs no special case.
  * `slow` — starts at `dummyNode`; ends on the node just before the target.
  * `fast` — starts at `head`; goes `n` steps first, then moves with `slow`.
* **Invariant:** After the first loop, `slow` and `fast` stay a fixed distance apart (`n + 1` links, counting from `slow` to `fast`). So when `fast` is `None`, `slow.next` is the `n`-th node from the end.
* **Edge cases:**
  * Remove the head (`n` equals the length): `fast` is `None` after the first loop, the second loop doesn't run, `slow` is still `dummyNode`, so `dummyNode.next` moves to the second node.
  * One node (`[1]`, `n = 1`): the result is the empty list.
  * Remove the tail (`n = 1`): `slow` stops on the second-to-last node.
  * `n` is always valid (1 ≤ n ≤ length), so `slow.next` is never `None` at the removal step.

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

    def removeNthFromEnd(
        self, head: ListNode | None, n: int
    ) -> ListNode | None:
        dummyNode = ListNode(0, head)

        slow = dummyNode
        fast = head

        # Step 1: Advance fast pointer n steps forward
        while n > 0 and fast:
            fast = fast.next
            n -= 1

        # Step 2: Move both pointers until fast hits the end
        while fast:
            slow = slow.next
            fast = fast.next

        # Step 3: Skip the target node
        slow.next = slow.next.next

        return dummyNode.next


if __name__ == "__main__":
    solution = Solution()
    assert to_list(solution.removeNthFromEnd(build_list([1, 2, 3, 4, 5]), 2)) == [1, 2, 3, 5]
    assert to_list(solution.removeNthFromEnd(build_list([1]), 1)) == []
    assert to_list(solution.removeNthFromEnd(build_list([1, 2]), 1)) == [1]
    assert to_list(solution.removeNthFromEnd(build_list([1, 2]), 2)) == [2]
    assert to_list(solution.removeNthFromEnd(build_list([1, 2, 3]), 3)) == [2, 3]
    print("All tests passed")
```

## 4. Dry Run

`head = 1 → 2 → 3 → 4 → 5`, `n = 2`. Start: `dummy → 1 → 2 → 3 → 4 → 5`, `slow = dummy`, `fast = 1`. Target is node `4`.

| Step | `slow` | `fast` | What happens |
| --- | --- | --- | --- |
| Start | `dummy` | `1` | – |
| Gap 1 | `dummy` | `2` | `fast` moves, `n = 1` |
| Gap 2 | `dummy` | `3` | `fast` moves, `n = 0`; gap is set |
| Walk 1 | `1` | `4` | both move |
| Walk 2 | `2` | `5` | both move |
| Walk 3 | `3` | `None` | both move; `fast` is off the end |
| Remove | `3` | `None` | `slow.next = slow.next.next`: `3 → 5` |

Node `4` is skipped. Return `dummy.next` = `1 → 2 → 3 → 5`.

## 5. Complexity

* **Time:** O(n) — `fast` goes through the list once; `slow` follows behind it, so the total work is about one pass.
* **Space:** O(1) — only `dummyNode`, `slow` and `fast`; the node is unlinked in place.

## 6. Recall (30 seconds)

* `dummyNode = ListNode(0, head)`, `slow = dummyNode`, `fast = head`.
* Move `fast` `n` steps first, then move `slow` and `fast` together until `fast` is `None`.
* `slow` is now just before the target: `slow.next = slow.next.next`; return `dummyNode.next`.
