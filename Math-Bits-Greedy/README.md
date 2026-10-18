# Math, Bits & Greedy — Google Interview Study Repo

A small, readable set of notes for the smaller **math, bit-manipulation and greedy** topics for a Google SWE
interview: XOR and bit tricks, digit and number arithmetic, fast exponentiation, the sieve, random-number
tricks, and a few greedy patterns. It covers the problems from LeetCode's Top 150 and the NeetCode 150 that
don't fit any other repo, plus two extras that come up in Google-style interviews.

Every file is built to be re-read in ~3 minutes and fully recalled — this is a reference you come back to,
not a one-time cram sheet.

---

## How to use this repo

1. Work through the topics in order, 1 → 3 (see [problems.md](problems.md)) — each topic in the repo root is
   its own folder. Do the **Core** problems first; **Stretch** problems are extra reps.
2. These topics come up less often than arrays, trees or graphs. If you're short on time, learn the Core
   problems in Topic 1 and the tricks in the cheat sheet below, and skim the rest.
3. Each problem file is self-contained, so you can jump straight to any single file later as a refresher.
4. Each topic folder has its own `README.md` with the pattern that topic follows, how to recognize a problem
   that belongs to it, and what changes from problem to problem.

Every problem file has the same header line (LC #, source, difficulty, priority, pattern) and the same six
sections, in the same order:

| Section | What you get |
|---|---|
| **1. Intuition** | A short story + bullets tied to specific lines of the code + a one-line **Recall** |
| **2. Approach** | The idea, the trick it relies on, what stays true, and the edge cases |
| **3. Code** | The solution (any alternative approach sits under it as a sub-heading) |
| **4. Dry Run** | One small example, traced step by step (show bits in binary where relevant) |
| **5. Complexity** | Time and space, each with a one-line "why" based on the code |
| **6. Recall (30 seconds)** | Three bullets to re-read before an interview |

---

## House style

- **Explicit names.** `mask`, `carry`, `result`, `bit_count`, `last_index`, `open_low`, `open_high` — never `a`, `b`, `c`.
- **Type hints** on every function signature and return value.
- **Show numbers in binary** in dry runs (`0b1011`) whenever bits are involved.
- **Name the trick in one sentence** before the code, for example "`n & (n - 1)` clears the lowest set bit".
- **State the edge cases up front:** zero, negative numbers, overflow (`-2**31` to `2**31 - 1`), and empty
  input. Python integers don't overflow, so 32-bit problems need an explicit mask (`& 0xFFFFFFFF`).
- **Every problem file is runnable.** It ends with an `if __name__ == "__main__":` block of `assert`s
  against the examples from the problem statement.

---

## Bit tricks to know cold

| Trick | What it does | Used in |
|---|---|---|
| `a ^ a == 0`, `a ^ 0 == a` | Equal values cancel | Single Number, Missing Number |
| `n & (n - 1)` | Clears the lowest set bit | Number of 1 Bits, power of two |
| `n & -n` | Isolates the lowest set bit | Bitmask problems, Fenwick trees |
| `n >> 1`, `n << 1` | Divide / multiply by 2 | Counting Bits, Reverse Bits |
| `(n >> i) & 1` | Read bit `i` | Reverse Bits, Single Number II |
| `a ^ b` and `(a & b) << 1` | Sum without carry, and the carry | Sum of Two Integers |
| `n & (n - 1) == 0` (and `n > 0`) | `n` is a power of two | Many easy questions |

---

## Pattern-recognition cheat sheet

| If the problem says... | Reach for | Core template / key line |
|---|---|---|
| "every element appears twice except one" | **XOR everything** | `result ^= x` |
| "count the 1 bits" | **Clear the lowest bit until zero** | `while n: n &= n - 1; count += 1` |
| "add without using `+`" | **XOR + carry loop** | `a, b = a ^ b, (a & b) << 1` |
| "reverse the digits / bits" | **Peel and rebuild** | `result = result * 10 + x % 10` (or shift bits) |
| "x to the power n" | **Fast exponentiation** | square the base, halve the exponent |
| "count primes below n" | **Sieve of Eratosthenes** | cross out multiples starting at `p * p` |
| "random from another random" | **Rejection sampling** | build a bigger uniform range, re-roll the unusable values |
| "cut into as few groups as possible" | **Last-occurrence greedy** | `end = max(end, last[ch])`, cut when `i == end` |
| "`*` can be anything" (wildcards) | **Track a range of possibilities** | `low` and `high` counts |

Quick decision test when you're stuck:

- Do pairs of equal values need to **disappear**? → XOR.
- Do you need to **process a number digit by digit**? → `% 10` and `// 10` (or shifts for bits).
- Is a brute force **`O(n²)` on a number range**? → look for a sieve, or a number-theory shortcut.

---

## Problem index

The full topic-by-topic problem list — with each problem's source, LeetCode number, difficulty, priority,
status, and a link to its file — lives in **[problems.md](problems.md)**.

That file is the single tracker and the single source of truth; this README deliberately does not repeat the
checklist. Each topic gets its own folder in the repo root (e.g. `01-bit-manipulation/`), and the problem
write-ups (`01`–`22`, global numbering) live inside it.

---

## Complexity quick-reference

- **Bit tricks are `O(1)` per operation.** Looping over the bits of a 32-bit number is `O(32)`, which is `O(1)`.
- **Counting bits with `n & (n - 1)`** runs once per set bit, not once per bit — faster on sparse numbers.
- **Fast exponentiation is `O(log n)`,** versus `O(n)` for repeated multiplication.
- **The Sieve of Eratosthenes is `O(n log log n)`** time and `O(n)` space. Trial division for each number is
  about `O(n√n)`.
- **Digit peeling is `O(log₁₀ n)`** — one step per digit.
- **Rejection sampling** has an expected cost that is constant, but no worst-case bound. Say so if asked.
- **Say the trade-off out loud.** "XOR needs no extra memory, where a hash set would use `O(n)`" is the kind
  of sentence interviewers listen for.
