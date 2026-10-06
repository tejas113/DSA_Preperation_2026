# 394. Decode String

**LC 394** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Stack of pending pieces; on `]`, unwind and expand

---

## 1. Intuition

Think of `3[a2[c]]` as a set of nested boxes. You can't expand an outer box until the boxes inside it are done. So keep everything you've read on a stack, and the moment you see a `]`, the innermost unfinished box is sitting on top: unwind it, repeat it, and put the result back as one piece.

* `stack` holds single characters (digits, letters, `'['`) plus already-expanded strings like `"cc"`. The top is the most recent unfinished piece.
* `if s[i] != "]": stack.append(s[i])` pushes everything until a closer shows up.
* `substr = stack.pop() + substr` pops back to the matching `'['`. The new character goes on the front, because popping reads the text right to left.
* `stack.pop()` after that loop throws away the `'['`.
* `k = stack.pop() + k` collects the digits under the `'['`, so `100[a]` becomes `100`.
* `stack.append(int(k) * substr)` puts the expanded text back as one piece, so the outer box can use it later.
* `"".join(stack)` at the end glues together the finished pieces.

**Recall:** push until `]`, then pop the text, pop `[`, pop the digits, push `k * text` back.

## 2. Approach

* **Idea:** Push every character except `]`. On `]`, unwind the innermost box and push its expansion back as a single piece.
* **Data structure / pointers:** `stack` is a plain list of strings (characters or expanded pieces; top is `stack[-1]`). `substr` is the text being unwound. `k` is the repeat count, built as a digit string and then turned into `int(k)`.
* **Invariant:** between `]` events, `stack` holds the decoded-so-far text in order, with any still-open `digits + '['` markers sitting in it. After each `]`, the innermost box is gone and replaced by its finished text.
* **Edge cases:**
  * **Stack empty when popping:** the text loop is guarded by `while stack and ...`, and for valid input a `'['` is always found, so `stack.pop()` for the bracket is safe. The digit loop is guarded the same way, so it stops cleanly when the stack runs out. In `"3[a]"`, popping the digits empties the stack, and that is fine.
  * **Multi-digit counts** (`"100[a]"`): the digit loop keeps popping, so `k` is `"100"`.
  * **Sequential boxes** (`"2[a]3[b]"`): `"aa"` stays on the stack while `3[b]` becomes `"bbb"`, and the final join gives `"aabbb"`.
  * **Deep nesting** (`"2[a2[b2[c]]]"`): the innermost `]` is handled first, and each result is pushed back for the next level.
  * **Plain letters, no brackets** (`"abc"`): everything is pushed and the join returns `"abc"`.
  * **Empty string** (`""`): the join of an empty stack is `""`.

## 3. Code

```python
class Solution:

    def decodeString(self, s: str) -> str:
        stack = []

        for i in range(len(s)):
            if s[i] != "]":
                stack.append(s[i])
            else:
                # 1. Pop characters until reaching the opening bracket '['
                substr = ""
                while stack and stack[-1] != "[":
                    substr = stack.pop() + substr

                # 2. Pop the opening bracket '[' itself
                stack.pop()

                # 3. Pop the digits to build the repetition count `k`
                k = ""
                while stack and stack[-1].isdigit():
                    k = stack.pop() + k

                # 4. Multiply the substring and push it back onto the stack
                stack.append(int(k) * substr)

        # 5. Join all decoded segments in the stack to form the result
        return "".join(stack)


if __name__ == "__main__":
    solution = Solution()
    assert solution.decodeString("3[a]2[bc]") == "aaabcbc"
    assert solution.decodeString("3[a2[c]]") == "accaccacc"
    assert solution.decodeString("2[abc]3[cd]ef") == "abcabccdcdcdef"
    assert solution.decodeString("abc") == "abc"
    assert solution.decodeString("") == ""
    assert solution.decodeString("2[a]3[b]") == "aabbb"
    assert solution.decodeString("2[a2[b2[c]]]") == "abccbccabccbcc"
    assert solution.decodeString("10[a]") == "a" * 10
    print("All tests passed")
```

## 4. Dry Run

Input: `s = "3[a2[c]]"`

| Step | Trigger | Popped `substr` | Popped `k` | `stack` after |
|---|---|---|---|---|
| 1 | push `'3'` | - | - | `['3']` |
| 2 | push `'['` | - | - | `['3', '[']` |
| 3 | push `'a'` | - | - | `['3', '[', 'a']` |
| 4 | push `'2'` | - | - | `['3', '[', 'a', '2']` |
| 5 | push `'['` | - | - | `['3', '[', 'a', '2', '[']` |
| 6 | push `'c'` | - | - | `['3', '[', 'a', '2', '[', 'c']` |
| 7 | `']'`: unwind, push `2 * "c"` | `"c"` | `2` | `['3', '[', 'a', 'cc']` |
| 8 | `']'`: unwind, push `3 * "acc"` | `"acc"` | `3` | `['accaccacc']` |

End of string: `"".join(stack)` = `"accaccacc"`

## 5. Complexity

* **Time:** about O(L × depth), where L is the length of the decoded output and depth is the nesting level, because each level re-pops and re-repeats the text its inner levels already built. Building `substr` with `pop() + substr` copies the string on every prepend, so one long segment costs more than linear, but the problem caps the input at 30 characters and the output at 10^5, so it is fast in practice. (Say "proportional to the output size" in an interview.)
* **Space:** O(L), because `stack` holds the decoded text built so far, and `substr` and `k` are temporary.

## 6. Recall (30 seconds)

* Push every character except `]`. On `]`, pop the text up to `'['`, pop the `'['`, then pop the digits into `k`.
* Push `int(k) * substr` back as one piece, so outer boxes can use it.
* At the end, `"".join(stack)` is the answer.
