# 43. Multiply Strings

**LC 43** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Simulate grade-school long multiplication, digit by digit

---

## 1. Intuition

Numbers too big to fit in a native integer type still multiply the way you learned by hand: every digit of
`num1` multiplies every digit of `num2`, and each partial product lands at a *predictable* position in the
final result based on the two digits' positions — no need to track place value explicitly, just index math.

* The result of multiplying two numbers of length `m` and `n` can never exceed `m + n` digits, so `res = [0] * (m + n)` is always large enough.
* For digits at positions `i` (in `num1`) and `j` (in `num2`), their product lands split across two positions: `p2 = i + j + 1` (the ones digit of this partial product) and `p1 = i + j` (where any carry goes).
* `total = mul + res[p2]` adds the new partial product on top of whatever's already accumulated at that position — since multiple `(i, j)` pairs can contribute to the same `p2`.
* `res[p2] = total % 10` keeps the ones digit there; `res[p1] += total // 10` carries the rest one position to the left, added (not overwritten) since that position may already hold a partial sum.
* Leading zeros are stripped at the end, since `res` always has exactly `m + n` slots even when the true product has fewer digits.

**Recall:** for each digit pair `(i, j)`, the product's ones digit goes to `res[i+j+1]` and its carry accumulates into `res[i+j]`; strip leading zeros at the end.

---

## 2. Approach

* **Idea:** simulate the digit-by-digit multiplication you'd do on paper, using array positions to track place value instead of relying on a fixed-size integer type.
* **Data structure / pointers:** `res` (the result buffer, indexed by digit position); `i`, `j` walk `num1` and `num2` from right to left (least significant digit first).
* **Invariant:** at any point during the double loop, `res[k]` holds the correct accumulated value (possibly `>= 10`, resolved later as digits are finalized) for everything contributed to position `k` so far — nothing is ever lost, only added to.
* **Edge cases:**
  * Either input is `"0"` → returned immediately as `"0"`, avoiding a result like `""` or `"000"` that stripping leading zeros from an all-zero `res` array could otherwise produce.
  * Single-digit inputs (`"2"` × `"3"`) → `res` has size `2`, correctly holds `[0, 6]`, strips to `"6"`.
  * Very large inputs (200-digit numbers) → this simulation handles them the same way as small ones, since it never relies on native integer arithmetic overflowing.
  * Overlapping contributions to the same position (`p1` from one pair equals `p2` from another) → handled correctly, since every write to `res[p2]` and `res[p1]` uses `+=` or reads the existing value first, never a blind overwrite.

---

## 3. Code

```python
class Solution:

    def multiply(self, num1: str, num2: str) -> str:
        if num1 == "0" or num2 == "0":
            return "0"

        m, n = len(num1), len(num2)
        res = [0] * (m + n)

        # Right-to-left digit-by-digit multiplication
        for i in range(m - 1, -1, -1):
            d1 = ord(num1[i]) - ord("0")
            for j in range(n - 1, -1, -1):
                d2 = ord(num2[j]) - ord("0")

                mul = d1 * d2
                p1, p2 = i + j, i + j + 1

                total = mul + res[p2]

                res[p2] = total % 10
                res[p1] += total // 10

        # Strip leading zeros
        result_str = []
        for digit in res:
            if not (len(result_str) == 0 and digit == 0):
                result_str.append(str(digit))

        return "".join(result_str)


if __name__ == "__main__":
    solution = Solution()
    assert solution.multiply("12", "34") == "408"
    assert solution.multiply("0", "5") == "0"
    assert solution.multiply("2", "3") == "6"
    assert solution.multiply("123", "456") == "56088"
    print("All tests passed")
```

---

## 4. Dry Run

`num1 = "12"`, `num2 = "34"` (`m=2, n=2`), starting `res = [0, 0, 0, 0]`

| `(i, j)` | `d1 × d2` | `(p1, p2)` | `res[p2]` before | `total` | `res[p2]` after | `res[p1]` after | `res` state |
| --- | --- | --- | --- | --- | --- | --- | --- |
| `(1, 1)` | `2 × 4 = 8` | `(2, 3)` | `0` | `8` | `8` | `0` | `[0, 0, 0, 8]` |
| `(1, 0)` | `2 × 3 = 6` | `(1, 2)` | `0` | `6` | `6` | `0` | `[0, 0, 6, 8]` |
| `(0, 1)` | `1 × 4 = 4` | `(1, 2)` | `6` | `10` | `0` | `1` | `[0, 1, 0, 8]` |
| `(0, 0)` | `1 × 3 = 3` | `(0, 1)` | `1` | `4` | `4` | `0` | `[0, 4, 0, 8]` |

**Strip leading zero:** `[0, 4, 0, 8]` → **`"408"`**

---

## 5. Complexity

* **Time:** `O(m · n)` — every digit of `num1` is multiplied against every digit of `num2`.
* **Space:** `O(m + n)` — `res` holds one entry per possible result digit.

---

## 6. Recall (30 seconds)

* **Position formula:** digit `i` of `num1` times digit `j` of `num2` contributes its ones digit to `res[i+j+1]` and its carry to `res[i+j]`.
* **Accumulate, don't overwrite:** `res[p2]` and `res[p1]` both add onto whatever's already there, since multiple digit pairs can land on the same position.
* **Zero guard first:** `"0"` as either input short-circuits to `"0"` before any of the index math runs.
