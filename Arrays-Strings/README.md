# Arrays & Strings — Google Interview Study Repo

A small, readable set of notes for mastering **arrays and strings** for a Google SWE interview: hashing,
two pointers, sliding window, prefix sums, intervals, matrices, in-place tricks, greedy scans and string
parsing. It covers the array/string problems from LeetCode's Top Interview 150 and the NeetCode 150, plus a
few extras that come up often in Google-style interviews.

Binary Search, Stack, Heap and Linked List are their own topics and are not here. Trees, Graphs, DP and
Backtracking live in their own sibling repos.

Every file is built to be re-read in ~3 minutes and fully recalled — this is a reference you come back to,
not a one-time cram sheet.

---

## How to use this repo

1. Work through the topics in order, 1 → 9 (see [problems.md](problems.md)) — each topic in the repo root is
   its own folder. Do the **Core** problems first; **Stretch** problems are extra reps.
2. Each problem file is self-contained: it teaches its own idea from scratch, so you can jump straight to any
   single file later as a refresher.
3. Each topic folder has its own `README.md` with the pattern that topic follows, how to recognize a problem
   that belongs to it, and what changes from problem to problem. Start there when you're not sure which
   technique a question needs.
4. When you come back after weeks away, don't reread everything — open [problems.md](problems.md), scan the
   topic tables, and re-read just the file(s) covering whatever pattern you're rusty on.
5. There is no `concepts/` guide by default. If a topic ever needs a standalone primer, it gets added there
   explicitly.

