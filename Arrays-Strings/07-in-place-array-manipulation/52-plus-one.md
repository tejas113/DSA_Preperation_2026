# 66. Plus One

**LC 66** · **Source:** LC150 + NC150 · **Difficulty:** Easy · **Priority:** Stretch · **Pattern:** Carry propagation, walked from the least significant digit

---

## 1. Intuition

Adding `1` to a number only ever changes more than the last digit when there's a carry — and a carry only
keeps propagating through digits that are already `9`. So walk from the last digit backward: the first digit
that isn't a `9` just absorbs the `+1` and you're done; every `9` along the way rolls over to `0` and the
carry keeps moving left.

* `for i in range(n - 1, -1, -1)` walks from the least significant digit to the most significant.
* `if digits[i] < 9: digits[i] += 1; return digits` — no carry needed past this point, so return immediately.
* `digits[i] = 0` — a `9` rolls over to `0`, and the loop continues to carry the `+1` into the next digit left.
* If the loop finishes without ever returning, every digit was a `9` and is now `0` — the carry has nowhere left to go inside the array, so `[1] + digits` prepends the final carry digit.

**Recall:** walk from the last digit; the first non-`9` absorbs the `+1` and returns immediately; every `9` becomes `0` and the carry keeps moving; if it carries past the front, prepend `1`.

---

## 2. Approach

* **Idea:** simulate elementary-school addition, one digit at a time from the right, stopping as soon as the carry is absorbed.
* **Data structure / pointers:** `i` walks backward through `digits`; no extra storage needed except the loop variable.
* **Invariant:** every digit to the right of `i` (already processed) correctly reflects `digits + 1` for that portion, assuming the carry keeps propagating; the loop returns the instant that assumption is confirmed false (a digit `< 9` absorbs it).
* **Edge cases:**
  * Single digit, not `9` (`[5]`) → returns `[6]` immediately, `O(1)`.
  * Single digit `9` (`[9]`) → becomes `[0]`, loop ends, returns `[1, 0]`.
  * All digits `9` (`[9, 9, 9]`) → every digit becomes `0`, then `[1] + [0, 0, 0] = [1, 0, 0, 0]`.
  * Trailing `9`s followed by a non-`9` digit (`[4, 3, 9, 9]`) → only the trailing `9`s roll over; the first non-`9` digit encountered (from the right) absorbs the carry and the loop returns without ever reaching the front.

---

## 3. Code

```python
class Solution:

    def plusOne(self, digits: list[int]) -> list[int]:
        n = len(digits)

        # Traverse backwards from LSD to MSD
        for i in range(n - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                return digits
            digits[i] = 0

        # If all digits were 9 (e.g., [9, 9] -> [0, 0]), prepend 1
        return [1] + digits


if __name__ == "__main__":
    solution = Solution()
    assert solution.plusOne([1, 2, 9]) == [1, 3, 0]
    assert solution.plusOne([9, 9, 9]) == [1, 0, 0, 0]
    assert solution.plusOne([0]) == [1]
    assert solution.plusOne([9]) == [1, 0]
    assert solution.plusOne([4, 3, 9, 9]) == [4, 4, 0, 0]
    print("All tests passed")
```

---

## 4. Dry Run

**Case 1 — carry stops partway (`digits = [1, 2, 9]`):**

| `i` | `digits[i]` | Condition | Action | `digits` after |
| --- | --- | --- | --- | --- |
| `2` | `9` | `== 9` | set to `0`, continue | `[1, 2, 0]` |
| `1` | `2` | `< 9` | `+= 1`, **return** | `[1, 3, 0]` |

**Case 2 — carry propagates through everything (`digits = [9, 9, 9]`):**

| `i` | `digits[i]` | Condition | Action | `digits` after |
| --- | --- | --- | --- | --- |
| `2` | `9` | `== 9` | set to `0` | `[9, 9, 0]` |
| `1` | `9` | `== 9` | set to `0` | `[9, 0, 0]` |
| `0` | `9` | `== 9` | set to `0` | `[0, 0, 0]` |

Loop ends without returning → prepend `1` → **`[1, 0, 0, 0]`**

---

## 5. Complexity

* **Time:** `O(n)` worst case (all `9`s), but `O(1)` on average — most inputs don't have a long run of trailing `9`s, so the loop returns after very few steps.
* **Space:** `O(1)` in place, except the all-`9`s case, which allocates a new list one element longer (`[1] + digits`).

---

## 6. Recall (30 seconds)

* **Walk from the right, stop at the first non-`9`:** that digit absorbs the carry and you return immediately.
* **`9` rolls to `0` and keeps going:** the carry only propagates through consecutive `9`s.
* **Carry past the front:** if the loop finishes with no return, every digit was `9` — prepend `1` for the final overflow digit.
