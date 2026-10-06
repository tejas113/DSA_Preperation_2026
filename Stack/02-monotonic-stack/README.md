# Topic 2 — Monotonic Stack

## The pattern

Keep a stack whose values are always in one order (say, decreasing). When a new value breaks that order, **pop everything it beats** — and each popped item has just found its answer: the new value is its "next greater element".

```python
answer = [-1] * len(nums)
stack = []                                     # indices still waiting for a greater value
for i, x in enumerate(nums):
    while stack and nums[stack[-1]] < x:       # x is greater than the waiting item
        j = stack.pop()
        answer[j] = x                          # (or i - j for "days until", or a width for a histogram)
    stack.append(i)
```

Store **indices** on the stack when you need distances or widths, **values** when you only need the value.

## How to spot this topic

* Every element needs **the nearest element on its left or right that is bigger or smaller**.
* Words to look for: **"next greater element"**, **"days until a warmer temperature"**, **"largest rectangle"**, **"fleets"**, **"span"**.
* Quick test: *if I keep a stack of "unanswered" elements, does each new element answer several of them at once?* If yes, it's this topic.

**Not this topic if:** the brackets or nesting matter (→ Topic 1), or you evaluate arithmetic (→ Topic 3).

## Why it's O(n)

Each element is pushed once and popped at most once. The inner `while` loop looks like it could be `O(n²)`, but the total number of pops over the whole run is at most `n`.

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 5 | Next Greater Element I | Build a map `value → next greater` with the stack, then look up each query |
| 6 | Daily Temperatures | Same stack of indices; the answer for a popped day is `i - j` |
| 7 | Car Fleet | Sort by position (closest to the target first); a car that arrives later than the fleet ahead joins it |
| 8 | Largest Rectangle in Histogram | Increasing stack of indices; when a bar is popped, its width runs from the new top to `i` |
| E1 (extra) | Next Greater Element II | Circular array: loop `2n` times using `i % n` |
