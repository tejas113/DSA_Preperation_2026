# 150. Evaluate Reverse Polish Notation

**LC 150** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Operand stack (pop two, apply, push)

---

## 1. Intuition

In Reverse Polish Notation the operator comes **after** its two numbers: `["4", "13", "5", "/", "+"]` means `4 + (13 / 5)`. So read left to right, keep numbers on a stack, and when an operator shows up, the two numbers it needs are the top two on the stack. Replace them with the result.

* `stack` holds **operands** (ints) that are waiting for an operator. The top, `stack[-1]`, is the most recent number or result.
* `stack.append(int(token))` in the `else` branch pushes every number, including negatives like `"-11"`.
* For `-` and `/`, order matters. The first pop is the **right** operand and the second pop is the **left** one: `b, a = stack.pop(), stack.pop()`, then `a - b` or `a / b`.
* For `+` and `*`, order doesn't matter, so `stack.pop() + stack.pop()` is fine.
* `int(a / b)` truncates toward zero, which is what this problem wants. Python's `a // b` rounds down instead, which gives the wrong answer for negative results (`10 // -3` is `-4`, but the answer must be `-3`).
* The result goes back on the stack with `stack.append(...)`, so later operators can use it. At the end, one number is left: `stack[0]`.

**Recall:** push numbers; on an operator pop `b` then `a`, push `a op b`; divide with `int(a / b)`; the answer is `stack[0]`.

## 2. Approach

* **Idea:** Scan `tokens` once. Push numbers. For each operator, pop two operands, apply it, and push the result.
* **Data structure / pointers:** `stack` is a plain list of ints (top is `stack[-1]`). `token` is the current string. `b` is the right operand (popped first) and `a` is the left operand (popped second).
* **Invariant:** at every step, `stack` holds the values of all the sub-expressions finished so far that haven't been used by an operator yet. After the last token, exactly one value remains.
* **Edge cases:**
  * **Stack empty or short when an operator arrives:** this would crash on `pop()`. The problem guarantees the expression is valid, so every operator always finds two operands on the stack and the code has no guard.
  * **Single token** (`["18"]`): no operator runs, `18` is pushed, and `stack[0]` is `18`.
  * **Negative numbers** (`"-11"`): they go to the `else` branch, because only the exact strings `"+"`, `"-"`, `"*"`, `"/"` are operators. `int("-11")` is `-11`.
  * **Division truncates toward zero:** `int(-7 / 2)` is `-3` (not `-4`) and `int(6 / -132)` is `0`.
  * **Operand order for `-` and `/`:** `a - b` and `a / b` use the second pop as `a`, so `["3", "5", "-"]` is `-2`, not `2`.

## 3. Code

```python
class Solution:

    def evalRPN(self, tokens: list[str]) -> int:
        stack = []

        for token in tokens:
            if token == "+":
                stack.append(stack.pop() + stack.pop())
            elif token == "-":
                b, a = stack.pop(), stack.pop()
                stack.append(a - b)
            elif token == "*":
                stack.append(stack.pop() * stack.pop())
            elif token == "/":
                b, a = stack.pop(), stack.pop()
                stack.append(int(a / b))  # `int(a / b)` truncates towards zero
            else:
                stack.append(int(token))

        return stack[0]


if __name__ == "__main__":
    solution = Solution()
    assert solution.evalRPN(["2", "1", "+", "3", "*"]) == 9
    assert solution.evalRPN(["4", "13", "5", "/", "+"]) == 6
    assert solution.evalRPN(
        ["10", "6", "9", "3", "+", "-11", "*", "/", "*", "17", "+", "5", "+"]
    ) == 22
    assert solution.evalRPN(["18"]) == 18
    assert solution.evalRPN(["3", "5", "-"]) == -2
    assert solution.evalRPN(["7", "-2", "/"]) == -3
    assert solution.evalRPN(["10", "-3", "/"]) == -3
    assert solution.evalRPN(["-7", "2", "/"]) == -3
    print("All tests passed")
```

## 4. Dry Run

Input: `tokens = ["4", "13", "5", "/", "+"]`

| Step | `token` | What happens | `stack` after |
|---|---|---|---|
| 1 | `"4"` | Number, push | `[4]` |
| 2 | `"13"` | Number, push | `[4, 13]` |
| 3 | `"5"` | Number, push | `[4, 13, 5]` |
| 4 | `"/"` | `b = 5`, `a = 13`, push `int(13 / 5) = 2` | `[4, 2]` |
| 5 | `"+"` | Pop `2` and `4`, push `2 + 4 = 6` | `[6]` |

Result: `stack[0]` = `6`

## 5. Complexity

* **Time:** O(n), because the loop visits each token once, and each push, pop and arithmetic step is O(1).
* **Space:** O(n), because `stack` can hold up to about n/2 numbers at once (when all the numbers come before the operators).

## 6. Recall (30 seconds)

* Numbers go on `stack`; an operator pops two, and the **first pop is `b`, the second is `a`**, so compute `a op b`.
* Divide with `int(a / b)` to truncate toward zero. Never use `//` here.
* Push the result back; the answer is `stack[0]`.
