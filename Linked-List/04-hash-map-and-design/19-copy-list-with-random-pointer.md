# 138. Copy List with Random Pointer

**LC 138** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Hash map old node → new node (or interleaving nodes)

---

## 1. Intuition

You want to photocopy a chain of people where each person also points at some random other person. If you copy people one by one, a `random` pointer may point at someone you haven't copied yet. So: first make every copy (no wiring), keep a lookup "original → copy", then wire all the pointers using that lookup.

* `oldToCopy = {None: None}` — the lookup table; the `None` entry means a null `next` or `random` needs no special case.
* Pass 1 (`oldToCopy[cur] = copy`) — creates one new node per old node, with only the value copied.
* Pass 2 (`copy.next = oldToCopy[cur.next]`) — the copy's `next` is the *copy of* the old `next`, never the old node itself.
* `copy.random = oldToCopy[cur.random]` — same for `random`; it works even for `random` pointing forward, backward, or at itself.
* `return oldToCopy[head]` — the copy of the head; `None` if the list is empty.

**Recall:** pass 1 makes the copies and fills `oldToCopy`; pass 2 wires `next` and `random` through `oldToCopy`.

## 2. Approach

* **Idea:** Two passes over the original list. Pass 1 creates all copies and records which copy belongs to which original. Pass 2 sets each copy's `next` and `random` by looking up the copies of the originals' targets.
* **Data structure / pointers:**
  * `oldToCopy` — dict mapping each original node to its copy, plus `None → None`.
  * `cur` — the original node being processed.
  * `copy` — the copy of `cur`.
* **Invariant:** After pass 1, every original node has exactly one copy in `oldToCopy`. So in pass 2, any `cur.next` or `cur.random` (even `None`) can be translated into the right copy.
* **Edge cases:**
  * Empty list: no loops run, `oldToCopy[None]` returns `None`.
  * `random` points to the node itself: `oldToCopy[cur.random]` is `copy`, so the copy points to itself.
  * All `random` pointers are `None`: every lookup gives `None`.
  * `random` points backward or forward: fine, since all copies exist before any wiring.
  * Duplicate values: the dict is keyed by node object, not by value, so duplicates don't clash.

## 3. Code

```python
from typing import Optional


class Node:
    def __init__(self, x: int, next: "Node" = None, random: "Node" = None):
        self.val = int(x)
        self.next = next
        self.random = random


def build_list(pairs: list[list]) -> Optional[Node]:
    """pairs[i] = [val, random_index or None]; builds the original list."""
    nodes = [Node(val) for val, _ in pairs]
    for i, (_, random_index) in enumerate(pairs):
        if i + 1 < len(nodes):
            nodes[i].next = nodes[i + 1]
        if random_index is not None:
            nodes[i].random = nodes[random_index]
    return nodes[0] if nodes else None


def to_pairs(head: Optional[Node]) -> list[list]:
    """Inverse of build_list: [val, random_index or None] for each node."""
    index_of = {}
    node = head
    while node:
        index_of[node] = len(index_of)
        node = node.next
    pairs = []
    node = head
    while node:
        pairs.append([node.val, index_of[node.random] if node.random else None])
        node = node.next
    return pairs


class Solution:

    def copyRandomList(self, head: "Optional[Node]") -> "Optional[Node]":
        # Mapping old_node -> copy_node, including None -> None for boundary handling
        oldToCopy = {None: None}

        # Pass 1: Instantiate all cloned nodes without wiring pointers
        cur = head
        while cur:
            copy = Node(cur.val)
            oldToCopy[cur] = copy
            cur = cur.next

        # Pass 2: Connect next and random pointers using the hash map
        cur = head
        while cur:
            copy = oldToCopy[cur]
            copy.next = oldToCopy[cur.next]
            copy.random = oldToCopy[cur.random]
            cur = cur.next

        return oldToCopy[head]
```

### Alternative: O(1) space interleaving

Weave each copy right after its original (`A → A' → B → B'`). Then `A'.random = A.random.next` needs no map. Finally, unweave the two lists. The tests below run both approaches.

```python
class SolutionSpaceOptimized:

    def copyRandomList(self, head: "Optional[Node]") -> "Optional[Node]":
        if not head:
            return None

        # Pass 1: Interleave cloned nodes: A -> A' -> B -> B'
        cur = head
        while cur:
            nxt = cur.next
            copy = Node(cur.val, nxt)
            cur.next = copy
            cur = nxt

        # Pass 2: Assign random pointers for cloned nodes
        cur = head
        while cur:
            if cur.random:
                cur.next.random = cur.random.next
            cur = cur.next.next

        # Pass 3: Unweave the interleaved list
        dummy = Node(0)
        copy_curr = dummy
        cur = head
        while cur:
            nxt = cur.next.next
            copy = cur.next
            copy_curr.next = copy
            copy_curr = copy

            cur.next = nxt
            cur = nxt

        return dummy.next


if __name__ == "__main__":
    examples = [
        [[7, None], [13, 0], [11, 4], [10, 2], [1, 0]],
        [[1, 1], [2, 1]],
        [[3, None], [3, 0], [3, None]],
        [],
    ]
    for solution in (Solution(), SolutionSpaceOptimized()):
        for pairs in examples:
            original = build_list(pairs)
            copied = solution.copyRandomList(original)
            assert to_pairs(copied) == pairs  # same structure
            assert to_pairs(original) == pairs  # original not damaged
            seen = set()
            node = original
            while node:
                seen.add(node)
                node = node.next
            node = copied
            while node:
                assert node not in seen  # no shared nodes: a true deep copy
                assert node.random is None or node.random not in seen
                node = node.next
    print("All tests passed")
```

## 4. Dry Run

`head = [[7, null], [13, 0]]`: node `A(7)` with `random = None`, and node `B(13)` with `random = A`.

**Pass 1** — `oldToCopy = {None: None, A: A', B: B'}` (`A'` and `B'` have no pointers yet).

**Pass 2:**

| `cur` | `copy` | `copy.next = oldToCopy[cur.next]` | `copy.random = oldToCopy[cur.random]` |
| --- | --- | --- | --- |
| `A(7)` | `A'` | `oldToCopy[B]` = `B'` | `oldToCopy[None]` = `None` |
| `B(13)` | `B'` | `oldToCopy[None]` = `None` | `oldToCopy[A]` = `A'` |

Return `oldToCopy[head]` = `A'`, which is `A'(7) → B'(13)` with `B'.random = A'`.

## 5. Complexity

* **Time:** O(n) — two passes over the n nodes, with O(1) dict operations per node.
* **Space:** O(n) — `oldToCopy` holds one entry per node (the copies themselves are the required output).
* *Interleaving version:* time O(n) (three passes), space O(1) extra, since the copies are woven into the original list instead of stored in a map.

## 6. Recall (30 seconds)

* `oldToCopy = {None: None}`; pass 1: for each `cur`, `oldToCopy[cur] = Node(cur.val)`.
* Pass 2: `copy.next = oldToCopy[cur.next]` and `copy.random = oldToCopy[cur.random]`. Return `oldToCopy[head]`.
* O(1)-space alternative: weave `A → A' → B → B'`, set `A'.random = A.random.next`, then unweave and restore the original.
