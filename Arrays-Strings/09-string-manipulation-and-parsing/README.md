# Topic 9 — String Manipulation & Parsing

## The pattern

Read the string with an index, apply the rules **exactly as stated**, and build the result in a **list** that you `"".join(...)` once at the end. There is usually no clever algorithm — the difficulty is handling every edge case.

```python
result = []                                   # strings are immutable; build in a list
i = 0
while i < len(s):
    if <this character starts a token>:       # e.g. a digit, a sign, a non-space
        start = i
        while i < len(s) and <still part of the token>:
            i += 1
        result.append(s[start:i])
    else:
        i += 1
return "".join(result)
```

Common checks: **leading and trailing spaces**, **a `+` / `-` sign**, **empty string**, **overflow**, **a character that ends the number**, and **off-by-one at the end of the string**.

## How to spot this topic

* The task is to **parse, convert, format or simulate** a set of stated rules on a string.
* Words to look for: **"convert"**, **"without using built-in"**, **"reverse the words"**, **"roman numerals"**, **"parse an integer"**, **"justify text"**, **"find the first occurrence"**.
* Quick test: *is the challenge following the rules carefully, not choosing an algorithm?* If yes, it's this topic.

**Not this topic if:** the question is about a **contiguous chunk with a condition** (→ Topic 3), **counting or grouping characters** (→ Topic 1), or **comparing from both ends** (→ Topic 2).

## Problems here

| # | Problem | The key idea |
|---|---|---|
| 69 | Longest Common Prefix | Compare column by column; stop at the first mismatch or the shortest string's end |
| 70 | Reverse Words in a String | Split on whitespace (dropping empties), reverse the list, join with one space |
| 71 | Roman to Integer | If a symbol is smaller than the next one, subtract it; otherwise add it |
| 72 | Find the Index of the First Occurrence in a String | Slide the needle over the haystack (KMP is the follow-up) |
| 73 | Multiply Strings | Digit-by-digit: `i + j` and `i + j + 1` are the positions each product lands in |
| 74 | String to Integer (atoi) | Skip spaces, read the sign, read digits, clamp on overflow |
| 75 | Length of Last Word | Scan from the end: skip spaces, then count letters |
| 76 | Integer to Roman | Greedy: subtract the largest value from a value table, append its symbol |
| 77 | Zigzag Conversion | Bounce a row index up and down, appending each character to its row |
| 78 | String Compression | Read / write pointers on characters; write the letter, then the count digits |
| 79 | Text Justification | Pack words per line, then distribute the spaces evenly (extra spaces go left) |
| 80 | Compare Version Numbers | Split on `.`, compare the numbers pair by pair, and treat a missing part as `0` |
