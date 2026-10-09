# 17. Letter Combinations of a Phone Number

**LC 17** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Build-a-String Backtracking (fixed mapping)

---

## 1. Intuition

Think of the digits as slots in a row. For each slot pick **one** of the letters on that key. So the depth of the recursion is the position in `digits`, and each level branches over that key's letters (3 or 4).

* `index` — which digit we're deciding now. `string` — the letters picked so far.
* `for char in digitToChar[digits[index]]` — branch on every letter of the current digit.
* `backtrack(index + 1, string + char)` — pick that letter and move on to the next digit.
* `len(string) == len(digits)` — every digit has a letter, so save `string`.
* There is **no `.pop()`**: `string + char` builds a *new* string for the child call, so the parent's `string` is untouched. The undo happens automatically when the call returns.
* `if digits:` — guards the empty input, so we return `[]` and not `[""]`.

**Recall:** depth = digit index, branches = that digit's letters, no `pop` because strings are immutable.

---

## 2. Template

* **Choose:** `string + char` — a new string for the child call
* **Explore:** `backtrack(index + 1, string + char)`
* **Un-choose:** automatic — the parent's `string` was never changed
* **Prune / dedup:** none — every letter is valid; the only limit is the length of `digits`.

---

## 3. Code

```python
class Solution:
    def letterCombinations(self, digits: str) -> list[str]:
        res = []
        digitToChar = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "pqrs",
            "8": "tuv",
            "9": "wxyz",
        }

        def backtrack(index: int, string: str):
            # Base Case: String length matches digits length
            if len(string) == len(digits):
                res.append(string)
                return

            # Branching: Try every character mapped to current digit
            for char in digitToChar[digits[index]]:
                # Recurse with incremented index and updated string candidate
                backtrack(index + 1, string + char)

        # Guard against empty input string
        if digits:
            backtrack(0, "")

        return res

```

---

## 4. Dry Run (`digits = "23"`)

```text
                                     backtrack(0, "")
                     /                      |                      \
            'a'     /              'b'      |              'c'      \
                   /                        |                        \
        backtrack(1, "a")            backtrack(1, "b")            backtrack(1, "c")
        /       |       \            /       |       \            /       |       \
     'd'|    'e'|    'f'|         'd'|    'e'|    'f'|         'd'|    'e'|    'f'|
        v       v       v            v       v       v            v       v       v
      "ad"    "ae"    "af"         "bd"    "be"    "bf"         "cd"    "ce"    "cf"

```

---

## 5. Complexity

* **Time: O(n · 4^n)** — `n` is `len(digits)`. Each digit has at most 4 letters (`7` and `9`), so there are at most `4^n` strings, and each is built by `n` concatenations.
* **Space: O(n)** — the recursion is at most `n` deep (each call holds a string of up to `n` characters; the output list isn't counted).

---

## 6. Recall (30 seconds)

* Depth = position in `digits`; branches = that digit's letters.
* Save when `len(string) == len(digits)`.
* `string + char` needs no `pop`; guard `if digits:` for empty input.
