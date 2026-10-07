# 208. Implement Trie (Prefix Tree)

**Category:** NC150 / LeetCode Top 150 | **Difficulty:** Medium | **Pattern:** Trie Node Traversal & Marker Tracking

---

### 1. The Core Logic

A **Trie** is a tree data structure used for efficient retrieval of keys in dataset of strings.

* **Node Structure:**
* `children`: A hash map (or fixed-size array of size 26) mapping characters to child `TrieNode`s.
* `is_end_of_word`: A boolean flag signaling if a complete word ends at that specific node.


* **Operations:**
* **`insert(word)`:** Iterate character by character starting from `root`. Create a new node whenever a path does not exist. Mark the final node's `is_end_of_word = True`.
* **`search(word)`:** Traverse path for `word`. Returns `True` **only if** the path exists AND the final node has `is_end_of_word == True`.
* **`startsWith(prefix)`:** Traverse path for `prefix`. Returns `True` as long as the entire character path exists (regardless of `is_end_of_word`).



---

### 2. Code Implementation

```python
class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False


class Trie:

    def __init__(self):
        self.root = TrieNode()

    def insert(self, word: str) -> None:
        curr = self.root
        for char in word:
            if char not in curr.children:
                curr.children[char] = TrieNode()
            curr = curr.children[char]
        curr.is_end_of_word = True

    def search(self, word: str) -> bool:
        curr = self.root
        for char in word:
            if char not in curr.children:
                return False
            curr = curr.children[char]
        return curr.is_end_of_word

    def startsWith(self, prefix: str) -> bool:
        curr = self.root
        for char in prefix:
            if char not in curr.children:
                return False
            curr = curr.children[char]
        return True


# Your Trie object will be instantiated and called as such:
# obj = Trie()
# obj.insert(word)
# param_2 = obj.search(word)
# param_3 = obj.startsWith(prefix)

```

---

### 3. Step-by-Step Dry Run

Tracing **Example 1**:

```text
Operations: insert("apple"), search("apple"), search("app"), startsWith("app")

Root
 └── 'a'
      └── 'p'
           └── 'p' [is_end_of_word = False]
                └── 'l'
                     └── 'e' [is_end_of_word = True]

```

1. **`insert("apple")`**: Traverses/creates nodes for `'a' -> 'p' -> 'p' -> 'l' -> 'e'`. Sets `e.is_end_of_word = True`.
2. **`search("apple")`**: Follows path to `'e'`. Since `e.is_end_of_word == True`, returns **`True`**.
3. **`search("app")`**: Follows path to second `'p'`. Path exists, but `p.is_end_of_word == False`. Returns **`False`**.
4. **`startsWith("app")`**: Follows path to second `'p'`. Path exists. Returns **`True`**.

---

### 4. Complexity Analysis

| Operation | Time Complexity | Auxiliary Space Complexity |
| --- | --- | --- |
| **`insert(word)`** | $\mathcal{O}(L)$ | $\mathcal{O}(L)$ for new nodes created |
| **`search(word)`** | $\mathcal{O}(L)$ | $\mathcal{O}(1)$ |
| **`startsWith(prefix)`** | $\mathcal{O}(L)$ | $\mathcal{O}(1)$ |

*(where $L$ is the length of `word` or `prefix`)*

---

### 5. Quick Revision Summary (30-Second Recall)

* **Node Blueprint:** `self.children = {}` and `self.is_end_of_word = False`.
* **Search vs StartsWith:** `search` requires `curr.is_end_of_word == True` at the end; `startsWith` only requires reaching the end of the prefix path.
* **Key Advantage:** Fast string lookups in $\mathcal{O}(L)$ independent of total stored words ($N$).

---