Every problem file has the same header line (LC #, source, difficulty, priority, pattern) and the same six
sections, in the same order:

| Section | What you get |
|---|---|
| **1. Intuition** | A short story + bullets tied to specific lines of the code + a one-line **Recall** |
| **2. Approach** | The idea, the data structure or pointers used, the invariant (what stays true), and the edge cases |
| **3. Code** | The solution (any alternative approach sits under it as a sub-heading) |
| **4. Dry Run** | One small example, traced step by step |
| **5. Complexity** | Time and space, each with a one-line "why" based on the code |
| **6. Recall (30 seconds)** | Three bullets to re-read before an interview |

---

## House style

- **Explicit, state-meaningful names.** `left`, `right`, `write_index`, `window_start`, `seen`, `freq`,
  `prefix_sum`, `farthest` — never single letters except loop counters (`i`, `j`, `r`, `c`, `_`).
- **Type hints** on every function signature and return value.
- **State the edge cases up front:** empty input, one element, all elements equal, negatives, duplicates,
  already sorted. Ask the interviewer which of these can happen.
- **Every file names its approach and why:** hash lookup (trade space for time), two pointers (needs sorted or
  symmetric data), sliding window (needs a contiguous answer), prefix sum (handles negatives), in place
  (`O(1)` extra space).
- **Say what stays true.** For pointer and window problems, write the invariant in plain English — for
  example "everything left of `write_index` is already kept" or "the window never has a repeat".
- **Every problem file is runnable.** It ends with an `if __name__ == "__main__":` block of `assert`s
  against the examples from the problem statement.

---

## Pattern-recognition cheat sheet

Read the prompt, match a phrase, reach for the pattern.

| If the problem says... | Reach for | Core template / key line |
|---|---|---|
| "duplicate", "does it appear twice", "have I seen this" | **Hash set** of what you've seen | `if x in seen: return True; seen.add(x)` |
| "two numbers that add up to a target" (unsorted) | **Hash map**: look up the complement | `if target - x in seen: return [seen[target - x], i]` |
| "anagram", "same letters", "count each character" | **Frequency count** (`Counter` or a 26-slot array) | `counts[ch] += 1` |
| "group items that are equivalent" | **Canonical key** in a dict | `groups[tuple(sorted(word))].append(word)` |
| "top k frequent" | **Count, then bucket by frequency** | `buckets[count].append(value)` |
| "longest run of consecutive numbers" | **Set, start only at the beginning of a run** | `if x - 1 not in nums: ...count up...` |
| "sorted array, find a pair / triplet" | **Two pointers** from both ends | `if total < target: left += 1 else: right -= 1` |
| "palindrome", "compare from both ends" | **Two pointers** moving inward | `while left < right: ...` |
| "longest / shortest substring or subarray that ..." | **Sliding window** — grow right, shrink left when invalid | `while window_is_invalid: ...; left += 1` |
| "window of size k" | **Fixed window** — add one, remove one | `add nums[right]; remove nums[right - k]` |
| "max in every window of size k" | **Monotonic deque** | pop smaller values from the back |
| "subarray sums to k" (negatives allowed) | **Prefix sum + hash map** | `answer += counts[prefix - k]` |
| "max sum subarray" | **Kadane** | `curr = max(x, curr + x)` |
| "product / sum of everything except this one" | **Prefix and suffix passes** | `result[i] = prefix[i - 1] * suffix[i + 1]` |
| "merge / overlap / meeting rooms / intervals" | **Sort by start**, compare with the last one | `if start <= last_end: merge` |
| "fewest intervals to remove / arrows to burst" | **Sort by end**, keep the earliest-ending | `if start >= last_end: keep` |
| "rotate / spiral / in place" (2D) | **Transpose + reverse**, or peel layers | `matrix[r][c], matrix[c][r] = matrix[c][r], matrix[r][c]` |
| "in place", "return the new length", "O(1) extra space" | **Read / write pointers** | `if keep: nums[write] = nums[read]; write += 1` |
| "can you reach the end", "minimum jumps", "circular route" | **Greedy scan** with a running summary | `farthest = max(farthest, i + nums[i])` |
| "parse", "convert", "without built-in", "simulate the rules" | **Careful scan** — build in a list, `join` at the end | handle sign, spaces, overflow, empty input |

Quick decision test when you're stuck:

- Is the answer a **contiguous chunk**? Yes → sliding window (all positive) or prefix sum + hash map (negatives allowed).
- Is the input **sorted** or symmetric? → two pointers.
- Do you only need to know **"have I seen this?"** → hash set or map.
- Must you use **`O(1)` extra space**? → two pointers, read / write pointers, or in-place tricks.
- Does the question involve **[start, end] pairs**? → sort them first.

---

## Problem index

The full topic-by-topic problem list — with each problem's source (LC150 / NC150 / both / Claude addition),
LeetCode number, difficulty, priority (Core / Stretch), status, and a link to its file — lives in
**[problems.md](problems.md)**.

That file is the single tracker and the single source of truth; this README deliberately does not repeat the
checklist. Each topic gets its own folder in the repo root (e.g. `01-arrays-and-hashing/`), and the problem
write-ups (`01`–`80`, global numbering) live inside it.

---

## Complexity quick-reference

Almost every array/string problem starts with a brute force that is `O(n²)` (or worse) and gets a better
bound by **remembering something** or **not looking twice**.

- **Hash map / set:** `O(n)` time, `O(n)` space. You trade memory for speed: every lookup becomes `O(1)`
  instead of a scan.
- **Two pointers:** `O(n)` time, `O(1)` space — each pointer only moves one way, so the total moves are at
  most `n`. Sorting first adds `O(n log n)`.
- **Sliding window:** `O(n)` time — `right` moves `n` times and `left` moves at most `n` times in total, so
  the inner `while` loop doesn't make it `O(n²)`. Space is the window state (`O(k)` for `k` distinct items).
- **Prefix sum:** `O(n)` to build, then `O(1)` per range query. With a hash map it finds subarray sums in
  one pass.
- **Sorting-based (intervals, 3Sum):** `O(n log n)` — the sort dominates the scan that follows.
- **In place:** `O(1)` extra space, but you must be careful about overwriting values you still need — that is
  why merging fills from the back.
- **Strings are immutable in Python.** `s += ch` inside a loop copies the string each time (`O(n²)` total).
  Collect pieces in a list and `"".join(...)` once at the end.
- **Say the trade-off out loud.** "Sorting costs `O(n log n)` but lets me use two pointers with no extra
  space" is the kind of sentence interviewers listen for.
