# 79. Word Search

**LC 79** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Grid DFS Backtracking (mark / unmark)

---

## 1. Intuition

Walk through the grid one letter at a time. You may step up, down, left or right, and you may not step on the same cell twice in one path. `dfs(r, c, i)` means: *"I'm standing on cell `(r, c)` and it must match `word[i]`."*

* `i == len(word)` — every letter matched. Return `True`.
* The guard line (out of bounds, wrong letter, or `(r, c) in visited`) — a dead end. Return `False`.
* `visited.add((r, c))` — **paint** this cell as used on the current path.
* The four `dfs(...)` calls joined with `or` — try each neighbor for the next letter `i + 1`. `or` stops as soon as one direction finds the word.
* `visited.remove((r, c))` — **unpaint when you leave.** The paint belongs only to the current path; another path may need this cell later.
* The outer double loop — the word can start from any cell.

**Recall:** mark the cell → try 4 directions → unmark the cell.

---

## 2. Template

* **Choose:** `visited.add((r, c))` — step onto the cell
* **Explore:** `dfs(...)` on the 4 neighbors with `i + 1`
* **Un-choose:** `visited.remove((r, c))`
* **Prune / dedup:** return `False` immediately if the cell is out of bounds, doesn't match `word[i]`, or is already visited.

---

## 3. Code

```python
class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        rows, columns = len(board), len(board[0])
        visited = set()

        def dfs(r, c, i):
            # Base Case: All characters in word matched
            if i == len(word):
                return True

            # Boundary, Character Match, and Visited Guard
            if not (0 <= r < rows and 0 <= c < columns) or board[r][c] != word[i] or (r, c) in visited:
                return False

            # Choice: Mark cell as visited
            visited.add((r, c))

            # Recurse: Explore 4 directional neighbors
            found = (
                dfs(r + 1, c, i + 1) or 
                dfs(r - 1, c, i + 1) or 
                dfs(r, c + 1, i + 1) or 
                dfs(r, c - 1, i + 1)
            )

            # Backtrack: Unmark cell
            visited.remove((r, c))

            return found

        for r in range(rows):
            for c in range(columns):
                if dfs(r, c, 0):
                    return True

        return False

```

### Alternative: In-Place Marking + Frequency Pruning

Same paint/unpaint idea without a `visited` set: write `'#'` into the cell and restore it. Two quick pruning checks run first: the board must contain enough of each letter, and the word is reversed if its last letter is rarer than its first (fewer starting points).

```python
from collections import Counter

class Solution:
    def exist(self, board: list[list[str]], word: str) -> bool:
        rows, cols = len(board), len(board[0])
        
        # Pruning 1: Board character frequency check
        board_counts = Counter(char for row in board for char in row)
        word_counts = Counter(word)
        for char, count in word_counts.items():
            if board_counts[char] < count:
                return False
        
        # Pruning 2: Reverse word if last letter is rarer than first letter
        if board_counts[word[0]] > board_counts[word[-1]]:
            word = word[::-1]

        def dfs(r, c, i):
            if i == len(word):
                return True
            
            if not (0 <= r < rows and 0 <= c < cols) or board[r][c] != word[i]:
                return False

            # In-place marking (saves hash set memory/lookup time)
            temp = board[r][c]
            board[r][c] = '#'

            found = (
                dfs(r + 1, c, i + 1) or
                dfs(r - 1, c, i + 1) or
                dfs(r, c + 1, i + 1) or
                dfs(r, c - 1, i + 1)
            )

            # Backtrack
            board[r][c] = temp
            return found

        for r in range(rows):
            for c in range(cols):
                if dfs(r, c, 0):
                    return True

        return False

```

---

## 4. Dry Run (`board = [["A","B"],["C","D"]]`, `word = "ABD"`)

```text
                                  dfs(r=0, c=0, i=0) ['A' == 'A']
                                 /                \
                       dfs(1, 0, 1) ['C']       dfs(0, 1, 1) ['B' == 'B']
                       ('C' != 'B')              /                 \
                          (FAIL)        dfs(0, 0, 2) ['A']       dfs(1, 1, 2) ['D' == 'D']
                                         (Already Visited)                  |
                                                                   dfs(1, 1, 3) (i == 3)
                                                                    Base Case True!

```

---

## 5. Complexity

* **Time: O(M · N · 3^L)** — `M × N` possible start cells; each search goes at most `L` letters deep, and after the first step it has at most 3 directions (the fourth is the cell you just came from, which is painted).
* **Space: O(L)** — recursion depth is at most `L`, plus the `visited` set holds at most `L` cells (the in-place version drops the set).

---

## 6. Recall (30 seconds)

* `dfs(r, c, i)`: cell must match `word[i]`; `i == len(word)` means success.
* Mark the cell, try 4 neighbors joined by `or`, then **unmark**.
* Try every cell as a start.
