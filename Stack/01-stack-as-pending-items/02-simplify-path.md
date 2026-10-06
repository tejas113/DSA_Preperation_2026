# 71. Simplify Path

**LC 71** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Split into parts + stack of directory names (`..` pops)

---

## 1. Intuition

A path is a walk: each folder name goes one level deeper, and `..` steps back out. The stack is your current location, from the root down to where you are now. Split the path into parts, push folder names, pop on `..`, and ignore the noise.

* `stack` holds the **directory names** (strings) of the current location. The top, `stack[-1]`, is the folder you are in.
* `path.split("/")` turns slashes into parts. Doubled slashes create empty parts, which `portion == ""` skips.
* `portion == "."` means "stay here", so it is skipped too.
* `portion == ".."` runs `stack.pop()` only `if stack:`, because you can't go above the root.
* Anything else, including `"..."`, is a real folder name, so `stack.append(portion)`.
* `"/" + "/".join(stack)` rebuilds the path, and an empty `stack` gives just `"/"`.

**Recall:** split on `/`, skip `""` and `.`, pop on `..` (if not empty), push everything else, then join.

## 2. Approach

* **Idea:** Break the path into parts. Walk through them, keeping the current folder chain on a stack. Join the stack at the end.
* **Data structure / pointers:** `components` is the list of parts from `split("/")`. `portion` is the current part. `stack` is a plain list of folder names (top is `stack[-1]`).
* **Invariant:** after each part, `stack` is the simplified path of everything read so far, with the root at the bottom and the current folder on top.
* **Edge cases:**
  * **Stack empty when `..` arrives** (`"/../"`): the `if stack:` check is false, so nothing is popped and the answer stays `"/"`.
  * **Repeated slashes** (`"///home///"`): the extra `""` parts are skipped, giving `"/home"`.
  * **Three dots** (`"/..."`): not equal to `"."` or `".."`, so it is a folder name and gives `"/..."`.
  * **Root only** (`"/"`): `split` gives `["", ""]`, both skipped, so the result is `"/"`.
  * **Trailing slash** (`"/home/"`): the final `""` is skipped, so the result is `"/home"`.

## 3. Code

```python
class Solution:

    def simplifyPath(self, path: str) -> str:
        stack = []
        # Split path by '/' to get individual tokens
        components = path.split("/")

        for portion in components:
            if portion == "" or portion == ".":
                # Skip redundant slashes and current directory pointers
                continue
            elif portion == "..":
                # Go up one directory level if possible
                if stack:
                    stack.pop()
            else:
                # Valid file/directory name (e.g., "home", "...", "foo")
                stack.append(portion)

        # Reconstruct canonical path starting with '/'
        return "/" + "/".join(stack)


if __name__ == "__main__":
    solution = Solution()
    assert solution.simplifyPath("/home/") == "/home"
    assert solution.simplifyPath("/home//foo/") == "/home/foo"
    assert solution.simplifyPath("/home/user/Documents/../Pictures") == "/home/user/Pictures"
    assert solution.simplifyPath("/../") == "/"
    assert solution.simplifyPath("/.../a/../b/c/../d/./") == "/.../b/d"
    assert solution.simplifyPath("/") == "/"
    assert solution.simplifyPath("///home///") == "/home"
    assert solution.simplifyPath("/...") == "/..."
    print("All tests passed")
```

## 4. Dry Run

Input: `path = "/.../a/../b/c/../d/./"`

`split("/")` gives `["", "...", "a", "..", "b", "c", "..", "d", ".", ""]`

| Step | `portion` | Action | `stack` after |
|---|---|---|---|
| 1 | `""` | Skip | `[]` |
| 2 | `"..."` | Folder name, push | `["..."]` |
| 3 | `"a"` | Push | `["...", "a"]` |
| 4 | `".."` | Pop `"a"` | `["..."]` |
| 5 | `"b"` | Push | `["...", "b"]` |
| 6 | `"c"` | Push | `["...", "b", "c"]` |
| 7 | `".."` | Pop `"c"` | `["...", "b"]` |
| 8 | `"d"` | Push | `["...", "b", "d"]` |
| 9 | `"."` | Skip | `["...", "b", "d"]` |
| 10 | `""` | Skip | `["...", "b", "d"]` |

Result: `"/" + "/".join(["...", "b", "d"])` = `"/.../b/d"`

## 5. Complexity

* **Time:** O(n), because `split` reads the string once and the loop visits each part once with O(1) push or pop, and `join` is O(n).
* **Space:** O(n), because `components` and `stack` together hold at most all the characters of `path`.

## 6. Recall (30 seconds)

* `split("/")`, then skip `""` and `"."`.
* `".."` pops only `if stack:` (no going above root). Any other name, even `"..."`, is pushed.
* Return `"/" + "/".join(stack)`, which is `"/"` when the stack is empty.
