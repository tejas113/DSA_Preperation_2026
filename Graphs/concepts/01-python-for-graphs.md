# Concept 01 — Python syntax you need for graphs

You said you don't know Python syntax. This file gives you **exactly** what graph
problems use — nothing more. Read it once, then keep it open while you do the first
few problems.

---

## Quick Card

```python
# --- the 5 containers ---
nums = [1, 2, 3]                 # list  : ordered, can change, duplicates OK
point = (2, 5)                   # tuple : ordered, CANNOT change -> usable as a dict key / set element
seen = {1, 2, 3}                 # set   : no order, no duplicates, O(1) "in" check
graph = {0: [1, 2], 1: [0]}     # dict  : key -> value lookups, O(1)
s = "abc"                        # str   : like a tuple of characters

# --- the 3 imports we always use ---
from collections import deque, defaultdict
import heapq

q = deque()          # a queue: append() on the right, popleft() from the left, both O(1)
g = defaultdict(list)  # a dict that auto-creates an empty list the first time you touch a key
heap = []            # a min-heap via heapq.heappush / heapq.heappop  -> smallest comes out first
```

---

## 1. Variables and printing

```python
x = 5                # no "int", no "let", no semicolon
name = "Tejas"
print(x, name)       # -> 5 Tejas
print(f"x is {x}")   # f-string: puts the value of x inside the text -> "x is 5"
```

Python uses **indentation** (4 spaces) instead of `{ }` to group code. The `:` at
the end of a line starts an indented block.

```python
if x > 3:
    print("big")     # this line is "inside" the if because it is indented
print("always")      # this line is outside the if
```

---

## 2. Lists — the workhorse

```python
a = [10, 20, 30]
a[0]            # 10        (first)
a[-1]           # 30        (last — negative counts from the end)
a[1:3]          # [20, 30]  (slice: from index 1 up to BUT NOT including 3)
len(a)          # 3
a.append(40)    # a is now [10, 20, 30, 40]      -- add to end,  O(1)
a.pop()         # returns 40, a is [10, 20, 30]  -- remove from end, O(1)
a.pop(0)        # returns 10, a is [20, 30]      -- remove from front, O(n)  <- slow, avoid; use deque
30 in a         # True      -- "is 30 somewhere in the list?"  O(n)  <- slow for big lists
```

Make a list of zeros of a fixed size:

```python
row = [0] * 5              # [0, 0, 0, 0, 0]
grid = [[0] * n for _ in range(m)]   # an m-by-n grid of zeros
```

> ⚠️ **Trap:** `[[0] * n] * m` looks the same but is WRONG — it makes `m` copies of
> the *same* inner list, so changing one row changes them all. Always use the
> `for _ in range(m)` form above.

Loop over a list:

```python
for value in a:              # value takes each element
    print(value)

for i in range(len(a)):      # i takes 0, 1, 2, ...  when you need the index
    print(i, a[i])

for i, value in enumerate(a):   # both at once
    print(i, value)
```

---

## 3. Tuples — for coordinates and "frozen" keys

```python
p = (2, 5)
r, c = p            # "unpacking": r = 2, c = 5
p[0]                # 2
```

A tuple **cannot be changed**, which is exactly why you can put it in a `set` or
use it as a `dict` key. A list cannot be a set element or dict key.

```python
seen = set()
seen.add((2, 5))       # OK — tuple
seen.add([2, 5])       # ERROR — list is not hashable
```

Directions as a tuple of tuples (our house style):

```python
DIRS = ((1, 0), (-1, 0), (0, 1), (0, -1))
for dr, dc in DIRS:            # unpack each inner tuple
    nr, nc = r + dr, c + dc
```

---

## 4. Sets — the "have I seen this?" tool

```python
seen = set()          # empty set  (NOT {}, that's an empty dict)
seen.add(3)
seen.add(3)           # no effect — sets ignore duplicates
3 in seen             # True   -- O(1), this is why we use sets for "visited"
seen.discard(3)       # remove 3 if present (no error if missing)
len(seen)             # count

start = {0}           # a set with one element
visited = {(0, 0)}    # a set with one tuple
```

For grids you can also use a `set` of `(r, c)` tuples as your "visited" marker.

---

## 5. Dicts — lookups and adjacency lists

```python
d = {}
d["a"] = 1
d["a"]            # 1
d.get("b", 0)     # 0   -- "give me d['b'], or 0 if 'b' is missing" (no error)
"a" in d          # True
for key in d:            # loops over keys
    print(key, d[key])
for key, val in d.items():   # loops over pairs
    print(key, val)
```

### `defaultdict` — auto-creating values

Normally `d["x"].append(5)` crashes if `"x"` isn't a key yet. `defaultdict(list)`
fixes that: touching a missing key auto-inserts an empty list first.

```python
from collections import defaultdict
graph = defaultdict(list)
graph[0].append(1)      # graph is now {0: [1]}   -- no KeyError
graph[0].append(2)      # graph is now {0: [1, 2]}
graph[5]                # just touching it creates {5: []}
```

`defaultdict(int)` auto-creates `0` — handy for counting (e.g. indegree):

```python
indeg = defaultdict(int)
indeg[node] += 1        # works even the first time
```

---

## 6. `deque` — the correct queue for BFS

A list's `pop(0)` is O(n) (it shifts every element). `deque` (double-ended queue)
does it in O(1).

```python
from collections import deque
q = deque()
q.append(1)         # add to the RIGHT
q.append(2)
q.popleft()         # remove from the LEFT -> returns 1   (this is FIFO, first-in-first-out)
q.appendleft(0)     # add to the LEFT (used in 0-1 BFS)
len(q)              # how many items
while q:            # "while the queue is not empty"
    node = q.popleft()

q = deque([start])          # start with one item
q = deque(list_of_items)    # start with many
```

