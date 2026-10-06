# Heap / Priority Queue — Google Interview Study Repo

A small, readable set of notes for mastering **heaps** for a Google SWE interview: top-k and kth element,
scheduling with a heap, and the two-heap median. It covers the heap problems from LeetCode's Top 150 and the
NeetCode 150, plus a few extras that come up often in Google-style interviews.

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
| **2. What the Heap Holds** | Min-heap or max-heap, what each entry is, the size limit, and what you pop |
| **3. Code** | The solution (any alternative approach sits under it as a sub-heading) |
| **4. Dry Run** | One small example, showing the heap after every step |
| **5. Complexity** | Time and space, each with a one-line "why" based on the code |
| **6. Recall (30 seconds)** | Three bullets to re-read before an interview |

---

## House style

- **Explicit names.** `heap`, `min_heap`, `max_heap`, `lower_half`, `upper_half`, `cooldown_queue` — never `h`, `q`.
- **Type hints** on every function signature and return value.
- **Say which heap and why** before any code: min or max, what one entry looks like (a number, a tuple), and
  whether the heap is capped at size `k`.
- **Remember Python's `heapq` is a min-heap.** For a max-heap, push the negative (`-x`) and negate on the way
  out. Say this out loud so it doesn't look like a mistake.
- **Tuples compare left to right.** `(priority, tie_break, item)` — the tie-break stops Python from comparing
  the items themselves (which may not be comparable).
- **State the edge cases up front:** `k` larger than the input, an empty input, all values equal, and ties.
- **Every problem file is runnable.** It ends with an `if __name__ == "__main__":` block of `assert`s
  against the examples from the problem statement.

---

## Pattern-recognition cheat sheet

| If the problem says... | Reach for | Core template / key line |
|---|---|---|
| "kth largest", "top k largest" | **Min-heap of size k** — the root is the kth largest | `heappush(heap, x); if len(heap) > k: heappop(heap)` |
| "kth smallest", "k smallest" | **Max-heap of size k** (negate values) | `heappush(heap, -x); if len(heap) > k: heappop(heap)` |
| "k closest to a point" | **Max-heap of size k** on the distance | push `(-distance, point)` |
| "top k frequent" | **Count, then a heap on the counts** | `heappush(heap, (count, item))` |
| "merge k sorted lists / arrays" | **Min-heap of the current heads** | push `(value, list_index, position)` |
| "repeatedly take the largest / smallest" | **Heap simulation** | `heappop` → process → `heappush` what's left |
| "cooldown", "no two adjacent the same" | **Max-heap of counts** + a holding area for the item just used | hold the last item back for one round |
| "median of a stream" | **Two heaps** — max-heap for the lower half, min-heap for the upper half | keep sizes equal or differing by 1 |
| "streaming top k" | **Min-heap of size k** | `if x > heap[0]: heapreplace(heap, x)` |

Quick decision test when you're stuck:

- Do you need the **best `k`** of something, without sorting everything? → a size-`k` heap.
- Do you need the **current best** item over and over as items come and go? → heap.
- Do you need the **middle** of changing data? → two heaps.
- Would **sorting once** do the job? → then you probably don't need a heap.

---

## Problem index

The full topic-by-topic problem list — with each problem's source, LeetCode number, difficulty, priority,
status, and a link to its file — lives in **[problems.md](problems.md)**.

That file is the single tracker and the single source of truth; this README deliberately does not repeat the
checklist. Each topic gets its own folder in the repo root (e.g. `01-top-k-and-kth-element/`), and the
problem write-ups (`01`–`12`, global numbering) live inside it.

---

## Complexity quick-reference

- **`heappush` and `heappop` are `O(log n)`.** Peeking at the root (`heap[0]`) is `O(1)`.
- **`heapify` a list is `O(n)`,** faster than pushing `n` items one by one (`O(n log n)`).
- **Top-k with a size-`k` heap is `O(n log k)`** time and `O(k)` space. That beats sorting (`O(n log n)`)
  when `k` is much smaller than `n`.
- **Quickselect** finds the kth element in `O(n)` on average (`O(n²)` worst case) — a follow-up for Kth
  Largest Element in an Array.
- **Two heaps:** adding a number is `O(log n)`; reading the median is `O(1)`.
- **Say the trade-off out loud.** "A heap of size `k` keeps memory small and lets me handle a stream; sorting
  is simpler but needs all the data" is the kind of sentence interviewers listen for.
