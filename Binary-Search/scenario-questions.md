# Binary Search — Scenario-Based Interview Question Bank

Google does not ask "implement binary search". It gives a short, vague, real-world situation and waits to see whether **you** notice that binary search applies. This file trains that one skill: **spotting the pattern with no hints**, then explaining the cost out loud.

How to use it:

1. Read **Part 1** (the 5-step framework) until you can say it without looking.
2. Skim **Part 2** (signal → pattern) before every mock.
3. In **Part 4**, cover everything except the **Scenario** line, answer it cold, then check yourself against the entry.
4. Re-read **Part 5** (traps) the night before.

Problem numbers (`#1`–`#13`) match [problems.md](problems.md); `LC` numbers are LeetCode's. Code snippets are lifted from the existing write-ups, so the loop forms (`left <= right` vs `left < right`) are the ones you already wrote.

---

## Part 1 — "Is this binary search?" framework (5 steps)

Run these five steps **out loud** on every vague question. If step 2 has no honest answer, it is not binary search.

### Step 1 — What is the search space?

Name the thing you are narrowing. It is almost never "the array" in a Google question.

| Search space | Looks like | Example |
|---|---|---|
| **An index range** `[0, n-1]` | Ordered data hidden in the story | Log lines in time order, IDs from a counter |
| **A boundary position** `[0, n]` | "Where would this go / first time X holds" | Insert position, first bad build |
| **A range of possible answers** | "Smallest capacity / slowest speed / largest gap such that …" | Koko's speed, shipping capacity |
| **A cut or a window start** | Two ordered things, or "k nearest" | Median of two arrays, k closest |
| **A virtual index** | 2D data that reads as one line | Row-by-row matrix, `mid // n`, `mid % n` |

Say: *"The thing I'm narrowing is ___, from ___ to ___."*

### Step 2 — What is the monotonic property?

Write the yes/no check as a row of booleans over the search space. It must flip **exactly once**:

```
candidate:  1   2   3   4   5   6   7   8
works?:     F   F   F   T   T   T   T   T      ← "if X works, everything larger also works"
```

Say it as a sentence: ***"If ___ works for mid, then it also works for everything larger (or smaller)."***

| Real property | Boolean row |
|---|---|
| `arr[mid] >= target` in ordered data | F F F T T T |
| `isBad(mid)` once a bug is introduced | F F F T T T |
| Speed `k` finishes in `h` hours | F F F T T T |
| `mid * mid <= x` | T T T F F F |
| Rotated array, `arr[mid] <= arr[last]` | F F F T T T |
| Peak: `arr[mid] < arr[mid+1]` (uphill) | T T T F F F |

**The test that kills false positives:** try to build one counter-example where the row goes `T F T`. If you can, it is not binary search.

### Step 3 — What does the check cost?

| Check | Cost per probe | Total |
|---|---|---|
| One comparison at `mid` | `O(1)` | `O(log R)` |
| Feasibility pass over the input (Koko, shipping) | `O(n)` | `O(n · log R)` |
| An API / expensive call (build + test run) | `O(C)` | `O(C · log R)` — and say you'd minimise the number of calls |

`R` is the size of the search space. Total cost = **(cost of one check) × (number of iterations)**. See Part 3.

### Step 4 — First true or last true?

| You want | Meaning | Update on a hit | Typical loop |
|---|---|---|---|
| **First true** (smallest X that works) | Boundary at the left of the `T` block | keep `mid`: `hi = mid` (or record `ans = mid`, then `right = mid - 1`) | `while lo < hi`, or `while lo <= hi` + `ans` |
| **Last true** (largest X that works) | Boundary at the right of the `T` block | record `ans = mid`, then `left = mid + 1` | `while lo <= hi` + `ans` |

Rules of thumb: "**minimum** speed / capacity / days" → first true. "**Maximum** side / gap / floor" → last true. Duplicates ("first / last occurrence") → same fork.

### Step 5 — Bounds and termination

Before writing any code, answer all of these:

1. **`lo` is the smallest legal answer**, `hi` is the largest (or `n` for "no such index"). Is the true answer guaranteed to be inside `[lo, hi]`?
2. **Loop form.** `hi = mid - 1` ⇒ `while lo <= hi`. `hi = mid` ⇒ `while lo < hi`. Never mix them (infinite loop).
3. **Progress.** Every branch must shrink the range (`mid + 1`, `mid - 1`, or `hi = mid` with `lo < hi`).
4. **What is returned** after the loop: `lo`, `ans`, or `-1`.
5. **Sanity trace** on a 1-element and a 2-element input, out loud.

### Questions to ask the interviewer (pick 2–3)

- Is the data **ordered**? Ascending or descending? Can it have **duplicates**? (Decides `<` vs `<=` and first/last.)
- How big can **n** be, and how big can the **values** be? (Decides bounds and overflow.)
- Is there always a valid answer? What do I return if **none** exists (`-1`, `n`, `""`)?
- Can the **data change** between queries (inserts, deletes)? One query or **many**? (Sort-once vs per-query.)
- Is the answer an **integer** or does it need **precision** (e.g. 1e-6)?
- For "minimum such that …": **if X works, does a bigger X always work?** (Confirms monotonicity.)
- Can I **load it all into memory**, or do I only have an API to probe it?
- If I'm being asked for a position: first or last of equals? **Any** peak, or a specific one?

---

## Part 2 — Signal → pattern cheat sheet

| What the question says | What it really is | Pattern | Problems |
|---|---|---|---|
| "Ordered data, does X exist / where is it?" | Exact match on an index range | Form 1: `while left <= right`, return `mid` | #1 Binary Search |
| "Where would this slot in?", "first time X ≥ threshold", "first bad …", "how many are below X" | Lower bound: first index where `arr[i] >= target` (or API says true) | Boundary search; `left` is the answer | #2, #13 |
| "First and last occurrence", "how many copies of X" | Lower bound and upper bound, count = difference | Run the same helper twice with opposite bias | #3 |
| "Latest value at or before time t", "what was it at moment t" | Floor lookup over time-ordered records | Record `res`, keep pushing right | #6 |
| "k nearest to x" in ordered data | Search the **start of a window** in `[0, n-k]` | Compare `x - arr[mid]` with `arr[mid+k] - x` | #5 |
| "Data was cut and glued / circular buffer / starts in the middle" | Rotated ordered data | One half is always ordered, or compare with the right end | #7, #8 |
| "Any local maximum / any day that beats both neighbours" | Peak finding, **not** ordered | Step uphill: `arr[mid] < arr[mid+1]` | #9 |
| "Grid where each row continues the previous one" | 2D that is one line in disguise | `row = mid // n`, `col = mid % n` | #4 |
| "Two ordered sources, middle value, don't merge" | Search a **cut** in the smaller source | Left halves ≤ right halves | #10 |
| "Slowest rate / smallest capacity / fewest workers such that the job still finishes" | **Search on the answer**, minimise | Check `feasible(mid)`; true → `hi = mid` | #11 (+ stretch #15, #16) |
| "Biggest whole number whose … fits", "integer root" | Search on the answer, largest value that passes a cheap test | Record `res = mid`, `left = mid + 1` | #12 |
| **"Maximise the minimum"** (spread things out, keep them far apart) | Search the answer *d*; check = greedy placement; larger d is harder | Last true: `ans = mid`, `left = mid + 1` | gap (Part 6) |
| **"Minimise the maximum"** (split work evenly, cap the worst load) | Search the answer *cap*; check = greedy grouping; larger cap is easier | First true: `hi = mid` | #15, #16 (gaps) |
| "Probe it only through a function / API, no length given" | Search on a function or unknown length | Double `hi` until the check flips, then binary search `[hi/2, hi]` | gap (Part 6) |
| "Stream: we only see items as they come" | Usually **not** plain binary search | Append keeps order → `bisect`; out of order → heap or tree | #6 vs Part 4 variants |
| "Square root / nth root / to 6 decimals" | Numeric search on a monotone function | Integer: `mid*mid <= x`. Real: loop on `hi - lo > eps` or fixed iterations | #12 |

