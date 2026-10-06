# 875. Koko Eating Bananas

**LC 875** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Search on the answer — binary search the eating speed with a feasibility check

---

## 1. Intuition

There's no array of candidates to search — the "search space" is every possible eating speed from `1` to `max(piles)`. Instead of comparing a value, each guess `k` gets tested with one full pass over `piles`: could Koko actually finish within `h` hours at that speed?

- `k_works(k)` sums `ceil(pile / k)` hours across all piles — that's how long speed `k` actually takes.
- The key fact that makes binary search valid: if speed `k` works, every faster speed `> k` also works (more speed never makes you slower). This monotonicity is what lets you binary search instead of checking every speed.
- `k_works(k)` is `True` → `k` is a candidate for the *minimum* working speed, so keep it and try slower: `r = k`.
- `k_works(k)` is `False` → `k` is too slow, the answer must be faster: `l = k + 1`.
- Same boundary-search shape as [#9 Find Peak Element](../02-rotated-modified-and-partition-searches/09-find-peak-element.md) — `while l < r`, `r = k` to keep a candidate, `l = k + 1` to discard one — just with a feasibility pass instead of a slope comparison.

**Recall:** binary search speed `k` in `[1, max(piles)]`; `k_works(k)` checked → `r = k` (search slower), else `l = k + 1` (search faster).

## 2. Approach

* **Idea:** search-on-the-answer (the Topic 3 pattern) — guess a speed, test feasibility with one pass, use monotonicity to halve the range.
* **Data structure / pointers:** `l`/`r` bound the candidate speed range; `k` is the guessed speed each iteration; `k_works` is the feasibility function, run fresh every call (no memoization needed since it's only called `O(log(max(piles)))` times).
* **Invariant:** the true minimum working speed always lies within `[l, r]`; every iteration either proves speeds `<= k` are too slow (discard them) or confirms `k` itself still works (keep it as the new upper bound).
* **Edge cases:**
  - `h == len(piles)` → Koko must clear every pile within exactly one hour each, forcing `k = max(piles)`.
  - Large pile values (up to `10^9`) → the search range is still only `~30` iterations (`log2(10^9) ≈ 30`), and each pass is `O(n)`, so it stays fast.
  - All piles equal → feasibility is uniform across piles, search still converges normally.

## 3. Code

```python
from math import ceil


class Solution:

    def minEatingSpeed(self, piles: list[int], h: int) -> int:

        def k_works(k: int) -> bool:
            hours = 0
            for num in piles:
                hours += ceil(num / k)
            return hours <= h

        l = 1
        r = max(piles)

        while l < r:
            k = (l + r) // 2
            if k_works(k):
                r = k  # k works, try searching for a smaller valid speed
            else:
                l = k + 1  # k is too slow, speed must be higher

        return r
```

## 4. Dry Run

`piles = [3, 6, 7, 11]`, `h = 8` (`l=1, r=11`)

| Iteration | `l` | `r` | `k` | Hours | Feasible? | Action |
|---|---|---|---|---|---|---|
| 1 | 1 | 11 | 6 | `1+1+2+2=6` | yes (`6<=8`) | `r = 6` |
| 2 | 1 | 6 | 3 | `1+2+3+4=10` | no (`10>8`) | `l = 4` |
| 3 | 4 | 6 | 5 | `1+2+2+3=8` | yes (`8<=8`) | `r = 5` |
| 4 | 4 | 5 | 4 | `1+2+2+3=8` | yes (`8<=8`) | `r = 4` |
| End | 4 | 4 | — | — | `l == r` | return `4` |

## 5. Complexity

* **Time:** `O(n log(max(piles)))` — each feasibility check is `O(n)` (one pass over `piles`), and there are `O(log(max(piles)))` guesses.
* **Space:** `O(1)` — only scalar bounds and an hours accumulator inside `k_works`.

## 6. Recall (30 seconds)

- No array to search — the candidates are speeds `1..max(piles)`, tested one at a time with a feasibility pass.
- Monotonicity is the whole trick: once a speed works, every faster speed works too, so binary search is valid.
- `k_works(k)` True → keep searching slower (`r = k`); False → must go faster (`l = k + 1`).
