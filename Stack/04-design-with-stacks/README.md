# Topic 4 — Design with Stacks

## The pattern

Use a stack (or two) **inside a data structure** to get an `O(1)` operation that the plain structure can't give you.

```python
# Min Stack: every push also records the minimum so far
self.stack.append((value, min(value, self.stack[-1][1] if self.stack else value)))
# get_min → self.stack[-1][1]

# Queue using two stacks: in_stack takes pushes; out_stack serves pops
def pop(self):
    if not self.out_stack:                     # refill only when empty → amortized O(1)
        while self.in_stack:
            self.out_stack.append(self.in_stack.pop())
    return self.out_stack.pop()
```

## How to spot this topic

* The question says **"design a class"** and asks for **`O(1)`** for every operation.
* Words to look for: **"design"**, **"implement … using stacks"**, **"get the minimum in constant time"**.
* Quick test: *is there a piece of information I could store on each push so a later query is instant?* If yes, it's this topic.

**Not this topic if:** the data structure needs a different container (a doubly linked list → Linked-List repo).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 12 | Min Stack | Store `(value, min so far)` on every push |
| E2 (extra) | Implement Queue using Stacks | `in_stack` for pushes, `out_stack` for pops; refill `out_stack` only when it is empty |
