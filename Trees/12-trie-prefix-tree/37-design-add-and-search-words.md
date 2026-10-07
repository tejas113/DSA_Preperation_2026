# 211. Design Add and Search Words Data Structure

**Category:** NC150 / LeetCode Top 150 | **Difficulty:** Medium | **Pattern:** Trie + Backtracking (DFS)

---

### 1. The Core Logic

This problem extends the standard Trie structure to support wildcard searching where `'.'` matches any character.

1. **`addWord(word)`:**
* Standard Trie insertion logic. Traverse character by character, adding nodes as necessary, and set `is_word = True` at the target terminal node.


2. **`search(word)`:**
* Use recursive DFS tracking `(index, node)`:
* **Literal Character:** If `word[i]` is a lowercase letter, navigate directly to `curr.children[char]`. If absent, return `False`.
* **Wildcard Character (`'.'`):** Branch out by calling `dfs(i + 1, child)` for **every** existing child node in `curr.children.values()`. If any branch returns `True`, return `True` immediately.
* **Base Case:** When `index == len(word)`, return `curr.is_word`.





---

### 2. Code Implementation

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_word = False

class WordDictionary:

    def __init__(self):
        self.root = TrieNode()

    def addWord(self, word: str) -> None:
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_word = True

    def search(self, word: str) -> bool:
        def dfs(index, node):
            curr = node
            for i in range(index, len(word)):
                char = word[i]
                if char == '.':
                    for child in curr.children.values():
                        if dfs(i + 1, child):
                            return True
                    return False
                else:
                    if char not in curr.children:
                        return False
                    curr = curr.children[char]
            return curr.is_word
        
        return dfs(0, self.root)

# Your WordDictionary object will be instantiated and called as such:
# obj = WordDictionary()
# obj.addWord(word)
# param_2 = obj.search(word)

```

---

### 3. Step-by-Step Dry Run

Tracing `addWord("bad")`, `addWord("dad")`, `addWord("mad")`, then `search(".ad")`:

```text
       Root
     /  |  \
    b   d   m
    |   |   |
    a   a   a
    |   |   |
    d*  d*  d*   (* indicates is_word = True)

```

1. **`search(".ad")`**:
* Starts at `dfs(0, Root)`. `word[0]` is `'.'`.
* Branches to all children of `Root`: `['b', 'd', 'm']`.


2. **Branch 1 (`'b'` node)**:
* Next call is `dfs(1, node_b)`.
* `word[1]` is `'a'`: matches `node_b.children['a']`. Moves to `node_ba`.
* `word[2]` is `'d'`: matches `node_ba.children['d']`. Moves to `node_bad`.
* Loop completes. Returns `node_bad.is_word` $\rightarrow$ **`True`**.


3. **Short-circuit:** Branch 1 returned `True`, so `search(".ad")` short-circuits and immediately returns **`True`**.

---

### 4. Complexity Analysis

* **`addWord(word)`:**
* **Time Complexity:** $\mathcal{O}(L)$ — where $L$ is the length of `word`.
* **Space Complexity:** $\mathcal{O}(L)$ — for adding new Trie nodes.


* **`search(word)`:**
* **Time Complexity:**
* **No dots:** $\mathcal{O}(L)$
* **With dots:** Worst-case $\mathcal{O}(\Sigma^K \cdot L)$ where $\Sigma = 26$ (alphabet size) and $K$ is the number of dots. Given the constraint of at most 2 dots, the search space remains tightly bounded.


* **Space Complexity:** $\mathcal{O}(L)$ call stack depth for recursive DFS.



---

### 5. Quick Revision Summary (30-Second Recall)

* **Hybrid DFS Approach:** Process normal letters iteratively to keep call stacks light; switch to recursive DFS only when encountering `'.'`.
* **Wildcard Branching:** `'.'` requires iterating through all active nodes in `curr.children.values()`.
* **Early Exit:** Return `True` as soon as any wildcard recursive branch yields a match.

---
