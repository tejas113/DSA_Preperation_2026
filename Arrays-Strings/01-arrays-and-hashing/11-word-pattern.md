# 290. Word Pattern

**LC 290** · **Source:** LC150 · **Difficulty:** Easy · **Priority:** Stretch · **Pattern:** Two-way mapping (two hash maps)

---

## 1. Intuition

This is Isomorphic Strings ([[09-isomorphic-strings]]) with words instead of letters. `pattern` is a
sequence of single characters, `s` is a sequence of words, and each character must map to exactly one
word — and each word back to exactly one character — the same two-way pairing as before, just on a
different alphabet.

* `words = s.split(" ")` turns the sentence into the sequence to pair against `pattern`.
* `if len(pattern) != len(words): return False` is a free early exit — a bijection needs equal counts on both sides.
* `char_to_word` remembers what each pattern character was paired with (`char` → `word`).
* `word_to_char` remembers the reverse (`word` → `char`).
* `if char in char_to_word and char_to_word[char] != word` catches a character that already has a *different* word (like `'a'` wanting both `"dog"` and `"cat"`).
* `if word in word_to_char and word_to_char[word] != char` catches a word already claimed by a *different* character (like `"dog"` being wanted by both `'a'` and `'b'`).

**Recall:** split `s` into words, check the lengths match, then use two maps (`char → word`, `word → char`) exactly like Isomorphic Strings.

---

## 2. Approach

* **Idea:** treat `pattern`'s characters and `s`'s words as two aligned sequences, and check they pair up one-to-one in both directions.
* **Data structure / pointers:** `words` is the split sentence. `char_to_word` and `word_to_char` are the two maps. `i` is the shared index, `char = pattern[i]`, `word = words[i]`.
* **Invariant:** after each step, the two maps are exact opposites of each other — `char_to_word[c] == w` exactly when `word_to_char[w] == c` — and they cover every pair seen so far.
* **Edge cases:**
  * `len(pattern) != len(words)` → `False` immediately, before either map is touched.
  * Empty `pattern` and empty `s` → `words = [""]` (one empty word), so lengths `0` vs `1` mismatch → `False`. `wordPattern("", "")` would need special handling if this case is expected, but the problem's constraints guarantee both are non-empty.
  * One character mapping to two different words (`"aa"`, `"dog cat"`) → caught by `char_to_word`.
  * Two characters mapping to the same word (`"ab"`, `"dog dog"`) → caught by `word_to_char`.
  * Repeated words with extra whitespace (`s.split(" ")` vs `s.split()`) — `split(" ")` produces empty strings on doubled spaces; the problem guarantees single spaces between words, so this does not come up here.

---

## 3. Code

```python
class Solution:

    def wordPattern(self, pattern: str, s: str) -> bool:
        words = s.split(" ")

        # A bijection requires an equal number of keys and values
        if len(pattern) != len(words):
            return False

        char_to_word = {}
        word_to_char = {}

        for i in range(len(pattern)):
            char = pattern[i]
            word = words[i]

            # Validate character -> word mapping
            if char in char_to_word and char_to_word[char] != word:
                return False

            # Validate word -> character mapping
            if word in word_to_char and word_to_char[word] != char:
                return False

            char_to_word[char] = word
            word_to_char[word] = char

        return True


if __name__ == "__main__":
    solution = Solution()
    assert solution.wordPattern("abba", "dog cat cat dog") is True
    assert solution.wordPattern("abba", "dog cat cat fish") is False
    assert solution.wordPattern("aaaa", "dog cat cat dog") is False
    assert solution.wordPattern("abba", "dog dog dog dog") is False
    print("All tests passed")
```

---

## 4. Dry Run

`pattern = "abba"`, `s = "dog cat cat dog"`

Setup: `words = ["dog", "cat", "cat", "dog"]`, and `len(pattern) == 4 == len(words)`, so the guard passes.

| Index `i` | `char` | `word` | `char_to_word` check | `word_to_char` check | `char_to_word` after | `word_to_char` after |
| --- | --- | --- | --- | --- | --- | --- |
| `0` | `'a'` | `"dog"` | not in map, pass | not in map, pass | `{'a': "dog"}` | `{"dog": 'a'}` |
| `1` | `'b'` | `"cat"` | not in map, pass | not in map, pass | `{'a': "dog", 'b': "cat"}` | `{"dog": 'a', "cat": 'b'}` |
| `2` | `'b'` | `"cat"` | `char_to_word['b'] == "cat"`, pass | `word_to_char["cat"] == 'b'`, pass | unchanged | unchanged |
| `3` | `'a'` | `"dog"` | `char_to_word['a'] == "dog"`, pass | `word_to_char["dog"] == 'a'`, pass | unchanged | unchanged |

The loop finishes → return `True`.

---

## 5. Complexity

* **Time:** `O(n)` — `s.split(" ")` is `O(n)`, and the loop makes one pass over `n` characters/words with `O(1)` average dict operations.
* **Space:** `O(n)` — `words` holds up to `n` words, and the two maps together hold up to `n` entries.

---

## 6. Recall (30 seconds)

* **Same idea as Isomorphic Strings, on words:** two maps, `char_to_word` and `word_to_char`.
* **Guard first:** `len(pattern) != len(words)` → `False` before building either map.
* **One-liner alternative:** `len(set(zip(pattern, words))) == len(set(pattern)) == len(set(words))` (after the length guard) checks the same bijection in one line.
