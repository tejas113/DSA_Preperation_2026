# 155. Min Stack

**LC 155** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Store the minimum-so-far next to every pushed value

---

## 1. Intuition

A normal stack can't tell you its minimum without looking at every item. The trick: when you push a value, also remember **what the minimum was at that moment**. The minimum only changes when something is pushed or popped, so if each item carries its own "minimum so far", popping an item automatically brings back the previous minimum.

* `self.stack` holds the **values** pushed, in order. Its top, `self.stack[-1]`, is what `top()` returns.
* `self.min_stack` holds one **minimum-so-far** per value, in the same order, so both lists always have the same length. Its top, `self.min_stack[-1]`, is what `getMin()` returns.
* `current_min = min(val, self.min_stack[-1] if self.min_stack else val)` compares the new value with the old minimum. The `if self.min_stack else val` part handles the very first push.
* `pop()` removes from both lists, so the old minimum is back on top of `self.min_stack`. Nothing needs to be recomputed.
* Duplicates are fine: each copy of the minimum has its own entry, so popping one leaves the other.

**Recall:** every push stores `(value, min so far)`; pop removes both; `getMin()` and `top()` read the top of each.

## 2. Approach

* **Idea:** Keep a second stack, `min_stack`, that moves in lock step with `stack`. Each entry in `min_stack` is the smallest value in `stack` at or below that position.
* **Data structure / pointers:** `self.stack` is a plain list of values (top is `self.stack[-1]`). `self.min_stack` is a plain list of minimums-so-far (top is `self.min_stack[-1]`). `val` is the pushed value and `current_min` is the new entry for `min_stack`.
* **Invariant:** `len(self.stack) == len(self.min_stack)` always, and `self.min_stack[i]` is the minimum of `self.stack[0..i]`. So `self.min_stack[-1]` is the minimum of everything currently in the stack.
* **Edge cases:**
  * **Stack empty on `push`:** `self.min_stack` is empty, so the code uses `val` itself as the minimum.
  * **Stack empty on `pop`, `top` or `getMin`:** these would raise an `IndexError`. The problem guarantees they are only called on a non-empty stack, so the code has no guard.
  * **Duplicate minimums** (`push(2), push(1), push(1)`): `min_stack` is `[2, 1, 1]`. After one `pop()`, it is `[2, 1]` and `getMin()` is still `1`.
  * **A larger value pushed on top of the minimum:** `current_min` stays the old minimum, so `min_stack` repeats it.
  * **Negative values:** nothing special, `min` works the same way.

## 3. Code

```python
class MinStack:

    def __init__(self):
        self.stack = []
        self.min_stack = []

    def push(self, val: int) -> None:
        self.stack.append(val)
        # Calculate minimum relative to current top of min_stack
        current_min = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(current_min)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

### Alternative: Single stack of `(val, min)` pairs

The same idea with one list: push a tuple `(val, current_min)` so the value and its minimum can never get out of sync.

```python
class MinStackSingleList:

    def __init__(self):
        self.stack = []  # Stores tuple: (val, min_at_this_state)

    def push(self, val: int) -> None:
        current_min = min(val, self.stack[-1][1] if self.stack else val)
        self.stack.append((val, current_min))

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]

    def getMin(self) -> int:
        return self.stack[-1][1]


if __name__ == "__main__":
    # Shared tests: run against both MinStack and MinStackSingleList
    for stack_class in (MinStack, MinStackSingleList):
        min_stack = stack_class()
        min_stack.push(-2)
        min_stack.push(0)
        min_stack.push(-3)
        assert min_stack.getMin() == -3
        min_stack.pop()
        assert min_stack.top() == 0
        assert min_stack.getMin() == -2

        duplicates = stack_class()
        duplicates.push(2)
        duplicates.push(1)
        duplicates.push(1)
        duplicates.pop()
        assert duplicates.getMin() == 1
        duplicates.pop()
        assert duplicates.getMin() == 2

        single = stack_class()
        single.push(5)
        assert single.top() == 5
        assert single.getMin() == 5
    print("All tests passed")
```

## 4. Dry Run

Operations: `push(-2)`, `push(0)`, `push(-3)`, `getMin()`, `pop()`, `top()`, `getMin()`

| Step | Call | What happens | `self.stack` after | `self.min_stack` after | Returns |
|---|---|---|---|---|---|
| 1 | `push(-2)` | `min_stack` empty, so `current_min = -2` | `[-2]` | `[-2]` | `None` |
| 2 | `push(0)` | `current_min = min(0, -2) = -2` | `[-2, 0]` | `[-2, -2]` | `None` |
| 3 | `push(-3)` | `current_min = min(-3, -2) = -3` | `[-2, 0, -3]` | `[-2, -2, -3]` | `None` |
| 4 | `getMin()` | Read `min_stack[-1]` | `[-2, 0, -3]` | `[-2, -2, -3]` | `-3` |
| 5 | `pop()` | Remove the top of both lists | `[-2, 0]` | `[-2, -2]` | `None` |
| 6 | `top()` | Read `stack[-1]` | `[-2, 0]` | `[-2, -2]` | `0` |
| 7 | `getMin()` | Read `min_stack[-1]` | `[-2, 0]` | `[-2, -2]` | `-2` |

## 5. Complexity

* **Time:** O(1) for `push`, `pop`, `top` and `getMin`, because each one does a fixed number of list appends, pops, index reads and one `min` of two values.
* **Space:** O(n), because `min_stack` (or the second half of each pair in the alternative) adds one extra value for each of the n pushed items.

## 6. Recall (30 seconds)

* Every `push` also records the minimum so far, `min(val, previous minimum)`; the very first push uses `val` itself.
* `pop()` removes from both, so the previous minimum is back on top.
* `top()` reads `stack[-1]` and `getMin()` reads `min_stack[-1]`, both O(1).
