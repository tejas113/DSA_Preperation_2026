# 21. Merge Two Sorted Lists

**LC 21** · **Source:** LC150 + NC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Dummy node + tail (`dummy`, `curr`)

---

## 1. Intuition

Two sorted queues merge into one by repeatedly taking whichever front person is smaller. A dummy node in front of the result means the very first pick needs no special case. When one queue is empty, the other is already sorted, so you attach it whole.

* `dummy = ListNode(0)` / `curr = dummy` — `curr` is the tail of the merged list; `dummy.next` is its head.
* `while list1 and list2` — keep going while both lists still have nodes to compare.
* `if list1.val <= list2.val` — take the smaller front node. Using `<=` takes `list1` on ties.
* `curr.next = list1` (or `list2`), then advance that list and `curr` — splice the existing node in; no new nodes are created.
* `curr.next = list1 if list1 else list2` — attach whichever list still has nodes, in one step.

**Recall:** dummy + `curr`; compare fronts, splice the smaller; when one ends, attach the rest.

## 2. Approach

* **Idea:** Compare the two front nodes, splice the smaller one onto the tail of the result, and repeat. Attach the leftover list at the end.
* **Data structure / pointers:**
  * `list1`, `list2` — the front (smallest unused) node of each input list.
  * `dummy` — fake node before the result, so `dummy.next` is the real head.
  * `curr` — the last node of the merged list so far.
* **Invariant:** The list from `dummy.next` to `curr` is sorted and holds all the nodes taken so far. Every node still in `list1` or `list2` is greater than or equal to `curr.val`.
* **Edge cases:**
  * One or both lists empty: the loop is skipped; returns the other list (or `None`).
  * Disjoint ranges (`[1, 2]` and `[5, 6]`): `list1` runs out first, then `list2` is attached whole.
  * Duplicates / ties: `<=` takes from `list1`, so the merge is stable.
  * Different lengths: the leftover tail of the longer list is attached.

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

    def mergeTwoLists(
        self, list1: ListNode | None, list2: ListNode | None
    ) -> ListNode | None:
        dummy = ListNode(0)
        curr = dummy

        while list1 and list2:
            if list1.val <= list2.val:
                curr.next = list1
                list1 = list1.next
            else:
                curr.next = list2
                list2 = list2.next
            curr = curr.next

        # Attach remaining non-empty list
        curr.next = list1 if list1 else list2

        return dummy.next


if __name__ == "__main__":
    solution = Solution()
    assert to_list(solution.mergeTwoLists(build_list([1, 2, 4]), build_list([1, 3, 4]))) == [1, 1, 2, 3, 4, 4]
    assert to_list(solution.mergeTwoLists(build_list([]), build_list([]))) == []
    assert to_list(solution.mergeTwoLists(build_list([]), build_list([0]))) == [0]
    assert to_list(solution.mergeTwoLists(build_list([1, 2]), build_list([5, 6]))) == [1, 2, 5, 6]
    print("All tests passed")
```

## 4. Dry Run

`list1 = 1 → 2 → 4`, `list2 = 1 → 3 → 4`.

| Step | `list1.val` | `list2.val` | Compare | Node taken | Merged so far |
| --- | --- | --- | --- | --- | --- |
| 1 | 1 | 1 | `1 <= 1` yes | `list1` (1) | `1` |
| 2 | 2 | 1 | `2 <= 1` no | `list2` (1) | `1 → 1` |
| 3 | 2 | 3 | `2 <= 3` yes | `list1` (2) | `1 → 1 → 2` |
| 4 | 4 | 3 | `4 <= 3` no | `list2` (3) | `1 → 1 → 2 → 3` |
| 5 | 4 | 4 | `4 <= 4` yes | `list1` (4) | `1 → 1 → 2 → 3 → 4` |
| End | `None` | 4 | loop stops | attach rest of `list2` | `1 → 1 → 2 → 3 → 4 → 4` |

Return `dummy.next` = `1 → 1 → 2 → 3 → 4 → 4`.

## 5. Complexity

* **Time:** O(m + n) — each loop step moves one node into the result, so the loop runs at most m + n times; attaching the leftover is O(1).
* **Space:** O(1) — the existing nodes are re-linked in place; only `dummy` and a few pointers are created.

## 6. Recall (30 seconds)

* `dummy = ListNode(0)`, `curr = dummy`; return `dummy.next`.
* `while list1 and list2`: splice the smaller node (`<=` for ties), advance that list, then advance `curr`.
* After the loop, `curr.next = list1 if list1 else list2` — no copying, the leftover is already sorted.
