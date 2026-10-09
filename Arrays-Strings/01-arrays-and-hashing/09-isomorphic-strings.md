# 205. Isomorphic Strings

**LC 205** · **Source:** LC150 · **Difficulty:** Easy · **Priority:** Core · **Pattern:** Two-way mapping (two hash maps)

---

## 1. Intuition

Two strings are isomorphic when you can rename the letters of `s` to get `t`, with one rule: each letter
has exactly one new name, and no two letters share the same new name. Think of it as pairing letters
up — the pairing must work from `s` to `t` *and* from `t` back to `s`. One map only checks one direction,
so keep two.

* `mapST` remembers what each letter of `s` was paired with (`s` → `t`).
* `mapTS` remembers the reverse (`t` → `s`).
* `if a in mapST and mapST[a] != b` catches a letter of `s` that was already paired with a *different* letter (`"foo"` vs `"bar"`: `'o'` was paired with `'a'`, now wants `'r'`).
* `if b in mapTS and mapTS[b] != a` catches a letter of `t` that is already taken by a *different* letter of `s` (`"ab"` vs `"aa"`: `'a'` in `t` is already used by `'a'`, and `'b'` wants it too).
* `mapST[a] = b` and `mapTS[b] = a` run only after both checks pass, so the two maps always agree.

**Recall:** two maps, `s → t` and `t → s`; return `False` if either side is already paired with something else.

---

## 2. Approach

* **Idea:** walk both strings together. For each pair `(a, b)`, check that neither side is already paired with a different partner, then record the pair in both maps.
* **Data structure / pointers:** `mapST` maps a character of `s` to its partner in `t`; `mapTS` maps the other way. `i` is the shared index, `a = s[i]` and `b = t[i]`.
* **Invariant:** after each step, the two maps are exact opposites — `mapST[x] == y` exactly when `mapTS[y] == x` — and they cover every pair seen so far.
* **Edge cases:**
  * `s` and `t` have the same length (the problem guarantees it); the loop reads `t[i]` for every `i` in `s`.
  * Empty strings → `True` (nothing to check).
  * A character can map to itself (`"aa"` vs `"aa"`).
  * Two different letters mapping to the same letter (`"ab"` vs `"aa"`) → `False`, caught by `mapTS`.
  * One letter mapping to two different letters (`"aa"` vs `"ab"`) → `False`, caught by `mapST`.

---

## 3. Code

```python
class Solution:
    def isIsomorphic(self, s: str, t: str) -> bool:
        mapST = {}
        mapTS = {}

        for i in range(len(s)):
            a, b = s[i], t[i]

            if a in mapST and mapST[a] != b:
                return False

            if b in mapTS and mapTS[b] != a:
                return False

            mapST[a] = b
            mapTS[b] = a

        return True


if __name__ == "__main__":
    solution = Solution()
    assert solution.isIsomorphic("egg", "add") is True
    assert solution.isIsomorphic("foo", "bar") is False
    assert solution.isIsomorphic("paper", "title") is True
    assert solution.isIsomorphic("badc", "baba") is False
    print("All tests passed")
```

---

## 4. Dry Run

`s = "egg"`, `t = "add"`

| Index `i` | `a` | `b` | `a in mapST` check | `b in mapTS` check | `mapST` after | `mapTS` after |
| --- | --- | --- | --- | --- | --- | --- |
| `0` | `'e'` | `'a'` | not in `mapST`, pass | not in `mapTS`, pass | `{'e': 'a'}` | `{'a': 'e'}` |
| `1` | `'g'` | `'d'` | not in `mapST`, pass | not in `mapTS`, pass | `{'e': 'a', 'g': 'd'}` | `{'a': 'e', 'd': 'g'}` |
| `2` | `'g'` | `'d'` | `mapST['g'] == 'd'`, pass | `mapTS['d'] == 'g'`, pass | `{'e': 'a', 'g': 'd'}` | `{'a': 'e', 'd': 'g'}` |

The loop finishes → return `True`.

---

## 5. Complexity

* **Time:** `O(n)` — one pass over the `n` characters, with `O(1)` average dict lookups and inserts.
* **Space:** `O(k)` — each map holds at most one entry per distinct character (`k`); that is bounded by the character set (about 256 for ASCII), so it is `O(1)` in practice.

---

## 6. Recall (30 seconds)

* **Rule:** the mapping must be one-to-one in both directions.
* **Two maps:** `mapST` stops one letter of `s` from becoming two letters; `mapTS` stops two letters of `s` from becoming the same letter.
* **One-liner alternative:** `len(set(zip(s, t))) == len(set(s)) == len(set(t))` gives the same answer, but builds sets over the whole input and cannot exit early.
