# 151. Reverse Words in a String

**LC 151** · **Source:** LC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Right-to-left extraction, build result in a list

---

## 1. Intuition

Reversing word order — while also collapsing arbitrary runs of spaces into single spaces — is easiest done
by walking from the *end* of the string, pulling out one word at a time in the order they should appear in
the output, and joining them all at once. No word ever needs to be re-ordered later, since scanning
right-to-left naturally produces them last-word-first.

* The outer `while i >= 0` loop extracts one word per iteration until the whole string is consumed.
* `while i >= 0 and s[i] == " ": i -= 1` skips any run of spaces — trailing, leading, or between words — treating one space or ten identically.
* `if i < 0: break` handles the case where skipping spaces ran off the front of the string (nothing left to extract).
* `j = i` marks the word's last character; the inner `while i >= 0 and s[i] != " ": i -= 1` then walks backward to just before the word's first character.
* `s[i + 1 : j + 1]` slices out exactly the word, since `i` overshot by one past the word's start.
* `words.append(...)` collects words in the order they're found — right to left — which is already the reversed order the answer needs, so no separate reversal step is required.

**Recall:** scan right to left; skip spaces, then extract one word at a time via `s[i+1:j+1]`; append in that order and `join` with single spaces.

---

## 2. Approach

* **Idea:** since words must appear in reverse order in the output, extracting them right-to-left produces them already in the correct output order — no separate reverse step needed.
* **Data structure / pointers:** `i` scans backward through the string; `j` marks the end of the current word being extracted; `words` collects the result in final order.
* **Invariant:** at the top of each outer loop iteration, `s[i+1:]` (everything already scanned) has been fully accounted for — either already added to `words`, or confirmed to be only spaces.
* **Edge cases:**
  * Leading and trailing spaces (`"  hello world  "`) → trailing spaces are skipped by the space-skip loop before the first word is found; leading spaces are skipped the same way right before the loop hits `i < 0` and breaks cleanly.
  * Multiple spaces between words (`"a   b"`) → collapsed to nothing by the space-skip loop, regardless of how many spaces there are.
  * A single word surrounded by spaces (`"   word   "`) → extracts just `"word"`, with no extra spaces in the result.
  * Empty string → the outer loop condition `i >= 0` is `False` immediately (`i` starts at `-1`), returning `""` from `" ".join([])`.

---

## 3. Code

```python
class Solution:

    def reverseWords(self, s: str) -> str:
        words = []
        i = len(s) - 1

        while i >= 0:
            # Skip spaces
            while i >= 0 and s[i] == " ":
                i -= 1
            if i < 0:
                break

            j = i
            # Find start of word
            while i >= 0 and s[i] != " ":
                i -= 1

            words.append(s[i + 1 : j + 1])

        return " ".join(words)


if __name__ == "__main__":
    solution = Solution()
    assert solution.reverseWords("a good   example") == "example good a"
    assert solution.reverseWords("  hello world  ") == "world hello"
    assert solution.reverseWords("a   b") == "b a"
    assert solution.reverseWords("   word   ") == "word"
    print("All tests passed")
```

### Alternative: Python's built-in `split()`

```python
class SolutionSplit:

    def reverseWords(self, s: str) -> str:
        # s.split() strips leading/trailing spaces and merges multiple spaces
        return " ".join(s.split()[::-1])


if __name__ == "__main__":
    solution = SolutionSplit()
    assert solution.reverseWords("a good   example") == "example good a"
    assert solution.reverseWords("  hello world  ") == "world hello"
    print("All tests passed")
```

**Follow-up:** in a mutable-string language (C++, C-style char arrays), the same result can be built with
`O(1)` extra space by reversing the whole string first, then reversing each individual word back in place,
then cleaning up extra spaces with a two-pointer write pass — Python strings are immutable, so this
particular trick doesn't apply here directly.

---

## 4. Dry Run

`s = "a good   example"` (length 16), `i` starts at `15`

| Step | `i` range scanned | Word extracted | `words` after |
| --- | --- | --- | --- |
| **1** | `15 → 8` | `"example"` | `["example"]` |
| **2** | `6 → 1` | `"good"` | `["example", "good"]` |
| **3** | `0 → -1` | `"a"` | `["example", "good", "a"]` |

**Return:** `" ".join(["example", "good", "a"]) = "example good a"`

---

## 5. Complexity

* **Time:** `O(n)` — each character is visited at most twice (once by the space-skip, once by the word scan) across the whole backward pass.
* **Space:** `O(n)` — `words` and the final joined string each hold up to `n` characters total.

---

## 6. Recall (30 seconds)

* **Scan right to left:** words come out already in reversed order — no separate reverse step.
* **Skip spaces first, then extract a word:** `s[i+1:j+1]`, using `j` as the word's end marker.
* **`split()` does all of this for free:** `" ".join(s.split()[::-1])` handles the same edge cases in one line.
