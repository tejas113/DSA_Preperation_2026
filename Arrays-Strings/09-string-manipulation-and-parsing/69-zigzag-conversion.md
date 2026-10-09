# 6. Zigzag Conversion

**LC 6** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Stretch · **Pattern:** Simulate the bounce, one row-bucket per row

---

## 1. Intuition

Rather than deriving an index formula for where each character lands in the final zigzag pattern, just
simulate the physical motion directly: walk down the rows one character at a time, and the instant you hit
the top or bottom row, reverse direction. Each row gets its own string bucket to collect characters in the
order it visits them; concatenating the buckets at the end reproduces the zigzag reading order.

* `rows = [""] * numRows` — one growing string per row.
* `current_row` tracks which row the current character belongs to; `step` (`+1` or `-1`) is the current direction of travel.
* `rows[current_row] += char` — always append first, *then* decide whether to bounce.
* `if current_row == numRows - 1: step = -1` and `elif current_row == 0: step = 1` — flips direction only at the two boundary rows; anywhere in between, the direction stays whatever it already was.
* `current_row += step` — moves to the next row for the *next* character, after the bounce check.

**Recall:** one bucket per row; append the character, then bounce direction at row `0` or `numRows - 1`; join all buckets at the end.

---

## 2. Approach

* **Idea:** the zigzag pattern is exactly the path a single point traces bouncing between the top and bottom row — simulating that path directly avoids needing to derive a closed-form index formula.
* **Data structure / pointers:** `rows` (one string bucket per row), `current_row` (current position), `step` (current direction, `+1` or `-1`).
* **Invariant:** at every point, `rows[r]` holds exactly the characters that have visited row `r` so far, in the order the zigzag path passed through them — which is also the correct final reading order for that row.
* **Edge cases:**
  * `numRows == 1` → there's only one row, so the string is unchanged; guarded explicitly, since `numRows - 1 == 0` would otherwise make the top and bottom boundary checks both trigger on every single character.
  * `numRows >= len(s)` → the string is too short to ever reach a full column, so each character goes straight down without bouncing, meaning the output equals the input; guarded explicitly to skip unnecessary work.
  * Single-character string → caught by the `numRows >= len(s)` guard, returned as-is.
  * `numRows == 2` → the pattern degenerates to alternating rows, bouncing every single character; still handled correctly by the general bounce logic.

---

## 3. Code

```python
class Solution:

    def convert(self, s: str, numRows: int) -> str:
        # Edge cases: 1 row or string shorter than numRows needs no rearrangement
        if numRows == 1 or numRows >= len(s):
            return s

        rows = [""] * numRows
        current_row = 0
        step = 1

        for char in s:
            rows[current_row] += char

            # Bounce direction at top and bottom boundaries
            if current_row == numRows - 1:
                step = -1
            elif current_row == 0:
                step = 1

            current_row += step

        return "".join(rows)


if __name__ == "__main__":
    solution = Solution()
    assert solution.convert("PAYPALISHIRING", 3) == "PAHNAPLSIIGYIR"
    assert solution.convert("PAYPALISHIRING", 4) == "PINALSIGYAHRPI"
    assert solution.convert("A", 1) == "A"
    assert solution.convert("AB", 5) == "AB"
    print("All tests passed")
```

---

## 4. Dry Run

`s = "PAYPALISHIRING"`, `numRows = 3`

| Char | `current_row` used | `step` after bounce check | `rows` after append | Next `current_row` |
| --- | --- | --- | --- | --- |
| `'P'` | `0` | `+1` | `["P", "", ""]` | `1` |
| `'A'` | `1` | `+1` | `["P", "A", ""]` | `2` |
| `'Y'` | `2` | **`-1`** (hit bottom) | `["P", "A", "Y"]` | `1` |
| `'P'` | `1` | `-1` | `["P", "AP", "Y"]` | `0` |
| `'A'` | `0` | **`+1`** (hit top) | `["PA", "AP", "Y"]` | `1` |
| `'L'` | `1` | `+1` | `["PA", "APL", "Y"]` | `2` |
| `'I'` | `2` | **`-1`** (hit bottom) | `["PA", "APL", "YI"]` | `1` |

*(pattern continues bouncing through the rest of the string)*

**Final buckets:** `rows[0] = "PAHN"`, `rows[1] = "APLSIIG"`, `rows[2] = "YIR"`

**Return:** `"PAHNAPLSIIGYIR"`

---

## 5. Complexity

* **Time:** `O(n)` — one pass through `s`, `O(1)` work per character.
* **Space:** `O(n)` — `rows` collectively holds all `n` characters across its buckets.

---

## 6. Recall (30 seconds)

* **Simulate, don't derive a formula:** append to the current row, then bounce at the top/bottom boundary.
* **Append before bounce-check:** the character always lands in the row it's currently pointed at, before direction is reconsidered for the *next* character.
* **Guard `numRows == 1` explicitly:** without it, the top/bottom boundary checks would both fire on the same row every time.
