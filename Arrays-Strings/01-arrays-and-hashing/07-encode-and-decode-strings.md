# 271. Encode and Decode Strings

**LC 271** · **Source:** NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Length-prefix encoding

---

## 1. Intuition

You must pack a list of strings into one string and get the exact list back. A plain separator like `,` or
`#` breaks as soon as a string contains that character. So instead of marking where each string *ends*,
write down how long it is *before* it. When decoding, read the length first, then take exactly that many
characters — whatever is inside them is never treated as a separator.

* `str(len(s)) + "#" + s` writes each string as `length#content`, for example `5#hello`.
* In `decode`, `while s[j] != "#"` finds the end of the length number. `i` always points at the first digit of a length, so the first `#` after it is the real separator, not one inside a string.
* `length = int(s[i:j])` reads how many characters the content has.
* `s[j + 1 : j + 1 + length]` takes exactly `length` characters, so a `#` or a digit inside the content is just content.
* `i = j + 1 + length` jumps past the whole record to the start of the next length.

**Recall:** write `length#content` for each string; to decode, read the length, then take exactly that many characters.

---

## 2. Approach

* **Idea:** `encode` joins `length#content` for every string. `decode` repeats: read digits up to `#`, read that many characters, move on.
* **Data structure / pointers:** `res` is the encoded string in `encode`, and the output list in `decode`. In `decode`, `i` is the start of the current record (its first digit), and `j` scans forward to the `#` that ends the length.
* **Invariant:** at the top of each `decode` loop, `i` points at the first digit of the next record, and every record before `i` has already been added to `res`.
* **Edge cases:**
  * Empty list `[]` → encodes to `""`, and `decode("")` returns `[]` because the loop never runs.
  * A list with one empty string `[""]` → encodes to `"0#"`, which decodes back to `[""]`, so it is not confused with `[]`.
  * Strings containing `#` or digits, such as `"hello#world"` or `"3#abc"` → safe, because `length` decides where the content ends.
  * Multi-digit lengths (`"11#..."`) → handled, since `j` scans to the `#`.

---

## 3. Code

```python
class Solution:

    def encode(self, strs: list[str]) -> str:
        """Encodes a list of strings to a single string."""
        res = ""
        for s in strs:
            # Append string length, delimiter '#', and the actual string
            res += str(len(s)) + "#" + s
        return res

    def decode(self, s: str) -> list[str]:
        """Decodes a single string to a list of strings."""
        res, i = [], 0

        while i < len(s):
            j = i
            # Find where the delimiter '#' is located
            while s[j] != "#":
                j += 1

            # Extract the integer length of the upcoming string segment
            length = int(s[i:j])

            # Slice the actual string using the parsed length
            res.append(s[j + 1 : j + 1 + length])

            # Move the index pointer past the current string
            i = j + 1 + length

        return res


if __name__ == "__main__":
    solution = Solution()
    assert solution.encode(["hello#world", ""]) == "11#hello#world0#"
    for strs in (
        ["neet", "code", "love", "you"],
        ["we", "say", ":", "yes"],
        ["hello#world", ""],
        [""],
        [],
    ):
        assert solution.decode(solution.encode(strs)) == strs
    print("All tests passed")
```

---

## 4. Dry Run

`strs = ["hello#world", ""]`

**Encode:**

1. `s = "hello#world"` → `len(s) = 11` → `res += "11#hello#world"`
2. `s = ""` → `len(s) = 0` → `res += "0#"`
3. **Encoded string:** `"11#hello#world0#"` (16 characters)

**Decode** (`s = "11#hello#world0#"`):

1. **First record:**
    * `i = 0`; scan `j` until `s[j] == "#"` → `j = 2`, so `s[0:2] = "11"`.
    * `length = int("11") = 11`.
    * Take `s[3 : 14] = "hello#world"` (the `#` inside is just content).
    * Move on: `i = 2 + 1 + 11 = 14`.
2. **Second record:**
    * `i = 14`; scan `j` until `s[j] == "#"` → `s[14] = "0"`, `s[15] = "#"`, so `j = 15` and `s[14:15] = "0"`.
    * `length = int("0") = 0`.
    * Take `s[16 : 16] = ""`.
    * Move on: `i = 15 + 1 + 0 = 16`.
3. `i == 16 == len(s)`, so the loop ends.

**Decoded output:** `["hello#world", ""]`

---

## 5. Complexity

* **Time:** `O(n)` — here `n` is the total number of characters across all strings. `decode` moves `j` and `i` only forward and copies each string once. `encode` is `O(n)` in practice, but `res += ...` can copy the growing `res` each time, so the worst case is higher; collecting pieces in a list and calling `"".join(...)` once guarantees `O(n)`.
* **Space:** `O(n)` — the encoded string and the decoded list each hold all `n` characters.

---

## 6. Recall (30 seconds)

* **Format:** `<length>#<string>` for every string, for example `"5#hello"`.
* **Why `#` inside a string is safe:** `decode` never searches inside the content — the length says exactly how many characters to skip.
* **Edge cases:** `""` becomes `"0#"`, and `[]` becomes `""` (the `decode` loop never runs).
