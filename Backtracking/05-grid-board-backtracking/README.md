# Topic 5 — Grid / Board Backtracking

## The pattern

Two flavors, both on a 2D board. Pick the one that matches the question.

**A. Explore from a cell (Word Search).** Step onto a cell, try the 4 neighbors, step off. The mark you leave on a cell belongs only to the current path, so you must remove it when you leave.

```python
def dfs(r, c, i):
    if i == len(word): return True                     # all letters matched
    if <out of bounds or wrong letter or visited>: return False
    mark (r, c)                                        # choose
    found = dfs(r+1, c, i+1) or dfs(r-1, c, i+1) or dfs(r, c+1, i+1) or dfs(r, c-1, i+1)   # explore
    unmark (r, c)                                      # un-choose
    return found
```

**B. Place one item per row (N-Queens).** Fill the board row by row. In each row, try every column and skip squares already attacked by an earlier placement.

```python
def backtrack(r):
    if r == n: save board (or count += 1); return      # every row filled
    for c in range(n):
        if c in col or (r + c) in posDiag or (r - c) in negDiag: continue   # attacked
        place queen; add c, r+c, r-c to the sets       # choose
        backtrack(r + 1)                               # explore
        remove queen; remove c, r+c, r-c               # un-choose
```

## How to spot this topic

* **Flavor A:** the input is a **grid**, and you look for a **path** or a **word** through **adjacent cells**, without reusing a cell.
* **Flavor B:** you must **place items on a board** so that **none of them conflict**, and the answer is the board layouts (or how many there are).
* Quick test: *is the "state" a position on a 2D board?* If yes, it's this topic.
* Then ask: *am I walking a path (A), or placing one thing per row/column with rules (B)?*

**Not this topic if:** the grid question asks for the **shortest** path or a **count of regions** (that is BFS/DFS from the Graphs repo), or asks for a **min/max** value (that is DP).

## Problems here

| # | Problem | What changes from the pattern |
|---|---|---|
| 11 | [Word Search](11-word-search.md) | Flavor A — mark / unmark cells |
| 12 | [N-Queens](12-n-queens.md) | Flavor B — three attack sets, save the board |
| 13 | [N-Queens II](13-n-queens-ii.md) | Flavor B — same search, just `res += 1` |
