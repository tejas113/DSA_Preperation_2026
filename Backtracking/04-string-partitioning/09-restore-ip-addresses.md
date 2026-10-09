# 93. Restore IP Addresses

**LC 93** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** String Partitioning with Validity Checks

---

## 1. Intuition

An IP address is four numbers separated by dots. So cut the string into **exactly 4 pieces**, choosing at each step how long the next piece is: 1, 2 or 3 digits.

* `len(path) == 4` — four pieces are placed. It only counts if `start == n` too, meaning every digit was used. Both must be true.
* `for length in range(1, 4)` — a piece has 1 to 3 digits. `if start + length > n: break` — we ran out of digits, so stop trying longer pieces.
* `len(part) > 1 and part[0] == '0'` — `"0"` is fine, but `"01"` or `"00"` is not (no leading zeros).
* `int(part) > 255` — each number must be at most 255.
* `n < 4 or n > 12` at the top — 4 pieces of 1–3 digits means a valid string has 4 to 12 digits, so anything else is rejected right away.

**Recall:** 4 pieces, each 1–3 digits, no leading zero, at most 255, and every digit used.

---

## 2. Template

* **Choose:** `path.append(part)` — take `s[start : start + length]`
* **Explore:** `bt_dfs(start + length, path)`
* **Un-choose:** `path.pop()`
* **Prune / dedup:** skip a piece with a leading zero or a value over 255; `break` when out of digits; reject `n < 4 or n > 12` up front.

---

## 3. Code

```python
class Solution:
    def restoreIpAddresses(self, s: str) -> list[str]:
        res = []
        n = len(s)

        # Early exit optimization for impossible lengths
        if n < 4 or n > 12:
            return []

        def bt_dfs(start: int, path: list[str]):
            # Base Case: Exactly 4 segments placed
            if len(path) == 4:
                # Valid only if all characters in 's' were used
                if start == n:
                    res.append(".".join(path))
                return

            # Try placing 1, 2, or 3 digits in the current segment
            for length in range(1, 4):
                if start + length > n:
                    break

                part = s[start : start + length]

                # Condition 1: No leading zeros allowed for multi-digit segments
                if len(part) > 1 and part[0] == '0':
                    continue

                # Condition 2: Value must be <= 255
                if int(part) > 255:
                    continue

                # Choice: TAKE current segment
                path.append(part)

                # Recurse from start + length
                bt_dfs(start + length, path)

                # Backtrack
                path.pop()

        bt_dfs(0, [])
        return res

```

---

## 4. Dry Run (`s = "25525511135"`)

```text
                                     bt_dfs(start=0, path=[])
                                    /           |            \
                          "2" (t=255)      "25" (t=255)   "255" (t=255)
                          /                     |                \
                     (Fails later)         (Fails later)     bt_dfs(3, ["255"])
                                                                  |
                                                            "255" (valid)
                                                                  |
                                                            bt_dfs(6, ["255", "255"])
                                                            /                   \
                                                 "11" (valid)               "111" (valid)
                                                      |                           |
                                           bt_dfs(8, [..., "11"])     bt_dfs(9, [..., "111"])
                                                      |                           |
                                                 "135" (valid)                "35" (valid)
                                                      |                           |
                                           res: "255.255.11.135"       res: "255.255.111.35"

```

---

## 5. Complexity

* **Time: O(1)** — the depth is fixed at 4 pieces and each piece has at most 3 lengths, so there are at most 3^4 = 81 paths. The string is capped at 12 digits, so this is constant work.
* **Space: O(1)** — recursion depth is 4 and `path` holds at most 4 pieces.

---

## 6. Recall (30 seconds)

* Exactly 4 pieces, each 1–3 digits, and `start == n` at the end.
* Reject a leading zero (`"01"`) and any value over 255.
* Length must be 4–12, otherwise return `[]` immediately.
