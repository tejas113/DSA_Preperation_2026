# 135. Candy

**LC 135** · **Source:** LC150 · **Difficulty:** Hard · **Priority:** Stretch · **Pattern:** Two-pass greedy, left neighbor then right neighbor

---

## 1. Intuition

Each child needs more candy than a *lower-rated* neighbor. That's two separate, independent constraints per
child — one against the left neighbor, one against the right — so it's natural to resolve them in two
separate passes rather than trying to satisfy both directions at once. A left-to-right pass alone can
guarantee "more than my left neighbor if I outrank them," but it can't also guarantee "more than my right
neighbor," so a second right-to-left pass fixes up whatever the first pass missed, without ever undoing what
the first pass already got right.

* `candies = [1] * n` — every child starts with the minimum, since everyone needs at least one candy.
* Left-to-right pass: `if ratings[i] > ratings[i-1]: candies[i] = candies[i-1] + 1` — only looks left; a rising streak in ratings gets a rising streak in candies.
* Right-to-left pass: `if ratings[i] > ratings[i+1]: candies[i] = max(candies[i], candies[i+1] + 1)` — only looks right, and uses `max` (not a plain overwrite) so it never *reduces* what the first pass already guaranteed.
* `sum(candies)` — the answer is the total candy given out, not the array itself.

**Recall:** two passes — left-to-right raises candies for a rising rating streak from the left; right-to-left raises them (via `max`, never lowers) for a rising streak from the right.

---

## 2. Approach

* **Idea:** split "must beat both neighbors when higher-rated" into two independent one-directional constraints, each solvable with a single greedy pass, then combine with `max` so both constraints hold simultaneously.
* **Data structure / pointers:** `candies` (one entry per child, mutated across both passes); `i` walks forward then backward.
* **Invariant:** after the left-to-right pass, `candies[i] > candies[i-1]` whenever `ratings[i] > ratings[i-1]`, for every `i`. After the right-to-left pass, that invariant *still* holds (since `max` only ever increases values), and additionally `candies[i] > candies[i+1]` whenever `ratings[i] > ratings[i+1]`.
* **Edge cases:**
  * Single child → `candies = [1]`, sum is `1`, no neighbor to compare against.
  * All ratings equal → neither pass ever triggers (no strict increase in either direction), everyone keeps the minimum of `1`.
  * A single peak (`[1, 2, 2]`) → the tied pair `[2, 2]` doesn't force either to beat the other, only the up-slope from `1` to the first `2` matters.
  * A rating that's a local peak flanked by lower values on both sides (like `[1, 3, 2, 2, 1]`) → gets boosted by both passes, since it's greater than both neighbors.

---

## 3. Code

```python
class Solution:

    def candy(self, ratings: list[int]) -> int:
        n = len(ratings)
        candies = [1] * n

        # Left-to-right: satisfy "more than left neighbor" when rating rises
        for i in range(1, n):
            if ratings[i] > ratings[i - 1]:
                candies[i] = candies[i - 1] + 1

        # Right-to-left: satisfy "more than right neighbor" when rating rises,
        # without ever reducing what the first pass already guaranteed
        for i in range(n - 2, -1, -1):
            if ratings[i] > ratings[i + 1]:
                candies[i] = max(candies[i], candies[i + 1] + 1)

        return sum(candies)


if __name__ == "__main__":
    solution = Solution()
    assert solution.candy([1, 0, 2]) == 5
    assert solution.candy([1, 2, 2]) == 4
    assert solution.candy([1]) == 1
    assert solution.candy([1, 3, 2, 2, 1]) == 7
    print("All tests passed")
```

---

## 4. Dry Run

`ratings = [1, 0, 2]`

**Left-to-right pass** (start `candies = [1, 1, 1]`):

| `i` | `ratings[i]` vs `ratings[i-1]` | Action | `candies` after |
| --- | --- | --- | --- |
| `1` | `0 > 1`? No | no change | `[1, 1, 1]` |
| `2` | `2 > 0`? Yes | `candies[2] = candies[1] + 1` | `[1, 1, 2]` |

**Right-to-left pass:**

| `i` | `ratings[i]` vs `ratings[i+1]` | Action | `candies` after |
| --- | --- | --- | --- |
| `1` | `0 > 2`? No | no change | `[1, 1, 2]` |
| `0` | `1 > 0`? Yes | `candies[0] = max(1, candies[1]+1) = 2` | `[2, 1, 2]` |

**Return:** `sum([2, 1, 2]) = 5`

---

## 5. Complexity

* **Time:** `O(n)` — two linear passes over `ratings`.
* **Space:** `O(n)` — the `candies` array.

---

## 6. Recall (30 seconds)

* **Two one-directional passes, not one two-directional pass:** left-to-right handles "beat my left neighbor," right-to-left handles "beat my right neighbor."
* **`max`, not overwrite, on the second pass:** guarantees the first pass's guarantees are never undone.
* **Answer is the sum**, not the array — every child still gets at least `1`.
