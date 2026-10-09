# 61. Rotate List

**LC 61** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Close the list into a ring, then cut at the new tail (`tail`, `new_tail`, `new_head`)

---

## 1. Intuition

Rotating right by `k` means the last `k` nodes jump to the front. Picture the list as a circle: join the tail back to the head, then just cut the circle at a different place. The cut goes after the new tail, which is `length - k - 1` steps from `head`.

* `length` and `tail` — one pass to count the nodes and find the last node.
* `k = k % length` — rotating by `length` gives the same list, so only the remainder matters (this also handles huge `k`).
* `tail.next = head` — makes the ring.
* `steps_to_new_tail = length - k - 1` — the new tail is the node just before the last `k` nodes.
* `new_head = new_tail.next` and `new_tail.next = None` — the node after the cut starts the answer; cutting the link opens the ring.

**Recall:** count and find `tail`; `k %= length`; ring it with `tail.next = head`; walk `length - k - 1` to `new_tail`; cut.

## 2. Approach

* **Idea:** Make the list circular, walk to the new tail, and break the ring right after it. The new head is the node after the new tail.
* **Data structure / pointers:**
  * `tail` — the original last node; after the first pass it is linked back to `head`.
  * `length` — number of nodes.
  * `new_tail` — the node at index `length - k - 1`; its `next` will be set to `None`.
  * `new_head` — `new_tail.next` before the cut; the head of the result.
* **Invariant:** After `tail.next = head`, every node is reachable in a circle of `length` nodes. Cutting after the node `k` places before the old tail leaves exactly the last `k` nodes in front.
* **Edge cases:**
  * Empty list or one node: returned as is.
  * `k = 0`, or `k` a multiple of `length`: `k % length == 0`, return `head` unchanged (this check also stops us from forming a ring and cutting it at the wrong spot).
  * `k` larger than `length` (up to about 2 × 10⁹): handled by `k % length`.
  * Two nodes: `k % 2` is 0 or 1, and 1 swaps them.

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

    def rotateRight(self, head: ListNode | None, k: int) -> ListNode | None:
        if not head or not head.next or k == 0:
            return head

        # Step 1: Compute the length and locate the original tail
        length = 1
        tail = head
        while tail.next:
            tail = tail.next
            length += 1

        # Step 2: Normalize k
        k = k % length
        if k == 0:
            return head

        # Step 3: Form a circular list
        tail.next = head

        # Step 4: Find the new tail at position (length - k - 1)
        steps_to_new_tail = length - k - 1
        new_tail = head
        for _ in range(steps_to_new_tail):
            new_tail = new_tail.next

        # Step 5: Sever the loop and establish new head
        new_head = new_tail.next
        new_tail.next = None

        return new_head


if __name__ == "__main__":
    solution = Solution()
    assert to_list(solution.rotateRight(build_list([1, 2, 3, 4, 5]), 2)) == [4, 5, 1, 2, 3]
    assert to_list(solution.rotateRight(build_list([0, 1, 2]), 4)) == [2, 0, 1]
    assert to_list(solution.rotateRight(build_list([1, 2, 3]), 3)) == [1, 2, 3]
    assert to_list(solution.rotateRight(build_list([1, 2]), 1)) == [2, 1]
    assert to_list(solution.rotateRight(build_list([1]), 99)) == [1]
    assert to_list(solution.rotateRight(build_list([]), 5)) == []
    assert to_list(solution.rotateRight(build_list([1, 2, 3]), 2_000_000_000)) == [2, 3, 1]
    print("All tests passed")
```

## 4. Dry Run

`head = 1 → 2 → 3 → 4 → 5`, `k = 2`.

| Step | State | Result |
| --- | --- | --- |
| Count | `length = 5`, `tail = 5` | – |
| Normalize | `k = 2 % 5 = 2` | – |
| Ring | `tail.next = head` | `1 → 2 → 3 → 4 → 5 → 1 → …` |
| Walk | `steps_to_new_tail = 5 - 2 - 1 = 2`: `new_tail` goes `1 → 2 → 3` | `new_tail = 3` |
| Cut | `new_head = new_tail.next = 4`, then `new_tail.next = None` | `4 → 5 → 1 → 2 → 3 → None` |

Return `new_head` = `4 → 5 → 1 → 2 → 3`.

## 5. Complexity

* **Time:** O(n) — one pass to find `length` and `tail`, then at most `length - 1` steps to reach `new_tail`.
* **Space:** O(1) — only a few pointers and counters; the list is relinked in place.

## 6. Recall (30 seconds)

* One pass: get `length` and `tail`; `k %= length`; if `k == 0`, return `head`.
* `tail.next = head` (ring); `new_tail` is `length - k - 1` steps from `head`.
* `new_head = new_tail.next`, `new_tail.next = None`, return `new_head`.
