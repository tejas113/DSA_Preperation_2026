# 92. Reverse Linked List II

**LC 92** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Sublist reversal with a dummy node (`leftPrev`, `cur`, `prev`)

---

## 1. Intuition

Walk to the spot just before the section to flip, reverse exactly that many nodes with the usual three-pointer move, then stitch the flipped section back between the two untouched parts. A dummy node in front means "flip from the very first node" needs no special case.

* `dummy = ListNode(0, head)` — gives `leftPrev` something to stand on when `left = 1`.
* `for _ in range(left - 1)` — stops with `leftPrev` just before position `left` and `cur` at position `left`.
* `for _ in range(right - left + 1)` — the normal reversal, run only on the sublist.
* After that loop, `prev` is the node at `right` (new sublist head) and `cur` is the node after `right`.
* `leftPrev.next.next = cur` — `leftPrev.next` is still the old `left` node, now the sublist tail; it points to the rest.
* `leftPrev.next = prev` — the part before the sublist points to the new sublist head.

**Recall:** dummy, walk `left - 1`, reverse `right - left + 1`, then tail → `cur` and `leftPrev` → `prev`.

## 2. Approach

* **Idea:** One pass. Move to the node before `left`, reverse `right - left + 1` nodes in place, reconnect both ends.
* **Data structure / pointers:**
  * `dummy` — fake node before `head`, so the head can change.
  * `leftPrev` — node just before position `left`; never moves during the reversal.
  * `cur` — first the node at `left`, then the node being reversed, finally the node after `right`.
  * `prev` — head of the reversed sublist so far; ends at the node at `right`.
  * `tmpNext` — saved `cur.next` before the link is flipped.
* **Invariant:** During the reversal, `prev` is the reversed part of the sublist and `cur` is the untouched rest. `leftPrev.next` keeps pointing at the old `left` node, which is the tail of the reversed part.
* **Edge cases:**
  * `left == right`: one reversal step, then the reconnect puts the same node back. The list is unchanged.
  * `left = 1`: `leftPrev` stays on `dummy`, so `dummy.next` becomes the new head. This is why `return dummy.next`.
  * `right` is the last node: `cur` becomes `None`, and the old `left` node ends the list.
  * One node: `left = right = 1`, works as above.

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

    def reverseBetween(
        self, head: ListNode | None, left: int, right: int
    ) -> ListNode | None:
        dummy = ListNode(0, head)

        # 1) Advance pointers to position "left"
        leftPrev, cur = dummy, head
        for _ in range(left - 1):
            leftPrev, cur = cur, cur.next

        # cur = node at "left", leftPrev = node before "left"

        # 2) Reverse sublist from left to right
        prev = None
        for _ in range(right - left + 1):
            tmpNext = cur.next
            cur.next = prev
            prev = cur
            cur = tmpNext

        # 3) Reconnect boundary links
        leftPrev.next.next = cur  # Reconnect old sublist head (now tail) to rest of list
        leftPrev.next = prev  # Reconnect leftPrev to new sublist head

        return dummy.next


if __name__ == "__main__":
    solution = Solution()
    assert to_list(solution.reverseBetween(build_list([1, 2, 3, 4, 5]), 2, 4)) == [1, 4, 3, 2, 5]
    assert to_list(solution.reverseBetween(build_list([5]), 1, 1)) == [5]
    assert to_list(solution.reverseBetween(build_list([1, 2, 3, 4]), 1, 3)) == [3, 2, 1, 4]
    assert to_list(solution.reverseBetween(build_list([3, 5]), 1, 2)) == [5, 3]
    assert to_list(solution.reverseBetween(build_list([1, 2, 3]), 2, 3)) == [1, 3, 2]
    print("All tests passed")
```

## 4. Dry Run

`head = 1 → 2 → 3 → 4 → 5`, `left = 2`, `right = 4`. Start: `dummy → 1 → 2 → 3 → 4 → 5 → None`.

| Step | `leftPrev` | `cur` | `prev` | What happens |
| --- | --- | --- | --- | --- |
| Positioning (1 step) | `1` | `2` | `None` | `cur` is at `left` |
| Reverse 1 | `1` | `3` | `2` | `2 → None` |
| Reverse 2 | `1` | `4` | `3` | `3 → 2 → None` |
| Reverse 3 | `1` | `5` | `4` | `4 → 3 → 2 → None` |
| Reconnect | `1` | `5` | `4` | `leftPrev.next.next = cur` makes `2 → 5`; `leftPrev.next = prev` makes `1 → 4` |

Result: `dummy → 1 → 4 → 3 → 2 → 5 → None`, so return `[1, 4, 3, 2, 5]`.

## 5. Complexity

* **Time:** O(n) — the two loops together visit at most `right` nodes, each once.
* **Space:** O(1) — only a few pointers (`dummy`, `leftPrev`, `cur`, `prev`, `tmpNext`) are used; the links are changed in place.

## 6. Recall (30 seconds)

* `dummy` before `head`; move `leftPrev, cur` forward `left - 1` times.
* Reverse exactly `right - left + 1` nodes: `tmpNext`, `cur.next = prev`, `prev = cur`, `cur = tmpNext`.
* Reconnect in this order: `leftPrev.next.next = cur`, then `leftPrev.next = prev`. Return `dummy.next`.
