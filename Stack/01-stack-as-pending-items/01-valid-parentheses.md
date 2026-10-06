# 20. Valid Parentheses

**LC 20** · **Source:** LC150 + NC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Stack of pending open brackets (LIFO matching)

---

## 1. Intuition

Every open bracket is a promise: "someone must close me." The most recent unclosed bracket is always the next one that has to be closed, so a stack fits. Push each opener, and when a closer arrives, it must match the bracket on top.

* `stack` holds the **open brackets** (characters) still waiting for their closer. The top, `stack[-1]`, is the most recent one.
* `close_to_open` maps each closer to the opener it needs, so the check `stack[-1] == close_to_open[char]` is one lookup.
* `stack.pop()` runs only when the top matches, which means that pair is finished.
* `return False` inside the loop catches a wrong type (`"(]"`) or a closer with nothing open (`")"`).
* `return len(stack) == 0` catches leftover openers (`"((("`).

**Recall:** push openers, pop on a matching closer, valid only if the stack ends empty.

## 2. Approach

* **Idea:** Scan left to right. Push openers. For a closer, the top of the stack must be its matching opener, otherwise the string is invalid.
* **Data structure / pointers:** `stack` is a plain list of open-bracket characters (top is `stack[-1]`). `close_to_open` is a dict from closer to opener. `char` is the current character.
* **Invariant:** at every step, `stack` holds exactly the open brackets seen so far that are not yet closed, in the order they were opened. Everything already popped was matched correctly.
* **Edge cases:**
  * **Stack empty when a closer arrives** (`")("`): the `if stack and ...` check fails, so return `False`.
  * **Leftover openers** (`"((("`): the loop ends without error, but `len(stack) == 3`, so return `False`.
  * **Empty string** (`""`): nothing is pushed, the stack is empty, return `True`.
  * **Wrong type on top** (`"([)]"`): the top is `'['` but `')'` needs `'('`, so return `False`.
  * **Optional:** an odd-length string can never be valid, so a `len(s) % 2` check at the start could return `False` early. The code below does not do this.

## 3. Code

```python
class Solution:

    def isValid(self, s: str) -> bool:
        stack = []
        close_to_open = {")": "(", "}": "{", "]": "["}

        for char in s:
            if char in close_to_open:
                # If stack is non-empty and top element matches corresponding open bracket
                if stack and stack[-1] == close_to_open[char]:
                    stack.pop()
                else:
                    return False
            else:
                # Character is an opening bracket
                stack.append(char)

        # Valid only if all brackets were properly matched and closed
        return len(stack) == 0


if __name__ == "__main__":
    solution = Solution()
    assert solution.isValid("()") is True
    assert solution.isValid("()[]{}") is True
    assert solution.isValid("(]") is False
    assert solution.isValid("([])") is True
    assert solution.isValid("([)]") is False
    assert solution.isValid(")(") is False
    assert solution.isValid("(((") is False
    assert solution.isValid("") is True
    print("All tests passed")
```

## 4. Dry Run

Input: `s = "([)]"`

| Step | `char` | Action | `stack` after | Result |
|---|---|---|---|---|
| 1 | `'('` | Opener, push | `['(']` | - |
| 2 | `'['` | Opener, push | `['(', '[']` | - |
| 3 | `')'` | Closer needs `'('`, but top is `'['` | `['(', '[']` | return `False` |

## 5. Complexity

* **Time:** O(n), one pass over `s`, and each push, pop and dict lookup is O(1).
* **Space:** O(n), because `stack` grows to `n` when `s` is all openers like `"((((("`.

## 6. Recall (30 seconds)

* Openers go onto `stack`. A closer must match `stack[-1]` via `close_to_open`.
* Closer with an empty `stack`, or a mismatch, means `return False` right away.
* At the end, the answer is `len(stack) == 0`, so leftover openers fail.
