# Linked List — Google Interview Study Repo

A small, readable set of notes for mastering **linked lists** for a Google SWE interview: reversing, fast and
slow pointers, merging, dummy nodes, deep copying, and the LRU cache. It covers the linked-list problems from
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
| **2. Pointers & Invariant** | Which pointers you use and what each one means, what stays true at every step, and the edge cases |
| **3. Code** | The solution (any alternative approach sits under it as a sub-heading) |
| **4. Dry Run** | One small list, traced pointer by pointer |
| **5. Complexity** | Time and space, each with a one-line "why" based on the code |
| **6. Recall (30 seconds)** | Three bullets to re-read before an interview |

---

## House style

- **Explicit names.** `prev`, `curr`, `next_node`, `slow`, `fast`, `dummy`, `tail`, `head` — never `p`, `q`, `t`.
- **Type hints** on every function signature and return value, using `Optional[ListNode]`.
- **Every file includes the small `ListNode` class** plus two helpers, `build_list(values)` and
  `to_list(head)`, so the asserts can run on plain Python lists.
- **Say what each pointer means** before any code, and what stays true after each step.
- **Draw the pointer moves.** Dry runs show the list as `1 → 2 → 3 → None` with the pointers marked.
- **State the edge cases up front:** empty list, one node, two nodes, the head being removed, a cycle that
  includes the head, and lists of different lengths.
- **Every problem file is runnable.** It ends with an `if __name__ == "__main__":` block of `assert`s
  against the examples from the problem statement.

---

## Pattern-recognition cheat sheet

| If the problem says... | Reach for | Core template / key line |
|---|---|---|
| "reverse the list" (or part, or groups) | **Three pointers** | `next_node = curr.next; curr.next = prev; prev, curr = curr, next_node` |
| "find the middle" | **Slow / fast** | `slow = slow.next; fast = fast.next.next` |
| "is there a cycle" / "where does it start" | **Floyd's algorithm** | slow and fast meet → reset one to `head`, move both by 1 |
| "n-th node from the end" | **Gap pointers** | move `fast` n steps ahead, then move both |
| "palindrome" / "reorder" | **Middle + reverse second half** | find the middle, reverse from there, then compare or interleave |
| "merge two sorted lists" | **Dummy node + tail** | `tail.next = smaller; tail = tail.next` |
| "the head might be removed / changed" | **Dummy node before the head** | `dummy = ListNode(0, head)` … `return dummy.next` |
| "add numbers digit by digit" | **Walk both lists with a carry** | `total = a + b + carry; carry = total // 10` |
| "merge k sorted lists" | **Min-heap of heads**, or divide and conquer | heap of `(value, index, node)` |
| "sort a linked list" | **Merge sort** | find middle, split, sort halves, merge |
| "two lists that share a tail" | **Switch heads at the end** | `a = a.next if a else headB` |
| "deep copy with random pointers" | **Map old node → new node** | `copies[node] = Node(node.val)` |
| "O(1) get and put with eviction" | **Hash map + doubly linked list** | map key → node; move node to the front on every use |

Quick decision test when you're stuck:

- Do you need the **head** to possibly change? → add a dummy node.
- Do you need something **from the end** or the **middle** in one pass? → slow/fast or gap pointers.
- Do you need **random access** to a node? → add a hash map.
- Are you **rewiring** `next` pointers? → save `next_node` *before* you overwrite `curr.next`.

---

## Problem index

The full topic-by-topic problem list — with each problem's source, LeetCode number, difficulty, priority,
status, and a link to its file — lives in **[problems.md](problems.md)**.

That file is the single tracker and the single source of truth; this README deliberately does not repeat the
checklist. Each topic gets its own folder in the repo root (e.g. `01-reversal-and-rewiring/`), and the problem
write-ups (`01`–`20`, global numbering) live inside it.

---

## Complexity quick-reference

- **Most pointer problems are `O(n)` time and `O(1)` space.** You visit each node a constant number of times
  and only keep a few pointers.
- **Recursion costs `O(n)` stack.** A recursive reverse is elegant, but it uses `O(n)` space and can hit the
  recursion limit on long lists. Prefer the iterative version unless asked.
- **Slow / fast is still `O(n)`.** The fast pointer moves twice as far, but the loop ends after about `n / 2`
  steps.
- **Merging `k` lists** costs `O(N log k)` with a heap or divide and conquer, where `N` is the total number of
  nodes. Merging them one after another costs `O(N · k)`.
- **A dummy node costs `O(1)` space** and removes a whole class of head-related bugs.
- **LRU Cache:** `get` and `put` are both `O(1)` because the hash map finds the node and the doubly linked
  list moves it in constant time.
- **Say the trade-off out loud.** "A hash map makes the copy `O(n)` space but simple; interleaving nodes makes
  it `O(1)` space but trickier" is the kind of sentence interviewers listen for.
