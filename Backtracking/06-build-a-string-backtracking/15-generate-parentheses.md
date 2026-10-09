# 22. Generate Parentheses

**LC 22** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Build-a-String Backtracking (counter constraints)

---

## 1. Intuition

Build the string one character at a time, and only ever add a character that keeps the string **well-formed**. Then every string that reaches length `2n` is guaranteed valid, and no final validity check is needed.

* `open_count < n` → may add `'('`. We have `n` pairs, so at most `n` opening brackets.
* `closing_count < open_count` → may add `')'`. A `')'` needs an unmatched `'('` before it. If the counts are equal, every `'('` is already closed, and another `')'` would give something like `")"` or `"())"`.
* `len(current_str) == 2 * n` — all `n` pairs are placed. Save `current_str`.
* `current_str + "("` builds a *new* string for the child call, so there is no `.pop()` — the undo is automatic.

**Recall:** `(` while `open < n`; `)` while `close < open`.

---

## 2. Template

* **Choose:** `current_str + "("` or `current_str + ")"` — a new string for the child call
* **Explore:** `backtrack(open_count + 1, closing_count, ...)` or `backtrack(open_count, closing_count + 1, ...)`
* **Un-choose:** automatic — the parent's `current_str` was never changed
* **Prune / dedup:** add `'('` only if `open_count < n`; add `')'` only if `closing_count < open_count`.

---

## 3. Code

```python
class Solution:
    def generateParenthesis(self, n: int) -> list[str]:
        res = []

        def backtrack(open_count: int, closing_count: int, current_str: str):
            # Base Case: Total length equals 2 * n (n pairs placed)
            if len(current_str) == 2 * n:
                res.append(current_str)
                return

            # Choice 1: Add '(' if we haven't reached the limit of 'n'
            if open_count < n:
                backtrack(open_count + 1, closing_count, current_str + "(")

            # Choice 2: Add ')' if there are unmatched '(' to close
            if closing_count < open_count:
                backtrack(open_count, closing_count + 1, current_str + ")")

        backtrack(0, 0, "")
        return res

```

---

## 4. Dry Run (`n = 2`)

```text
                                  backtrack(0, 0, "")
                                           |
                                  backtrack(1, 0, "(")
                                 /                    \
                     backtrack(2, 0, "((")        backtrack(1, 1, "()")
                               |                            |
                     backtrack(2, 1, "(()")       backtrack(2, 1, "()(")
                               |                            |
                     backtrack(2, 2, "(())")      backtrack(2, 2, "()()")
                            [Base Case]                  [Base Case]

```

---

## 5. Complexity

* **Time: O(4^n / √n)** — the code only ever builds valid prefixes, so the number of results is the n-th Catalan number ≈ `4^n / (n·√n)`. Each result has length `2n`, which multiplies it by `n`.
* **Space: O(n)** — recursion depth is at most `2n` (the output list isn't counted).

---

## 6. Recall (30 seconds)

* Add `(` only while `open_count < n`.
* Add `)` only while `closing_count < open_count`.
* The number of results is the Catalan number → about `4^n / √n` work.
