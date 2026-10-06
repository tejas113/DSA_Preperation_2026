# Stack — Google Interview Study Repo

A small, readable set of notes for mastering **stacks** for a Google SWE interview: bracket matching, nested
decoding, monotonic stacks, expression evaluation, and stack-based design. It covers the stack problems from
LeetCode's Top 150 and the NeetCode 150, plus a few extras that come up often in Google-style interviews.

Every file is built to be re-read in ~3 minutes and fully recalled — this is a reference you come back to,
not a one-time cram sheet.

---

## How to use this repo

1. Work through the topics in order, 1 → 4 (see [problems.md](problems.md)) — each topic in the repo root is
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
| **2. What the Stack Holds** | What gets pushed, when it gets popped, and what order the stack guarantees |
| **3. Code** | The solution (any alternative approach sits under it as a sub-heading) |
| **4. Dry Run** | One small example, showing the stack after every step |
| **5. Complexity** | Time and space, each with a one-line "why" based on the code |
| **6. Recall (30 seconds)** | Three bullets to re-read before an interview |

---

## House style

- **Explicit names.** `stack`, `open_brackets`, `next_greater`, `running_result`, `operand_stack` — never `s`, `st`.
- **Type hints** on every function signature and return value.
- **Say what the stack holds** in plain English before any code: values or indices? pairs? what does the top
  mean?
- **Always guard the pop.** Write `if stack` before `stack[-1]` and `stack.pop()`, and say what an empty stack
  means for the answer.
- **State the edge cases up front:** empty input, one element, everything increasing, everything decreasing,
  and unmatched or extra brackets.
- **Every problem file is runnable.** It ends with an `if __name__ == "__main__":` block of `assert`s
  against the examples from the problem statement.

---

## Pattern-recognition cheat sheet

| If the problem says... | Reach for | Core template / key line |
|---|---|---|
| "valid brackets", "matching pairs" | **Stack of open brackets** | `if ch in "([{": stack.append(ch) else: pop and compare` |
| "nested", "decode", "simplify a path" | **Stack of partial results** | push the state on `[`, restore it on `]` |
| "next greater / smaller element" | **Monotonic stack** of indices | `while stack and nums[stack[-1]] < x: answer[stack.pop()] = x` |
| "how many days until warmer" | **Monotonic decreasing stack** | pop colder days; the gap is `i - j` |
| "largest rectangle", "histogram" | **Monotonic increasing stack** with widths | pop taller bars; width = `i - stack[-1] - 1` |
| "evaluate an expression" | **Operand stack** | pop two, apply the operator, push the result |
| "operator precedence" | **Apply `*` and `/` at once; push `+` and `-` as signed numbers** | `stack.append(-num)` for `-` |
| "parentheses in an expression" | **Push the running result and sign, restart inside** | `stack.append(result); stack.append(sign)` |
| "get the min in O(1)" | **Store `(value, min_so_far)`** | `stack.append((x, min(x, stack[-1][1])))` |
| "queue using stacks" | **Two stacks:** `in` and `out` | move `in` → `out` only when `out` is empty |
| "collisions / survivors" | **Stack of survivors** | compare the new item with the top until it survives or is destroyed |

Quick decision test when you're stuck:

- Is there a **last-in-first-out** flavor — the most recent unfinished thing is the next one to resolve? →
  stack.
- Does each element want **the nearest element to its left or right that is bigger or smaller**? → monotonic
  stack.
- Are there **brackets or nesting**? → stack of pending items.

---

## Problem index

The full topic-by-topic problem list — with each problem's source, LeetCode number, difficulty, priority,
status, and a link to its file — lives in **[problems.md](problems.md)**.

That file is the single tracker and the single source of truth; this README deliberately does not repeat the
checklist. Each topic gets its own folder in the repo root (e.g. `01-stack-as-pending-items/`), and the
problem write-ups (`01`–`12`, global numbering) live inside it.

---

## Complexity quick-reference

- **Most stack problems are `O(n)` time and `O(n)` space.** Each element is pushed once and popped at most once.
- **Monotonic stacks look nested but are `O(n)`.** The `while` loop inside the `for` loop pops each element at
  most once in total, so the pops across the whole run add up to at most `n`. This is the same argument as a
  sliding window.
- **Min Stack** is `O(1)` for every operation, at the cost of `O(n)` extra space for the minimums.
- **Queue using two stacks** is `O(1)` amortized per operation: each element moves from `in` to `out` at most
  once.
- **Expression evaluation** is `O(n)` in the length of the expression.
- **A brute force for "next greater" is `O(n²)`.** Saying "I can do it in one pass with a monotonic stack" is
  the sentence interviewers want to hear.
