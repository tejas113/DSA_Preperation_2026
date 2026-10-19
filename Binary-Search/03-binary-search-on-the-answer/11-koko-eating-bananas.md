# 875. Koko Eating Bananas

**LC 875** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Search on the answer — binary search the eating speed with a feasibility check

---

## 1. Intuition

There's no array of candidates to search — the "search space" is every possible eating speed from `1` to `max(piles)`. Instead of comparing a value, each guess `k` gets tested with one full pass over `piles`: could Koko actually finish within `h` hours at that speed?

- `k_works(k)` sums `ceil(pile / k)` hours across all piles — that's how long speed `k` actually takes.
- The key fact that makes binary search valid: if speed `k` works, every faster speed `> k` also works (more speed never makes you slower). This monotonicity is what lets you binary search instead of checking every speed.
- `k_works(k)` is `True` → `k` is a candidate for the *minimum* working speed, so record it (`ans = k`) and try slower: `r = k - 1`.
- `k_works(k)` is `False` → `k` is too slow, the answer must be faster: `l = k + 1`.
- Same "record + keep pushing" shape as [#3 Find First and Last Position](../01-binary-search-on-sorted-sequences/03-find-first-and-last-position-of-element-in-sorted-array.md) — exact-match style (`while l <= r`), remembering the best candidate seen in `ans` instead of narrowing toward a final `l == r`.

**Recall:** binary search speed `k` in `[1, max(piles)]`; `k_works(k)` true → record `ans = k` and search slower (`r = k - 1`), else go faster (`l = k + 1`).

## 2. Approach

* **Idea:** search-on-the-answer (the Topic 3 pattern) — guess a speed, test feasibility with one pass, use monotonicity to halve the range. This version uses the exact-match loop shape (`while l <= r`) with an explicit `ans` tracker, instead of the boundary-search shape (`while l < r`) that converges `l` and `r` to the same value.
* **Data structure / pointers:** `l`/`r` bound the candidate speed range; `k` is the guessed speed each iteration; `ans` holds the best (slowest confirmed-working) speed found so far, seeded at `r = max(piles)` since that speed always works; `k_works` is the feasibility function, run fresh every call (no memoization needed since it's only called `O(log(max(piles)))` times).
* **Invariant:** `ans` always holds a working speed at least as good as any seen before it; the search keeps narrowing toward slower speeds (`r = k - 1`) while a faster fallback remains confirmed in `ans`.
* **Edge cases:**
  - `h == len(piles)` → Koko must clear every pile within exactly one hour each, forcing `k = max(piles)`; `ans` is seeded with exactly this value, so even if the loop never improved on it, the answer would stay correct.
  - Large pile values (up to `10^9`) → the search range is still only `~30` iterations (`log2(10^9) ≈ 30`), and each pass is `O(n)`, so it stays fast.
  - All piles equal → feasibility is uniform across piles, search still converges normally.

## 3. Code

```python
from math import ceil

class Solution:
    def minEatingSpeed(self, piles: list[int], h: int) -> int:
        def k_works(k):
            hours = 0
            for num in piles:
                hours += ceil(num / k)
            return hours <= h

        l = 1
        r = max(piles)
        ans = r

        while l <= r:
            k = (l + r) // 2
            if k_works(k):
                ans = k  # Save the valid speed
                r = k - 1  # Try to find a smaller valid speed on the left
            else:
                l = k + 1  # Too slow, need a higher speed on the right

        return ans
```

## 4. Dry Run

`piles = [3, 6, 7, 11]`, `h = 8` (`l=1, r=11, ans=11`)

| Iteration | `l` | `r` | `k` | Hours | Feasible? | Action |
|---|---|---|---|---|---|---|
| 1 | 1 | 11 | 6 | `1+1+2+2=6` | yes (`6<=8`) | `ans = 6`, `r = 5` |
| 2 | 1 | 5 | 3 | `1+2+3+4=10` | no (`10>8`) | `l = 4` |
| 3 | 4 | 5 | 4 | `1+2+2+3=8` | yes (`8<=8`) | `ans = 4`, `r = 3` |
| End | 4 | 3 | — | — | `l > r` | return `ans = 4` |

## 5. Complexity

* **Time:** `O(n log(max(piles)))` — each feasibility check is `O(n)` (one pass over `piles`), and there are `O(log(max(piles)))` guesses.
* **Space:** `O(1)` — only scalar bounds, `ans`, and an hours accumulator inside `k_works`.

## 6. Recall (30 seconds)

- No array to search — the candidates are speeds `1..max(piles)`, tested one at a time with a feasibility pass.
- Monotonicity is the whole trick: once a speed works, every faster speed works too, so binary search is valid.
- `k_works(k)` True → record it (`ans = k`) and keep searching slower (`r = k - 1`); False → must go faster (`l = k + 1`).
