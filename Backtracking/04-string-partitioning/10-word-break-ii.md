# 140. Word Break II

**LC 140** · **Source:** [+] Claude · **Difficulty:** Hard · **Priority:** Stretch · **Pattern:** String Partitioning Backtracking (memoization is the follow-up)

---

## 1. Intuition

Same scissors idea as Palindrome Partitioning (#8). Standing at `start`, try every possible first piece `s[start:end]`. The only change is the rule: #8 asked "is this piece a palindrome?", here we ask **"is this piece a dictionary word?"** And we collect *every* way of cutting, joined into sentences.

* `word_set = set(wordDict)` — makes each "is it a word?" check a quick lookup.
* `for end in range(start + 1, n + 1)` — every possible length for the next word.
* `if word in word_set` — only keep a cut if the piece is a real word.
* `bt_dfs(end, path)` — the rest of the string begins where this word ended.
* `start == n` — the whole string is used up, so `path` is a full sentence. Save `" ".join(path)`.

**Heads-up:** this code is plain backtracking. The same leftover suffix (say, from index `7`) can be reached by different earlier cuts and gets solved again each time. Caching the answer per `start` in a `memo` dict removes that repeated work — that's the "memoized" version an interviewer may ask about.

**Recall:** cut a prefix that is a word, recurse on the rest, sentence is complete when `start == n`.

---

## 2. Template

* **Choose:** `path.append(word)` — take `s[start:end]`
* **Explore:** `bt_dfs(end, path)`
* **Un-choose:** `path.pop()`
* **Prune / dedup:** only cut where `word in word_set`.

---

## 3. Code

```python
class Solution:
    def wordBreak(self, s: str, wordDict: list[str]) -> list[str]:
        res = []
        word_set = set(wordDict)  # O(1) lookups
        n = len(s)

        def bt_dfs(start: int, path: list[str]):
            # Base Case: Reached the end of the string
            if start == n:
                res.append(" ".join(path))
                return

            # Try every possible substring starting from 'start'
            for end in range(start + 1, n + 1):
                word = s[start:end]

                # Constraint Check: Substring must be in dictionary
                if word in word_set:
                    # Choice: Append word to current path
                    path.append(word)

                    # Recurse: Move start pointer forward to 'end'
                    bt_dfs(end, path)

                    # Backtrack: Undo choice
                    path.pop()

        bt_dfs(0, [])
        return res

```

---

## 4. Dry Run (`s = "catsanddog"`, `wordDict = ["cat","cats","and","sand","dog"]`)

```text
                                       bt_dfs(start=0, path=[])
                                      /                        \
                          end=3 ("cat")                        end=4 ("cats")
                          /                                        \
              bt_dfs(3, ["cat"])                                bt_dfs(4, ["cats"])
                     |                                               |
              end=7 ("sand")                                  end=7 ("and")
                     |                                               |
         bt_dfs(7, ["cat", "sand"])                       bt_dfs(7, ["cats", "and"])
                     |                                               |
              end=10 ("dog")                                  end=10 ("dog")
                     |                                               |
      bt_dfs(10, ["cat", "sand", "dog"])               bt_dfs(10, ["cats", "and", "dog"])
              Base Case: start == 10!                         Base Case: start == 10!
          res: ["cat sand dog"]                     res: ["cat sand dog", "cats and dog"]

```

---

## 5. Complexity

* **Time: O(n · 2^n)** — worst case is a string like `"aaaa"` with words `a, aa, aaa, aaaa`, which has `2^(n-1)` sentences, and each `" ".join` costs up to `n`. With no memo, branches that dead-end get re-explored, so it can do extra work beyond the output size.
* **Space: O(n + W)** — recursion depth and `path` are at most `n`, plus the word set of total size `W` (the output list isn't counted).

---

## 6. Recall (30 seconds)

* Like #8, but a piece is valid when `word in word_set`.
* `start == n` → save `" ".join(path)`.
* No memo here → same suffix can be re-solved; `memo[start]` is the fix.
