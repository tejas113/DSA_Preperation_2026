# 767. Reorganize String

**LC 767** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Max-heap of counts + hold back the last letter used (`prev`), with even/odd index filling as the alternative

---

## 1. Intuition

Build the string one letter at a time. Always use the letter with the most copies left, because the most common letter is the hardest to keep apart. But the letter you just used cannot go straight after itself, so hold it aside for one step and put it back in the pile afterwards.

* `max_heap` holds `[-cnt, char]` for every letter that can be used now. `heapq` is a min-heap, so the count is stored negated and the biggest count sits at the root.
* `cnt, char = heapq.heappop(max_heap)` takes the most frequent letter that is allowed. `cnt += 1` uses one copy (the count is negative, so adding 1 moves it toward 0).
* `prev` is the letter we just placed, held out of the heap for exactly one step. The `if prev: heappush(max_heap, prev)` line returns the previous held letter after the next letter has been placed.
* `if cnt != 0: prev = [cnt, char]` holds the current letter only if copies of it are left.
* `if prev and not max_heap: return ""` means the only letter left is the one we just placed. Using it would put two equal letters side by side, so it is impossible.

**Recall:** pop the biggest, place it, push the previous held letter back, then hold the current one; if only the held one is left, return `""`.

---

## 2. Approach

* **Idea:** Greedily place the most frequent letter that is not the one just placed. The held-back `prev` is what stops two equal letters from touching.
* **Data structure / pointers:**
  * `count`: a `Counter` of letter to copies.
  * `max_heap`: a **max-heap** of `[-cnt, char]` lists (negated count first), built with `heapify`. It has no size cap. Root is the letter with the most copies left.
  * Tie-breaker: lists compare left to right, so two letters with the same count are compared by `char`. This only picks which of two equal counts goes first, and any valid answer is accepted. The `char` is a plain string, so the comparison never fails.
  * `prev`: the one letter held back for a step, as `[cnt, char]`, or `None`.
  * `res`: the list of letters placed so far.
* **Invariant:** The last letter in `res` is never in `max_heap`. It is either held in `prev` or has no copies left. So the next pop can never be the same letter as the one before it.
* **Edge cases:**
  * One letter (`"a"`): it is placed, no copies are left, and `"a"` is returned.
  * One letter repeated (`"aa"`): after the first `a`, `prev` is set and the heap is empty, so `""` is returned.
  * Impossible (`"aaab"`): the string is possible only if the most frequent letter appears at most `(len(s) + 1) // 2` times. Here `a` appears 3 times, which is more than 2, so the result is `""`.
  * Exactly possible (`"aba"`, `"abab"`): the most common letter fills every other position.
  * Empty string does not occur, because LeetCode guarantees at least one character.

---

## 3. Code

```python
from collections import Counter
import heapq


class Solution:

    def reorganizeString(self, s: str) -> str:
        count = Counter(s)
        max_heap = [[-cnt, char] for char, cnt in count.items()]
        heapq.heapify(max_heap)

        prev = None
        res = []

        while max_heap or prev:
            # If we need a character but max_heap is empty, it's impossible
            if prev and not max_heap:
                return ""

            cnt, char = heapq.heappop(max_heap)
            res.append(char)
            cnt += 1  # Reduce remaining count (since cnt is negative)

            # Re-insert the previous character back into the heap
            if prev:
                heapq.heappush(max_heap, prev)
                prev = None

            # Hold current character for the next turn if count remains > 0
            if cnt != 0:
                prev = [cnt, char]

        return "".join(res)
```

### Alternative: Even/odd index filling (O(n) time, no heap)

If the most frequent letter appears more than `(len(s) + 1) // 2` times, the answer is impossible. Otherwise, write that letter into positions `0, 2, 4, ...`, then write every other letter into the remaining positions, continuing at `1, 3, 5, ...`.

```python
class SolutionGreedyFill:

    def reorganizeString(self, s: str) -> str:
        count = Counter(s)
        max_cnt, max_char = 0, ""

        for char, cnt in count.items():
            if cnt > max_cnt:
                max_cnt, max_char = cnt, char

        # Impossible threshold check
        if max_cnt > (len(s) + 1) // 2:
            return ""

        res = [""] * len(s)
        idx = 0

        # Fill most frequent character on even indices
        while count[max_char] > 0:
            res[idx] = max_char
            idx += 2
            count[max_char] -= 1

        # Fill remaining characters
        for char, cnt in count.items():
            while cnt > 0:
                if idx >= len(s):
                    idx = 1  # Switch to odd indices
                res[idx] = char
                idx += 2
                cnt -= 1

        return "".join(res)


# Shared tests: they run against both solutions above.
if __name__ == "__main__":
    for solution in (Solution(), SolutionGreedyFill()):
        for s in ("aab", "abab", "a", "aabbcc"):
            result = solution.reorganizeString(s)
            assert sorted(result) == sorted(s)
            assert all(result[i] != result[i + 1] for i in range(len(result) - 1))
        assert solution.reorganizeString("aaab") == ""
        assert solution.reorganizeString("aa") == ""
    print("All tests passed")
```

---

## 4. Dry Run

`s = "aab"`. Start: `max_heap = [[-2, 'a'], [-1, 'b']]`, `prev = None`.

| Turn | Popped `[cnt, char]` | Placed | `prev` pushed back | New `prev` | `max_heap` after | `res` |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | `[-2, 'a']` | `a` | none | `[-1, 'a']` | `[[-1, 'b']]` | `"a"` |
| 2 | `[-1, 'b']` | `b` | `[-1, 'a']` | `None` (`b` has none left) | `[[-1, 'a']]` | `"ab"` |
| 3 | `[-1, 'a']` | `a` | none | `None` | `[]` | `"aba"` |

Both `max_heap` and `prev` are empty, so the loop ends. Return `"aba"`.

For `"aaab"`, turn 3 places `a` and leaves `prev = [-1, 'a']` with an empty heap. The next check `prev and not max_heap` is true, so the function returns `""`.

---

## 5. Complexity

* **Time:** O(n log k), where `n = len(s)` and `k` is the number of distinct letters. Each of the `n` placements does one pop and at most one push. Since `k <= 26`, each heap operation is O(log 26), which is O(1), so the total is effectively O(n).
* **Space:** O(k), which is O(1) for lowercase letters. The heap holds at most 26 entries (the result string itself is O(n)).

---

## 6. Recall (30 seconds)

* Max-heap of `[-cnt, char]`. Each turn: pop and place a letter, push the previous held letter back, then hold the current letter if copies remain.
* If `prev` exists but the heap is empty, return `""`. That is the impossible case, and it happens when the top letter appears more than `(n + 1) // 2` times.
* Alternative: put the top letter on even indices, then fill the rest, switching to odd indices.
