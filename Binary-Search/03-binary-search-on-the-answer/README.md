# Topic 3 — Binary Search on the Answer

## The pattern

There is no array to search. Instead, the **possible answers form a range**, and you can test any guess with a yes/no question. If the test is monotonic (once a guess works, every larger guess also works), you can binary search the range.

```python
lo, hi = smallest_possible_answer, largest_possible_answer
while lo < hi:
    mid = (lo + hi) // 2
    if feasible(mid): hi = mid           # mid works — try something smaller
    else:             lo = mid + 1       # mid is too small
return lo                                # the smallest feasible answer
```

`feasible(mid)` is usually **one pass over the input**, so the total cost is `O(n · log(range))`.

## How to spot this topic

* The question asks for the **minimum X such that …** or the **maximum X such that …**.
* Words to look for: **"minimum speed / capacity / days"**, **"largest minimum"**, **"smallest maximum"**, **"integer square root"**, **"minimize the maximum"**.
* Quick test: *if I guess an answer, can I check it with one pass — and does a bigger guess never hurt?* If yes, it's this topic.

**Not this topic if:** you're searching for a value in a sorted array (→ Topic 1).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 11 | Koko Eating Bananas | Search the speed `k` in `[1, max(piles)]`; feasible if `sum(ceil(p / k)) <= h` |
| 12 | Sqrt(x) | Find the largest `mid` with `mid * mid <= x` |
| 15 *(Extra)* | Capacity To Ship Packages Within D Days | Search the capacity in `[max(weights), sum(weights)]`; feasible if days needed `<= D` |
| 16 *(Extra)* | Split Array Largest Sum | Same as #15: search the largest allowed sum; feasible if pieces needed `<= k` |
