# 52. N-Queens II

**LC 52** · **Source:** LC150 · **Difficulty:** Hard · **Priority:** Stretch · **Pattern:** Row-by-Row Placement Backtracking (count only)

---

## 1. Intuition

The search is identical to N-Queens (#12): one queen per row, with three sets tracking attacks — `col`, `posDiag` (`r + c`, the `/` diagonal) and `negDiag` (`r - c`, the `\` diagonal). Only the ending changes.

* `r == n` — every row has a queen, so that's one more valid arrangement. Just do `res += 1`.
* No board is built or copied, so there is no `board` at all.
* Place a queen: add to the three sets. Undo: remove from the three sets.

**Recall:** same as #12, but `res += 1` at the base case.

---

## 2. Template

* **Choose:** add `c`, `r + c`, `r - c` to `col`, `posDiag`, `negDiag`
* **Explore:** `backtrack(r + 1)`
* **Un-choose:** remove all three
* **Prune / dedup:** `if c in col or (r + c) in posDiag or (r - c) in negDiag: continue` — the square is attacked.

---

## 3. Code

```python
class Solution:
    def totalNQueens(self, n: int) -> int:
        col = set()
        posDiag = set()  # Tracks (r + c) anti-diagonals /
        negDiag = set()  # Tracks (r - c) main diagonals \

        res = 0

        def backtrack(r: int):
            nonlocal res
            # Base Case: All N queens successfully placed
            if r == n:
                res += 1
                return

            for c in range(n):
                # Constraint Check: Column or Diagonals already under attack
                if c in col or (r + c) in posDiag or (r - c) in negDiag:
                    continue

                # Choice: Place Queen and record attacked lines
                col.add(c)
                posDiag.add(r + c)
                negDiag.add(r - c)

                # Recurse to next row
                backtrack(r + 1)

                # Backtrack: Revert state
                col.remove(c)
                posDiag.remove(r + c)
                negDiag.remove(r - c)

        backtrack(0)
        return res

```

### Alternative: Bitmask (interview flex)

Replace each set with one number, where bit `c` set to `1` means "column `c` is taken/attacked".

* `full_mask = (1 << n) - 1` — `n` ones, meaning all columns.
* `valid_spots = full_mask & ~(cols | pos_diag | neg_diag)` — the columns that are *not* attacked in this row.
* `bit = valid_spots & -valid_spots` — grab the lowest free column. `valid_spots ^= bit` removes it so the `while` loop tries the next free column.
* Next row: the two diagonal masks shift by one — one drifts toward higher columns (`<< 1`), the other toward lower columns (`>> 1`), because a diagonal attack moves one column sideways per row down.

```python
class Solution:
    def totalNQueens(self, n: int) -> int:
        count = 0
        
        # Limit mask to 'n' bits (e.g., for n=4 -> 0b1111)
        full_mask = (1 << n) - 1

        def backtrack(row, cols, pos_diag, neg_diag):
            nonlocal count
            if row == n:
                count += 1
                return

            # Available spots: 1s indicate UNATTACKED positions
            valid_spots = full_mask & ~(cols | pos_diag | neg_diag)

            while valid_spots:
                # Pick the rightmost available bit (lowest set bit)
                bit = valid_spots & -valid_spots
                
                # Clear bit from available spots
                valid_spots ^= bit

                # Recurse: shift diagonals left/right for the next row
                backtrack(
                    row + 1,
                    cols | bit,
                    (pos_diag | bit) << 1,
                    (neg_diag | bit) >> 1
                )

        backtrack(0, 0, 0, 0)
        return count

```

---

## 4. Dry Run (`n = 4`)

Same search as #12; each line is a queen placed in that row, and only unattacked squares are listed. Rows 0 and 1 for `c=2` and `c=3` mirror the `c=1` and `c=0` starts.

```text
row 0: c=0                                    row 0: c=1
  └─ row 1: c=2                                 └─ row 1: c=3   (only free square)
  │     └─ row 2: no free square  ✗              └─ row 2: c=0
  └─ row 1: c=3                                        └─ row 3: c=2  ✔ res += 1
        └─ row 2: c=1
              └─ row 3: no free square  ✗
```

The two mirror-image solutions give `res = 2` for `n = 4`.

---

## 5. Complexity

* **Time: O(n!)** — the same search as #12: row 0 has `n` choices, row 1 at most `n - 1`, and the diagonals cut it further. There is no board copy per solution.
* **Space: O(n)** — the three sets and the recursion depth are at most `n`, and no board is stored.

---

## 6. Recall (30 seconds)

* Same search as #12; the base case is `res += 1`.
* No board → space drops to `O(n)`.
* Bitmask: sets become numbers, `x & -x` grabs the lowest free column.