### How to tell search-on-answer from greedy or DP

| Signal | Technique | Why |
|---|---|---|
| Asks "**minimum / maximum X such that** the job is possible", and checking a *given* X is easy | **Binary search on the answer** (check is often a greedy pass) | Hard to *construct* the optimum, easy to *test* a guess |
| A local rule is provably optimal (always take the earliest-ending interval) and gives the answer in one pass | **Greedy only** | No guess needed; the rule *is* the answer |
| Asks "**how many ways**", "min cost over choices", states overlap, or a bigger X does **not** always keep working | **DP** | The yes/no flips more than once, or you need counts |
| Both "minimise the largest piece" **and** split into exactly *k* pieces | **BS on answer** (fast) or **DP** (`O(k n²)`) | State the BS version first; mention DP as the fallback |

**Quick discriminator:** ask *"If I'm told the answer is X, can I verify it quickly, and does a better X also pass?"* Yes to both → binary search on the answer. Yes to the first only → probably DP or greedy.

### What to say when the data is NOT sorted but the answer space is monotonic

> *"The array isn't ordered, but the **answer** is. If capacity C is enough to finish in D days, then C+1 is enough too. So I won't search the array at all — I'll search the capacity from the heaviest single item up to the total weight, and use one linear pass as the yes/no check. That's `O(n · log(total))`."*

Three beats: **(1)** name the space, **(2)** state the monotonic sentence, **(3)** cost = one pass × number of iterations.

---

## Part 3 — Time & space complexity patterns

| Pattern | Time | Space | Reasoning |
|---|---|---|---|
| Exact match / boundary in ordered array | `O(log n)` | `O(1)` | Range halves each step |
| First + last occurrence | `O(log n)` | `O(1)` | Two searches: `2 · log n` is still `O(log n)` |
| Rotated search / min, peak | `O(log n)` | `O(1)` | One compare at `mid` discards half |
| …with **duplicates** (rotated II, plateaus) | `O(log n)` avg, **`O(n)` worst** | `O(1)` | When `left == mid == right` you can only shrink by 1 |
| 2D flattened matrix | `O(log(m·n))` = `O(log m + log n)` | `O(1)` | Virtual array of `m·n` items |
| 2D with only row+column order (staircase, not BS) | `O(m + n)` | `O(1)` | Each step drops a row or a column |
| K closest (window start) | `O(log(n − k) + k)` | `O(1)` aux | Search over `n − k + 1` starts, then slice `k` |
| Time-keyed floor lookup | `set O(1)`, `get O(log K)` | `O(N)` total | Appends keep order for free |
| Median of two (cut search) | `O(log min(m, n))` | `O(1)` | Search only the smaller array |
| **Search on the answer** | **`O(C · log R)`**, `C` = cost of the check | `O(1)` + what the check uses | `log R` iterations × one check each |
| …Koko: `C = n`, `R = max(piles)` | `O(n · log(max))` | `O(1)` | One pass per guess |
| …Sqrt: `C = O(1)`, `R = x // 2` | `O(log x)` | `O(1)` | A multiply per guess |
| Real-valued answer | `O(C · log((hi − lo) / eps))` | `O(1)` | Iterations set by the precision you need |
| Unknown length | `O(log p)` + `O(log p)` | `O(1)` | `p` = position of the answer: doubling, then search |
| Sort first, then many queries | `O(n log n + q log n)` | `O(n)` | Pays off when `q` is roughly more than `log n` |

### Counting iterations

> **iterations ≈ ⌈log₂(R)⌉, where R = hi − lo + 1 is the size of the search space.**
> **Total time = iterations × cost of one check.**

| Search-space size `R` | Iterations (≈ log₂ R) |
|---|---|
| 1,000 | 10 |
| 1,000,000 | 20 |
| 1,000,000,000 | 30 |
| 2³¹ ≈ 2.1 × 10⁹ | 31 |
| 10¹⁸ | 60 |
| Real answer, range 10⁴ to precision 10⁻⁶ → `R = 10¹⁰` | ~34 |

**Worked example (say it out loud).** Koko: `n = 10⁴` piles, each up to `10⁹`.

1. Search space = speeds `1 … max(piles)` → `R = 10⁹`.
2. Iterations = `log₂(10⁹) ≈ 30`.
3. Check = one pass over `n = 10⁴` piles.
4. Total = `30 × 10⁴ = 3 × 10⁵` operations → `O(n · log(max piles))`.

**Space:** an iterative binary search is `O(1)`. A recursive one uses `O(log n)` stack. Search on the answer is `O(1)` plus whatever the check allocates (for example the sorted copy of positions in "maximise the minimum").

**Doesn't-pay-off check:** if the data isn't ordered and you'd have to sort (`O(n log n)`) for one query, a linear scan (`O(n)`) is better. Sort once only when there are many queries.

---

## Part 4 — Scenario entries (one per write-up)

Entry order: **Original question → Scenario → Ask first → Spot it → Brute force → Solve → Cost → Follow-up → Variant A → Variant B.**

### 1. Binary Search — LC 704

**Original question.** Given an array of integers `nums` sorted in ascending order and an integer `target`, return the index of `target` if it exists, otherwise `-1`. Must run in `O(log n)`.

**Scenario.** *A warehouse holds 50 million parts on one long shelf, filled in delivery order, and every part's ID came from a counter at the dock. A scanner reads one ID and must say which shelf slot holds that part, or that it isn't on the shelf. Walking the aisle takes hours.*

**Ask first.**
1. Does the counter ever go backwards or reuse IDs (duplicates)?
2. If the ID isn't there, do you want a "not found" marker or the slot where it *would* be?

**Spot it.** IDs from a counter + shelved in arrival order ⇒ **the shelf is ordered by ID** even though nobody said so. One look at a slot tells you which side the ID lives on.

**Brute force.** Walk slot by slot: `O(n)`, 50 million comparisons per scan.

**Solve** (from [01-binary-search.md](01-binary-search-on-sorted-sequences/01-binary-search.md)):
```python
left, right = 0, len(nums) - 1
while left <= right:                 # <= so a 1-element range still gets checked
    mid = (left + right) // 2
    if nums[mid] == target:  return mid
    elif nums[mid] < target: left = mid + 1
    else:                    right = mid - 1
return -1
```

