# 206. Reverse Linked List

**LC 206** · **Source:** NC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Three-pointer reversal (`prev`, `curr`, `nxt`)

---

## 1. Intuition

Imagine a line of people each pointing at the person in front. To reverse the line, walk down it and make every person point *backward* instead. Before turning someone around, remember who they were pointing at, or you lose the rest of the line.

* `nxt = curr.next` — save the rest of the list *before* breaking the link.
* `curr.next = prev` — the actual reversal: point backward.
* `prev = curr` — `prev` grows by one node; it is the head of the already-reversed part.
* `curr = nxt` — step forward into the unprocessed part.
* `return prev` — when `curr` is `None`, `prev` sits on the old tail, which is the new head.

**Recall:** save `nxt`, flip `curr.next` to `prev`, slide both forward, return `prev`.

## 2. Approach

* **Idea:** Walk the list once. At each node, point `next` backward instead of forward.
* **Data structure / pointers:**
  * `prev` — head of the reversed part so far (starts `None`).
  * `curr` — the node being processed (starts at `head`).
  * `nxt` — saved `curr.next`, so the unprocessed part isn't lost.
* **Invariant:** Before each loop step, `prev` is the fully reversed list of the nodes already visited, and `curr` is the head of the untouched rest.
* **Edge cases:**
  * Empty list (`head = None`): loop is skipped, returns `prev` = `None`.
  * One node: `1.next` becomes `None`, returns that node.
  * Two nodes: the second becomes the head and points to the first, which points to `None`.

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

    def reverseList(self, head: ListNode | None) -> ListNode | None:
        prev = None
        curr = head

        while curr:
            nxt = curr.next  # Save next node
            curr.next = prev  # Reverse pointer
            prev = curr  # Move prev forward
            curr = nxt  # Move curr forward

        return prev


if __name__ == "__main__":
    solution = Solution()
    assert to_list(solution.reverseList(build_list([1, 2, 3, 4, 5]))) == [5, 4, 3, 2, 1]
    assert to_list(solution.reverseList(build_list([1, 2]))) == [2, 1]
    assert to_list(solution.reverseList(build_list([1]))) == [1]
    assert to_list(solution.reverseList(build_list([]))) == []
    print("All tests passed")
```

### Alternative: Recursive (follow-up)

Trust that `reverseList(head.next)` returns the reversed rest, then make the node after `head` point back to `head`.

```python
class SolutionRecursive:

    def reverseList(self, head: ListNode | None) -> ListNode | None:
        # Base case: empty list or single node
        if not head or not head.next:
            return head

        # Reverse the rest of the list
        new_head = self.reverseList(head.next)

        # Re-link head's next node back to head
        head.next.next = head
        head.next = None

        return new_head
```

## 4. Dry Run

`head = 1 → 2 → 3 → None`

| Step | `prev` | `curr` | `nxt` | After `curr.next = prev` | `prev` becomes | `curr` becomes |
| --- | --- | --- | --- | --- | --- | --- |
| Start | `None` | `1` | – | – | – | – |
| 1 | `None` | `1` | `2` | `1 → None` | `1` | `2` |
| 2 | `1` | `2` | `3` | `2 → 1 → None` | `2` | `3` |
| 3 | `2` | `3` | `None` | `3 → 2 → 1 → None` | `3` | `None` |

`curr` is `None`, so the loop stops. Return `prev` = `3 → 2 → 1 → None`.

## 5. Complexity

* **Time:** O(n) — the `while curr` loop visits each node exactly once.
* **Space:** O(1) — only `prev`, `curr` and `nxt` are stored, whatever the list length.
* *Recursive version:* time O(n), space O(n) — one stack frame per node, and it can hit Python's recursion limit on long lists.

## 6. Recall (30 seconds)

* Three pointers: `prev = None`, `curr = head`, and `nxt` saved *first* in every step.
* Loop body, in order: `nxt = curr.next` → `curr.next = prev` → `prev = curr` → `curr = nxt`.
* Return `prev`, not `curr` (`curr` is `None` at the end). Empty list works with no special case.
