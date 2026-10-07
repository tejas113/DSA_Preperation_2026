# 297. Serialize and Deserialize Binary Tree

**Category:** NC150 / LeetCode Top 150 | **Difficulty:** Hard | **Pattern:** Pre-Order DFS / Marker Encoding

---

### 1. The Core Logic

Standard preorder traversal alone cannot uniquely reconstruct a tree because it doesn't specify where leaves terminate. However, if we **explicitly record null children** as a designated marker (e.g., `'N'`), Pre-Order traversal uniquely represents any binary tree structure.

1. **Serialization (Tree $\rightarrow$ String):**
* Perform Pre-Order DFS (`Root -> Left -> Right`).
* If a node is `None`, append `'N'` to our result array.
* If a node exists, append `str(node.val)` and recursively call `dfs(node.left)` then `dfs(node.right)`.
* Join elements with commas: `",".join(vals)`.


2. **Deserialization (String $\rightarrow$ Tree):**
* Split the string by commas into an array `vals`.
* Maintain a global pointer/index `self.i`.
* Read `vals[self.i]`:
* If `'N'`, increment `self.i` and return `None`.
* Otherwise, construct `node = TreeNode(int(vals[self.i]))`, increment `self.i`, then assign `node.left = dfs()` and `node.right = dfs()`.





---

### 2. Code Implementation

```python
# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Codec:

    def serialize(self, root):
        """Encodes a tree to a single string.
        
        :type root: TreeNode
        :rtype: str
        """
        vals = []

        def dfs(node):
            if not node:
                vals.append('N')
                return

            vals.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(vals)

    def deserialize(self, data):
        """Decodes your encoded data to tree.
        
        :type data: str
        :rtype: TreeNode
        """
        vals = data.split(',')
        self.i = 0
        
        def dfs():
            if vals[self.i] == "N":
                self.i += 1
                return None

            node = TreeNode(int(vals[self.i]))
            self.i += 1

            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()

# Your Codec object will be instantiated and called as such:
# ser = Codec()
# deser = Codec()
# ans = deser.deserialize(ser.serialize(root))

```

---

### 3. Step-by-Step Dry Run

Tracing **Example 1**: `root = [1, 2, 3, null, null, 4, 5]`

```text
        1
       / \
      2   3
         / \
        4   5

```

#### Serialization Steps:

1. `dfs(1)` $\rightarrow$ `['1']`
2. `dfs(2)` $\rightarrow$ `['1', '2']`
3. `dfs(2.left)` $\rightarrow$ `['1', '2', 'N']`
4. `dfs(2.right)` $\rightarrow$ `['1', '2', 'N', 'N']`
5. `dfs(3)` $\rightarrow$ `['1', '2', 'N', 'N', '3']`
6. `dfs(4)` $\rightarrow$ `['1', '2', 'N', 'N', '3', '4', 'N', 'N']`
7. `dfs(5)` $\rightarrow$ `['1', '2', 'N', 'N', '3', '4', 'N', 'N', '5', 'N', 'N']`

**Serialized Output:** `"1,2,N,N,3,4,N,N,5,N,N"`

#### Deserialization Steps:

* `vals = ["1", "2", "N", "N", "3", "4", "N", "N", "5", "N", "N"]`
* `self.i = 0`: Reads `"1"` $\rightarrow$ Creates Root `1`. Advances `self.i = 1`.
* Recurse `node.left`: Reads `"2"` $\rightarrow$ Creates Node `2`. Reads `"N"`, `"N"` for children $\rightarrow$ returns Node `2`.
* Recurse `node.right`: Reads `"3"` $\rightarrow$ Creates Node `3`. Recurses `4` and `5` for children.
* Returns recreated Root `1`.

---

### 4. Complexity Analysis

* **Time Complexity:** $\mathcal{O}(N)$ — Both `serialize` and `deserialize` visit every node and null marker exactly once.
* **Space Complexity:** $\mathcal{O}(N)$ — To store the serialized string/list representation and handle the recursion stack.

---

### 5. Quick Revision Summary (30-Second Recall)

* **Pre-Order Structure:** Pre-order traversal with explicit null markers (`'N'`) preserves full tree topology.
* **Pointer Management:** During deserialization, consume elements sequentially using a shared index `self.i`.
* **Subtree Construction:** Always assign `node.left = dfs()` before `node.right = dfs()` to mirror the Pre-Order sequence.

---