**Cost.** `O(log n)` time, `O(1)` space. Range halves every step: `log₂(50,000,000) ≈ 26` probes instead of 50 million.

**Follow-up.** *"What if the part IDs repeat and I need the first slot?"* → don't return on a match; record and keep going left (#3). *"What if the shelf length isn't known?"* → Variant B.

**Variant A — Smallest Letter Greater Than Target (LC 744)**
- **Question.** Given a sorted array of lowercase letters `letters` and a character `target`, return the smallest letter strictly greater than `target`. Letters wrap around: if none is greater, return `letters[0]`.
- **Scenario.** *A bus company names its stops A–Z around a ring road. A rider's phone says "where I am now: stop M". Which stop is the next one that follows M on the route you'd call out, wrapping back to the start after the last stop?* (stops listed in route order)
- **Pattern and cost.** Upper-bound boundary: first index with `letters[i] > target`; `left % n` handles the wrap. `O(log n)` time, `O(1)` space.

**Variant B — Search in a Sorted Array of Unknown Size (LC 702)** *(crosses into: search on a function / unknown length)*
- **Question.** You can only read the array through `reader.get(i)`, which returns `2³¹ − 1` when `i` is out of bounds. The array is sorted ascending and its length is unknown. Return the index of `target` or `-1`.
- **Scenario.** *A telemetry feed lets you ask "what was the reading at tick i?" for any tick, but nobody knows how many ticks exist; past the end you get a huge sentinel number. Locate the tick that has a given reading, with as few probes as you can.*
- **Pattern and cost.** Doubling then binary search: `hi = 1; while reader.get(hi) < target: lo = hi; hi *= 2`, then normal Form 1 on `[lo, hi]`. `O(log p)` probes to find the bracket and `O(log p)` to search, where `p` is the target's position. `O(1)` space.

---

### 2. Search Insert Position — LC 35

**Original question.** Given a sorted array of distinct integers and a target, return the index if found. If not, return the index where it would be inserted in order. `O(log n)`.

**Scenario.** *A concert hall seats guests row after row by ticket number, and every seat holds a guest. A latecomer arrives with ticket 4021, which no seated guest holds. At which seat position should the host squeeze them in so the ticket order along the rows stays intact?*

**Ask first.**
1. Can two guests share a ticket number (so "insert before or after the equals")?
2. What if the new ticket is bigger than every ticket, or smaller than every ticket?

**Spot it.** Seats filled by ticket number ⇒ ordered. "Where would it go" is "the first seat whose number is **not smaller** than mine" — a boundary, so the yes/no row is `F F F T T T`.

**Brute force.** Scan until you meet a bigger ticket: `O(n)`.

**Solve** (from [02-search-insert-position.md](01-binary-search-on-sorted-sequences/02-search-insert-position.md)):
```python
left, right = 0, len(nums) - 1
while left <= right:
    mid = left + (right - left) // 2
    if nums[mid] == target:  return mid
    elif nums[mid] < target: left = mid + 1
    else:                    right = mid - 1
return left                  # first index with nums[i] >= target
```
The invariant: everything left of `left` is `< target`, everything right of `right` is `>= target`; when they cross, `left` is the slot.

**Cost.** `O(log n)` time, `O(1)` space.

**Follow-up.** *"Return `len(nums)` when it is bigger than everything — does your code?"* Yes: `left` walks to `n`. *"With duplicates, insert before the first equal"* → switch to the pure boundary form (`hi = mid` when `nums[mid] >= target`).

**Variant A — Successful Pairs of Spells and Potions (LC 2300)**
- **Question.** Given `spells` and `potions`, a pair is successful if `spell × potion >= success`. For each spell, count the successful potions.
- **Scenario.** *A game studio has 100k hero strengths and a pool of 100k charm values. A hero wins a fight when strength × charm reaches a fixed threshold. For every hero, how many charms in the pool would let them win?*
- **Pattern and cost.** The pool isn't ordered yet — **order it once** (`O(m log m)`), then per hero find the first charm `>= ceil(success / strength)` with a lower bound; count = `m − index`. `O((n + m) log m)` time, `O(1)`–`O(m)` space.

**Variant B — Rank of x in an unordered list, many queries** *(crosses into: sort once vs scan)*
- **Question.** Given an unsorted array of `n` numbers and `q` queries, each asks how many numbers are less than `x_i`.
- **Scenario.** *An exam board has 200k raw marks in the order students handed in papers. Students ring in one at a time asking "how many people scored below me?"*
- **Pattern and cost.** Binary search only works on ordered data. **One** query: linear count `O(n)` is optimal — sorting would cost more. **Many** queries: sort once `O(n log n)`, then each query is `bisect_left` in `O(log n)`; total `O(n log n + q log n)`. It pays off once `q` exceeds roughly `log n`. If marks are also being *added* over time, a sorted array costs `O(n)` per insert — use a Fenwick tree or an order-statistics tree.

---

### 3. Find First and Last Position of Element in Sorted Array — LC 34

**Original question.** Given a sorted array `nums` (possibly with duplicates) and `target`, return `[first, last]` indices of `target`, or `[-1, -1]` if absent. `O(log n)`.

**Scenario.** *A boiler's sensor writes one reading per second, and in a heating cycle the level never drops. Operations asks, for a particular level L: at which second did it first read L, and at which second did it last read L? There are 80 million readings and thousands of such questions per day.*

**Ask first.**
1. Can the level stay flat for a long stretch (so many copies)?
2. If L never appeared, what should I return?

**Spot it.** "Never drops" ⇒ ordered by time and by value. "First and last" means the match is a **block**; plain binary search can land on any copy.

**Brute force.** Scan, track first and last hit: `O(n)` per question, so `O(n · q)`.

**Solve** (from [03-find-first-and-last-position-of-element-in-sorted-array.md](01-binary-search-on-sorted-sequences/03-find-first-and-last-position-of-element-in-sorted-array.md)):
```python
def findBound(isFirst: bool) -> int:
    left, right, bound = 0, len(nums) - 1, -1
    while left <= right:
        mid = left + (right - left) // 2
        if nums[mid] == target:
            bound = mid                      # remember it, keep pushing
            if isFirst: right = mid - 1      # look for an earlier copy
            else:       left = mid + 1       # look for a later copy
        elif nums[mid] < target: left = mid + 1
        else:                    right = mid - 1
    return bound
return [findBound(True), findBound(False)]
```

**Cost.** `O(log n)` time (two searches), `O(1)` space. Brute force would be 80M per question; this is ~27 probes × 2.

**Follow-up.** *"Only the count is needed."* → `last − first + 1`, or `upper_bound − lower_bound`. *"The array doesn't fit in memory."* → the data is on disk in pages: binary search the page index first, then inside the page; same `O(log n)` seeks.

**Variant A — Check If a Number Is Majority Element in a Sorted Array (LC 1150)**
- **Question.** Given a sorted array `nums` and `target`, return true if `target` appears more than `n / 2` times.
- **Scenario.** *A voting log lists ballots grouped by candidate ID in one block each. Does a particular candidate hold strictly more than half of the 2 million ballots?*
- **Pattern and cost.** Lower bound gives the first index `i` of `target`; majority iff `nums[i + n // 2] == target`. `O(log n)` time, `O(1)` space — one search, no counting pass.

