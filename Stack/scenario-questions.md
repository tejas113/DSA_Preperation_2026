# Stack: Scenario Question Bank (Google L3 style)

Google doesn't say "use a stack" or "monotonic stack". It gives a short, vague scenario, and **you** have to notice that "the most recent unfinished thing is the next one to resolve" or "each item is waiting for the nearest bigger one" is a stack problem, and work out what goes on it.
This file has one scenario per solved problem in this repo, plus two more variants of each, so you practise the *recognition* step and not just the solution.
Problem numbers match [problems.md](problems.md). The repo has write-ups for 9 of the 12 tracked problems; #8, #10 and #11 are still **TBD** in the tracker, so they appear here as variants and in the gaps list (Part 6) instead of as their own entries.

**Disguised on purpose:** scenarios avoid words like "stack", "brackets", "nested", "next greater", "monotonic" and "histogram" when those words would give the technique away. Each one has an **Ask first** line (the clarifying questions a good candidate asks), a **Spot it** line (the clue that gives the stack away), and a **Brute force** line (so you can say what the stack improves).

**How to use:** read only the **Scenario** line, then say out loud: *what is "pending" or "waiting" here, and what event resolves it? what would I do with pencil and paper? what is the brute force and what work does it repeat?* Only then read the rest. About half of the variants deliberately cross over into a neighbouring technique (a plain counter, two pointers, a heap, a deque, recursion, DP) so you learn where a stack stops being the right tool.

---

## Part 1. The 5-step "Is this a stack problem?" framework

1. **Smell test: is there a last-in-first-out flavour?** Ask: *"is the most recent unfinished thing the next one to be resolved?"* Typical signs:
   - **Matching pairs** that must close in reverse order (brackets, tags, nested blocks).
   - **Undo / backtrack to the last state** (`..` in a path, a collision that removes the previous item, going back to the last saved result).
   - **"Nearest bigger / smaller / warmer to the left or right"** for every element. Each element waits for the first later element that beats it.
   - **Evaluating an expression** where an operator needs the two most recent operands.
   - **A data structure with an extra `O(1)` query** (current minimum, most frequent) layered on top of push and pop.

