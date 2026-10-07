# 94. Binary Tree Inorder Traversal (with Preorder & Postorder comparison)

**Category:** [+] Claude | **Difficulty:** Easy | **Pattern:** Iterative Traversal / Explicit Stack

Both the **Recursive** and **Iterative** implementations for **Inorder**, **Preorder**, and **Postorder** traversals, for comparison.

---

### Traversal Orders Overview

* **Inorder:** Left $\rightarrow$ Root $\rightarrow$ Right
* **Preorder:** Root $\rightarrow$ Left $\rightarrow$ Right
* **Postorder:** Left $\rightarrow$ Right $\rightarrow$ Root

---

### 1. Inorder Traversal (LC 94)

#### Recursive Implementation

```python
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res = []
        
        def dfs(node):
            if not node:
                return
            dfs(node.left)
            res.append(node.val)
            dfs(node.right)
            
        dfs(root)
        return res

```

#### Iterative Implementation (Explicit Stack)

```python
class Solution:
    def inorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res, stack = [], []
        cur = root
        
        while cur or stack:
            # Go as far left as possible
            while cur:
                stack.append(cur)
                cur = cur.left
            
            # Process node
            cur = stack.pop()
            res.append(cur.val)
            
            # Move to right subtree
            cur = cur.right
            
        return res

```

---

### 2. Preorder Traversal (LC 144)

#### Recursive Implementation

```python
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res = []
        
        def dfs(node):
            if not node:
                return
            res.append(node.val)
            dfs(node.left)
            dfs(node.right)
            
        dfs(root)
        return res

```

#### Iterative Implementation (Explicit Stack)

```python
class Solution:
    def preorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
            
        res, stack = [], [root]
        
        while stack:
            node = stack.pop()
            res.append(node.val)
            
            # Push right child first so left child is processed first (LIFO stack)
            if node.right:
                stack.append(node.right)
            if node.left:
                stack.append(node.left)
                
        return res

```

---

### 3. Postorder Traversal (LC 145)

#### Recursive Implementation

```python
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        res = []
        
        def dfs(node):
            if not node:
                return
            dfs(node.left)
            dfs(node.right)
            res.append(node.val)
            
        dfs(root)
        return res

```

#### Iterative Implementation (Reverse Preorder Trick)

> **Key Insight:** Standard Preorder goes `Root -> Left -> Right`. If you traverse `Root -> Right -> Left` and reverse the final list, you get `Left -> Right -> Root` (Postorder).

```python
class Solution:
    def postorderTraversal(self, root: Optional[TreeNode]) -> List[int]:
        if not root:
            return []
            
        res, stack = [], [root]
        
        while stack:
            node = stack.pop()
            res.append(node.val)
            
            # Push left first so right is processed first
            if node.left:
                stack.append(node.left)
            if node.right:
                stack.append(node.right)
                
        # Reverse to transform (Root -> Right -> Left) into (Left -> Right -> Root)
        return res[::-1]

```

---

### Complexity Comparison

| Traversal Method | Time Complexity | Space Complexity (Recursive) | Space Complexity (Iterative) |
| --- | --- | --- | --- |
| **Inorder** | $\mathcal{O}(n)$ | $\mathcal{O}(h)$ call stack | $\mathcal{O}(h)$ explicit stack |
| **Preorder** | $\mathcal{O}(n)$ | $\mathcal{O}(h)$ call stack | $\mathcal{O}(h)$ explicit stack |
| **Postorder** | $\mathcal{O}(n)$ | $\mathcal{O}(h)$ call stack | $\mathcal{O}(h)$ explicit stack |

*Note: $h$ represents the height of the tree ($\mathcal{O}(\log n)$ for balanced trees, $\mathcal{O}(n)$ for skewed trees).*

---