**FIFO (first-in-first-out)** = BFS. If you instead `pop()` from the right, a deque
behaves as a stack (LIFO) = iterative DFS.

---

## 7. `heapq` — the min-heap for Dijkstra / Prim

A heap always gives you the **smallest** item first, in `O(log n)` per operation.
Python's `heapq` works on a plain list.

```python
import heapq
heap = []
heapq.heappush(heap, (5, "a"))
heapq.heappush(heap, (2, "b"))
heapq.heappush(heap, (8, "c"))
heapq.heappop(heap)        # -> (2, "b")   -- smallest FIRST element wins; ties break on the 2nd
heap[0]                    # peek at the smallest without removing
heapq.heapify(some_list)   # turn an existing list into a heap in O(n)
```

We push **tuples** `(cost, node)` so the heap orders by `cost`. For a *max*-heap,
push `(-cost, node)` and negate again when you pop.

---

## 8. Strings

```python
s = "abc"
s[0]            # "a"
len(s)          # 3
s[1:]           # "bc"
list(s)         # ["a", "b", "c"]   -- strings can't be edited, so convert to a list to change a letter

chars = list(s)
chars[0] = "x"
"".join(chars)  # "xbc"   -- join the list back into a string

for ch in s:    # loop over characters
    ...

"cat" == "cat"  # True — string comparison is by content
```

Turn a word into a "hashable key" for a set: strings are already hashable, so
`seen.add("cat")` just works. To use a *list of words* as a key, convert to a
tuple: `tuple(["a", "b"])`.

---

## 9. Comprehensions — build a list/set/dict in one line

```python
squares = [x * x for x in range(5)]           # [0, 1, 4, 9, 16]
evens = [x for x in range(10) if x % 2 == 0]  # [0, 2, 4, 6, 8]
seen = {(r, c) for r, c in cells}             # a set
indeg = {node: 0 for node in range(n)}        # a dict

# 2D grid of zeros (house style)
dist = [[float("inf")] * n for _ in range(m)]
```

Read it right-to-left: "for each x in range(5), compute x*x, collect into a list".

---

## 10. Functions and nested functions

```python
def add(a, b):
    return a + b

def solve(grid):
    m, n = len(grid), len(grid[0])
    seen = set()

    def dfs(r, c):                 # a function INSIDE solve — it can see grid, m, n, seen
        seen.add((r, c))
        for dr, dc in DIRS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < m and 0 <= nc < n and (nr, nc) not in seen:
                dfs(nr, nc)

    dfs(0, 0)
    return len(seen)
```

The inner `dfs` can **read** outer variables (`grid`, `seen`) freely. To
**reassign** an outer *number* from inside, you need `nonlocal`:

```python
def solve(grid):
    count = 0
    def dfs(r, c):
        nonlocal count       # without this line, "count += 1" would crash
        count += 1
    ...
```

You don't need `nonlocal` to *mutate* a list/set/dict (`seen.add(...)`,
`res.append(...)`), only to *rebind* a name to a new value.

---

## 11. `float("inf")` — a number bigger than everything

Used as "no distance yet / unreachable".

```python
best = float("inf")
best = min(best, 5)     # 5
10 < float("inf")       # True
```

---

## 12. `None`, truthiness, common operators

```python
x = None                 # "no value"
if x is None: ...        # the correct way to check for None

if not q: ...            # empty deque / list / set / string / dict is "falsy"
if q: ...                # non-empty is "truthy"

7 // 2      # 3     integer division (floor)
7 % 2       # 1     remainder (modulo)
2 ** 10     # 1024  power
a, b = b, a  # swap in one line
```

---

## 13. Classes — because LeetCode gives you `class Solution`

```python
class Solution:
    def numIslands(self, grid):     # 'self' is always the first parameter of a method
        return 0

sol = Solution()                    # make an object
sol.numIslands([["1"]])             # call the method — you do NOT pass 'self'
```

`self` lets a method reach the object's own data (`self.parent`, `self.rank` in our
`DSU` class). You will mostly just write the one required method.

Type hints (what you'll see on LeetCode) are optional labels, ignored at runtime:

```python
from typing import List
def numIslands(self, grid: List[List[str]]) -> int:
    ...
```

You can write them or skip them; they don't change behavior.

---

## 14. Recursion limit

Python stops recursion at ~1000 deep by default and raises
`RecursionError`. A DFS over a 200×200 grid can go 40000 deep. Fix:

```python
import sys
sys.setrecursionlimit(10 ** 6)
```

Put it at the top of the file. Alternatively use the iterative (stack) version —
every problem file shows both.

---

## 15. The `if __name__ == "__main__":` block

Everything under this line runs **only when you execute the file directly**
(`python file.py`), not when it's imported. We put our tests there.

```python
if __name__ == "__main__":
    sol = Solution()
    assert sol.numIslands([["1","1"],["0","1"]]) == 1
    print("all tests passed")
```

`assert CONDITION` does nothing if the condition is `True`, and crashes with
`AssertionError` if it's `False`. That's our lightweight test.

---

## Cheat-sheet recap

| You want to... | Use |
|---|---|
| Visited marker, "have I seen X?" | `set`, `X in seen` |
| Adjacency list | `defaultdict(list)` |
| Counter (indegree, frequency) | `defaultdict(int)` |
| BFS queue | `deque`, `append` + `popleft` |
| Iterative DFS stack | `list` or `deque`, `append` + `pop` |
| Always-get-the-smallest | `heapq` on a list of `(cost, node)` tuples |
| Coordinate you can store in a set | `tuple` `(r, c)` |
| "Infinity" | `float("inf")` |
| Change a letter in a word | `list(word)` → edit → `"".join(...)` |
