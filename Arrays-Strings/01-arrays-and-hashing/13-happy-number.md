# 202. Happy Number

**LC 202** · **Source:** LC150 + NC150 · **Difficulty:** Easy · **Priority:** Stretch · **Pattern:** Hash set cycle detection

---

## 1. Intuition

Repeatedly replacing `n` with the sum of the squares of its digits either lands on `1`, or it starts
repeating a loop of numbers forever (`4 → 16 → 37 → ... → 4`). A `seen` set catches that loop: if a number
ever comes back, we're going in circles and will never reach `1`.

* `while n != 1 and n not in seen` keeps going until we hit `1` (happy) or repeat a number (unhappy loop).
* `seen.add(n)` records the number *before* transforming it, so the next repeat is caught.
* `n = sum(int(digit) ** 2 for digit in str(n))` is the transform: turn `n` into digits via `str(n)`, square each, and sum them.
* `return n == 1` — the loop can only end one of two ways, so checking `n == 1` at the end tells you which one happened.

**Recall:** keep transforming `n` by summing squared digits; stop and return `False` the moment a number repeats, `True` if you reach `1`.

---

## 2. Approach

* **Idea:** simulate the transformation, using a `seen` set to detect a repeat instead of running forever.
* **Data structure / pointers:** `seen` is the set of every value `n` has taken so far. `n` itself is updated each iteration.
* **Invariant:** at the top of each loop iteration, `n` has never appeared in `seen` before (otherwise the loop would already have stopped), and `seen` holds every value seen so far except the current `n`.
* **Edge cases:**
  * `n = 1` → the `while` condition is false immediately, so it returns `True` without looping.
  * Single-digit unhappy numbers, like `n = 2` → still caught, since `2`'s chain eventually revisits `4`.
  * Numbers that take many steps before repeating are still bounded: no path grows without limit, because any number with more than 3 digits produces a smaller sum of squared digits than itself, so `n` shrinks into a small range quickly.

---

## 3. Code

```python
class Solution:

    def isHappy(self, n: int) -> bool:
        seen = set()

        while n != 1 and n not in seen:
            seen.add(n)
            # Sum of squared digits
            n = sum(int(digit) ** 2 for digit in str(n))

        return n == 1


if __name__ == "__main__":
    solution = Solution()
    assert solution.isHappy(19) is True
    assert solution.isHappy(2) is False
    assert solution.isHappy(1) is True
    assert solution.isHappy(7) is True
    print("All tests passed")
```

### Alternative: O(1) space with digit math (no string conversion)

```python
def sumOfSquares(n: int) -> int:
    total = 0
    while n > 0:
        digit = n % 10
        total += digit * digit
        n //= 10
    return total
```

### Alternative: Floyd's cycle detection (fast & slow pointers)

Same idea as detecting a cycle in a linked list: `slow` moves one step at a time, `fast` moves two. If they
ever meet before `fast` (or `slow`) reaches `1`, there's a cycle. This drops space from `O(log n)` to
`O(1)`, at the cost of computing the transform up to twice as often.

---

## 4. Dry Run

`n = 19`

| Step | `n` before | Squared-digit sum | `n` after | `seen` after |
| --- | --- | --- | --- | --- |
| **1** | `19` | `1² + 9² = 82` | `82` | `{19}` |
| **2** | `82` | `8² + 2² = 68` | `68` | `{19, 82}` |
| **3** | `68` | `6² + 8² = 100` | `100` | `{19, 82, 68}` |
| **4** | `100` | `1² + 0² + 0² = 1` | `1` | `{19, 82, 68, 100}` |

`n == 1` now, so the loop stops and returns `True`.

---

## 5. Complexity

* **Time:** `O(log n)` — for a starting value of size `n`, the number of digits is `O(log n)`, and each transform sums that many squared digits. In practice `n` shrinks to at most 3 digits after the first step, so the whole chain runs in very few iterations before it hits `1` or repeats.
* **Space:** `O(log n)` — `seen` stores the distinct values visited, which is small in practice for the same reason.

---

## 6. Recall (30 seconds)

* **Transform:** `n = sum of (each digit)²`, computed via `str(n)`.
* **Stop condition:** `n == 1` (happy) or `n` repeats in `seen` (stuck in a cycle, unhappy).
* **O(1)-space alternative:** Floyd's fast & slow pointers detect the same cycle without a set.
