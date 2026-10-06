# 69. Sqrt(x)

**LC 69** · **Source:** LC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Search on the answer — the simplest version: find the largest `mid` with `mid * mid <= x`

---

## 1. Intuition

`mid * mid` grows monotonically as `mid` grows, so just like Koko's eating speed, you can binary search the candidate answers directly instead of computing a square root formula. The candidates here are integers from `1` to `x // 2` (since for `x >= 2`, the square root can never exceed half of `x`).

- `square == x` → exact root found, return immediately.
- `square < x` → `mid` is a valid floor candidate (the true answer could be `mid` or bigger), so remember it (`res = mid`) and push right looking for a bigger valid one: `left = mid + 1`.
- `square > x` → `mid` overshot, discard it and look left: `right = mid - 1`.
- This is the exact same "record + keep pushing" shape as [#3 Find First and Last Position](../01-binary-search-on-sorted-sequences/03-find-first-and-last-position-of-element-in-sorted-array.md) — the "value" being searched for is just `mid * mid` instead of an array lookup.

**Recall:** binary search integers, testing `mid * mid` against `x`; keep the largest `mid` whose square doesn't exceed `x`.

## 2. Approach

* **Idea:** search-on-the-answer (Form 1 style, `while left <= right`), using `mid * mid <= x` as the feasibility test instead of a separate function.
* **Data structure / pointers:** `left`/`right` bound the candidate range `[1, x // 2]`; `res` holds the best (largest) valid candidate found so far, defaulting to `0`.
* **Invariant:** `res` always holds the largest `mid` tested so far whose square was `<= x`; the search keeps pushing `left` right to see if an even larger one exists.
* **Edge cases:**
  - `x = 0` or `x = 1` → handled by the `x < 2` guard, returning `x` directly without entering the loop (`√0 = 0`, `√1 = 1`).
  - Large `x` (up to `2^31 - 1`) → `right = x // 2` keeps the range reasonable, and `log2` of even a huge range is small, so it stays fast and doesn't overflow in Python.
  - `x` is a perfect square → `square == x` triggers the early return.

## 3. Code

```python
class Solution:

    def mySqrt(self, x: int) -> int:
        if x < 2:
            return x

        left, right = 1, x // 2
        res = 0

        while left <= right:
            mid = (left + right) // 2
            square = mid * mid

            if square == x:
                return mid
            elif square < x:
                res = mid  # mid is a valid floor candidate
                left = mid + 1
            else:
                right = mid - 1

        return res
```

## 4. Dry Run

`x = 8` (`left=1, right=4, res=0`)

| Iteration | `left` | `right` | `mid` | `mid*mid` | Comparison | `res` | Action |
|---|---|---|---|---|---|---|---|
| 1 | 1 | 4 | 2 | 4 | `4 < 8` | 2 | `left = 3` |
| 2 | 3 | 4 | 3 | 9 | `9 > 8` | 2 | `right = 2` |
| End | 3 | 2 | — | — | `left > right` | 2 | return `2` |

## 5. Complexity

* **Time:** `O(log x)` — halves the integer range `[1, x // 2]` every iteration.
* **Space:** `O(1)` — only `left`, `right`, `mid`, `res`.

## 6. Recall (30 seconds)

- Same "search on the answer" idea as Koko: here the feasibility test is just `mid * mid <= x`.
- Record the best candidate as you go (`res = mid`) since an exact match might not exist — the answer is the floor.
- `x < 2` is the only special case, handled up front before the loop even starts.
