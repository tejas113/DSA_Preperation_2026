# 2. Add Two Numbers

**LC 2** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Dummy node + tail, walk both lists with a carry

---

## 1. Intuition

This is column addition on paper. The digits are stored in reverse order (ones digit first), so walking from the head is already walking from the ones column. Add the two digits plus the carry, write down one digit, carry the rest.

* `dummy` / `curr` — build the answer list by appending at `curr`, with no special case for the first node.
* `val1 = l1.val if l1 else 0` — a list that has run out just contributes `0`, so different lengths work.
* `total = val1 + val2 + carry` — one column of the sum (at most 9 + 9 + 1 = 19).
* `carry = total // 10` and `digit = total % 10` — the carry for the next column, and the digit to write here.
* `while l1 or l2 or carry` — the `or carry` creates one extra node at the end, e.g. `99 + 1 = 100`.

**Recall:** dummy + tail, `total = a + b + carry`, digit is `% 10`, carry is `// 10`, loop while any of `l1`, `l2` or `carry` is left.

## 2. Approach

* **Idea:** Walk both lists together, adding digit by digit with a carry, and append each result digit to a new list.
* **Data structure / pointers:**
  * `l1`, `l2` — current digit of each input; become `None` when exhausted.
  * `dummy` — fake node before the answer, so `dummy.next` is the real head.
  * `curr` — tail of the answer list, where the next digit is appended.
  * `carry` — 0 or 1, passed to the next column.
* **Invariant:** Before each loop step, the answer list holds the correct digits for all columns processed so far, and `carry` is what still has to be added to the next column.
* **Edge cases:**
  * Lists of different lengths: the shorter one counts as `0`.
  * Final carry: `[9, 9] + [1]` gives `[0, 0, 1]`, which needs the `or carry` in the loop.
  * Both lists are `[0]`: gives `[0]`.
  * One input much longer than the other, e.g. `[9]*7 + [9]*4`.

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

    def addTwoNumbers(
        self, l1: ListNode | None, l2: ListNode | None
    ) -> ListNode | None:
        dummy = ListNode(0)
        curr = dummy
        carry = 0

        while l1 or l2 or carry:
            val1 = l1.val if l1 else 0
            val2 = l2.val if l2 else 0

            # Calculate sum and new carry
            total = val1 + val2 + carry
            carry = total // 10
            digit = total % 10

            # Append new digit node
            curr.next = ListNode(digit)
            curr = curr.next

            # Move input pointers forward
            if l1:
                l1 = l1.next
            if l2:
                l2 = l2.next

        return dummy.next


if __name__ == "__main__":
    solution = Solution()
    assert to_list(solution.addTwoNumbers(build_list([2, 4, 3]), build_list([5, 6, 4]))) == [7, 0, 8]
    assert to_list(solution.addTwoNumbers(build_list([0]), build_list([0]))) == [0]
    assert to_list(
        solution.addTwoNumbers(build_list([9, 9, 9, 9, 9, 9, 9]), build_list([9, 9, 9, 9]))
    ) == [8, 9, 9, 9, 0, 0, 0, 1]
    assert to_list(solution.addTwoNumbers(build_list([9, 9]), build_list([1]))) == [0, 0, 1]
    print("All tests passed")
```

## 4. Dry Run

`l1 = 2 → 4 → 3` (342), `l2 = 5 → 6 → 4` (465). Expected 807, stored as `7 → 0 → 8`.

| Step | `val1` | `val2` | `carry` in | `total` | `digit` | `carry` out | Answer so far |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 2 | 5 | 0 | 7 | 7 | 0 | `7` |
| 2 | 4 | 6 | 0 | 10 | 0 | 1 | `7 → 0` |
| 3 | 3 | 4 | 1 | 8 | 8 | 0 | `7 → 0 → 8` |

`l1`, `l2` and `carry` are all empty/zero, so the loop ends. Return `dummy.next` = `7 → 0 → 8`.

## 5. Complexity

* **Time:** O(max(m, n)) — one loop step per column, and the loop runs at most `max(m, n) + 1` times (the +1 is the final carry).
* **Space:** O(max(m, n)) — the output list has that many nodes (plus at most one). Apart from that output, only a few variables are used.

## 6. Recall (30 seconds)

* `dummy` and `curr` build the answer; `carry` starts at 0.
* `while l1 or l2 or carry`: missing digits count as `0`, `total = val1 + val2 + carry`, append `total % 10`, set `carry = total // 10`.
* Advance `l1` and `l2` only if they are not `None`. Return `dummy.next`.
