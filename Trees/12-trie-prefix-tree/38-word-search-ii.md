# 212. Word Search II

**Category:** NC150 / LeetCode Top 150 | **Difficulty:** Hard | **Pattern:** Backtracking + Trie with Dynamic Pruning

---

### 1. The Core Logic

Combining **Trie** with **Backtracking DFS** enables searching all dictionary words simultaneously on a 2D grid instead of running independent searches per word.

* **Prefix Matching via Trie:** Build a Trie of all dictionary words. If a character on the board is not in `node.children`, prune that search path immediately.
* **Trie Pruning (Essential for Hard Constraints):**
* When a word is matched, set `node.word = None` so it isn't recorded again.
* If a `child` node has no remaining children after DFS returns, delete it from `curr.children`. This collapses branch paths once all words under them are discovered.


* **In-Place Cell Marking:** Temporarily replace `board[r][c]` with `'#'` to mark it visited, then restore it on backtracking.

---

### 2. Optimized Code Implementation

```python
from typing import List

class TrieNode:
    def __init__(self):
        self.children = {}
        self.word = None  # Stores full word at terminal node

    def addWord(self, word: str) -> None:
        curr = self
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.word = word


class Solution:
    def findWords(self, board: List[List[str]], words: List[str]) -> List[str]:
        root = TrieNode()
        for w in words:
            root.addWord(w)

        ROWS, COLS = len(board), len(board[0])
        res = []

        def dfs(r: int, c: int, parent: TrieNode):
            char = board[r][c]
            curr = parent.children[char]

            # 1. Match check
            if curr.word:
                res.append(curr.word)
                curr.word = None  # Prevent duplicate additions

            # 2. Mark visited in-place
            board[r][c] = '#'

            # 3. Explore 4-directional neighbors
            for dr, dc in ((-1, 0), (1, 0), (0, -1), (0, 1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < ROWS and 0 <= nc < COLS and board[nr][nc] in curr.children:
                    dfs(nr, nc, curr)

            # 4. Backtrack board cell
            board[r][c] = char

            # 5. Trie Pruning: Leaf node cleanup
            if not curr.children:
                del parent.children[char]

        # Start DFS from every cell matching root's children
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] in root.children:
                    dfs(r, c, root)

        return res

```

---

### 3. Step-by-Step Dry Run

Tracing `board = [["o","a"],["e","t"]]`, `words = ["oath"]`:

```text
  o  a
  e  t

```

1. `(r=0, c=0)` has character `'o'`, which is in `root.children`.
2. `dfs(0, 0, root)`:
* `curr = node('o')`. `board[0][0]` becomes `'#'`.
* Check neighbor `(0, 1)` $\rightarrow$ `'a'` is in `curr.children`. Calls `dfs(0, 1, node('o'))`.
* `curr = node('a')`. `board[0][1]` becomes `'#'`.
* Check neighbor `(1, 1)` $\rightarrow$ `'t'` is in `curr.children`. Calls `dfs(1, 1, node('a'))`.
* `curr = node('t')`. `board[1][1]` becomes `'#'`.
* Check neighbor `(1, 0)` $\rightarrow$ `'e'` is NOT in `node('t').children` (needs `'h'`).


3. Backtracks `board[1][1] = 't'`.
4. After exploring all paths, leaf nodes without remaining children are pruned from their parents using `del parent.children[char]`.

---

### 4. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(M \cdot N \cdot 3^{L-1})$ worst-case without pruning, where $M \times N$ is grid size and $L$ is maximum word length. With dynamic Trie pruning, the actual runtime drops close to $\mathcal{O}(\text{Total Letters in Grid})$.
* **Space Complexity:** $\mathcal{O}(W \cdot L)$ for Trie construction (where $W$ is total words and $L$ is max word length), plus $\mathcal{O}(L)$ for recursion stack depth.

---

### 5. Quick Revision Summary (30-Second Recall)

* **Trie + Grid DFS:** Eliminates redundant searches across shared prefixes (`"eat"`, `"oath"`).
* **Word Storage:** Save `word` inside terminal nodes to eliminate string building during DFS.
* **Pruning Strategy:** Delete dead Trie nodes (`del parent.children[char]`) when `not curr.children` to avoid re-searching exhausted paths.

---
