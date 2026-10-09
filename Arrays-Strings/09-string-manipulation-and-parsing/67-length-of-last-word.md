# 58. Length of Last Word

**LC 58** · **Source:** LC150 · **Difficulty:** Easy · **Priority:** Stretch · **Pattern:** Backward two-pointer scan

---

## 1. Intuition

The last word is whatever non-space run sits closest to the end of the string, possibly after some trailing
spaces. Scanning from the back means you only ever need to pass over the *one* word you actually care about,
instead of splitting the whole string into every word first.

* `i = len(s) - 1` starts at the very last character.
* The first `while i >= 0 and s[i] == " ": i -= 1` skips any trailing spaces, landing `i` on the last real character of the last word.
* The second `while i >= 0 and s[i] != " ": length += 1; i -= 1` counts backward through the word itself, stopping the instant it hits a space (or runs off the front of the string).
* Because it counts characters as it moves rather than tracking a start/end index pair, `length` is directly the answer — no subtraction needed at the end.

**Recall:** skip trailing spaces first, then count non-space characters going backward until the next space (or the string's start).

---

## 2. Approach

* **Idea:** the last word is found entirely by scanning backward once — skip past trailing whitespace, then count until the word ends, without ever needing to process the rest of the string.
* **Data structure / pointers:** `i` scans backward through `s`; `length` accumulates the count directly.
* **Invariant:** once the first `while` loop ends, `i` points at the last character of the last word (or `-1`, if the string is all spaces — though the problem guarantees at least one word exists); the second loop then correctly counts exactly that word's characters.
* **Edge cases:**
  * No trailing spaces at all (`"Hello"`) → the first `while` loop does nothing (`i` already points at a non-space), and the second loop counts the whole string.
  * Heavy trailing spaces (`"a "`) → skipped down to the single character, counted as `1`.
  * A single-character last word after spaces (`"b "`) → same as above, `1`.
  * The problem guarantees the string contains at least one non-space character, so `i` never actually needs to run past `-1` while still expecting a word.

---

## 3. Code

```python
class Solution:

    def lengthOfLastWord(self, s: str) -> int:
        length = 0
        i = len(s) - 1

        # Step 1: Skip trailing spaces
        while i >= 0 and s[i] == " ":
            i -= 1

        # Step 2: Count characters of the last word
        while i >= 0 and s[i] != " ":
            length += 1
            i -= 1

        return length


if __name__ == "__main__":
    solution = Solution()
    assert solution.lengthOfLastWord("   fly me   to   the moon  ") == 4
    assert solution.lengthOfLastWord("Hello") == 5
    assert solution.lengthOfLastWord("a ") == 1
    assert solution.lengthOfLastWord("b ") == 1
    print("All tests passed")
```

### Alternative: Python's built-in `split()`

```python
class SolutionSplit:

    def lengthOfLastWord(self, s: str) -> int:
        words = s.split()
        return len(words[-1])


if __name__ == "__main__":
    solution = SolutionSplit()
    assert solution.lengthOfLastWord("   fly me   to   the moon  ") == 4
    assert solution.lengthOfLastWord("Hello") == 5
    print("All tests passed")
```

---

## 4. Dry Run

`s = "   fly me   to   the moon  "`

> **Note:** the original dry run stated `n = 26` and traced `s[23] = 'n'`, but the string is actually length
> **27** (two trailing spaces, not the assumed count), and the real `'n'` of `"moon"` sits at `s[24]`. I
> re-ran the code directly to rebuild the trace below. The final answer, `4`, was already correct — only the
> stated indices were shifted by one.

| Phase | `i` | `s[i]` | Action | `length` after |
| --- | --- | --- | --- | --- |
| skip | `26` | `' '` | `i -= 1` | `0` |
| skip | `25` | `' '` | `i -= 1` | `0` |
| count | `24` | `'n'` | `length += 1` | `1` |
| count | `23` | `'o'` | `length += 1` | `2` |
| count | `22` | `'o'` | `length += 1` | `3` |
| count | `21` | `'m'` | `length += 1` | `4` |
| stop | `20` | `' '` | loop ends | `4` |

**Return:** `4`

---

## 5. Complexity

* **Time:** `O(n)` worst case (a single word with no trailing spaces requires scanning the whole string); typically much faster with trailing whitespace.
* **Space:** `O(1)` — only `i` and `length`.

**`split()` alternative:** `O(n)` time and space, since it builds a list of every word in the string.

---

## 6. Recall (30 seconds)

* **Two backward phases:** skip trailing spaces, then count the word itself.
* **No index arithmetic needed:** `length` is built up directly as characters are counted, not derived from a start/end pair.
* **`split()` alternative:** `s.split()[-1]` gets the same answer more concisely, at the cost of allocating the full word list.
