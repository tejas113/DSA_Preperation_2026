# 735. Asteroid Collision

**LC 735** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Stack of survivors (new item fights the top until it survives or dies)

---

## 1. Intuition

Positive numbers fly right, negative numbers fly left, and the size is the absolute value. A collision can only happen when a right-mover is **already on the stack** and a left-mover **arrives behind it**. The newcomer fights the top of the stack, one asteroid at a time, until it wins, loses or ties.

* `stack` holds the **surviving asteroids** (signed ints), in the order they appear. The top, `stack[-1]`, is the asteroid the newcomer meets first.
* `while stack and a < 0 and stack[-1] > 0` is the only collision case: `a` goes left, the top goes right.
* `diff = a + stack[-1]` compares sizes in one number. Negative means `a` is bigger, positive means the top is bigger, and zero is a tie.
* `diff < 0`: `stack.pop()` removes the smaller top, and the loop runs again so `a` can hit the next one.
* `diff > 0`: `break`, because `a` is destroyed and must not be pushed.
* `diff == 0`: `stack.pop()` then `break`, because both are destroyed.
* The `else:` on the `while` runs only when the loop ended **without** a `break`, which means `a` survived, so `stack.append(a)`.

**Recall:** a left-mover fights right-movers on top of the stack; pop the smaller ones, stop if it dies, push it only if it survives.

## 2. Approach

* **Idea:** For each asteroid `a`, let it collide with the top of the stack while a collision is possible. If it survives, push it.
* **Data structure / pointers:** `stack` is a plain list of surviving signed ints (top is `stack[-1]`). `a` is the current asteroid. `diff` is `a + stack[-1]`, which tells who is bigger.
* **Invariant:** `stack` never contains a collision waiting to happen. It looks like some left-movers (negatives) followed by some right-movers (positives), because a negative on top of a positive would already have collided.
* **Edge cases:**
  * **Stack empty when `a` arrives or after pops** (`while stack and ...` is false): there is nothing to hit, so the loop ends without `break` and `a` is pushed.
  * **Left-movers first** (`[-2, -1, 1, 2]`): nothing is to their left to hit, and later right-movers move away from them, so all survive.
  * **Equal sizes** (`[8, -8]`): `diff == 0`, so pop `8` and `break`. Neither is pushed, and the result is `[]`.
  * **Chain** (`[10, 2, -5]`): `-5` destroys `2`, then dies to `10`, and the result is `[10]`.
  * **Same direction** (`[5, 10]` or `[-5, -10]`): no collision, so both are pushed.

## 3. Code

```python
class Solution:

    def asteroidCollision(self, asteroids: list[int]) -> list[int]:
        stack = []

        for a in asteroids:
            # Collision happens ONLY if stack top moves right (> 0) and current moves left (< 0)
            while stack and a < 0 and stack[-1] > 0:
                diff = a + stack[-1]
                if diff < 0:
                    # Top asteroid explodes; current asteroid `a` continues moving left
                    stack.pop()
                elif diff > 0:
                    # Current asteroid `a` explodes
                    break
                else:
                    # Both asteroids explode
                    stack.pop()
                    break
            else:
                # Executes if while loop didn't hit a `break` (i.e., `a` survived)
                stack.append(a)

        return stack


if __name__ == "__main__":
    solution = Solution()
    assert solution.asteroidCollision([5, 10, -5]) == [5, 10]
    assert solution.asteroidCollision([8, -8]) == []
    assert solution.asteroidCollision([10, 2, -5]) == [10]
    assert solution.asteroidCollision([3, 5, -6, 2, -1, 4]) == [-6, 2, 4]
    assert solution.asteroidCollision([-2, -1, 1, 2]) == [-2, -1, 1, 2]
    assert solution.asteroidCollision([-2, -2, 1, -2]) == [-2, -2, -2]
    assert solution.asteroidCollision([1]) == [1]
    print("All tests passed")
```

## 4. Dry Run

Input: `asteroids = [3, 5, -6, 2, -1, 4]`

| Step | `a` | What happens | `stack` after |
|---|---|---|---|
| 1 | `3` | Not a left-mover, push | `[3]` |
| 2 | `5` | Not a left-mover, push | `[3, 5]` |
| 3 | `-6` | Meets `5`: `diff = -1 < 0`, pop `5` | `[3]` |
| 3 (cont.) | `-6` | Meets `3`: `diff = -3 < 0`, pop `3` | `[]` |
| 3 (cont.) | `-6` | Stack empty, loop ends, push | `[-6]` |
| 4 | `2` | Not a left-mover, push | `[-6, 2]` |
| 5 | `-1` | Meets `2`: `diff = 1 > 0`, `break` (`-1` dies) | `[-6, 2]` |
| 6 | `4` | Not a left-mover, push | `[-6, 2, 4]` |

Result: `[-6, 2, 4]`

## 5. Complexity

* **Time:** O(n), because each asteroid is pushed at most once and popped at most once, so the `while` loop does at most n pops across the whole run.
* **Space:** O(n), because `stack` can hold every asteroid when none collide.

## 6. Recall (30 seconds)

* Only a left-mover (`a < 0`) meeting a right-mover on top (`stack[-1] > 0`) collides.
* `diff = a + stack[-1]`: negative pops the top and keeps going, positive breaks (`a` dies), zero pops and breaks.
* The `while ... else` pushes `a` only when no `break` happened, which includes an empty stack.
