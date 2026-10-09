# Topic 4 — Hash Map + List / Design

## The pattern

A linked list can't jump to a node, so pair it with a **hash map** that can. Two uses:

```python
# 1. Copy with random pointers: map every old node to its copy
copies = {None: None}
node = head
while node:
    copies[node] = Node(node.val)
    node = node.next
node = head
while node:
    copies[node].next = copies[node.next]
    copies[node].random = copies[node.random]
    node = node.next
return copies[head]

# 2. LRU Cache: map key → node in a DOUBLY linked list (most recent at the front)
#    get:  find the node in the map, move it to the front, return its value
#    put:  insert/update at the front; if over capacity, remove the node at the back (and its map entry)
```

The doubly linked list gives `O(1)` "move to front" and "remove from back"; the hash map gives `O(1)` lookup.

## How to spot this topic

* You need **`O(1)` lookup by key** *and* an **ordering** (recent use, insertion order), or you need to **copy** a structure whose nodes point at other nodes.
* Words to look for: **"deep copy"**, **"random pointer"**, **"least recently used"**, **"evict"**, **O(1) get and put**.
* Quick test: *do I need to find a specific node instantly, and also keep the nodes in an order?* If yes, it's this topic.

**Not this topic if:** the pointers are simple and can be handled with two pointers (→ Topics 1–3).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 19 | Copy List with Random Pointer | Map old node → new node (or weave the copies between the originals for `O(1)` space) |
| 20 | LRU Cache | Hash map for lookup + doubly linked list with sentinel head and tail for the recency order |
