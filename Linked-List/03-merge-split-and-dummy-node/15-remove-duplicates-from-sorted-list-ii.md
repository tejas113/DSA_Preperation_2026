# 82. Remove Duplicates from Sorted List II

**LC 82** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Dummy node + `prev` (last kept node) + skip duplicate runs

---

## 1. Intuition

In a sorted list, equal values sit next to each other. If a value appears more than once, delete *every* copy of it, not just the extras. The first node might be deleted too, so a dummy node goes in front, and `prev` always marks the last node we have decided to keep.

* `dummy = ListNode(0, head)` / `prev = dummy` — `prev` is the last confirmed-unique node; the dummy lets `prev` exist even if the head is deleted.
* `head.next and head.val == head.next.val` — `head` starts a run of duplicates.
* Inner `while ...: head = head.next` — moves `head` to the *last* node of the run.
* `prev.next = head.next` — cuts out the whole run in one step. `prev` stays put, since the node after the cut is not checked yet.
* `else: prev = prev.next` — `head` is unique, so keep it and advance `prev`.
* `head = head.next` — always step forward to the first node after the run (or after the unique node).

**Recall:** dummy + `prev`; if `head` starts a run, skip to its end and set `prev.next = head.next`; otherwise move `prev`. Then `head = head.next`.

## 2. Approach

* **Idea:** Walk with `head`. When `head` begins a block of equal values, jump over the whole block by changing `prev.next`. Otherwise `head` is unique, so advance `prev`.
* **Data structure / pointers:**
  * `dummy` — fake node before `head`, so the head itself can be removed.
  * `prev` — last node known to be kept; `prev.next` is where the next kept node gets attached.
  * `head` — the node being examined (reused as the scanning pointer).
* **Invariant:** The list from `dummy` to `prev` contains only values that appear exactly once in the original list. `head` is at the first node not yet examined, and every node after `prev` and before `head` has already been judged (kept nodes are in the chain; duplicates are cut).
* **Edge cases:**
  * Empty list: the loop never runs, returns `None`.
  * All elements equal (`[1, 1, 1]`): `prev` stays on `dummy`, `dummy.next` becomes `None`.
  * Duplicates at the head (`[1, 1, 2, 3]`): `dummy.next` jumps to `2`, which is why the dummy is needed.
  * Duplicates at the tail (`[1, 2, 3, 3]`): `prev.next` becomes `None`.
  * A run of three or more equal nodes is skipped in one inner loop.
  * No duplicates: `prev` simply follows `head`, and the list is unchanged.

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

    def deleteDuplicates(self, head: ListNode | None) -> ListNode | None:
        dummy = ListNode(0, head)
        prev = dummy

        while head:
            # Check if current node is the start of a duplicate sequence
            if head.next and head.val == head.next.val:
                # Advance head to the last node of the duplicate sequence
                while head.next and head.val == head.next.val:
                    head = head.next
                # Skip all duplicate nodes by linking prev to the node after duplicates
                prev.next = head.next
            else:
                # No duplicate for this node; advance prev pointer
                prev = prev.next

            head = head.next

        return dummy.next


if __name__ == "__main__":
    solution = Solution()
    assert to_list(solution.deleteDuplicates(build_list([1, 2, 3, 3, 4, 4, 5]))) == [1, 2, 5]
    assert to_list(solution.deleteDuplicates(build_list([1, 1, 1, 2, 3]))) == [2, 3]
    assert to_list(solution.deleteDuplicates(build_list([1, 1, 1]))) == []
    assert to_list(solution.deleteDuplicates(build_list([1, 2, 3, 3]))) == [1, 2]
    assert to_list(solution.deleteDuplicates(build_list([1, 2, 3]))) == [1, 2, 3]
    assert to_list(solution.deleteDuplicates(build_list([]))) == []
    print("All tests passed")
```

## 4. Dry Run

`head = 1 → 2 → 3 → 3 → 4 → 4 → 5`. Start: `prev = dummy`, `head = 1`.

| Step | `head` | Duplicate run? | After the step | `prev` |
| --- | --- | --- | --- | --- |
| 1 | `1` | No (`1 != 2`) | list unchanged | `1` |
| 2 | `2` | No (`2 != 3`) | list unchanged | `2` |
| 3 | `3` | Yes (`3 == 3`) | inner loop moves `head` to the 2nd `3`; `prev.next = 4`: `dummy → 1 → 2 → 4 → 4 → 5` | `2` (stays) |
| 4 | `4` | Yes (`4 == 4`) | inner loop moves `head` to the 2nd `4`; `prev.next = 5`: `dummy → 1 → 2 → 5` | `2` (stays) |
| 5 | `5` | No (`head.next` is `None`) | list unchanged | `5` |

After each step `head = head.next`; after step 5 it is `None`, so the loop ends. Return `dummy.next` = `1 → 2 → 5`.

## 5. Complexity

* **Time:** O(n) — `head` only moves forward, and the inner loop uses the same `head`, so each node is passed over once.
* **Space:** O(1) — only `dummy`, `prev` and `head`; links are changed in place.

## 6. Recall (30 seconds)

* `dummy = ListNode(0, head)`, `prev = dummy`; loop `while head`.
* If `head.val == head.next.val`: run `head` to the end of the block, then `prev.next = head.next` (`prev` does *not* move). Otherwise `prev = prev.next`.
* Always finish the step with `head = head.next`; return `dummy.next`.