**Variant B — Counting while the data keeps changing** *(crosses into: ordered tree)*
- **Question.** Maintain a multiset supporting `add(x)`, `remove(x)`, and `countBetween(a, b)`.
- **Scenario.** *A price tracker receives new prices all day and drops expired ones. At any moment a trader asks "how many live prices sit between $40 and $60?"*
- **Pattern and cost.** Binary search still answers `countBetween` (two bounds), but a plain array pays `O(n)` per insert/delete. Use an ordered structure (balanced BST, `SortedList`, or a Fenwick tree over bucketed values): `O(log n)` per operation. Say: *"Binary search needs the data to stay ordered; with heavy updates I need a structure that keeps order cheaply."*

---

### 4. Search a 2D Matrix — LC 74

**Original question.** An `m × n` integer matrix has each row sorted left to right, and the first integer of each row is greater than the last integer of the previous row. Return whether `target` is in the matrix. `O(log(m·n))`.

**Scenario.** *A cinema's seats carry booking numbers that continue row after row, front to back, and every row has the same width. The gate scans a number and must say whether that seat exists in the hall — without checking row by row.*

**Ask first.**
1. Do the numbers really continue from the end of one row to the start of the next, or is each row only ordered by itself?
2. Can the hall have zero rows?

**Spot it.** "Continue row after row" ⇒ read in reading order, it is **one ordered line**; the grid is only a costume.

**Brute force.** Scan every cell `O(m·n)`; or binary search the right row then scan it `O(m + n)`.

**Solve** (from [04-search-a-2d-matrix.md](01-binary-search-on-sorted-sequences/04-search-a-2d-matrix.md)):
```python
if not matrix or not matrix[0]: return False
m, n = len(matrix), len(matrix[0])
left, right = 0, m * n - 1
while left <= right:
    mid = left + (right - left) // 2
    row, col = mid // n, mid % n          # virtual 1D index → 2D
    val = matrix[row][col]
    if val == target:  return True
    elif val < target: left = mid + 1
    else:              right = mid - 1
return False
```

**Cost.** `O(log(m·n))` = `O(log m + log n)` time, `O(1)` space — nothing is flattened, only the index is translated.

**Follow-up.** *"Rows are each ordered but a row can start below the previous row's end."* → flattening breaks (see Variant A). *"Dimensions are huge and sparse."* → binary search row-by-row on the first column, then within the row.

**Variant A — Search a 2D Matrix II (LC 240)** *(crosses into: staircase, not flatten)*
- **Question.** Each row is sorted ascending and each column is sorted ascending, but a row's first element need **not** exceed the previous row's last. Return whether `target` exists.
- **Scenario.** *A seating plan prices seats so a price never falls as you move right along a row or down a column, but the cheapest seat in row 3 can still be cheaper than the dearest seat in row 2. Does any seat cost exactly $85?*
- **Pattern and cost.** Flatten fails: reading order is not globally ordered. Start at the top-right: if the value is too big, step left; if too small, step down. `O(m + n)` time, `O(1)` space. (Alternative: binary search every row, `O(m log n)`.) Good place to say *"binary search stops working here because the one-line ordering is gone."*

**Variant B — Kth Smallest Element in a Sorted Matrix (LC 378)** *(crosses into: search on the answer)*
- **Question.** `n × n` matrix with rows and columns sorted ascending. Return the `k`-th smallest value in sorted order (not distinct).
- **Scenario.** *A school has 700 classes, each ranking its students by score, and classes are also ranked from weakest to strongest at each position. Without merging all the scores, what is the score of the 1,000th-lowest student overall?*
- **Pattern and cost.** The search space is the **value range** `[matrix[0][0], matrix[-1][-1]]`, not indices. Check: count entries `≤ mid` with the staircase walk in `O(n)`; first value whose count `≥ k` is the answer. `O(n · log(max − min))` time, `O(1)` space. Alternative: min-heap, `O(k log n)`.

---

### 5. Find K Closest Elements — LC 658

**Original question.** Given a sorted array `arr`, integers `k` and `x`, return the `k` integers closest to `x`, in ascending order. On ties prefer the smaller value.

**Scenario.** *A pricing team keeps a ladder of 1 million price points, cheapest first. A shopper types a budget of $B. The page must show the five price points closest to that budget.*

**Ask first.**
1. On a tie in distance (one point $2 below, another $2 above), which one wins?
2. Is `k` always at most the number of price points?

**Spot it.** "Ladder, cheapest first" ⇒ ordered. The answer is **always a contiguous block** of `k` points, so the unknown is *where the block starts* — a single integer in `[0, n − k]`.

**Brute force.** Compute every distance and sort: `O(n log n)`; or heap `O(n log k)`.

**Solve** (from [05-find-k-closest-elements.md](01-binary-search-on-sorted-sequences/05-find-k-closest-elements.md)):
```python
left, right, ans = 0, len(arr) - k, 0
while left <= right:
    mid = (left + right) // 2
    if mid + k < len(arr) and x - arr[mid] > arr[mid + k] - x:
        left = mid + 1                # arr[mid] is farther than the next outside → slide right
    else:
        ans = mid                     # valid start; look for an earlier one
        right = mid - 1
return arr[ans : ans + k]
```
Guard `mid + k < len(arr)`: without it the last start indexes past the end.

**Cost.** `O(log(n − k) + k)` time (search starts, then slice `k`), `O(1)` aux space.

**Follow-up.** *"Prices arrive unordered."* → heap of size `k` in `O(n log k)`, or quickselect `O(n)` average. *"Return the closest single price."* → lower bound, then compare the neighbours.

**Variant A — Kth Missing Positive Number (LC 1539)** *(hidden monotone property)*
- **Question.** Given a strictly increasing array `arr` of positive integers and `k`, return the `k`-th positive integer that is missing from `arr`.
- **Scenario.** *A school gave out locker numbers to students in order, skipping broken lockers. The caretaker has 50k numbers in use, in assignment order, and wants the 1,000th locker number that is not in use, counting from 1.*
- **Pattern and cost.** No target value, but `missing(i) = arr[i] − (i + 1)` never decreases as `i` grows. First index with `missing(i) >= k` is `lo`; the answer is `lo + k`. `O(log n)` time, `O(1)` space.

**Variant B — k nearest in unordered data** *(crosses into: heap / quickselect)*
- **Question.** Given an **unsorted** array, an integer `x`, and `k`, return the `k` values closest to `x`.
- **Scenario.** *A phone's step counter logs daily step totals in the order they happened, and a coach asks for the 7 days closest to a 10,000-step goal.*
- **Pattern and cost.** The "contiguous window" property depends on order, so the window-start search is invalid. Use a max-heap of size `k` (`O(n log k)`, `O(k)` space) or quickselect (`O(n)` average). If there are many queries on the same data, sort once and go back to binary search.

---

### 6. Time Based Key-Value Store — LC 981

**Original question.** Design a store with `set(key, value, timestamp)` and `get(key, timestamp)`. `get` returns the value set with the largest timestamp `<= timestamp` for that key, or `""` if none. Timestamps for each key arrive strictly increasing.

