# 12. Integer to Roman

**LC 12** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Greedy, largest value first

---

## 1. Intuition

This is the inverse of Roman to Integer ([[63-roman-to-integer]]). Instead of parsing symbols, greedily peel
off the largest possible value at every step — including the six subtractive forms (`CM`, `CD`, `XC`, `XL`,
`IX`, `IV`) treated as first-class entries in the value table, not as a special case to detect separately.
Because the table is sorted largest to smallest, always taking as many of the current value as fit is
guaranteed to build the correct numeral.

* `value_map` lists every symbol (including subtractive pairs) from largest value to smallest.
* `count = num // val` — how many times the current value fits into what's left of `num`.
* `if count: roman.append(symbol * count); num %= val` — append that many copies of the symbol, then remove that amount from `num` in one step via modulo, rather than subtracting in a loop.
* `if num == 0: break` — stops as soon as nothing is left to convert, avoiding wasted iterations through the smaller values.

**Recall:** walk a value table from largest to smallest (including the 6 subtractive pairs as entries); at each step, append `symbol * (num // val)` and reduce `num` with `%=`.

---

## 2. Approach

* **Idea:** treating the subtractive forms as ordinary entries in a sorted value table (rather than special-casing them) turns the whole conversion into one uniform greedy loop.
* **Data structure / pointers:** `value_map` (fixed value/symbol pairs, largest to smallest); `roman` (list of string chunks, joined at the end).
* **Invariant:** after processing each entry in `value_map`, `num` holds exactly what's left to convert using strictly smaller values than the one just processed — greedy correctness follows from the table's largest-to-smallest order.
* **Edge cases:**
  * Maximum constraint value (`3999`) → produces `"MMMCMXCIX"`, using every category of symbol at once.
  * A round power-of-ten value (`1000`) → the very first entry consumes the whole number (`count = 1`), and the loop's `if num == 0: break` ends things immediately.
  * A value needing multiple subtractive forms (`444` → `"CDXLIV"`) → `CD`, `XL`, and `IV` are each picked up as their own table entries, no special detection logic required.
  * `count` can be greater than `1` for the non-subtractive entries (e.g., `3000` → `"MMM"`, `count = 3`), which `symbol * count` handles directly.

---

## 3. Code

```python
class Solution:

    def intToRoman(self, num: int) -> str:
        value_map = [
            (1000, "M"),
            (900, "CM"),
            (500, "D"),
            (400, "CD"),
            (100, "C"),
            (90, "XC"),
            (50, "L"),
            (40, "XL"),
            (10, "X"),
            (9, "IX"),
            (5, "V"),
            (4, "IV"),
            (1, "I"),
        ]

        roman = []
        for val, symbol in value_map:
            if num == 0:
                break

            count = num // val
            if count:
                roman.append(symbol * count)
                num %= val

        return "".join(roman)


if __name__ == "__main__":
    solution = Solution()
    assert solution.intToRoman(1994) == "MCMXCIV"
    assert solution.intToRoman(3999) == "MMMCMXCIX"
    assert solution.intToRoman(1000) == "M"
    assert solution.intToRoman(444) == "CDXLIV"
    print("All tests passed")
```

### Alternative: hardcoded place-value lookup tables

Since `num <= 3999`, each digit (thousands, hundreds, tens, ones) can be looked up directly in its own
precomputed table of 0–9 (or 0–3 for thousands) Roman representations, avoiding the loop entirely.

```python
class SolutionHardcode:

    def intToRoman(self, num: int) -> str:
        thousands = ["", "M", "MM", "MMM"]
        hundreds = ["", "C", "CC", "CCC", "CD", "D", "DC", "DCC", "DCCC", "CM"]
        tens = ["", "X", "XX", "XXX", "XL", "L", "LX", "LXX", "LXXX", "XC"]
        ones = ["", "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX"]

        return (
            thousands[num // 1000]
            + hundreds[(num % 1000) // 100]
            + tens[(num % 100) // 10]
            + ones[num % 10]
        )


if __name__ == "__main__":
    solution = SolutionHardcode()
    assert solution.intToRoman(1994) == "MCMXCIV"
    assert solution.intToRoman(3999) == "MMMCMXCIX"
    print("All tests passed")
```

---

## 4. Dry Run

`num = 1994`

| `val` | `symbol` | `count = num // val` | Appended | `num` after |
| --- | --- | --- | --- | --- |
| `1000` | `"M"` | `1` | `"M"` | `994` |
| `900` | `"CM"` | `1` | `"CM"` | `94` |
| `500, 400, 100` | — | `0` each | (nothing) | `94` |
| `90` | `"XC"` | `1` | `"XC"` | `4` |
| `50, 40, 10, 9, 5` | — | `0` each | (nothing) | `4` |
| `4` | `"IV"` | `1` | `"IV"` | **`0`** |

Loop breaks (`num == 0`). **Return:** `"MCMXCIV"`

---

## 5. Complexity

* **Time:** `O(1)` — `value_map` has a fixed 13 entries, so the loop runs at most 13 times regardless of `num` (bounded at `3999`).
* **Space:** `O(1)` — the result string is at most 15 characters (e.g., `3888 → "MMMDCCCLXXXVIII"`).

---

## 6. Recall (30 seconds)

* **Table includes subtractive pairs directly:** `900: "CM"`, `400: "CD"`, `90: "XC"`, `40: "XL"`, `9: "IX"`, `4: "IV"` sit in the table alongside the plain symbols — no special-case detection needed.
* **One formula per entry:** `symbol * (num // val)`, then `num %= val`.
* **Inverse problem:** Roman to Integer ([[63-roman-to-integer]]) does the opposite by comparing each symbol to its neighbor.
