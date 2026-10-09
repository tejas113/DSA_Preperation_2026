# 30. Substring with Concatenation of All Words

**LC 30** · **Source:** LC150 · **Difficulty:** Hard · **Priority:** Stretch · **Pattern:** Fixed-size sliding window on whole-word chunks, run once per starting offset

---

## 1. Intuition

Every word in `words` has the same length `word_len`, so a valid answer is really "a run of chunks of size
`word_len`, using each word in `words` exactly once, in any order." That's Minimum Window Substring's
"cover a required multiset" idea ([[27-minimum-window-substring]]), except the "characters" are whole words
instead of single letters — so the window grows and shrinks by `word_len` at a time, not by `1`.

* Because chunk boundaries only line up correctly if you start reading at the right offset, you have to run `word_len` separate sliding windows — one starting at each offset `0, 1, ..., word_len - 1` — to be sure every possible alignment is checked.
* `seen[word]` tracks how many times each word currently appears in the window; `count` tracks how many *total* word-slots are filled.
* `if word in word_freq: seen[word] += 1; count += 1` — a valid word joins the window.
* `while seen[word] > word_freq[word]: ... l += word_len` — this word is now overused, so shrink from the left by whole chunks until the excess is gone. This is the same idea as Minimum Window Substring's shrink, but per-word instead of per-character.
* `else: seen.clear(); count = 0; l = r` — a chunk that isn't a word in `words` at all can never be part of a valid window that includes it, so the whole window resets past it, instead of shrinking one piece at a time.
* `if count == num_words: ans.append(l)` — once every word slot is filled, the window `[l, r)` is a valid answer.

**Recall:** run one sliding window per starting offset (`0` to `word_len - 1`); grow by one word-chunk at a time; shrink by whole chunks on overuse; reset entirely on an unknown chunk.

---

## 2. Approach

* **Idea:** treat the string as a sequence of `word_len`-sized chunks (starting from a fixed offset) instead of individual characters, then run the same "match a required multiset" sliding window as Minimum Window Substring, one independent pass per offset.
* **Data structure / pointers:** `word_freq` (target: how many times each word must appear), `seen` (how many times each word appears in the current window), `count` (total filled word-slots), `l`/`r` (window bounds, always moving in `word_len`-sized jumps).
* **Invariant:** within a single offset's pass, every chunk between `l` and `r` (exclusive) is a word from `words`, and `seen` exactly reflects their counts — the moment an unknown chunk is seen, that invariant is preserved by resetting the whole window past it, rather than trying to track a partially-broken window.
* **Edge cases:**
  * `words` is empty, or `s` is empty → `[]` immediately (guarded explicitly).
  * `s` shorter than `total_len = word_len * num_words` → no window can ever be checked; both approaches naturally produce `[]`.
  * Duplicate words in `words` (like `["foo", "foo", "bar"]`) → handled correctly, since `word_freq` and `seen` are counts, not just a set of allowed words.
  * A chunk that's a real word but already at its required count → caught by the `while seen[word] > word_freq[word]` shrink, not the `else` reset — those are two different failure modes (unknown chunk vs. overused chunk).
  * Overlapping valid windows starting at different offsets or positions → each offset's independent pass can find its own matches; they don't interfere with each other because each offset only ever looks at chunks aligned to it.

---

## 3. Code

```python
from collections import Counter, defaultdict
from typing import List


class Solution:

    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:
            return []

        word_len = len(words[0])
        num_words = len(words)
        total_len = word_len * num_words
        word_freq = Counter(words)
        ans = []

        # Iterate over all possible word offset positions (0 to word_len - 1)
        for offset in range(word_len):
            l = offset
            r = offset
            seen = defaultdict(int)
            count = 0  # Number of valid words currently in window

            while r + word_len <= len(s):
                word = s[r : r + word_len]
                r += word_len

                if word in word_freq:
                    seen[word] += 1
                    count += 1

                    # If frequency exceeds required, shrink left pointer l
                    while seen[word] > word_freq[word]:
                        left_word = s[l : l + word_len]
                        seen[left_word] -= 1
                        count -= 1
                        l += word_len

                    # If valid window found
                    if count == num_words:
                        ans.append(l)

                else:
                    # Invalid word: reset window
                    seen.clear()
                    count = 0
                    l = r

        return ans


if __name__ == "__main__":
    solution = Solution()
    assert sorted(solution.findSubstring("barfoothefoobarman", ["foo", "bar"])) == [0, 9]
    assert solution.findSubstring("wordgoodgoodgoodbestword", ["word", "good", "best", "word"]) == []
    assert sorted(solution.findSubstring("barfoofoobarthefoobarman", ["bar", "foo", "the"])) == [6, 9, 12]
    print("All tests passed")
```