**Scenario.** *A config service stores every change to every setting with the time of the change, and changes always arrive in clock order. Support asks, for a given setting: "what was its value at 3:07 pm last Tuesday?" There are millions of changes and constant lookups.*

**Ask first.**
1. Do writes for one setting always arrive in time order, or can they come late?
2. What should I return if the setting didn't exist yet at that moment?

**Spot it.** "Arrive in clock order" ⇒ appending keeps each setting's history **ordered for free**. "Value at or before time t" is a floor lookup ⇒ boundary.

**Brute force.** Scan the history for the latest change `<= t`: `O(K)` per query.

**Solve** (from [06-time-based-key-value-store.md](01-binary-search-on-sorted-sequences/06-time-based-key-value-store.md)):
```python
def set(self, key, value, timestamp):
    self.store[key].append((timestamp, value))     # order is free

def get(self, key, timestamp):
    res = ""
    values = self.store.get(key, [])
    left, right = 0, len(values) - 1
    while left <= right:
        mid = (left + right) // 2
        if values[mid][0] <= timestamp:
            res = values[mid][1]                   # valid candidate; look for a later one
            left = mid + 1
        else:
            right = mid - 1
    return res
```

**Cost.** `set` `O(1)`; `get` `O(log K)` for `K` changes of that key; `O(N)` space for `N` sets.

**Follow-up.** *"Writes can arrive out of order."* → Variant B. *"Memory is too big for one machine."* → shard by key; each shard keeps the same structure. *"Old history can be dropped."* → truncate the front; indices shift, store a base offset.

**Variant A — Snapshot Array (LC 1146)**
- **Question.** Implement `SnapshotArray(length)` with `set(index, val)`, `snap()` returning a snapshot id, and `get(index, snap_id)` returning the value at `index` when that snapshot was taken.
- **Scenario.** *A spreadsheet app lets users edit cells and press "save version". Later they open version 12 and read one cell. Millions of cells exist but only a few change per version.*
- **Pattern and cost.** Per cell keep a list of `(snap_id, value)` appended only on change; `get` is "last entry with `snap_id <= requested`" (`bisect_right − 1`). `set` `O(1)`, `get` `O(log changes)`, space proportional to the number of edits.

**Variant B — Out-of-order writes** *(crosses into: ordered tree)*
- **Question.** Same as above, but `set` can be called with **any** timestamp, in any order (think My Calendar-style inserts, LC 729).
- **Scenario.** *Sensors across a factory report readings over a flaky network, so a reading from 2:00 pm may arrive after one from 2:05 pm. Dashboards still ask "what was the last reading at or before time t?"*
- **Pattern and cost.** Appending no longer keeps order, so binary search on a list is invalid unless you insert in order. With `bisect.insort`: lookup `O(log K)`, insert `O(K)` (a memory shift). With a balanced tree / `SortedList`: both `O(log K)`. Interview line: *"binary search needs the order to survive; if writes break it, I choose a structure that maintains order."*

---

### 13. First Bad Version — LC 278

**Original question.** Versions `1 … n`; once a version is bad, all later versions are bad. Using `isBadVersion(version)`, return the first bad version while minimising API calls.

**Scenario.** *A release train has 2 billion builds, numbered in the order they shipped. A defect first appeared in some build and every build after it inherits it. Running the test suite on one build takes 20 minutes. Which build introduced the defect, with as few test runs as possible?*

**Ask first.**
1. Is it certain that the defect never disappears in a later build?
2. Is the test run itself reliable, or can it flake?

**Spot it.** "Every build after it inherits it" is the **monotonic yes/no sentence** handed to you: `F F F T T T`. And each probe is expensive, so number of probes is the metric.

**Brute force.** Test builds one by one from 1: up to `n` runs. At 20 min each, forever.

**Solve** (from [13-first-bad-version.md](01-binary-search-on-sorted-sequences/13-first-bad-version.md)):
```python
left, right = 1, n
while left < right:                      # < not <=, because right = mid keeps mid
    mid = left + (right - left) // 2
    if isBadVersion(mid): right = mid    # mid might be the first bad one
    else:                 left = mid + 1
return left
```

**Cost.** `O(log n)` calls: `log₂(2×10⁹) ≈ 31` test runs ≈ 10 hours, vs billions. `O(1)` space.

**Follow-up.** *"The test flakes 5% of the time."* → Variant B. *"You can run tests in parallel on 8 machines."* → probe 7 points to cut the range into 8 parts; log base 8 rounds.

**Variant A — Guess Number Higher or Lower (LC 374)**
- **Question.** A number is picked in `1 … n`. `guess(num)` returns `-1` if your guess is too high, `1` if too low, `0` if right. Return the picked number.
- **Scenario.** *A support bot asks a customer to pick a ticket tier from 1 to 1,000,000. After each proposal, the customer replies only "go lower", "go higher", or "yes".*
- **Pattern and cost.** The API result is a three-way compare; use Form 1 with `guess(mid)` in place of `nums[mid] == target`. `O(log n)` calls, `O(1)` space.

**Variant B — Flaky tests** *(crosses into: where binary search stops working)*
- **Question.** The yes/no function is not monotonic: some bad builds pass and some good builds fail.
- **Scenario.** *The nightly test says builds 1–40 pass, 41 fails, 42–60 pass, 61 onward fail. A manager asks which build "broke it first".*
- **Pattern and cost.** The row is `F…F T F…F T…T`; it flips more than once, so binary search returns *a* transition, not necessarily the first. Options: re-run each probe several times and take the majority (still `O(log n · r)`), fix the flakiness, or scan linearly `O(n)` if the number of builds is small. Say: *"Binary search is only valid if the predicate flips exactly once."*

---

### 7. Search in Rotated Sorted Array — LC 33

**Original question.** An ascending array of distinct values was rotated at an unknown pivot (e.g. `[0,1,2,4,5,6,7]` → `[4,5,6,7,0,1,2]`). Given `target`, return its index or `-1`. `O(log n)`.

**Scenario.** *A conveyor belt carries 300k labelled bins. Labels run upward along the belt, but the belt's start marker got bumped, so reading from the marker you see 40…99 and then 1…39. A worker needs the position of one label without reading every bin.*

**Ask first.**
1. Are labels all different?
2. Could the belt be un-bumped (no rotation at all)?

**Spot it.** "Upward, but wraps once" ⇒ order is broken only at one spot. Cut anywhere and **at least one side is still plainly ordered**; that side lets you decide.

**Brute force.** Walk the belt: `O(n)`. Or find the pivot first, then binary search the right half: `2 × O(log n)`.

**Solve** (from [07-search-in-rotated-sorted-array.md](02-rotated-modified-and-partition-searches/07-search-in-rotated-sorted-array.md)):
```python
left, right = 0, len(nums) - 1
while left <= right:
    mid = (left + right) // 2
    if nums[mid] == target: return mid
    if nums[left] <= nums[mid]:                    # left half is ordered
        if nums[left] <= target < nums[mid]: right = mid - 1
        else:                                         left = mid + 1
    else:                                          # right half is ordered
        if nums[mid] < target <= nums[right]: left = mid + 1
        else:                                         right = mid - 1
return -1
```

