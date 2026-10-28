# 143. Reorder List

**LC 143** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Middle (slow/fast) + reverse the second half + merge alternately

---

## 1. Intuition

You want `L0 → Ln → L1 → Ln-1 → L2 → …`: one from the front, one from the back, alternating. A singly linked list can't walk backward, so make the back half walk forward: split the list in the middle, reverse the second half, then zip the two halves together. It is three small moves you already know.

* `slow`, `fast` loop — finds the middle (same as Middle of the Linked List); `slow` ends on the last node of the first half.
* `prev, curr = None, slow.next` and `slow.next = None` — the second half starts after `slow`; setting `slow.next = None` cuts the list into two halves.
* The `while curr:` loop — the standard three-pointer reversal; `prev` ends as the head of the reversed second half.
* `first, second = head, prev` — the two lists to zip: the first half and the reversed second half.
* `tmp1, tmp2 = first.next, second.next` — save both `next` pointers *before* rewiring.
* `first.next = second` and `second.next = tmp1` — put one node of the second half after each node of the first half.

**Recall:** find the middle; cut and reverse the second half; zip with `first.next = second`, `second.next = tmp1`.

## 2. Approach

* **Idea:** Split in the middle, reverse the second half, then interleave: one node from the first half, one from the reversed second half.
* **Data structure / pointers:**
  * `slow`, `fast` — find the middle; `slow` ends as the tail of the first half. For even length it is the second of the two middles, so the first half is the longer one.
  * `prev`, `curr`, `nxt` — reverse the second half; `prev` is its new head.
  * `first`, `second` — current nodes of the first half and the reversed second half.
  * `tmp1`, `tmp2` — saved `next` pointers of `first` and `second`.
* **Invariant:** While zipping, everything before `first` is already in the final order, and `first` / `second` are the heads of the two lists still to be merged. The second half is never longer than the first, so `while second` is enough.
* **Edge cases:**
  * Empty list or one node: returned immediately (the guard `not head or not head.next`).
  * Two nodes: the second half is a single node `2`. After the cut, `slow.next = None` and `curr` is `None`, so `second` is `None` and the zip loop doesn't run; the list is already `1 → 2`.
  * Odd length: the middle node stays at the end of the first half and ends last in the result.
  * Even length: the first half is longer by one, so the leftover first-half node ends last.
  * The function returns nothing; it changes the list in place.

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
    def reorderList(self, head: ListNode | None) -> None:
        """
        Do not return anything, modify head in-place instead.
        """
        if not head or not head.next:
            return

        # Step 1: Find the middle of the linked list using slow and fast pointers
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Step 2: Reverse the second half of the list
        prev, curr = None, slow.next
        slow.next = None  # Cut the list into two halves
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        # Step 3: Merge the two halves alternately
        first, second = head, prev
        while second:
            tmp1, tmp2 = first.next, second.next
            first.next = second
            second.next = tmp1
            first, second = tmp1, tmp2


if __name__ == "__main__":
    solution = Solution()
    head = build_list([1, 2, 3, 4])
    solution.reorderList(head)
    assert to_list(head) == [1, 4, 2, 3]
    head = build_list([1, 2, 3, 4, 5])
    solution.reorderList(head)
    assert to_list(head) == [1, 5, 2, 4, 3]
    head = build_list([1])
    solution.reorderList(head)
    assert to_list(head) == [1]
    head = build_list([1, 2])
    solution.reorderList(head)
    assert to_list(head) == [1, 2]
    head = build_list([1, 2, 3])
    solution.reorderList(head)
    assert to_list(head) == [1, 3, 2]
    print("All tests passed")
```

## 4. Dry Run

`head = 1 → 2 → 3 → 4 → 5`.

| Phase | State |
| --- | --- |
| 1. Find the middle | `slow` ends on `3` |
| 2. Cut and reverse | `slow.next = None`: first half `1 → 2 → 3`; second half `4 → 5` reversed to `5 → 4` |
| 3. Zip | see the table below |

| Zip step | `first` | `second` | `tmp1`, `tmp2` | After rewiring |
| --- | --- | --- | --- | --- |
| 1 | `1` | `5` | `2`, `4` | `1 → 5 → 2 → 3` (second half left: `4`) |
| 2 | `2` | `4` | `3`, `None` | `1 → 5 → 2 → 4 → 3` |
| End | `3` | `None` | – | loop stops |

Result: `1 → 5 → 2 → 4 → 3`. Node `3` already had `next = None` from the cut, so the list ends cleanly.

## 5. Complexity

* **Time:** O(n) — three passes, each at most n steps: find the middle, reverse the half, merge.
* **Space:** O(1) — only pointers (`slow`, `fast`, `prev`, `curr`, `nxt`, `first`, `second`, `tmp1`, `tmp2`); everything is relinked in place.

## 6. Recall (30 seconds)

* Three steps: (1) slow/fast to the middle, (2) `slow.next = None` and reverse the second half, (3) zip.
* Zip loop: save `tmp1, tmp2`; `first.next = second`; `second.next = tmp1`; move `first, second = tmp1, tmp2`; loop `while second`.
* Guard `not head or not head.next` first. The first half is never shorter than the second, so ending on `second` is safe.