### Alternative: brute force, one full check per starting index

Checks every possible starting index from scratch, re-counting the whole window each time — correct, but
redoes work that the offset-based version reuses across steps.

```python
from collections import defaultdict
from typing import List


class SolutionBruteWindow:

    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:
            return []

        word_freq = defaultdict(int)
        for word in words:
            word_freq[word] += 1

        word_len = len(words[0])
        window = len(words) * word_len
        ans = []

        for i in range(len(s) - window + 1):
            substr_freq = defaultdict(int)
            j = i

            while j < i + window:
                current = s[j : j + word_len]

                if current not in word_freq:
                    break

                substr_freq[current] += 1

                if substr_freq[current] > word_freq[current]:
                    break

                j += word_len

            if j == i + window:
                ans.append(i)

        return ans


if __name__ == "__main__":
    brute = SolutionBruteWindow()
    assert sorted(brute.findSubstring("barfoothefoobarman", ["foo", "bar"])) == [0, 9]
    assert brute.findSubstring("wordgoodgoodgoodbestword", ["word", "good", "best", "word"]) == []
    print("All tests passed")
```

---

## 4. Dry Run

`s = "barfoothefoobarman"`, `words = ["foo", "bar"]` → `word_len = 3`, `num_words = 2`, `word_freq = {foo:1, bar:1}`

Only offset `0` finds anything here (offsets `1` and `2` never see a recognized word):

| `l` | `r` | chunk (`s[r-3:r]`) | Action | `count` | Match? |
| --- | --- | --- | --- | --- | --- |
| `0` | `3` | `"bar"` | `seen[bar]=1` | `1` | No |
| `0` | `6` | `"foo"` | `seen[foo]=1` | `2` | **Yes → append `0`** |
| `9` | `9` | `"the"` | unknown chunk → reset, `l = r = 9` | `0` | No |
| `9` | `12` | `"foo"` | `seen[foo]=1` | `1` | No |
| `9` | `15` | `"bar"` | `seen[bar]=1` | `2` | **Yes → append `9`** |
| `18` | `18` | `"man"` | unknown chunk → reset | `0` | No |

**Return:** `[0, 9]`

---

## 5. Complexity

* **Time:** `O(n · l)` — `n = len(s)`, `l = word_len`. There are `l` offsets, and within each offset both `l` and `r` only move forward through `s`, so each offset's pass is `O(n / l)` chunk-steps of `O(l)` work each (slicing/hashing a chunk) — `l` passes of `O(n)` total work each gives `O(n · l)` overall.
* **Space:** `O(k · l)` — `k = num_words`; `word_freq` and `seen` each hold up to `k` distinct words of length `l`.

**Brute force:** `O((n - k·l) · k · l)` — re-scans and re-counts an entire window of `k` words from scratch at every one of the `~n` starting positions, instead of reusing work between positions.

---

## 6. Recall (30 seconds)

* **Chunk, don't scan character by character:** treat `word_len`-sized pieces of `s` as the unit, like Permutation in String ([[25-permutation-in-string]]) treats whole characters.
* **One pass per offset:** run `word_len` independent sliding windows, starting at `0, 1, ..., word_len - 1`, to cover every possible chunk alignment.
* **Two ways to fail, two responses:** an *unknown* chunk resets the whole window (`l = r`); an *overused* chunk only shrinks from the left until it's no longer overused.