**Cost.** `O(log n)` time, `O(1)` space.

**Follow-up.** *"Labels can repeat."* → Variant A. *"Find where the belt was bumped."* → #8.

**Variant A — Search in Rotated Sorted Array II (LC 81)** *(crosses into: worst case `O(n)`)*
- **Question.** Same as above, but values may repeat. Return whether `target` exists.
- **Scenario.** *The same bumped belt, but now many bins carry the same label. Is a certain label on the belt at all?*
- **Pattern and cost.** When `nums[left] == nums[mid] == nums[right]` you can't tell which side is ordered (`[1,1,1,0,1]`), so shrink both ends by 1. Average `O(log n)`, **worst `O(n)`**, `O(1)` space. Say the worst case yourself before they ask.

**Variant B — Find in Mountain Array (LC 1095)**
- **Question.** An array rises strictly to a peak then falls strictly. You may only call `get(i)` and `length()`. Return the smallest index holding `target`, or `-1`.
- **Scenario.** *A river-gauge feed has hourly levels that climbed to one flood crest then receded. You can only ask "what was the level at hour i?" with a small query budget. When was a given level first reached?*
- **Pattern and cost.** Three searches: (1) peak by uphill step, (2) ordinary search in the rising part, (3) mirrored search in the falling part only if (2) missed. `O(log n)` calls, `O(1)` space.

---

### 8. Find Minimum in Rotated Sorted Array — LC 153

**Original question.** An ascending array of unique values was rotated between 1 and `n` times. Return the minimum element. `O(log n)`.

**Scenario.** *A device logs counter readings into a ring buffer of 1 million slots. The counter only rises, but the write pointer wrapped some time ago, so the oldest reading sits somewhere in the middle. Which slot holds the oldest reading?*

**Ask first.**
1. Are readings ever equal?
2. Can the buffer be unwrapped (oldest at slot 0)?

**Spot it.** Counter only rises + write pointer wrapped ⇒ one drop point. The oldest reading *is* the drop point; comparing a slot to the buffer's edge says which side hides the drop.

**Brute force.** Scan for the smallest: `O(n)`.

