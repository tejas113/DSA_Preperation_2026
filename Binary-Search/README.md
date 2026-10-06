# Binary Search — Google Interview Study Repo

A small, readable set of notes for mastering **binary search** for a Google SWE interview: exact and boundary
searches, 2D matrices, rotated arrays, peak finding, partition search, and search-on-the-answer. It covers the
binary-search problems from LeetCode's Top 150 and the NeetCode 150, plus a few extras that come up often in
Google-style interviews.

Every file is built to be re-read in ~3 minutes and fully recalled — this is a reference you come back to,
not a one-time cram sheet.

---

## How to use this repo

1. Work through the topics in order, 1 → 3 (see [problems.md](problems.md)) — each topic in the repo root is
   its own folder. Do the **Core** problems first; **Stretch** problems are extra reps.
2. Each problem file is self-contained, so you can jump straight to any single file later as a refresher.
3. Each topic folder has its own `README.md` with the pattern that topic follows, how to recognize a problem
   that belongs to it, and what changes from problem to problem.
4. When you come back after weeks away, open [problems.md](problems.md), scan the topic tables, and re-read
   just the file(s) covering whatever pattern you're rusty on.

Every problem file has the same header line (LC #, source, difficulty, priority, pattern) and the same six
sections, in the same order:

| Section | What you get |
|---|---|
| **1. Intuition** | A short story + bullets tied to specific lines of the code + a one-line **Recall** |
| **2. Search Space & Condition** | What `lo` and `hi` mean, the test that decides which half to keep, the loop form, and the edge cases |
| **3. Code** | The solution (any alternative approach sits under it as a sub-heading) |
| **4. Dry Run** | One small example, traced step by step (`lo`, `hi`, `mid` at each step) |
| **5. Complexity** | Time and space, each with a one-line "why" based on the code |
| **6. Recall (30 seconds)** | Three bullets to re-read before an interview |

---

## House style

- **Explicit names.** `lo`, `hi`, `mid`, `left`, `right`, `feasible(...)`, `min_speed` — never cryptic letters.
- **Type hints** on every function signature and return value.
- **Say what `lo` and `hi` mean** in plain English before any code, and which of the two loop forms you use.
- **Name the invariant.** For example: "the answer is always inside `[lo, hi]`", or "everything left of `lo`
  fails the condition".
- **State the edge cases up front:** empty array, one element, target smaller or larger than everything,
  duplicates, and a rotation of 0.
- **Every problem file is runnable.** It ends with an `if __name__ == "__main__":` block of `assert`s
  against the examples from the problem statement.

---

## The two loop forms (learn these cold)

```python
# Form 1 — exact match:  the answer is mid itself, so the range shrinks past mid on both sides
lo, hi = 0, len(nums) - 1
while lo <= hi:
    mid = (lo + hi) // 2
    if nums[mid] == target: return mid
    if nums[mid] < target:  lo = mid + 1
    else:                   hi = mid - 1
return -1

# Form 2 — boundary:  find the FIRST index where a condition is true;  mid might be the answer
lo, hi = 0, len(nums)               # hi = len(nums) means "no such index"
while lo < hi:
    mid = (lo + hi) // 2
    if <condition true at mid>: hi = mid          # keep mid
    else:                       lo = mid + 1      # drop mid
return lo
```

If you write `hi = mid` you must use `while lo < hi`; if you write `hi = mid - 1` you must use `while lo <= hi`.
Mixing them is the usual cause of an infinite loop.

---

## Pattern-recognition cheat sheet

| If the problem says... | Reach for | Core template / key line |
|---|---|---|
| "sorted array, find the target" | **Exact-match binary search** | Form 1 |
| "first / last position", "insert position", "first bad version" | **Boundary search** | Form 2 with `nums[mid] >= target` |
| "sorted 2D matrix" | **Flatten the index** | `row, col = mid // cols, mid % cols` |
| "k closest elements" | **Search the window start** | compare `x - arr[mid]` with `arr[mid + k] - x` |
| "latest value at or before time t" | **Boundary search over timestamps** | `bisect_right(times, t) - 1` |
| "rotated sorted array" | **One half is always sorted** | `if nums[lo] <= nums[mid]: left half sorted` |
| "minimum in a rotated array" | **Compare with the right end** | `if nums[mid] > nums[hi]: lo = mid + 1 else: hi = mid` |
| "peak element" | **Move uphill** | `if nums[mid] < nums[mid + 1]: lo = mid + 1 else: hi = mid` |
| "median of two sorted arrays" | **Search the cut** in the smaller array | left halves ≤ right halves |
| "minimum speed / capacity / days such that ..." | **Search on the answer** with a feasibility check | `if feasible(mid): hi = mid else: lo = mid + 1` |
| "integer square root", "nth root" | **Search the answer range** | largest `x` with `x * x <= n` |

Quick decision test when you're stuck:

- Is the input **sorted** (or rotated, or a mountain)? → search the array.
- Is the question **"smallest X such that ..."** or **"largest X such that ..."** with a yes/no test?
  → search the answer. The test must be monotonic: once it passes, it keeps passing for bigger values (or the
  other way round).
- Do you need the **first / last** index where something holds? → boundary search (Form 2).

---

## Problem index

The full topic-by-topic problem list — with each problem's source, LeetCode number, difficulty, priority,
status, and a link to its file — lives in **[problems.md](problems.md)**.

That file is the single tracker and the single source of truth; this README deliberately does not repeat the
checklist. Each topic gets its own folder in the repo root (e.g. `01-binary-search-on-sorted-sequences/`),
and the problem write-ups (`01`–`16`, global numbering) live inside it.

---

## Complexity quick-reference

- **Searching an array: `O(log n)` time, `O(1)` space.** The range halves every step, so it takes about
  `log₂ n` steps — about 30 for a billion items.
- **Search on the answer: `O(n · log(range))`.** Each guess costs one feasibility pass over the input (`O(n)`),
  and there are `log(range)` guesses.
- **Median of two sorted arrays: `O(log(min(m, n)))`.** You only binary search the smaller array.
- **The array must be sorted (or have a monotonic test).** Sorting first costs `O(n log n)`, which usually
  defeats the point unless you search many times.
- **Watch the off-by-one.** Most binary-search bugs are a wrong loop condition, a wrong `hi` (`n` vs `n - 1`),
  or `lo = mid` without rounding up. Trace a 1-element and a 2-element array before you finish.
- **Python has `bisect`.** `bisect_left` and `bisect_right` are Form 2. Know them, but write the loop by hand
  in an interview unless the interviewer says otherwise.
