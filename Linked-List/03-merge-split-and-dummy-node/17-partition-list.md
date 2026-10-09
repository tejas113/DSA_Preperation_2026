# 86. Partition List

**LC 86** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Two dummy lists (`less_head`, `greater_head`) joined at the end

---

## 1. Intuition

Sort a deck into two piles without changing the order inside each pile: cards smaller than `x` go on one pile, the rest on the other. Then put the second pile under the first. With a dummy node and a tail pointer for each pile, appending never needs a special case.

* `less_head` / `greater_head` — two dummy nodes; each starts an empty pile.
* `less` / `greater` — the tail of each pile, where the next node is appended.
* `if curr.val < x` — decides the pile; ties (`curr.val == x`) go to `greater`.
* `curr = curr.next` — safe because we only change `less.next` or `greater.next`, never `curr.next`, until the end.
* `greater.next = None` — the last node of `greater` may still point at a node that is now in `less`; without this cut you get a cycle.
* `less.next = greater_head.next` — joins the two piles; return `less_head.next`.

**Recall:** two dummies, two tails; `< x` goes to `less`, else to `greater`; `greater.next = None`; join `less.next = greater_head.next`.

## 2. Approach

* **Idea:** One pass. Move each existing node onto the end of the `less` list or the `greater` list, keeping relative order. Then connect `less` to `greater`.
* **Data structure / pointers:**
  * `less_head`, `greater_head` — dummy heads of the two lists.
  * `less`, `greater` — current tails of the two lists.
  * `curr` — the node being sorted into a list.
* **Invariant:** `less_head.next ... less` holds, in original order, all nodes seen so far with value `< x`. `greater_head.next ... greater` holds those `>= x`. `curr` is the first node not yet sorted.
* **Edge cases:**
  * Empty list: the loop is skipped, returns `None`.
  * All nodes `< x`: `greater` is empty, `greater_head.next` is `None`, so `less.next = None` is correct.
  * All nodes `>= x`: `less` is empty, so `less_head.next` ends up pointing straight at the first `greater` node.
  * Equal to `x`: goes to the `greater` side; the relative order is kept in both lists (stable).
  * Stale `next` pointer on the last `greater` node: removed by `greater.next = None`.

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

    def partition(self, head: ListNode | None, x: int) -> ListNode | None:
        less_head = ListNode(0)
        greater_head = ListNode(0)

        less = less_head
        greater = greater_head

        curr = head

        while curr:
            if curr.val < x:
                less.next = curr
                less = less.next
            else:
                greater.next = curr
                greater = greater.next

            # Advance input list pointer
            curr = curr.next

        # Disconnect the tail of the greater list to avoid cycles
        greater.next = None

        # Link the two partitions
        less.next = greater_head.next

        return less_head.next


if __name__ == "__main__":
    solution = Solution()
    assert to_list(solution.partition(build_list([1, 4, 3, 2, 5, 2]), 3)) == [1, 2, 2, 4, 3, 5]
    assert to_list(solution.partition(build_list([2, 1]), 2)) == [1, 2]
    assert to_list(solution.partition(build_list([1, 2]), 3)) == [1, 2]
    assert to_list(solution.partition(build_list([4, 3, 5]), 3)) == [4, 3, 5]
    assert to_list(solution.partition(build_list([]), 1)) == []
    print("All tests passed")
```

## 4. Dry Run

`head = 1 → 4 → 3 → 2 → 5 → 2`, `x = 3`.

| Step | `curr.val` | Test | `less` list | `greater` list |
| --- | --- | --- | --- | --- |
| 1 | 1 | `1 < 3` | `1` | – |
| 2 | 4 | `4 >= 3` | `1` | `4` |
| 3 | 3 | `3 >= 3` | `1` | `4 → 3` |
| 4 | 2 | `2 < 3` | `1 → 2` | `4 → 3` |
| 5 | 5 | `5 >= 3` | `1 → 2` | `4 → 3 → 5` |
| 6 | 2 | `2 < 3` | `1 → 2 → 2` | `4 → 3 → 5` |

After the loop: `greater.next = None` cuts `5` off from the final `2`. Then `less.next = greater_head.next` links `2 → 4`. Return `1 → 2 → 2 → 4 → 3 → 5`.

## 5. Complexity

* **Time:** O(n) — one loop over the n nodes, with O(1) work per node.
* **Space:** O(1) — only the two dummy nodes and a few pointers; the existing nodes are relinked, not copied.

## 6. Recall (30 seconds)

* Two dummies and two tails: `less_head`/`less` and `greater_head`/`greater`; `< x` goes to `less`, everything else to `greater`.
* After the loop, `greater.next = None` first (prevents a cycle).
* Then `less.next = greater_head.next`; return `less_head.next`.
