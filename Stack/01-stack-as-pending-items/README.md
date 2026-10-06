# Topic 1 — Stack as "Pending Items"

## The pattern

Push anything that is **still waiting** for something — an open bracket waiting for its closer, a partial string waiting for its repeat count, a path part waiting to be popped by `..`. When the thing it's waiting for arrives, pop it.

```python
stack = []
for ch in s:
    if ch in "([{":
        stack.append(ch)                       # waiting for its closer
    else:
        if not stack or not matches(stack.pop(), ch):
            return False                       # closer with nothing (or the wrong thing) waiting
return not stack                               # anything left on the stack was never closed
```

For nested structures (Decode String), push a **pair** — the string built so far and the repeat count — when you see `[`, and pop it back when you see `]`.

## How to spot this topic

* The input has **brackets, nesting, or things that cancel each other**, and the most recent unfinished item is the next one to resolve.
* Words to look for: **"valid parentheses"**, **"nested"**, **"decode"**, **"simplify path"**, **"collide"**, **"undo"**.
* Quick test: *when a closing thing arrives, does it always pair with the most recent open thing?* If yes, it's this topic.

**Not this topic if:** each element wants the **next bigger or smaller element** (→ Topic 2), or the input is an **arithmetic expression** (→ Topic 3).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 1 | Valid Parentheses | Push open brackets; each closer must match the top |
| 2 | Simplify Path | Split on `/`; push names, pop on `..`, skip `.` and empties |
| 3 | Decode String | Push `(string so far, repeat count)` on `[`; on `]` pop and repeat |
| 4 | Asteroid Collision | Push survivors; a new asteroid pops smaller ones going the opposite way |
