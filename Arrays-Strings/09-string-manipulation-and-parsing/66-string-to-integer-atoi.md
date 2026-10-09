# 8. String to Integer (atoi)

**LC 8** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Sequential parsing phases, careful edge-case handling

---

## 1. Intuition

`atoi` isn't algorithmically hard — it's a careful simulation of four strict phases that must run *in order*,
each one stopping the moment its rule is violated: skip whitespace, read an optional sign, read digits, then
clamp the result to fit a 32-bit signed integer. Nothing later can "rescue" a string that already failed an
earlier phase — a non-digit right after the sign means zero digits are read, giving `0`.

* `while i < n and s[i] == " ": i += 1` — only *leading* whitespace is skipped; any space later (e.g., between digits) is never revisited.
* `if s[i] == "-": sign = -1 ... elif s[i] == "+": ...` — at most one sign character, read once, immediately after the whitespace.
* `while i < n and "0" <= s[i] <= "9": res = res * 10 + digit` — digits accumulate for as long as they're consecutive; the *first* non-digit (including another sign, like in `"0-1"`) stops this phase permanently.
* `res *= sign` then clamp against `INT_MIN`/`INT_MAX` — the sign is applied only once, at the very end, after all digits are collected as a positive number.

**Recall:** skip leading spaces → read one optional sign → read consecutive digits → apply sign → clamp to `[-2^31, 2^31 - 1]`.

---

## 2. Approach

* **Idea:** each phase has a strict stopping condition, and once a phase ends (by hitting a character that doesn't belong to it), the algorithm never goes back — this is what keeps the logic simple despite handling many edge cases.
* **Data structure / pointers:** `i` walks forward through `s`, `sign` and `res` are scalars built up phase by phase.
* **Invariant:** at the start of the digit-parsing phase, `i` points exactly at the first digit (or the first non-digit, meaning zero digits will be read) — whitespace and an optional sign have already been fully consumed.
* **Edge cases:**
  * No digits at all (`"words and 987"`) → the digit loop never executes even once (the very first character isn't a digit), returning `0` — the `987` later in the string is never reached, since parsing already stopped.
  * A sign appearing mid-digits (`"0-1"`) → the digit loop reads `'0'`, then stops at `'-'` (not a digit), returning `0`, not `-1`.
  * Overflow (`"-91283472332"`) → the accumulated value before clamping exceeds `INT_MIN`, so the final clamp check returns `INT_MIN` exactly.
  * Only whitespace and a sign, no digits (`"   +"`) → the sign is read, then the digit loop finds nothing (`i` reaches the end of the string), leaving `res = 0`.

---

## 3. Code

```python
class Solution:

    def myAtoi(self, s: str) -> int:
        i = 0
        n = len(s)

        # Step 1: Skip leading whitespace
        while i < n and s[i] == " ":
            i += 1

        if i >= n:
            return 0

        # Step 2: Read optional sign
        sign = 1
        if s[i] == "-":
            sign = -1
            i += 1
        elif s[i] == "+":
            i += 1

        # Step 3: Parse digits
        res = 0
        INT_MIN, INT_MAX = -(2**31), 2**31 - 1

        while i < n and "0" <= s[i] <= "9":
            digit = ord(s[i]) - ord("0")
            res = res * 10 + digit
            i += 1

        # Step 4: Apply sign and clamp within 32-bit bounds
        res *= sign

        if res < INT_MIN:
            return INT_MIN
        if res > INT_MAX:
            return INT_MAX

        return res


if __name__ == "__main__":
    solution = Solution()
    assert solution.myAtoi("   -042") == -42
    assert solution.myAtoi("words and 987") == 0
    assert solution.myAtoi("0-1") == 0
    assert solution.myAtoi("-91283472332") == -2147483648
    assert solution.myAtoi("   +") == 0
    print("All tests passed")
```

---

## 4. Dry Run

`s = "   -042"` (three leading spaces, length `7` — corrected below)

> **Note:** the original dry run stated `n = 6`, but its own trace indexes up to `s[6]`, which only works if `n = 7`. I re-ran the code directly to confirm: the input that actually produces this trace is `"   -042"` with **three** leading spaces (length 7), not one or two. The final answer, `-42`, was already correct — only the stated length was off.

| Step | Index `i` | Character | Action | `res` / `sign` |
| --- | --- | --- | --- | --- |
| **Whitespace** | `0` → `1` → `2` | `' '`, `' '`, `' '` | skip each | — |
| **Sign** | `3` | `'-'` | `sign = -1`, `i = 4` | `sign = -1` |
| **Digit** | `4` | `'0'` | `res = 0*10 + 0` | `res = 0` |
| **Digit** | `5` | `'4'` | `res = 0*10 + 4` | `res = 4` |
| **Digit** | `6` | `'2'` | `res = 4*10 + 2` | `res = 42` |
| **Clamp & return** | `7` (end) | — | `res *= sign`; within bounds | **`-42`** |

---

## 5. Complexity

* **Time:** `O(n)` — a single pass through `s`.
* **Space:** `O(1)` — only scalar variables.

---

## 6. Recall (30 seconds)

* **Four strict phases, in order:** whitespace → sign → digits → clamp. Once a phase's stop condition is hit, it never resumes.
* **First non-digit ends parsing for good:** even a later digit sequence (like the `987` in `"words and 987"`) is unreachable once parsing has already stopped.
* **Clamp only at the very end:** the sign is applied to the fully-accumulated magnitude, then the result is clamped to `[-2^31, 2^31 - 1]`.
