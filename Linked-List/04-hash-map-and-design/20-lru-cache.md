# 146. LRU Cache

**LC 146** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Hash map + doubly linked list (`cache`, `head`, `tail`)

---

## 1. Intuition

Think of a stack of books on a desk. The book you used most recently goes on top; when the desk is full, you remove the one at the bottom. You need to (a) find any book instantly and (b) move a book to the top instantly. A hash map finds it, and a doubly linked list moves it, because a node with `prev` and `next` can unplug itself without any searching.

* `self.cache = {}` — `key → Node`, so `get` and `put` find a node in O(1).
* `prev` and `next` on each `Node` — a node can be removed in O(1) by joining its two neighbours (`_remove`).
* Dummy `head` and `tail` — the list is never really empty, so `_remove` and `_add_to_tail` never need `None` checks.
* Order: `head.next` is the **least** recently used node; `tail.prev` is the **most** recently used. New and just-used nodes are added just before `tail` (`_add_to_tail`).
* `get` — `_remove(node)` then `_add_to_tail(node)`: using a key makes it the newest.
* `put` — remove the old node if the key exists, add a fresh node at the tail, and if `len(self.cache) > self.capacity`, evict `self.head.next`.
* `del self.cache[lru_node.key]` — this is why each `Node` stores its `key` as well as its `value`.

**Recall:** map `key → node`, doubly linked list ordered oldest → newest between two dummies; every use moves a node to just before `tail`; evict `head.next`.

## 2. Approach

* **Idea:** Keep a hash map for lookup and a doubly linked list for usage order. Every `get` or `put` moves the node to the most-recently-used end; when over capacity, drop the node at the least-recently-used end.
* **Data structure / pointers:**
  * `self.cache` — dict from `key` to its `Node`.
  * `self.head` — dummy; `head.next` is the LRU node.
  * `self.tail` — dummy; `tail.prev` is the MRU node.
  * `Node.key`, `Node.value`, `Node.prev`, `Node.next` — the key is stored so an evicted node can be deleted from the dict.
  * `_remove(node)` — unlinks a node from the list. `_add_to_tail(node)` — links it just before `tail`.
* **Invariant:** The nodes between `head` and `tail` are exactly the entries in `self.cache`, ordered from least to most recently used. The cache never holds more than `capacity` entries after `put` returns.
* **Edge cases:**
  * Missing key on `get`: returns `-1` and changes nothing.
  * `put` on an existing key: the old node is removed first, so the key appears once and moves to MRU with the new value. The size doesn't grow, so nothing is evicted.
  * Capacity 1: every new key evicts the previous one; the dummies keep this safe.
  * `get` on the only element: removing it and re-adding it works because of the dummies.
  * Over capacity: only one eviction is ever needed per `put`.

## 3. Code

```python
class Node:

    def __init__(self, key: int = 0, value: int = 0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:

    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key -> Node

        # Dummy head and tail nodes
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        """Remove an existing node from the doubly linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_tail(self, node: Node) -> None:
        """Add a node right before the dummy tail (Most Recently Used position)."""
        prev_node = self.tail.prev
        prev_node.next = node
        node.prev = prev_node
        node.next = self.tail
        self.tail.prev = node

    def get(self, key: int) -> int:
        if key not in self.cache:
            return -1
        node = self.cache[key]
        # Move node to the tail (MRU)
        self._remove(node)
        self._add_to_tail(node)
        return node.value

    def put(self, key: int, value: int) -> None:
        if key in self.cache:
            # Remove existing node from DLL
            self._remove(self.cache[key])

        new_node = Node(key, value)
        self.cache[key] = new_node
        self._add_to_tail(new_node)

        if len(self.cache) > self.capacity:
            # Evict least recently used node (node right after dummy head)
            lru_node = self.head.next
            self._remove(lru_node)
            del self.cache[lru_node.key]


if __name__ == "__main__":
    # LeetCode example
    lru = LRUCache(2)
    lru.put(1, 1)
    lru.put(2, 2)
    assert lru.get(1) == 1
    lru.put(3, 3)  # evicts key 2
    assert lru.get(2) == -1
    lru.put(4, 4)  # evicts key 1
    assert lru.get(1) == -1
    assert lru.get(3) == 3
    assert lru.get(4) == 4

    # Capacity 1
    one = LRUCache(1)
    one.put(1, 10)
    one.put(2, 20)
    assert one.get(1) == -1
    assert one.get(2) == 20

    # Updating an existing key refreshes it and replaces the value
    upd = LRUCache(2)
    upd.put(1, 1)
    upd.put(2, 2)
    upd.put(1, 100)  # key 1 is now the newest
    upd.put(3, 3)  # evicts key 2, not key 1
    assert upd.get(2) == -1
    assert upd.get(1) == 100
    print("All tests passed")
```

## 4. Dry Run

Capacity 2. List shown from LRU (left) to MRU (right) between the dummies.

| Operation | Output | List (`head ↔ … ↔ tail`) | `head.next` (LRU) | `tail.prev` (MRU) | `cache` keys |
| --- | --- | --- | --- | --- | --- |
| start | – | `head ↔ tail` | – | – | `{}` |
| `put(1, 1)` | – | `[1:1]` | `1` | `1` | `{1}` |
| `put(2, 2)` | – | `[1:1] ↔ [2:2]` | `1` | `2` | `{1, 2}` |
| `get(1)` | `1` | `[2:2] ↔ [1:1]` | `2` | `1` | `{1, 2}` |
| `put(3, 3)` | – | `[1:1] ↔ [3:3]` | `1` | `3` | `{1, 3}` (3 > 2, so evict `head.next` = key 2) |
| `get(2)` | `-1` | `[1:1] ↔ [3:3]` | `1` | `3` | `{1, 3}` |

## 5. Complexity

* **Time:** O(1) for both `get` and `put` — the dict lookup is O(1) on average, and `_remove` and `_add_to_tail` only change a fixed number of pointers.
* **Space:** O(capacity) — at most `capacity` nodes and dict entries are stored, plus the two dummy nodes.

## 6. Recall (30 seconds)

* Dict `key → Node`, plus a doubly linked list between dummy `head` and `tail`: `head.next` = LRU, `tail.prev` = MRU.
* `get` and `put` always do `_remove` then `_add_to_tail`; `put` on an existing key removes the old node first.
* Over capacity: `lru_node = head.next`, `_remove(lru_node)`, `del cache[lru_node.key]` (that's why `Node` stores `key`).
