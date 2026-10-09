# 131. Palindrome Partitioning

**LC 131** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** String Partitioning Backtracking

---

## 1. Intuition

Imagine cutting the string with scissors. Standing at `start`, decide where the **first piece** ends. Try every end position. If the piece is a palindrome, keep it and solve the exact same problem on the rest of the string. If it isn't, don't go down that cut.

* `for end in range(start + 1, n + 1)` — every possible length for the first piece.
* `string == string[::-1]` — the only rule: the piece must be a palindrome. It's checked *before* recursing, so bad cuts die immediately.
* `bt_dfs(end, path)` — the rest of the string begins where this piece ended.
* `start == n` — nothing left to cut, so `path` is a complete valid partition. Save `path.copy()`.

**Recall:** pick a first piece (must be a palindrome), recurse on the rest, done when `start` reaches the end.

---

## 2. Template

* **Choose:** `path.append(string)` — take the piece `s[start:end]`
* **Explore:** `bt_dfs(end, path)`
* **Un-choose:** `path.pop()`
* **Prune / dedup:** only recurse if `string == string[::-1]`.

---

## 3. Code

```python
class Solution:
    def partition(self, s: str) -> list[list[str]]:
        res = []
        n = len(s)

        def bt_dfs(start: int, path: list[str]):
            # Base Case: String completely partitioned
            if start == n:
                res.append(path.copy())
                return

            # Try partitioning at every possible end index
            for end in range(start + 1, n + 1):
                string = s[start:end]

                # Constraint Check: Only recurse if current slice is a palindrome
                if string == string[::-1]:
                    # Choice: TAKE partition s[start:end]
                    path.append(string)
                    
                    # Recurse from new start position 'end'
                    bt_dfs(end, path)
                    
                    # Backtrack
                    path.pop()

        bt_dfs(0, [])
        return res

```

---

## 4. Dry Run (`s = "aab"`)

```text
                               bt_dfs(start=0, path=[]) -> res: []
                              /                        \
                  end=1 ("a") /                          \ end=2 ("aa")
                             /                            \
                bt_dfs(start=1, path=["a"])             bt_dfs(start=2, path=["aa"])
               /                     \                             |
   end=2 ("a") /                       \ end=3 ("ab")              | end=3 ("b")
              /                         \ (Not Palindrome)         |
  bt_dfs(2, ["a", "a"])                  \                  bt_dfs(3, ["aa", "b"])
         |                                \                  Base Case: start == 3!
   end=3 | ("b")                          \                  res: [["a","a","b"],
  bt_dfs(3, ["a", "a", "b"])               \                        ["aa","b"]]
   Base Case: start == 3!                   \
  res: [["a", "a", "b"]]                     \

```

---

## 5. Complexity

* **Time: O(n · 2^n)** — a string of length `n` has up to `2^(n-1)` ways to cut (worst case `"aaaa"`, where every piece is a palindrome). Each palindrome check `string[::-1]` costs up to `n`.
* **Space: O(n)** — recursion depth and `path` are at most `n` (the output list isn't counted).

---

## 6. Recall (30 seconds)

* Loop `end` from `start + 1` to `n` — every possible first piece.
* Recurse only if the piece is a palindrome; new `start` is `end`.
* `start == n` → save a copy of `path`.
