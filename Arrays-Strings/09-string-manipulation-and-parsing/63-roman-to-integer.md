# 13. Roman to Integer

**LC 13** · **Source:** LC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Compare adjacent values, subtract when out of order

---

## 1. Intuition

Roman numerals normally read largest-to-smallest, adding as you go (`VI = 5 + 1 = 6`). The one exception is
when a smaller value comes *before* a bigger one (`IV`, `IX`, `XL`, ...), which signals subtraction instead.
So the whole problem reduces to one question per character: does the *next* character represent a bigger
value? If so, this one should be subtracted; otherwise, added.

* `roman_map` translates each symbol to its numeric value.
* `if i < n - 1 and roman_map[s[i]] < roman_map[s[i + 1]]` checks two things at once: is there a next character, and is it bigger than this one?
* When that's true, `total -= roman_map[s[i]]` — this character is the "smaller" half of a subtractive pair like `IV`.
* Otherwise, `total += roman_map[s[i]]` — either it's a normal additive numeral, or it's the last character (with no next value to compare against).

**Recall:** for each character, if the next one is bigger, subtract this one; otherwise add it.

---

## 2. Approach

* **Idea:** every valid Roman numeral is a mix of additive runs and exactly one-symbol-early subtractive pairs — comparing each character only to its immediate neighbor is enough to tell which case applies.
* **Data structure / pointers:** `roman_map` (fixed symbol → value lookup), `i` (the current character's index).
* **Invariant:** at each step, `total` correctly reflects the value of every character processed so far, whether added outright or subtracted as part of a pair.
* **Edge cases:**
  * Single character (`"D"`) → `i < n - 1` is `False` immediately, so it's simply added, returning `500`.
  * A pure subtractive pair (`"IV"`) → `i=0` subtracts `1` (since `I < V`), `i=1` adds `5` (last character, nothing to compare), net `4`.
  * A run with no subtraction anywhere (`"III"`) → every comparison is `curr >= next` (or there's no next), so it's pure addition.
  * The problem guarantees well-formed Roman numeral input, so no invalid symbol combinations need to be handled.

---

## 3. Code

```python
class Solution:

    def romanToInt(self, s: str) -> int:
        roman_map = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000,
        }

        total = 0
        n = len(s)

        for i in range(n):
            if i < n - 1 and roman_map[s[i]] < roman_map[s[i + 1]]:
                total -= roman_map[s[i]]
            else:
                total += roman_map[s[i]]

        return total


if __name__ == "__main__":
    solution = Solution()
    assert solution.romanToInt("MCMXCIV") == 1994
    assert solution.romanToInt("D") == 500
    assert solution.romanToInt("IV") == 4
    assert solution.romanToInt("III") == 3
    print("All tests passed")
```

### Alternative: right-to-left, tracking the previous (larger-side) value

Walks the string backward instead, comparing each value to the largest value seen so far from the right.
Same result, opposite direction of comparison.

```python
class SolutionRTL:

    def romanToInt(self, s: str) -> int:
        roman_map = {
            "I": 1,
            "V": 5,
            "X": 10,
            "L": 50,
            "C": 100,
            "D": 500,
            "M": 1000,
        }

        total = 0
        prev_value = 0

        for char in reversed(s):
            curr_value = roman_map[char]
            if curr_value < prev_value:
                total -= curr_value
            else:
                total += curr_value
                prev_value = curr_value

        return total


if __name__ == "__main__":
    solution = SolutionRTL()
    assert solution.romanToInt("MCMXCIV") == 1994
    assert solution.romanToInt("IV") == 4
    print("All tests passed")
```

---

## 4. Dry Run

`s = "MCMXCIV"`, `n = 7`

| `i` | `s[i]` (value) | `s[i+1]` (value) | `curr < next`? | Action | `total` after |
| --- | --- | --- | --- | --- | --- |
| `0` | `M` (`1000`) | `C` (`100`) | False | `+1000` | `1000` |
| `1` | `C` (`100`) | `M` (`1000`) | **True** | `-100` | `900` |
| `2` | `M` (`1000`) | `X` (`10`) | False | `+1000` | `1900` |
| `3` | `X` (`10`) | `C` (`100`) | **True** | `-10` | `1890` |
| `4` | `C` (`100`) | `I` (`1`) | False | `+100` | `1990` |
| `5` | `I` (`1`) | `V` (`5`) | **True** | `-1` | `1989` |
| `6` | `V` (`5`) | — (last char) | N/A | `+5` | **`1994`** |

**Return:** `1994`

---

## 5. Complexity

* **Time:** `O(n)` — one pass; `n <= 15` per the problem's constraints, so this is effectively `O(1)` in practice.
* **Space:** `O(1)` — `roman_map` is a fixed 7-entry dictionary regardless of input.

---

## 6. Recall (30 seconds)

* **Compare each character to its neighbor:** if `s[i] < s[i+1]` in value, subtract; otherwise add.
* **Subtraction only happens one symbol early:** `IV`, `IX`, `XL`, `XC`, `CD`, `CM` — never more than one place ahead.
* **Inverse problem — Integer to Roman (LC 12):** solved with a greedy pass over value/symbol pairs sorted largest to smallest, including the subtractive pairs (`900: "CM"`, `400: "CD"`, etc.) as their own entries.
