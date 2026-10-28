# 234. Palindrome Linked List

**LC 234** · **Source:** [+] Claude · **Difficulty:** Easy · **Priority:** Stretch · **Pattern:** Middle (slow/fast) + reverse the second half + compare

---

## 1. Intuition

A palindrome reads the same forwards and backwards. A singly linked list can't be read backwards, so make the second half run backwards: find the middle, reverse everything from there, then walk inward from both ends and compare. It is the same middle + reverse combo as Reorder List, but ending with a compare.

* `slow`, `fast` loop — `slow` ends on the middle (the second middle if the length is even).
* The `while curr:` loop starting at `curr = slow` — reverses the list from the middle to the end; `prev` ends as the head of the reversed half, which is the old last node.
* `left, right = head, prev` — `left` walks from the front, `right` walks from the back (via the reversed half).
* `while right:` — only the reversed half's length is compared. For an odd length the middle node is compared to itself, which is harmless.
* `if left.val != right.val: return False` — the first mismatch settles it.

**Recall:** slow/fast to the middle; reverse from `slow`; compare `left` (from `head`) with `right` (from `prev`) while `right` exists.

## 2. Approach

* **Idea:** Reverse the second half in place, then compare it with the first half node by node. All matches → palindrome.
* **Data structure / pointers:**
  * `slow`, `fast` — find the middle. `slow` ends at index `n // 2`.
  * `prev`, `curr`, `nxt` — reverse from `slow` to the end; `prev` is the new head (the old last node).
  * `left` — walks the first half from `head`.
  * `right` — walks the reversed half from `prev`.
* **Invariant:** While comparing, `left` and `right` are always the same distance from their respective ends of the original list. So each pair compared is a mirror pair.
* **Edge cases:**
  * Empty list or one node: `True` (the guard `not head or not head.next`).
  * Two nodes: `[1, 1]` is `True`, `[1, 2]` is `False`.
  * Odd length: the middle node is compared with itself (same node), which always matches.
  * Even length: the halves have equal length, so every node is compared once.
  * The code does **not** restore the list: the first half's last node still points at the middle, and the reversed half now ends at it. If an interviewer wants the input unchanged, reverse the second half again after comparing.

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


class Solution:
    def isPalindrome(self, head: ListNode | None) -> bool:
        if not head or not head.next:
            return True

        # Step 1: Find the middle of the linked list using slow and fast pointers
        slow, fast = head, head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next

        # Step 2: Reverse the second half of the linked list
        prev = None
        curr = slow
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt

        # Step 3: Compare the first half and the reversed second half
        left, right = head, prev
        while right:
            if left.val != right.val:
                return False
            left = left.next
            right = right.next

        return True


if __name__ == "__main__":
    solution = Solution()
    assert solution.isPalindrome(build_list([1, 2, 2, 1])) is True
    assert solution.isPalindrome(build_list([1, 2])) is False
    assert solution.isPalindrome(build_list([1, 2, 3, 2, 1])) is True
    assert solution.isPalindrome(build_list([1, 2, 3, 1])) is False
    assert solution.isPalindrome(build_list([1])) is True
    assert solution.isPalindrome(build_list([1, 1])) is True
    assert solution.isPalindrome(build_list([])) is True
    print("All tests passed")
```

## 4. Dry Run

`head = 1 → 2 → 2 → 1` (indices 0 to 3).

| Phase | State |
| --- | --- |
| 1. Find the middle | `slow` goes `1 → 2 (index 1) → 2 (index 2)`; `fast` goes `1 → 2 (index 2) → None`. `slow` = index 2 |
| 2. Reverse from `slow` | `2 → 1` (indices 2, 3) becomes `1 → 2`. `prev` = the last `1` |

| Compare step | `left` | `right` | Equal? |
| --- | --- | --- | --- |
| 1 | `1` (index 0) | `1` (index 3) | yes |
| 2 | `2` (index 1) | `2` (index 2) | yes |
| 3 | `2` (index 2) | `None` | loop ends |

Every pair matched, so return `True`.

## 5. Complexity

* **Time:** O(n) — three passes, each at most n steps: find the middle, reverse the half, compare.
* **Space:** O(1) — only pointers (`slow`, `fast`, `prev`, `curr`, `nxt`, `left`, `right`); the reversal is in place. (Copying the values into a Python list would be O(n) space.)

## 6. Recall (30 seconds)

* Guard first: empty or one node is a palindrome. Then slow/fast to the middle.
* Reverse from `slow` to the end; `prev` becomes the head of the reversed half.
* Compare `left = head` with `right = prev` while `right`; any mismatch → `False`. The list is left modified.