**Solve** (from [08-find-minimum-in-rotated-sorted-array.md](02-rotated-modified-and-partition-searches/08-find-minimum-in-rotated-sorted-array.md)):
```python
left, right = 0, len(nums) - 1
while left <= right:
    if nums[left] <= nums[right]:         # segment already ordered
        return nums[left]
    mid = left + (right - left) // 2
    if nums[left] <= nums[mid]: left = mid + 1     # drop is after mid
    else:                       right = mid        # drop is at or before mid
return nums[left]
```
(The README's alternative: compare `nums[mid]` with `nums[hi]`, `while lo < hi`.)

**Cost.** `O(log n)` time, `O(1)` space.

**Follow-up.** *"Readings can repeat."* → Variant A; note that this write-up's early exit `nums[left] <= nums[right]` returns the wrong answer for `[3,3,1,3]`, so for duplicates use the right-end comparison. *"How many times was it rotated?"* → Variant B.

**Variant A — Find Minimum in Rotated Sorted Array II (LC 154)** *(crosses into: worst case `O(n)`)*
- **Question.** Same as #153, but values may repeat.
- **Scenario.** *The same ring buffer, but the counter sometimes stalls and writes the same reading several times in a row. Which slot holds the oldest reading?*
- **Pattern and cost.** Compare `nums[mid]` with `nums[hi]`: `>` ⇒ `lo = mid + 1`; `<` ⇒ `hi = mid`; `==` ⇒ `hi -= 1` (cannot tell which side). Average `O(log n)`, worst `O(n)` (all equal). `O(1)` space.

**Variant B — How many times has the array been rotated?**
- **Question.** Given an ascending array rotated an unknown number of times, return the number of rotations (= index of the minimum).
- **Scenario.** *A carousel of numbered horses was started at horse 1, then spun some number of positions. A lever reads the number under the gate. How many positions has it turned from the original arrangement?*
- **Pattern and cost.** Exactly #8, returning the **index** of the minimum instead of its value. `O(log n)` time, `O(1)` space.

---

### 9. Find Peak Element — LC 162

**Original question.** A peak element is strictly greater than its neighbours. Given an integer array `nums` where adjacent elements are never equal, return the index of any peak (`nums[-1] = nums[n] = −∞`). `O(log n)`.

**Scenario.** *An analyst has ten years of daily traffic numbers and wants any single day that beat both the day before and the day after — a good spot for a promo. Neighbouring days never tie, and the edges only need to beat the one neighbour they have. Reading all days is too slow.*

**Ask first.**
1. Do I need the *highest* peak or *any* peak?
2. Can two neighbouring days be equal?

**Spot it.** Nothing is ordered, but a **local slope is information**: if the day to the right is higher, a peak must exist in that direction (climb until it stops). So one comparison halves the space.

**Brute force.** Scan for the first day beating its neighbours: `O(n)`.

**Solve** (from [09-find-peak-element.md](02-rotated-modified-and-partition-searches/09-find-peak-element.md)):
```python
left, right = 0, len(nums) - 1
while left < right:
    mid = (left + right) // 2
    if nums[mid] < nums[mid + 1]: left = mid + 1    # uphill → peak to the right
    else:                         right = mid       # downhill → mid may be the peak
return left
```

**Alternative** (in the write-up): `while left <= right`; if `nums[mid-1] > nums[mid]` then `right = mid - 1`, elif `nums[mid+1] > nums[mid]` then `left = mid + 1`, else `return mid` (guard `mid > 0` and `mid < n - 1`). Same cost; it returns as soon as `mid` is a peak.

**Cost.** `O(log n)` time, `O(1)` space. `mid + 1` is safe because `mid < right ≤ n − 1`.

**Follow-up.** *"Highest overall?"* → binary search can't promise that; `O(n)`. *"Equal neighbours allowed?"* → Variant B. *"2D grid?"* → gap, see Part 6.

**Variant A — Peak Index in a Mountain Array (LC 852)**
- **Question.** An array strictly increases, then strictly decreases. Return the peak index.
- **Scenario.** *A rocket's altitude is recorded every second: it rises, reaches its highest point, then falls. At which second was the highest altitude?*
- **Pattern and cost.** Same loop as #162, and now the answer is unique. `O(log n)` time, `O(1)` space.

**Variant B — Plateaus** *(crosses into: where the uphill step breaks)*
- **Question.** Same as #162 but adjacent elements **may be equal** (e.g. `[1,2,2,2,1]`).
- **Scenario.** *A thermostat logs temperatures that sit flat for hours at a time. Find any moment that is a local high point, where it's higher than what comes right before and right after.*
- **Pattern and cost.** If `nums[mid] == nums[mid + 1]` you can't tell whether the plateau is a peak, a ramp up, or a ramp down; you must scan outward. Worst case `O(n)`. The uphill argument needs strictly different neighbours. Say that explicitly.

---

### 10. Median of Two Sorted Arrays — LC 4

**Original question.** Given sorted arrays `nums1` (size `m`) and `nums2` (size `n`), return the median of the two combined. `O(log(m + n))` required.

**Scenario.** *Two regional offices each keep a customer list ordered by age. Head office wants the median age across both regions, but must not copy or combine either list.*

**Ask first.**
1. Can one of the lists be empty?
2. For an even total, is the median the average of the two middle ages?

**Spot it.** "Don't combine" ⇒ you can't merge. The median is a **cut**: put half the people on the left side across both lists. Choose the cut in one list and the other cut is forced.

**Brute force.** Merge both lists, take the middle: `O(m + n)` time and space.

**Solve** (from [10-median-of-two-sorted-arrays.md](02-rotated-modified-and-partition-searches/10-median-of-two-sorted-arrays.md)):
```python
if len(nums1) > len(nums2): nums1, nums2 = nums2, nums1      # search the smaller
m, n = len(nums1), len(nums2)
low, high, total_left = 0, m, (m + n + 1) // 2
while low <= high:
    i = (low + high) // 2;  j = total_left - i
    max_left1  = -inf if i == 0 else nums1[i - 1];  min_right1 = inf if i == m else nums1[i]
    max_left2  = -inf if j == 0 else nums2[j - 1];  min_right2 = inf if j == n else nums2[j]
    if max_left1 <= min_right2 and max_left2 <= min_right1:
        if (m + n) % 2: return float(max(max_left1, max_left2))
        return (max(max_left1, max_left2) + min(min_right1, min_right2)) / 2
    elif max_left1 > min_right2: high = i - 1      # took too much from nums1
    else:                        low  = i + 1      # took too little
```

**Cost.** `O(log min(m, n))` time, `O(1)` space — only the smaller array is searched; `j` is derived.

**Follow-up.** *"Now the k-th smallest."* → Variant A. *"The numbers arrive as a stream."* → Variant B.

**Variant A — K-th smallest of two sorted arrays**
- **Question.** Given two sorted arrays and `k`, return the `k`-th smallest element of their union.
- **Scenario.** *Two shops list products by price. A comparison site wants the 7th-cheapest product across both shops, without merging.*
- **Pattern and cost.** Same cut search with `total_left = k` (the left side holds exactly `k` items); `i` ranges over `[max(0, k − n), min(k, m)]`. Answer is `max(max_left1, max_left2)`. `O(log min(m, n, k))`, `O(1)` space.

**Variant B — Median of a data stream (LC 295)** *(crosses into: two heaps)*
- **Question.** Support `addNum(num)` and `findMedian()` on a growing stream.
- **Scenario.** *A fitness band streams heart-rate readings, and the coach screen must always show the middle reading so far.*
- **Pattern and cost.** The data is not ordered and keeps growing, so there is nothing to cut. Keep a max-heap of the lower half and a min-heap of the upper half and rebalance. `addNum` `O(log n)`, `findMedian` `O(1)`, `O(n)` space.

---

### 11. Koko Eating Bananas — LC 875

**Original question.** `piles[i]` bananas, `h` hours. Each hour Koko picks one pile and eats `k` bananas from it (if the pile has fewer, she eats all and wastes the rest of that hour). Return the minimum integer `k` that lets her finish within `h` hours.

**Scenario.** *A courier has a list of parcel batches and exactly H hours before the depot closes. Each hour they work on just one batch, and they carry at one fixed rate for the whole day; if a batch finishes early, the rest of that hour is wasted. What is the slowest constant rate that still gets everything done?*

**Ask first.**
1. Can the rate be fractional, or must it be a whole number?
2. Is `H` guaranteed to be at least the number of batches (so a solution exists)?

**Spot it.** Nothing is ordered; there is no array to search. But **"if this rate works, any faster rate also works"** — the monotonic sentence — and "slowest rate that works" is a first-true question. The rate itself is the search space.

**Brute force.** Try rates 1, 2, 3, … until one works: `O(n · max(piles))`.

**Solve** (from [11-koko-eating-bananas.md](03-binary-search-on-the-answer/11-koko-eating-bananas.md)):
```python
def k_works(k): return sum(ceil(p / k) for p in piles) <= h

l, r = 1, max(piles)
ans = r
while l <= r:
    k = (l + r) // 2
    if k_works(k): ans = k; r = k - 1      # works → record, try slower
    else:          l = k + 1               # too slow → go faster
return ans
```

**Cost.** `O(n · log(max(piles)))` time — each check is one pass of `n`; guesses = `⌈log₂ max⌉` (≈ 30 for 10⁹) — and `O(1)` space.

**Follow-up.** *"Hours are not whole numbers."* → Variant A-style real search (see #12 Variant A). *"What if you could eat from several piles in one hour?"* → monotonicity still holds but the check changes (total bananas / k). *"What if cost was U-shaped in k?"* → binary search fails; you'd use ternary search.

**Variant A — Capacity To Ship Packages Within D Days (LC 1011)** *(Stretch #15)*
- **Question.** Packages with weights must be shipped in order. Each day load a prefix of the remaining packages up to capacity `C`. Return the least `C` that ships all within `D` days.
- **Scenario.** *A freight company must move a queue of crates, in the order they arrived, onto trucks, one truck per day with the same load limit each day. What's the smallest load limit that gets everything out in D days?*
- **Pattern and cost.** Space: `[max(weights), sum(weights)]`; check = greedy count of days; first true. `O(n · log(sum))`, `O(1)`.

**Variant B — Maximise the minimum: Aggressive Cows / Magnetic Force Between Two Balls (LC 1552)**
- **Question.** Given `n` positions and `m` items, place them to **maximise the minimum** distance between any two. Return that distance.
- **Scenario.** *A festival organiser has 40 possible stall spots along a street and 6 vendors. She wants the closest pair of vendors to be as far apart as possible. How far apart is that?*
- **Pattern and cost.** Order the spots first (`O(n log n)`). Search the gap `d`; check = greedy: place the first vendor, then the next spot at least `d` away, count `≥ m`. A bigger `d` is harder ⇒ **last true**: `ans = mid; left = mid + 1`. `O(n log n + n · log(range))`, `O(1)` extra.

---

### 12. Sqrt(x) — LC 69

**Original question.** Given a non-negative integer `x`, return the integer square root rounded down, without using any built-in exponent or root function.

**Scenario.** *A garden planner has A square metres of turf and wants the largest whole-metre square plot it can fully cover. Report the side length; the planner's tool has no square-root button.*

**Ask first.**
1. Rounded down, or nearest?
2. How large can `A` be, and is `0` valid?

**Spot it.** The side length is the thing to find, and "does side `s` fit within `A`?" (`s × s ≤ A`) flips from true to false exactly once as `s` grows. Last true. Cheap `O(1)` check.

**Brute force.** Try 1, 2, 3, … until the square exceeds `x`: `O(√x)`.

**Solve** (from [12-sqrtx.md](03-binary-search-on-the-answer/12-sqrtx.md)):
```python
if x < 2: return x
left, right, res = 1, x // 2, 0
while left <= right:
    mid = (left + right) // 2
    square = mid * mid
    if square == x:  return mid
    elif square < x: res = mid; left = mid + 1     # valid floor; try bigger
    else:            right = mid - 1
return res
```

**Cost.** `O(log x)` time, `O(1)` space — about 30 iterations for 2³¹.

**Follow-up.** *"6 decimal places."* → Variant A. *"What about overflow of `mid * mid`?"* In C++/Java cast to `long` or compare `mid <= x // mid`.

**Variant A — Square root to a given precision**
- **Question.** Return `√x` as a float accurate within `10⁻⁶`.
- **Scenario.** *A tile shop needs the exact side of a square floor of area A to the nearest millimetre, using only multiplication.*
- **Pattern and cost.** Real-valued search: `lo = 0`, `hi = max(1, x)`; `while hi − lo > 1e-7: mid = (lo + hi) / 2; if mid * mid <= x: lo = mid else: hi = mid` (no `±1`: the answer is not an integer). Iterations ≈ `log₂((hi − lo) / eps)`; for `x = 10⁹`, `eps = 10⁻⁷` ≈ 47. `O(log(x / eps))` time, `O(1)` space.

**Variant B — Huge numbers / faster convergence** *(crosses into: Newton's method)*
- **Question.** Compute `⌊√x⌋` for an `x` with thousands of digits.
- **Scenario.** *A security tool must test whether a 2,000-digit number is a perfect square before using it in a cryptographic step.*
- **Pattern and cost.** Binary search still works but needs about `⌈log₂ x⌉` ≈ 6,600 big-number multiplies. Newton's iteration `r = (r + x // r) // 2` converges quadratically (~dozens of steps, a good starting guess). Name the trade: BS is simple and always correct; Newton is faster but needs a good start and care at the stopping condition. In Python `math.isqrt` does this for you.

---

## Part 5 — Common traps to say out loud

Saying these before writing code is half the interview signal.

| Trap | How it bites | Say or do |
|---|---|---|
| **Infinite loop from `mid ± 1`** | `lo = mid` with `mid = (lo + hi) // 2` never moves when `hi = lo + 1`; or `while lo <= hi` with `hi = mid` never ends | "`hi = mid - 1` goes with `lo <= hi`; `hi = mid` goes with `lo < hi`." Trace a 2-element input. |
| **Off-by-one on the final answer** | After the loop, is it `lo`, `hi`, `ans`, or `hi - 1`? With `lo <= hi` + `ans`, return `ans`; with `lo < hi`, return `lo`; for "last true" in `lo <= hi`, `hi` ends as the last true | "After the loop `lo` is the first index where the check is true (or `n` if none)." |
| **Integer overflow in `(lo + hi) / 2`** | In C++/Java `lo + hi` can pass `2³¹ − 1` | "I'd write `lo + (hi - lo) / 2`." (Python ints don't overflow, but say it.) Same for `mid * mid`: compare `mid <= x / mid`. |
| **Wrong bounds for the answer range** | Koko starting at `lo = 0` divides by zero; shipping starting at `lo = 1` is a rate that can never work; `hi = n − 1` loses "insert at the end" | `lo` = the smallest *legal* answer, `hi` = a value you can **prove** works. Koko: `[1, max]`. Ship: `[max(weights), sum]`. |
| **Duplicates breaking "found it"** | Returning on the first `==` gives *some* copy, not the first or last | "On a match I record and keep going left (first) or right (last)." |
| **First true vs last true** | Writing the "minimise" update for a "maximise" problem returns the wrong end | Ask: "am I looking for the smallest X that works, or the largest?" Min ⇒ `hi = mid`. Max ⇒ `ans = mid; lo = mid + 1`. |
| **Non-monotonic predicate** | Flaky tests, U-shaped cost, equal neighbours: the row flips more than once | "Before I commit, can I make `T F T`? If so it's not binary search." |
| **`mid + 1` out of range** | Peak and k-closest compare `mid` with a neighbour | Guard `mid + k < len(arr)` (#5) or note `mid < hi` so `mid + 1` exists (#9). |
| **Mixing the two loop forms** | Your write-ups use both Form 1 (`<=` + record `ans`) and Form 2 (`<` + `hi = mid`) | Pick one per problem and keep it consistent. Be able to write **both** for a boundary search. |
| **Empty or one-element input** | `n = 0` makes `hi = -1` or `m*n - 1 = -1` | State the empty case before coding, then trace a 1-element input. |
| **Searching unsorted data** | Binary search on data that isn't ordered returns garbage silently | "I should confirm the order. If it isn't ordered, I either sort once (many queries) or scan." |

---

## Part 6 — Known gaps

Important binary-search problems the repo does **not** have a write-up for yet (or has only as `TBD` in [problems.md](problems.md)).

| Gap | Why it matters | Pattern | Where it sits |
|---|---|---|---|
| **Single Element in a Sorted Array (LC 540)** | Parity trick: `nums[mid] == nums[mid ^ 1]` | Index-pair invariant | Stretch #14, `TBD` |
| **Capacity To Ship Packages (LC 1011)** | The canonical "minimise the maximum" | Search on answer + greedy check | Stretch #15, `TBD` (covered only as Variant A of #11) |
| **Split Array Largest Sum (LC 410)** | Hard version of #15; also solvable with DP | Search on answer / DP | Stretch #16, `TBD` |
| **Aggressive Cows / Magnetic Force (LC 1552)** | The only "**maximise the minimum**" shape; last-true update | Search on answer, last true | Not in repo (Variant B of #11) |
| **Find Smallest Divisor Given a Threshold (LC 1283)** / **Min Days to Make Bouquets (LC 1482)** | Same as Koko with a different check; good for reps | Search on answer | Not in repo |
| **Search in Rotated Sorted Array II (LC 81)** and **Find Min II (LC 154)** | Duplicates; the `O(n)` worst case is a common follow-up | Rotated + shrink on ties | Out of scope in problems.md |
| **Search in a Sorted Array of Unknown Size (LC 702)** / **Find in Mountain Array (LC 1095)** | "Unknown length / API only": doubling, then search | Search on a function | Out of scope in problems.md |
| **Kth Smallest in a Sorted Matrix (LC 378)** | BS on the value range with a staircase count | Search on answer, 2D check | Lives in the Heap repo |
| **Random Pick with Weight (LC 528)** | Prefix sums + lower bound; very Google-flavoured | Boundary over prefix sums | Out of scope in problems.md |
| **Search a 2D Matrix II (LC 240)** | Teaches **where flattening stops working** | Staircase (not BS) | Not in repo |
| **Find a Peak Element II (LC 1901)** | 2D peak: binary search rows, take max of the middle column | Uphill on a grid | Not in repo |
| **Minimise Max Distance to Gas Station (LC 774)** / **Real-valued answers** | Floating-point binary search, termination by epsilon or fixed iterations | Search on a real answer | Not in repo |
| **Find K-th Smallest Pair Distance (LC 719)** | BS on the answer with a two-pointer count | Search on answer + sliding window | Not in repo |
| **Plain lower_bound / upper_bound write-up** | Your files mostly use `left <= right` plus `ans`; the README's `lo < hi, hi = mid` boundary form has no standalone write-up | Form 2 | Doc gap, not a missing problem |

**Suggested order to close the gaps:** #15 (LC 1011) → LC 1552 → LC 410 → LC 540 → LC 81/154 → LC 702/1095 → LC 378 → the rest.

