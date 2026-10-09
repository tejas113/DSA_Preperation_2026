# 68. Text Justification

**LC 68** · **Source:** LC150 · **Difficulty:** Hard · **Priority:** Stretch · **Pattern:** Greedy line-packing, then distribute leftover spaces evenly

---

## 1. Intuition

There are really two separate problems chained together: first, decide *which words go on which line*
(greedily pack as many as fit), and second, given a line's words, *spread the leftover space* between them
so the line hits exactly `maxWidth`. Neither step depends on the other's fine details — packing only cares
about total character counts, and spacing only cares about how many words and how many leftover characters
a line has.

* **Packing:** a word can join the current line only if the line (words plus a minimum one space between each) still fits within `maxWidth`. The check `line_len + len(line) + len(word) > maxWidth` computes the width the line *would* have with one word each — `line_len` is total word characters so far, `len(line)` is the number of words already in the line (which equals the number of single spaces needed between them), and `len(word)` is the new word about to join.
* **Spacing (non-last lines):** `total_spaces = maxWidth - line_len` is everything left to distribute; `gaps = len(words) - 1` is how many slots there are to put it in. `divmod(total_spaces, gaps)` splits that evenly, and any remainder (`extra`) goes to the *leftmost* gaps first, one at a time (`i < extra`).
* **Single-word lines:** with `len(words) - 1 == 0` gaps, distributing "evenly" is undefined — the word is just left-justified with trailing spaces filling the rest.
* **The last line** is handled completely differently: `" ".join(line)` gives single spaces between words (left-justified), then trailing spaces pad it out to `maxWidth` — it's never passed through the even-distribution logic at all.

**Recall:** pack greedily by total width; for a finished non-last line, split leftover space evenly across gaps with extras going left-to-right; the last line is single-spaced and left-justified with trailing padding.

---

## 2. Approach

* **Idea:** separate "which words belong together" (a greedy width check) from "how do the spaces within a line get arranged" (even distribution with a remainder rule) — treating them as two independent sub-problems keeps each one simple.
* **Data structure / pointers:** `line` (the words currently being packed), `line_len` (their total character count, spaces not yet included), `result` (the finished, justified lines).
* **Invariant:** whenever a line is finalized (either because the next word wouldn't fit, or because `words` has run out), `line` holds a set of words whose minimum single-spaced width already fits in `maxWidth`, and adding one more word from the input would not fit.
* **Edge cases:**
  * A single word too long to share a line with anything else → its own line, either padded (single-word non-last line) or left as-is if it's the last line and already exactly `maxWidth` (guaranteed by the problem's constraints).
  * The very last line → always left-justified with single spaces, regardless of how many words it has, never evenly distributed like the lines before it.
  * A line with only one word (not the last line) → all the leftover space goes to the right as trailing padding, since there's no gap to distribute into.
  * Leftover space that doesn't divide evenly among the gaps → the extra characters go to the leftmost gaps first, one each, until the remainder is used up.

---

## 3. Code

```python
class Solution:

    def fullJustify(self, words: list[str], maxWidth: int) -> list[str]:
        result = []
        line = []
        line_len = 0

        for word in words:
            # Would adding this word (plus its leading space) overflow the line?
            if line_len + len(line) + len(word) > maxWidth:
                result.append(self._justify_line(line, line_len, maxWidth))
                line = []
                line_len = 0
            line.append(word)
            line_len += len(word)

        # Last line: left-justified, single spaces, padded on the right
        last_line = " ".join(line)
        last_line += " " * (maxWidth - len(last_line))
        result.append(last_line)

        return result

    def _justify_line(self, words: list[str], line_len: int, maxWidth: int) -> str:
        if len(words) == 1:
            return words[0] + " " * (maxWidth - line_len)

        total_spaces = maxWidth - line_len
        gaps = len(words) - 1
        space_per_gap, extra = divmod(total_spaces, gaps)

        line = ""
        for i, word in enumerate(words):
            line += word
            if i != len(words) - 1:
                spaces = space_per_gap + (1 if i < extra else 0)
                line += " " * spaces
        return line


if __name__ == "__main__":
    solution = Solution()

    assert solution.fullJustify(
        ["This", "is", "an", "example", "of", "text", "justification."], 16
    ) == [
        "This    is    an",
        "example  of text",
        "justification.  ",
    ]

    assert solution.fullJustify(
        ["What", "must", "be", "acknowledgment", "shall", "be"], 16
    ) == [
        "What   must   be",
        "acknowledgment  ",
        "shall be        ",
    ]

    assert solution.fullJustify(["a"], 3) == ["a  "]

    print("All tests passed")
```

---

## 4. Dry Run

`words = ["This", "is", "an", "example", "of", "text", "justification."]`, `maxWidth = 16`

**Line 1 packing:** `"This"`(4) → `"is"`(2) → `"an"`(2) → try `"example"`(7): would need `4+2+2+7 + 3 spaces = 18 > 16`, so line 1 finalizes as `["This", "is", "an"]`, `line_len = 8`.

**Line 1 spacing:** `total_spaces = 16 - 8 = 8`, `gaps = 2`, `divmod(8, 2) = (4, 0)` — 4 spaces in each gap, no remainder.

`"This" + "    " + "is" + "    " + "an"` → `"This    is    an"`

**Line 2 packing:** `"example"`(7) → `"of"`(2) → `"text"`(4) → try `"justification."`(14): would overflow, so line 2 finalizes as `["example", "of", "text"]`, `line_len = 13`.

**Line 2 spacing:** `total_spaces = 16 - 13 = 3`, `gaps = 2`, `divmod(3, 2) = (1, 1)` — 1 space per gap, plus 1 extra to the *first* gap.

`"example" + "  " + "of" + " " + "text"` → `"example  of text"`

**Line 3 (last line):** only `["justification."]` remains. `" ".join([...]) = "justification."` (length 14), padded with `16 - 14 = 2` trailing spaces → `"justification.  "`

**Return:**
```
["This    is    an", "example  of text", "justification.  "]
```

---

## 5. Complexity

* **Time:** `O(n)` where `n` is the total number of characters across all words — each word is processed once during packing, and each line's spacing is built in time proportional to its own length.
* **Space:** `O(n)` — for the output lines, which together hold all the input characters plus padding.

---

## 6. Recall (30 seconds)

* **Two independent sub-problems:** greedy packing (which words share a line), then even space distribution (how the leftover space is spread across gaps).
* **Extra spaces go leftmost first:** `divmod(total_spaces, gaps)` gives the base amount per gap; the remainder is handed out one-per-gap starting from the left.
* **The last line is a special case, not evenly distributed:** single-spaced and left-justified, padded only on the right.