2. **Name what is on the stack.** Complete: *"The stack holds ___. I push when ___. I pop when ___, and each pop tells me ___."*
   - **Pending openers:** characters or tokens still waiting for their closer (#1).
   - **Path parts / survivors:** the current valid chain (#2, #4).
   - **A saved state:** the text built so far and a repeat count, to restore after a closer (#3).
   - **Indices (or values) waiting for a bigger or smaller one:** a monotonic stack (#5, #6).
   - **Fleet arrival times:** the stack summarises groups that already merged (#7).
   - **Operands:** every operator takes the top one or two (#9).
   - **`(value, extra info)` pairs:** the answer to the extra query travels with each entry (#12).

3. **Choose the shape, and check a cheaper tool.**
   - **Single bracket type, only validity needed:** a **counter** is enough (no stack). Several bracket types, or you need positions: a stack.
   - **Nearest bigger/smaller:** a **monotonic stack**. Decide *decreasing* (next greater) or *increasing* (next smaller) and whether it stores **values or indices**. Indices when you need distances or widths.
   - **Max or min of each window:** a **monotonic deque**, because items also leave from the front.
   - **Recursive structure** (nested expressions, trees): recursion is an implicit stack. Use an explicit stack to avoid Python's recursion limit (about 1000).
   - **Need the best of a changing set, not the most recent:** a **heap**, not a stack.

4. **Write the loop and the invariant.**
   - **Pending items:** `for each token: if opener, push; elif closer, pop and check`. *Invariant:* the stack holds exactly the items still waiting.
   - **Monotonic:** `while stack and x beats stack[-1]: pop and record the answer for it; then push x`. *Invariant:* the stack is sorted in one direction, and every item on it is still waiting.
   - **Expression:** `number → push; operator → pop two, apply, push`.
   - Say the invariant in plain English before coding. Say what is left on the stack at the end and what that means (leftover openers mean invalid; leftover indices mean "no answer, so `0` or `-1`").

5. **Cost: say it before you code.**
   - **Every element is pushed once and popped at most once, so the whole thing is `O(n)`**, even when a `while` sits inside the `for`. This is the same amortised argument as a sliding window.
   - Space is `O(n)` in the worst case (all openers, a strictly decreasing array).
   - Name any hidden cost: sorting first (`O(n log n)`, Car Fleet), repeated string concatenation (Decode String), or `min()` per push.

**Say-it-out-loud template:** *"Each [item] has to wait for [its closer / the next bigger value / its second operand]. So I keep a stack of the waiting [items]. When [the resolving event] arrives, I pop everything it resolves. Each element is pushed once and popped at most once, so `O(n)` time and `O(n)` space. The brute force looks to the right from every element: `O(n²)`."*

**Questions to ask the interviewer (cheap and impressive):**
- **Input:** Can the input be empty or have one element? Can it contain characters other than the ones I expect?
- **Validity:** Is the input guaranteed well-formed, or must I validate it (an operator with too few operands, an unmatched `]`)?
- **Ties:** For "next greater", does *equal* count as greater? (strict `>` vs `>=`)
- **Output:** The values, the indices, or the distances? What should I return when there is no answer (`0`, `-1`, `None`)?
- **Wrap-around:** Is the array circular?
- **Streaming:** Do the items arrive one at a time and must I answer after each? (decides whether I can look ahead)
- **Size:** How large can `n` get, and how deep can nesting go? (recursion limits, output size)
- **Arithmetic:** Integer division, and does it truncate toward zero or floor? Can values overflow?
- **Mutation / space:** May I modify the input? Is `O(1)` extra space required (then a stack isn't allowed)?

---

## Part 2. Signal → technique cheat sheet

Problem numbers match [problems.md](problems.md). **gap** means the repo has no write-up for it yet (see Part 6). Techniques owned by other repos are named so you still recognise them.

| What the question says | It is really | Technique | Problems |
|---|---|---|---|
| "every opener must be closed by the right closer, in the right order" | pending openers, resolved in reverse | **stack of openers** (a counter if there's only one kind) | 1 |
| "normalise a path", "`..` goes up one level" | a chain where `..` undoes the last step | **stack of parts**, `..` pops | 2 |
| "expand `3[ab2[c]]`", "repeat the enclosed part" | save the state at `[`, restore it at `]` | **stack of partial results** | 3 |
| "things moving toward each other collide; the bigger survives" | the new item fights the top until it survives or dies | **stack of survivors** | 4 |
| "for each item, the next bigger value later in the list" | each item waits for something that beats it | **monotonic decreasing stack** (values) | 5 |
| "for each day, how many days until it gets warmer" | the same, but I need the distance | **monotonic stack of indices** | 6 |
| "convoys / groups that merge when one catches up", sorted by position | sort, then the stack keeps one entry per group | **sort + stack of arrival times** | 7 |
| "largest rectangle", "widest span where I'm the smallest" | nearest smaller on both sides | **monotonic increasing stack** of indices | gap (#8) |
| "evaluate this expression in postfix notation" | operators need the two most recent operands | **operand stack** | 9 |
| "evaluate with `+ - * /` and precedence" | apply `*` `/` at once; push signed numbers for `+` `-` | **operand stack + last operator** | gap (#10) |
| "evaluate with parentheses" | save running result and sign at `(`, restore at `)` | **stack of (result, sign)** | gap (#11) |
| "`push`, `pop`, and the current minimum in O(1)" | the answer to the extra query is stored with each entry | **stack of `(value, min so far)`** | 12 |
| "implement a queue with stacks" | reverse twice | **two stacks (`in`, `out`), amortised `O(1)`** | gap (E2) |
| "max of every window of size k" | candidates that can still win; items leave from the front | **monotonic deque** (not a stack) | Arrays-Strings repo (#28) |
| "the best item of a changing set, not the latest" | priority, not recency | **heap** | Heap repo |
| "traverse a tree or graph without recursion" | the call stack made explicit | **explicit stack for DFS** | Trees / Graphs repos |
| "water trapped between bars", "next smaller on both sides" | two scans or a stack | **two pointers** or **monotonic stack** | Arrays-Strings repo (#20) |
| "remove k digits to make the number smallest" | greedy: drop a digit that is bigger than its successor | **monotonic increasing stack** | gap |
| "a counter is enough" (single bracket type, running balance) | no history needed, just a number | **a counter, no stack** | 1 (Variant B) |
| "how many ways" / "best total" with choices | overlapping subproblems | **DP** | DP repo |

**Red flags that you're being tested on stacks:** "matching", "nested", "balanced", "undo", "evaluate", "next greater / smaller / warmer", "span", "histogram", "collision", "survivor", "parse", "decode", "simplify", "get the minimum in `O(1)`", and any brute force that is "for each element, scan to the right until something happens".

### Stack or counter?

If you only need to know whether a **single kind** of bracket is balanced (or the minimum number of insertions to balance it), keep a running **count**: `+1` on `(`, `-1` on `)`, and never let it dip below zero. It is `O(1)` space. Use a real stack when there are **several types** (`()[]{}`), when you need the **positions**, or when the contents matter (Decode String, Simplify Path).

### Stack or recursion?

A recursive solution already uses the call stack. Prefer an **explicit stack** when the depth can be large (Python's default limit is about 1000), when you need to **pause and resume** iteratively, or when the interviewer asks "can you do it without recursion?". Prefer **recursion** when it is much clearer (a recursive-descent parser for nested expressions).

### Stack or monotonic deque?

- **A monotonic stack** only touches one end: you pop and push at the top, and an item leaves only when something beats it. Use it for **"next bigger/smaller"** and spans.
- **A monotonic deque** also removes from the **front** when an item falls out of a window. Use it for **window maximum/minimum** (#28 in the Arrays-Strings repo).

### Monotonic stack: decreasing or increasing?

| You want | Stack is | Pop when the new item is | Each pop tells you |
|---|---|---|---|
| next **greater** element (Daily Temperatures, NGE) | **decreasing** (bottom largest) | greater than the top | the next greater of the popped item is the new item |
| next **smaller** element (Histogram) | **increasing** (bottom smallest) | smaller than the top | the next smaller of the popped item is the new item |
| **previous** greater / smaller | the same stacks | (read the new top *before* pushing) | the item left on top after popping is the answer for the new item |

Say **strict or non-strict** out loud. Pop on `>` (strict) and equal items stay and wait together; pop on `>=` and they resolve each other.

### When it is really DP or greedy

Some "stack" problems are greedy with a stack as the bookkeeping (Remove K Digits, Asteroid Collision). If a choice now costs future options and a small counter-example breaks the greedy, it is DP instead. See the DP repo.

---

## Part 3. Complexity patterns

Every stack cost is **(number of pushes + pops) × work per operation**. Count the passes first.

| Pattern | Time | Extra space | Why |
|---|---|---|---|
| Pending-items stack (Valid Parentheses) | `O(n)` | `O(n)` | one pass; each char pushed or popped once; the stack is as deep as the unclosed openers |
| Same, with a single bracket type and a counter | `O(n)` | `O(1)` | the counter replaces the stack |
| Path simplification (Simplify Path) | `O(n)` | `O(n)` | `split` reads the string once; the loop visits each part once; `join` is `O(n)` |
| Decode String (stack of pieces) | about `O(L · depth)` for output length `L` | `O(L)` | each level re-pops and re-repeats text built by inner levels; `pop() + substr` copies, so say "proportional to the output size" |
| Survivor stack (Asteroid Collision) | `O(n)` | `O(n)` | each item pushed once, popped at most once; the inner `while` is amortised |
| Monotonic stack (Next Greater, Daily Temperatures, Histogram) | `O(n)` | `O(n)` | each index pushed once, popped at most once: at most `2n` operations in total |
| Monotonic stack, brute force alternative | `O(n²)` | `O(1)` | scan right from every element |
| Sort + stack (Car Fleet) | `O(n log n)` | `O(n)` | the sort dominates; the loop is `O(n)` |
| Expression evaluation (RPN, Calculators) | `O(n)` in tokens | `O(n)` | each token handled once; operators are `O(1)` |
| Min Stack: push, pop, top, min | `O(1)` each | `O(n)` | one extra value stored per push |
| Queue from two stacks | `O(1)` amortised per operation | `O(n)` | each element moves from `in` to `out` at most once |
| Max Frequency Stack | `O(1)` per operation | `O(n)` | a stack per frequency level plus a count map |

**How to work out complexity (say it in this order):**
1. **Count pushes and pops.** Each element is pushed at most once. It is popped at most once. So the total number of stack operations is at most `2n`.
2. **Look inside the `while`.** A `while` inside a `for` is **not** `O(n²)` if every iteration of the `while` pops an item that won't be pushed again. Add up total pops, don't multiply.
3. **Add the hidden costs:** a sort before the loop (`O(n log n)`), string building by repeated concatenation (`O(n²)` for long outputs), or a `min()` over a list per step.
4. **Space = the deepest the stack gets.** All openers: `O(n)`. A strictly decreasing array: `O(n)`. A balanced alternation: `O(1)` to `O(depth)`.
5. **State the brute force and its cost** (`O(n²)` for "scan to the right from every element") and then the improvement.

**Rules of thumb**
- **"Each element is pushed once and popped once" is the sentence interviewers want to hear** for any monotonic stack.
- **Counters beat stacks when no history is needed.** If only a single balance matters, say so and drop to `O(1)` space.
- **Python lists are fine stacks:** `append()` and `pop()` are `O(1)`. Don't use `pop(0)` or `insert(0, x)` for a stack (`O(n)`); for a queue, use `collections.deque`.
- **Recursion costs `O(depth)` of call-stack space,** and Python caps it near 1000. An explicit stack has the same asymptotic space but no cap.
- **Streams:** a monotonic stack works online (answer each item when it is resolved), but items still on the stack at the end have no answer yet.

---

## Part 4. The scenarios

Each entry has: **Original question** (the formal LeetCode statement), then **Scenario** (what you'd actually hear), **Ask first**, **Spot it** (the clue that reveals the technique), **Brute force** (the naive answer and its cost), **Solve** (the answer from your write-up), **Cost** (time and space, with the reasoning), **Follow-up** (what they'd push on), and **two more variants (A and B)** on the same pattern. Each variant gives the formal **Question** first, then the disguised **Scenario**, then **Pattern and cost**. Variants marked **(crossover)** leave the entry's technique on purpose, to show you where it stops working. A variant with no LC number is a classic interview question that has no single canonical LeetCode entry.

---

### Topic 1. Stack as "Pending Items"

---

### 1. Valid Parentheses (#1)

**Original question:** LC 20. Given a string `s` containing just the characters `'('`, `')'`, `'{'`, `'}'`, `'['` and `']'`, determine if the input string is valid: open brackets must be closed by the same type of brackets and in the correct order, and every close bracket has a matching open bracket.

**Scenario:** A code editor's linter reads a line of source. Every opening mark has to be closed by the matching kind of mark, and inner groups must close before outer groups do. Report whether the line is well-formed.

**Ask first:**
1. Is the input only made of these six characters, or can it contain other text? Can it be empty?
2. How long can the string get? (a stack of that depth is fine; recursion might not be)

**Spot it:** "Closed in the **reverse** order of opening" means the **most recent** unclosed opener must be the one that the next closer matches. That is last-in-first-out.

**Brute force:** Repeatedly delete adjacent matching pairs `()`, `[]`, `{}` until nothing changes: `O(n²)`. It works, but each pass rescans the string.

**Solve:** ([01-valid-parentheses.md](01-stack-as-pending-items/01-valid-parentheses.md))
```python
def isValid(s: str) -> bool:
    stack = []
    close_to_open = {")": "(", "}": "{", "]": "["}
    for char in s:
        if char in close_to_open:
            if stack and stack[-1] == close_to_open[char]:
                stack.pop()                    # matched: the opener is resolved
            else:
                return False                   # closer with no opener, or the wrong type on top
        else:
            stack.append(char)                 # an opener waits
    return len(stack) == 0                     # leftover openers mean invalid
```

**Cost:** One pass; each push, pop and dict lookup is `O(1)`: `O(n)` time. The stack grows to `n` for input like `"((((("`: `O(n)` space.
**Follow-up:** *Odd length?* It can never be valid, so return `False` early. *Only one kind of bracket?* A counter is enough: `O(1)` space (Variant B). *Return the position of the first error?* Return `i` where you return `False`, or the index at the bottom of the stack for an unclosed opener. *Longest valid substring?* Variant A.

**More scenarios on the same pattern**

**Variant A (crossover: positions on the stack)**
- **Question:** LC 32 Longest Valid Parentheses. Given a string containing just `'('` and `')'`, return the length of the longest valid (well-formed) parentheses substring.
- **Scenario:** A log line mixes opening and closing marks, some unmatched. What's the longest unbroken stretch that is perfectly balanced?
- **Pattern and cost:** Store **indices** on the stack, with `-1` at the bottom as a base. On `)`, pop; if the stack is empty, push the index as the new base; otherwise the stretch length is `i - stack[-1]`. `O(n)` time, `O(n)` space. Also solvable with DP, or with two counters and two passes in `O(1)` space.

**Variant B (crossover: a counter replaces the stack)**
- **Question:** LC 921 Minimum Add to Make Parentheses Valid. Given a string of `'('` and `')'`, return the minimum number of parentheses you must add to make it valid.
- **Scenario:** A formula checker only needs to know how many marks to insert so every opener has a closer, with a single kind of mark.
- **Pattern and cost:** No history is needed, just the balance. Keep `open_needed` and `close_needed` counters: `O(n)` time, **`O(1)` space**. Saying "a counter is enough because there is only one bracket type" is the signal of good judgement.

---

### 2. Simplify Path (#2)

**Original question:** LC 71. Given an absolute Unix-style `path`, convert it to the simplified canonical path: a single leading `/`, directories separated by one `/`, no trailing `/`, `.` means the current directory, `..` means the parent directory, and multiple slashes count as one. Names like `...` are valid directory names.

**Scenario:** A file explorer receives a messy location typed by a user, with repeated slashes, "stay here" parts and "go up one level" parts. Return the clean, shortest form of the same location.

**Ask first:**
1. Is the path always absolute (it starts with `/`)? What should `/..` at the root return?
2. Are parts like `...` or `.hidden` ordinary names? (Yes, only `.` and `..` are special.)

**Spot it:** "Go up one level" **undoes the last step**. The most recent directory is the next one to be removed. That is a stack of directory names.

**Brute force:** Repeatedly rewrite the string: remove `//`, remove `/./`, collapse `/name/../`: `O(n²)` in the worst case because each rewrite rescans.

**Solve:** ([02-simplify-path.md](01-stack-as-pending-items/02-simplify-path.md))
```python
def simplifyPath(path: str) -> str:
    stack = []
    for portion in path.split("/"):
        if portion == "" or portion == ".":
            continue                           # repeated slash, or "stay here"
        elif portion == "..":
            if stack:
                stack.pop()                    # go up one level; at the root, do nothing
        else:
            stack.append(portion)              # a real folder name (including "...")
    return "/" + "/".join(stack)
```

**Cost:** `split` is `O(n)`, the loop visits each part once with `O(1)` push or pop, and `join` is `O(n)`: `O(n)` time, `O(n)` space.
**Follow-up:** *Symbolic links?* Resolving them needs the filesystem, and it can create cycles. *Relative paths?* Start from the current directory's stack and allow leading `..`. *Windows paths?* Different separators and drive letters. *Only the depth?* Variant A (no stack needed).

**More scenarios on the same pattern**

**Variant A (crossover: a counter suffices)**
- **Question:** LC 1598 Crawler Log Folder. Given logs where `"../"` means go up one folder (not above the root), `"./"` means stay, and any other `"x/"` means go into folder `x`, return the minimum number of operations needed to go back to the main folder.
- **Scenario:** A crawler walks a site and logs each move. How many steps back does it need to return to the top?
- **Pattern and cost:** You never need the *names*, only the depth. A counter: `+1` for a folder, `max(0, depth - 1)` for `../`. `O(n)` time, **`O(1)` space**. A stack of names would work but wastes memory.

**Variant B (crossover: a stack of depths)**
- **Question:** LC 388 Longest Absolute File Path. Given a string representing a file system with `\n` and `\t` for nesting, return the length of the longest absolute path to a file, or `0`.
- **Scenario:** A storage tool prints a folder tree with indentation. What's the longest full path of any file?
- **Pattern and cost:** Count tabs for the depth, keep a stack (or an array indexed by depth) of **cumulative path lengths**; a file's length is the stack top plus the file name. `O(n)` time, `O(depth)` space. The stack stores *numbers*, not names.

---

### 3. Decode String (#3)

**Original question:** LC 394. Given an encoded string, return its decoded string. The encoding rule is `k[encoded_string]`, where `encoded_string` inside the brackets is repeated exactly `k` times. Encoded strings can be nested, and `k` is a positive integer (possibly more than one digit).

**Scenario:** A compression tool stores text as "repeat this chunk `k` times", and chunks can contain smaller chunks. Given the compressed line, reconstruct the full text.

**Ask first:**
1. Can counts have several digits? Can letters appear outside any group?
2. How big can the decoded output be? (it can be far bigger than the input)

**Spot it:** Nested groups: the **innermost group must be finished first**, and its result becomes part of the outer one. Push everything; when a group closes, unwind to its opener and push back the expanded text.

**Brute force:** Repeatedly find an innermost group (no brackets inside), expand it in place, and restart: `O(n²)`-ish string rewriting.

**Solve:** ([03-decode-string.md](01-stack-as-pending-items/03-decode-string.md))
```python
def decodeString(s: str) -> str:
    stack = []
    for char in s:
        if char != "]":
            stack.append(char)                       # letters, digits and "[" all wait
        else:
            substr = ""
            while stack and stack[-1] != "[":        # 1. unwind the group's text
                substr = stack.pop() + substr
            stack.pop()                              # 2. discard "["
            k = ""
            while stack and stack[-1].isdigit():     # 3. read the repeat count (maybe several digits)
                k = stack.pop() + k
            stack.append(int(k) * substr)            # 4. push the expansion back as one piece
    return "".join(stack)
```

**Cost:** About `O(L × depth)` for decoded length `L`: every level re-pops and re-repeats text already built by inner levels, and `pop() + substr` copies on each prepend. Say "proportional to the output size". Space `O(L)`.
**Follow-up:** *Avoid the repeated copying?* Two stacks: one of counts, one of the string built so far; on `[` push the current string and count, on `]` pop and combine. *Recursion instead?* A recursive-descent parser. *Huge expansion?* Stream the output instead of building it.

**More scenarios on the same pattern**

**Variant A (crossover: a stack of maps)**
- **Question:** LC 726 Number of Atoms. Given a chemical formula like `"K4(ON(SO3)2)2"`, return the count of each atom, sorted alphabetically, with counts appended (omitted if 1).
- **Scenario:** A lab tool reads a molecule formula in which sub-groups can be enclosed and followed by a multiplier, and groups can sit inside groups. How many of each element does it contain?
- **Pattern and cost:** On `(` push a fresh counter; on `)` pop it, multiply its counts by the number that follows, and merge into the one below. `O(n²)` worst case for deep groups, `O(n)` space. Same "save state, restore on close" idea, with maps instead of strings.

**Variant B (crossover: reverse inside groups)**
- **Question:** LC 1190 Reverse Substrings Between Each Pair of Parentheses. Reverse the strings in each pair of matching parentheses, starting from the innermost one, and return the result without any brackets.
- **Scenario:** A text tool must flip the text inside every group, working from the deepest group outwards.
- **Pattern and cost:** A stack of pieces, like #3: on `)` pop to the matching `(`, reverse that piece, and push its letters back. `O(n²)` worst case with this approach (`O(n)` with a clever two-pass jump table), `O(n)` space.

---

### 4. Asteroid Collision (#4)

**Original question:** LC 735. We are given an array `asteroids` of integers representing asteroids in a row. The absolute value is the size and the sign is the direction (positive moves right, negative moves left). All move at the same speed. When two meet, the smaller explodes; if equal, both explode; asteroids moving in the same direction never meet. Return the state after all collisions.

**Scenario:** Drones fly along a single line, some heading right and some heading left, all at the same speed. When two meet, the smaller one is destroyed (equal sizes destroy each other). Which drones are left at the end?

**Ask first:**
1. Does a value of `0` appear? (It doesn't in the original problem.)
2. Are all asteroids moving at the same speed, so only a right-mover followed by a left-mover can meet?

**Spot it:** A new item "fights" only the most recent survivor. It either destroys it and keeps going, dies, or both vanish: a **stack of survivors**.

**Brute force:** Repeatedly scan for an adjacent right/left pair and resolve it, until no pair remains: `O(n²)`.

**Solve:** ([04-asteroid-collision.md](01-stack-as-pending-items/04-asteroid-collision.md))
```python
def asteroidCollision(asteroids: list[int]) -> list[int]:
    stack = []
    for a in asteroids:
        while stack and a < 0 and stack[-1] > 0:      # collision: top moves right, a moves left
            diff = a + stack[-1]
            if diff < 0:
                stack.pop()                           # top explodes; a keeps going
            elif diff > 0:
                break                                 # a explodes
            else:
                stack.pop()                           # both explode
                break
        else:
            stack.append(a)                           # a survived (the while loop did not break)
    return stack
```

**Cost:** Each asteroid is pushed at most once and popped at most once, so the inner loop does at most `n` pops in total: `O(n)` time, `O(n)` space.
**Follow-up:** *Why `while … else`?* The `else` runs only when the loop ended without `break`, meaning the new asteroid survived. *Different speeds?* Collisions depend on timing; a different problem (Variant A). *Return how many collisions?* Count the pops.

**More scenarios on the same pattern**

**Variant A (crossover: sort by position, then a stack)**
- **Question:** LC 2751 Robot Collisions. Robots at given positions each have a health and a direction (`'L'` or `'R'`), all moving at the same speed. When robots collide, the one with lower health is removed and the survivor loses 1 health; if equal, both are removed. Return the healths of the survivors in the original input order.
- **Scenario:** Delivery robots on a single rail are given in no particular order, each with a battery level and a heading. Which robots survive, and with how much battery?
- **Pattern and cost:** The robots are not in positional order, so **sort the indices by position**, then run the survivor stack from #4 with the health rule. `O(n log n)` time, `O(n)` space.

**Variant B (crossover to adjacent cancellation)**
- **Question:** LC 1047 Remove All Adjacent Duplicates In String. Repeatedly remove two adjacent equal characters from a string until no more can be removed; return the final string.
- **Scenario:** A text cleaner deletes any pair of identical neighbouring characters, and deletions can create new pairs.
- **Pattern and cost:** Push each character; if it equals the top, pop instead. A stack of survivors again: `O(n)` time, `O(n)` space. A new neighbour pair appears only after a removal, which is why the stack remembers the previous character.

---

### Topic 2. Monotonic Stack

---

### 5. Next Greater Element I (#5)

**Original question:** LC 496. The next greater element of some element `x` in an array is the first greater element to the right of `x` in the same array. You are given two distinct integer arrays `nums1` and `nums2`, where `nums1` is a subset of `nums2`. For each `nums1[i]`, find its next greater element in `nums2`, or `-1` if none exists. Return the answers in the order of `nums1`.

**Scenario:** A trader has a full list of daily closing prices and a short watch list of prices that appear in it. For each watched price, report the first higher price that closes after it, or `-1` if the price never rises again.

**Ask first:**
1. Are all values distinct? (This lets me use a value as a dictionary key.)
2. Does "greater" mean strictly greater, and should I look only to the right?

**Spot it:** For **each item, the first later item that beats it.** Every item is "waiting" for something bigger, and the first bigger one resolves all the smaller ones that are waiting.

**Brute force:** For each watched price, find it in the list and scan right until a bigger one is found: `O(m·n)`.

**Solve:** ([05-next-greater-element-i.md](02-monotonic-stack/05-next-greater-element-i.md))
```python
def nextGreaterElement(nums1: list[int], nums2: list[int]) -> list[int]:
    nums1_index = {num: i for i, num in enumerate(nums1)}
    res = [-1] * len(nums1)
    stack = []                                      # decreasing: everything waiting for a bigger number
    for cur in nums2:
        while stack and cur > stack[-1]:
            val = stack.pop()                       # cur is the next greater of val
            res[nums1_index[val]] = cur
        if cur in nums1_index:                      # only track values we are asked about
            stack.append(cur)
    return res

def nextGreaterElementPrecompute(nums1: list[int], nums2: list[int]) -> list[int]:
    next_greater, stack = {}, []
    for cur in nums2:
        while stack and cur > stack[-1]:
            next_greater[stack.pop()] = cur
        stack.append(cur)
    return [next_greater.get(num, -1) for num in nums1]
```

**Cost:** Building `nums1_index` is `O(m)`. Each value of `nums2` is pushed at most once and popped at most once: `O(n)`. Total `O(m + n)` time. `O(m)` extra space (`O(n)` for the precompute version). Values left on the stack at the end have no next greater: `-1`.
**Follow-up:** *Circular array?* Variant A. *Why a decreasing stack?* Anything smaller than the new value is resolved and removed, so what remains is larger. *Duplicates?* Store indices, not values. *Stream?* Answer an item only when it gets resolved; Variant B.

**More scenarios on the same pattern**

**Variant A (crossover to wrap-around)**
- **Question:** LC 503 Next Greater Element II. Given a **circular** integer array `nums`, return the next greater number for every element (searching circularly), or `-1`.
- **Scenario:** The readings of a rotating sensor repeat in a loop. For each reading, what's the first higher reading that follows, wrapping around if needed?
- **Pattern and cost:** Loop over `2n` positions using `i % n`, pushing indices only during the first lap. `O(n)` time, `O(n)` space. The wrap-around simply means "every element can see the whole array to its right, then to its left".

**Variant B (crossover: a stream with counts)**
- **Question:** LC 901 Online Stock Span. Design `StockSpanner` with `next(price)` returning the span: the number of consecutive days up to and including today on which the price was less than or equal to today's price.
- **Scenario:** A ticker feeds in prices one at a time. For each new price, report how many days in a row (counting today) the price has been at or below it.
- **Pattern and cost:** Keep a stack of `(price, span)`; pop every entry with a price `<=` today's, adding its span to today's. Looks backward ("previous greater"), works online, **amortised `O(1)`** per call, `O(n)` space.

---

### 6. Daily Temperatures (#6)

**Original question:** LC 739. Given an array of integers `temperatures` representing the daily temperatures, return an array `answer` such that `answer[i]` is the number of days you have to wait after the `i`-th day to get a warmer temperature. If there is no future day for which this is possible, keep `answer[i] == 0`.

**Scenario:** A weather app has a list of daily highs. For each day, show how many days a visitor must wait for a hotter day, or `0` if it never gets hotter.

**Ask first:**
1. Does "warmer" mean strictly warmer, so equal temperatures don't count?
2. Do I return the *distance* in days or the temperature itself?

**Spot it:** The same "first later value that beats me", but now I need the **distance**, so the stack must hold **indices**, not values.

**Brute force:** For each day scan forward until a warmer day: `O(n²)`.

**Solve:** ([06-daily-temperatures.md](02-monotonic-stack/06-daily-temperatures.md))
```python
def dailyTemperatures(temperatures: list[int]) -> list[int]:
    res = [0] * len(temperatures)
    stack = []                                      # indices of days still waiting for a warmer day
    for i, t in enumerate(temperatures):
        while stack and t > temperatures[stack[-1]]:
            prev_i = stack.pop()
            res[prev_i] = i - prev_i                # today resolves the waiting day
        stack.append(i)
    return res
```

**Cost:** Each index is pushed once and popped at most once, so the inner `while` does at most `n` pops across the whole run: `O(n)` time. The stack holds every index when temperatures never rise: `O(n)` space.
**Follow-up:** *Equal temperatures?* The strict `>` keeps equal days waiting together, and one warmer day resolves them all. *Colder instead of warmer?* Flip the comparison. *Look backward instead?* Read the stack top before pushing. *`O(1)` extra space?* Possible by walking backward using the answers already computed (a "jump" trick), but it is fiddly.

**More scenarios on the same pattern**

**Variant A (crossover: nearest smaller on both sides)**
- **Question:** LC 84 Largest Rectangle in Histogram (tracker #8, not yet written up). Given the heights of bars of width 1, return the area of the largest rectangle in the histogram.
- **Scenario:** A billboard company wants the biggest rectangular ad that fits under a skyline of building heights.
- **Pattern and cost:** For each bar, find the nearest **smaller** bar on the left and on the right; the width between them times the bar's height is the best rectangle where that bar is the shortest. An **increasing** stack of indices finds both in one pass: when a bar is popped, its right boundary is the current index and its left boundary is the new top. Append a `0` sentinel to flush the stack. `O(n)` time, `O(n)` space. Brute force: expand from every bar, `O(n²)`.

**Variant B (crossover: a greedy with a monotonic stack)**
- **Question:** LC 402 Remove K Digits. Given a non-negative integer `num` as a string and `k`, remove `k` digits so the new number is as small as possible.
- **Scenario:** A lottery app must delete `k` digits from a ticket number to leave the smallest possible number.
- **Pattern and cost:** Scan left to right with an **increasing** stack; while `k > 0` and the top is bigger than the new digit, pop it (removing a larger digit that precedes a smaller one makes the number smaller). If `k` remains, trim from the end; strip leading zeros. `O(n)` time, `O(n)` space.

---

### 7. Car Fleet (#7)

**Original question:** LC 853. There are `n` cars at given `position`s heading to a `target` mile on a single-lane road, each with a given `speed`. A car cannot pass another; it slows down to match the car ahead and they travel together as a **fleet**. A car that catches up exactly at the target also joins the fleet. Return the number of car fleets that will arrive at the target.

**Scenario:** Several cars are heading to the same city on a one-lane road, each starting from a different spot and driving at its own speed. Nobody can overtake; a faster car stuck behind a slower one just follows it. How many separate convoys reach the city?

**Ask first:**
1. Is overtaking really impossible, and does catching up exactly at the finish count as joining?
2. Are the starting positions distinct, and are the inputs in any order?

**Spot it:** Order cars by **position** (front first). A car's arrival time tells you whether it catches the convoy ahead: if it would arrive **no later**, it merges. The stack of convoy arrival times stays strictly increasing.

**Brute force:** Simulate the road step by step, merging cars as they meet: depends on speeds and distances, can be far slower than `O(n²)`. A direct "compare each car with the next fleet" approach is `O(n²)`.

**Solve:** ([07-car-fleet.md](02-monotonic-stack/07-car-fleet.md))
```python
def carFleet(target: int, position: list[int], speed: list[int]) -> int:
    pair = [[p, s] for p, s in zip(position, speed)]
    stack = []                                      # arrival times of the fleets, front fleet first
    for p, s in sorted(pair, reverse=True):         # closest to the target first
        stack.append((target - p) / s)
        if len(stack) >= 2 and stack[-1] <= stack[-2]:
            stack.pop()                             # it catches the fleet ahead: it joins it
    return len(stack)
```

**Cost:** The sort is `O(n log n)`; the loop is `O(n)` with at most one push and one pop per car: `O(n log n)` time, `O(n)` space. A single `pop` (not a loop) is enough because the stack is always strictly increasing before the push.
**Follow-up:** *Why `<=`?* Arriving at the same moment means joining the fleet. *Floating-point worries?* Equal fractions give the exact same float, so the comparison is safe; you could also compare by cross-multiplication. *Avoid the sort?* If positions are small integers, bucket by position (Variant B). *Track which cars are in which fleet?* Keep indices on the stack.

**More scenarios on the same pattern**

**Variant A (crossover: a hard stack-of-collisions problem)**
- **Question:** LC 1776 Car Fleet II. Cars on a one-lane road are given by `[position, speed]`, in increasing position order. A car collides with the car in front of it if it catches up, and after the collision the two travel as one at the front car's speed. Return an array where `answer[i]` is the time at which car `i` collides with the next car, or `-1` if it never does.
- **Scenario:** For each truck in a convoy plan, when does it first catch up with the vehicle ahead?
- **Pattern and cost:** Process cars from the **front to the back** with a stack of candidate cars ahead, popping those that can never be caught first (slower and already merged). Each car is pushed and popped once: `O(n)` time, `O(n)` space. Hard; know the shape (stack of candidates, process from the end).

**Variant B (crossover: bucket instead of sort)**
- **Question:** Count car fleets when every starting position is an integer in `[0, target)`. (The usual follow-up to LC 853.)
- **Scenario:** Cars start on whole-numbered mile markers of a road of known length. How many convoys reach the end?
- **Pattern and cost:** Instead of sorting, write each car's arrival time into an array indexed by position, then sweep that array from the front: `O(n + target)` time, `O(target)` space. Trades the `log n` for a dependence on the road length, which is better only when `target` is small.

---

### Topic 3. Expression Evaluation

---

### 9. Evaluate Reverse Polish Notation (#9)

**Original question:** LC 150. You are given an array of strings `tokens` that represents an arithmetic expression in Reverse Polish Notation. Evaluate it and return the integer result. Valid operators are `+`, `-`, `*` and `/`; division between two integers truncates toward zero; the expression is always valid.

**Scenario:** An old calculator takes its input with the operator after the numbers it applies to, so `3 4 + 2 *` means `(3 + 4) * 2`. Given the list of tokens, compute the result.

**Ask first:**
1. Does division truncate toward zero (so `-7 / 2` is `-3`)? Can there be division by zero?
2. Can tokens be negative numbers like `"-11"`? Can I assume the expression is valid?

**Spot it:** An operator always applies to the **two most recent results**, then yields one result. That's a stack of operands: push numbers, pop two when an operator arrives, push the result.

**Brute force:** Repeatedly find the first operator preceded by two numbers, replace those three tokens with the result, and rescan: `O(n²)`.

**Solve:** ([09-evaluate-reverse-polish-notation.md](03-expression-evaluation/09-evaluate-reverse-polish-notation.md))
```python
def evalRPN(tokens: list[str]) -> int:
    stack = []
    for token in tokens:
        if token == "+":
            stack.append(stack.pop() + stack.pop())
        elif token == "-":
            b, a = stack.pop(), stack.pop()         # b was pushed last: it is the right operand
            stack.append(a - b)
        elif token == "*":
            stack.append(stack.pop() * stack.pop())
        elif token == "/":
            b, a = stack.pop(), stack.pop()
            stack.append(int(a / b))                # int() truncates toward zero
        else:
            stack.append(int(token))                # a number, possibly negative
    return stack[0]
```

**Cost:** One pass, each token `O(1)`: `O(n)` time. The stack holds up to about `n / 2` numbers (all numbers before any operator): `O(n)` space.
**Follow-up:** *Why `int(a / b)` and not `a // b`?* `//` floors, which differs for negatives. *Invalid input?* Check the stack depth before each pop. *Normal (infix) notation with precedence?* Variant A. *With parentheses?* Variant B. *Overflow?* Use a wider type in fixed-width languages.

**More scenarios on the same pattern**

**Variant A (crossover: precedence, tracker #10, not yet written up)**
- **Question:** LC 227 Basic Calculator II. Given a string containing non-negative integers, `+`, `-`, `*`, `/` and spaces, evaluate the expression. Division truncates toward zero. There are no parentheses.
- **Scenario:** A spreadsheet cell holds a formula like `3+2*2`. Compute its value, respecting that multiplication and division bind tighter than addition and subtraction.
- **Pattern and cost:** Read each number together with the operator **before** it. For `+` / `-`, push the number (negated for `-`). For `*` / `/`, pop the top and push `top * num` (or truncated `top / num`) immediately. The answer is the sum of the stack. `O(n)` time, `O(n)` space (an `O(1)` version keeps only the last term). Spaces and multi-digit numbers are the usual bugs.

**Variant B (crossover: parentheses, tracker #11, not yet written up)**
- **Question:** LC 224 Basic Calculator. Evaluate an expression with `+`, `-`, parentheses (including unary minus before a parenthesis) and spaces.
- **Scenario:** A formula bar accepts `1 - (2 + (3 - 4))`. Compute it.
- **Pattern and cost:** Keep the running `result` and the current `sign`. On `(` push both onto the stack and restart; on `)` pop the sign and the earlier result, then combine: `result = earlier + sign * result`. `O(n)` time, `O(n)` space (depth of nesting). The same "save state, restore on close" idea as Decode String (#3).

---

### Topic 4. Design with Stacks

---

### 12. Min Stack (#12)

**Original question:** LC 155. Design a stack that supports `push`, `pop`, `top`, and retrieving the minimum element, all in constant time. Implement `MinStack` with `push(val)`, `pop()`, `top()` and `getMin()`.

**Scenario:** An editor keeps an undo history of numeric readings. It must support adding the latest reading, removing it, peeking at it, and instantly reporting the smallest reading currently in the history, however long the history is.

**Ask first:**
1. Are `pop`, `top` and `getMin` ever called on an empty stack?
2. Can values repeat (so equal minimums need handling)? Is extra memory allowed?

**Spot it:** A **query that must stay `O(1)` after pushes and pops**. A single running minimum breaks on `pop` (what was the minimum before?). So store the minimum **so far** next to every entry.

**Brute force:** Scan the whole stack on each `getMin`: `O(n)`. Or keep one minimum variable and recompute it on every pop: `O(n)` per pop.

**Solve:** ([12-min-stack.md](04-design-with-stacks/12-min-stack.md))
```python
class MinStack:
    def __init__(self):
        self.stack = []
        self.min_stack = []                         # min_stack[i] = minimum of stack[0..i]

    def push(self, val: int) -> None:
        self.stack.append(val)
        current_min = min(val, self.min_stack[-1] if self.min_stack else val)
        self.min_stack.append(current_min)

    def pop(self) -> None:
        self.stack.pop()
        self.min_stack.pop()                        # always popped together

    def top(self) -> int:
        return self.stack[-1]

    def getMin(self) -> int:
        return self.min_stack[-1]
```

**Cost:** Every operation does a constant number of appends, pops, index reads and one `min` of two values: `O(1)` time. The second stack adds one value per push: `O(n)` space.
**Follow-up:** *Save space?* Push to `min_stack` only when `val <= current min`, and pop it only when the popped value equals the top of `min_stack` (the `<=` handles duplicates). *Max Stack?* Same, with `max`. *Remove the max (`popMax`) too?* Harder: a stack alone isn't enough (Variant A is the related design). *One list of pairs?* `(val, min)` tuples keep the two in sync.

**More scenarios on the same pattern**

**Variant A (crossover: a stack of stacks)**
- **Question:** LC 895 Maximum Frequency Stack. Design `FreqStack` with `push(val)` and `pop()`, where `pop` removes and returns the most frequent element; ties go to the element closest to the top.
- **Scenario:** A cache evicts the item used most often from its recent history, and among equally common items the one used most recently.
- **Pattern and cost:** Keep a count per value and a **dictionary of stacks**: `groups[f]` holds the values that have reached frequency `f`, in push order; track `max_freq`. `push` appends to `groups[count]`; `pop` takes from `groups[max_freq]`. **`O(1)` per operation**, `O(n)` space.

**Variant B (crossover: one structure from another)**
- **Question:** LC 232 Implement Queue using Stacks. Implement a FIFO queue using only stack operations: `push`, `peek`, `pop`, `empty`.
- **Scenario:** A system only offers last-in-first-out containers, but the product needs a first-come-first-served line.
- **Pattern and cost:** Two stacks, `in` and `out`. Push to `in`; on `pop` or `peek`, if `out` is empty move everything from `in` to `out` (reversing the order). **Amortised `O(1)`** per operation, since each element moves at most once, `O(n)` space. A worst-case single `pop` is `O(n)`; say "amortised".

---

## Part 5. Common traps to say out loud

Interviewers listen for these. Say the relevant one *before* you code it.

**Empty stack and boundaries**
- **Popping or peeking an empty stack** raises `IndexError`. Always check `if stack and ...` before `stack[-1]` or `pop()` (#1, #2, #4, #6). State when the problem guarantees non-empty (#12, #9).
- **Leftover items at the end.** Leftover openers mean invalid (#1). Leftover indices in a monotonic stack have **no** next-greater answer: leave `0` or `-1`. Say what the leftovers mean before you return.
- **Empty or single-element input.** `""` is a valid bracket string; one element in a monotonic stack is never popped (answer `0`/`-1`).
- **Off-by-one in widths and distances.** A popped bar's width is `i - stack[-1] - 1` (with a sentinel), a day's wait is `i - prev_i`. Draw a tiny example.

**Comparisons and ordering**
- **Strict vs non-strict.** `>` keeps equal items waiting together; `>=` resolves them one against the next. Daily Temperatures wants strict `>`; check the wording of "greater" every time (#5, #6).
- **Values or indices?** Use indices when you need distances or widths (#6). Use values when the elements are distinct and the answer is a value (#5). With duplicates, always store indices.
- **Which direction to scan?** "Next" scans left to right resolving earlier items; "previous" reads the top of the stack *before* pushing.
- **Operand order for `-` and `/`.** The first pop is the **right** operand: `b, a = pop(), pop()`, then `a - b` (#9).
- **Division truncates toward zero.** Use `int(a / b)`, not `a // b`, for negatives (`-7 / 2` is `-3`, but `-7 // 2` is `-4`). Division by zero if the problem allows it.

**Technique-specific**
- **A stack where a counter is enough.** For a single bracket type, mention the `O(1)`-space counter (#1, Variant B).
- **Decode String:** multi-digit counts (`"100[a]"`), nested groups, text outside any group, and the repeated string copying `pop() + substr`.
- **Asteroid Collision:** the new item can destroy **several** survivors in a row (chain); a left-mover with an empty stack, or only left-movers below, survives. Equal sizes: pop the top and **don't** push the new one. Python's `while ... else` runs the `else` only when the loop did **not** `break`.
- **Car Fleet:** sort by position descending; use `<=` for "arrives at the same time joins"; one `pop` is enough because the stack is already ordered.
- **Min Stack:** pop both stacks together; duplicates of the minimum must be handled (store the minimum with each entry, or use `<=`).
- **Expressions:** unary minus, spaces, multi-digit numbers, and the last number (flush after the loop; add a sentinel operator).
- **Monotonic stack in a stream:** an item has no answer *yet* until something resolves it.

**Python-specific**
- Use a list for a stack (`append`, `pop`), and `collections.deque` for a queue. `list.pop(0)` is `O(n)`.
- Recursive solutions hit Python's recursion limit near 1000 (deeply nested input); prefer an explicit stack.
- Strings are immutable: `substr = stack.pop() + substr` copies each time. Collect pieces in a list and `"".join` when output size matters.
- `sorted(pair, reverse=True)` sorts by position first, then speed. That's fine for Car Fleet, but be explicit about what you sort by.

---

## Part 6. Known gaps: important stack problems this repo doesn't cover yet

**Planned in [problems.md](problems.md) but not written up yet** (the entries above cover them only as variants, so write them up properly):

| # | Problem | Technique | Why it matters |
|---|---|---|---|
| 8 | Largest Rectangle in Histogram (LC 84, Core) | Increasing monotonic stack with widths | The hardest and most-asked monotonic-stack problem; scenario questions about "widest span where I'm the smallest" are this |
| 10 | Basic Calculator II (LC 227, Core) | Operand stack + operator precedence | Very commonly asked; sits between #9 and #11 |
| 11 | Basic Calculator (LC 224, Core) | Stack of `(result, sign)` for parentheses | The "save state, restore on close" pattern again |
| E1 | Next Greater Element II (LC 503) | Circular monotonic stack | Wrap-around variant of #5 |
| E2 | Implement Queue using Stacks (LC 232) | Two stacks, amortised `O(1)` | A common warm-up and a good amortised-analysis talking point |

**Not in the tracker at all, and likely to be asked:**

| Problem | Technique | Why add it |
|---|---|---|
| Online Stock Span (LC 901) | Monotonic stack with counts, online | The stream version of #6; tests amortised `O(1)` |
| Remove K Digits (LC 402), Remove Duplicate Letters (LC 316) | Greedy with an increasing stack | Stack as the bookkeeping of a greedy |
| Longest Valid Parentheses (LC 32) | Stack of indices (or DP / two counters) | The tracker lists it as a good extra after #1 and #11 |
| Trapping Rain Water, stack version (LC 42) | Monotonic stack | The tracker notes the two-pointer version is in Arrays-Strings |
| Sum of Subarray Minimums (LC 907), Maximal Rectangle (LC 85) | Monotonic stack, counting contributions / row-by-row histogram | Harder uses of #8 |
| Maximum Frequency Stack (LC 895) | Dictionary of stacks | A design question that extends #12 |
| Validate Stack Sequences (LC 946), Flatten Nested List Iterator (LC 341) | Simulate with a stack / explicit stack iterator | Easy-medium "simulate the stack" reps |
| Number of Atoms (LC 726), Basic Calculator III (LC 772) | Stack of maps / recursive-descent with a stack | Nested parsing, where Google likes to go deeper |
| Generate Parentheses (LC 22) | Backtracking | Out of scope here; lives in the Backtracking repo |
| Sliding Window Maximum (LC 239) | Monotonic **deque** | The "stack or deque?" decision; lives in Arrays-Strings (#28) |

**Notes on the repo's own write-ups** (so you can answer well if asked):
- **#3 Decode String** is not strictly `O(n)`. The write-up says "about `O(L × depth)`" because of repeated string copying. The two-stack version (counts and partial strings) is the cleaner follow-up.
- **#7 Car Fleet** uses a single `pop`, not a `while`. Know why: the stack is already strictly increasing before the push, so at most one element can break the order.
- **#12 Min Stack** has two forms (two stacks, or one stack of pairs). Know the space-saving trick of pushing to the minimum stack only on `<=`.
- **#5 Next Greater Element I** has a precompute alternative that computes the answer for every value of `nums2` first. Say which you'd choose and why.

**Confidence note:** the LeetCode numbers in the variants were written from memory, in the same spirit as the tracker's own caveat in [problems.md](problems.md). Before relying on a number, search the title on LeetCode. The techniques, costs and traps are the part to trust and rehearse.
