# 45. Jump Game II

**LC 45** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Greedy, level-by-level range expansion (implicit BFS)

---

## 1. Intuition

Jump Game ([[55-jump-game]]) only asked *whether* the end is reachable. This asks for the *fewest* jumps —
which is exactly what BFS gives you when each "level" is everything reachable within one more jump. Rather
than build a graph, track the current level's boundary (`current_end`) and the farthest the *next* jump could
reach (`max_reach`); the moment the scan reaches `current_end`, that whole level has been explored, and a
jump is forced to move to the next one.

* `max_reach` keeps growing as the scan considers every index within the current level, folding in each one's own reach.
* `if i == current_end` — the scan has now examined every index in the current level; a jump must be taken to advance, so `jumps += 1` and `current_end = max_reach` opens the next level.
* `for i in range(n - 1)` deliberately stops one short of the last index — once you've *arrived* at the last index, there's no need to consider jumping *from* it.

**Recall:** grow `max_reach` at every index; when `i` reaches `current_end`, take a jump (`jumps += 1`) and set `current_end = max_reach` — that's the next level's boundary.

---

## 2. Approach

* **Idea:** simulate BFS by levels without ever building the graph — a "level" is the set of positions reachable in exactly `jumps` jumps, and `current_end` marks where the current level ends.
* **Data structure / pointers:** `jumps` (the answer so far), `current_end` (boundary of the current level), `max_reach` (farthest reachable using one more jump from anywhere in the current level).
* **Invariant:** at the moment `i == current_end` triggers, `max_reach` already reflects the farthest reach from *every* index in the current level (`0` through `current_end`), since the scan has visited all of them by then — so it's safe to treat `max_reach` as the next level's boundary.
* **Edge cases:**
  * Single element → `n <= 1` returns `0` immediately, guarded explicitly (no jump needed, you're already there).
  * Two elements (`[3, 1]`) → the loop runs once (`i = 0`), immediately triggers a jump since `i == current_end == 0`, correctly returning `1`.
  * A huge first jump (`[10, 1, 1, 1]`) → `max_reach` jumps straight past the whole array on the first index, so `current_end` becomes large immediately and `jumps` never needs to increase past `1`.
  * The problem guarantees the last index is always reachable, so the loop is never at risk of ending without `current_end` having covered the target.

---

## 3. Code

```python
class Solution:

    def jump(self, nums: list[int]) -> int:
        n = len(nums)
        if n <= 1:
            return 0

        jumps = 0
        current_end = 0
        max_reach = 0

        # We don't need to process index n - 1
        for i in range(n - 1):
            max_reach = max(max_reach, i + nums[i])

            # Reached the end of the current jump's reach
            if i == current_end:
                jumps += 1
                current_end = max_reach

        return jumps


if __name__ == "__main__":
    solution = Solution()
    assert solution.jump([2, 3, 1, 1, 4]) == 2
    assert solution.jump([0]) == 0
    assert solution.jump([5]) == 0
    assert solution.jump([3, 1]) == 1
    assert solution.jump([10, 1, 1, 1]) == 1
    print("All tests passed")
```

---

## 4. Dry Run

`nums = [2, 3, 1, 1, 4]`, `n = 5`

| `i` | `nums[i]` | `max_reach` after | `i == current_end`? | `jumps` after | `current_end` after |
| --- | --- | --- | --- | --- | --- |
| `0` | `2` | `max(0, 0+2) = 2` | `0 == 0` → **True** | `1` | `2` |
| `1` | `3` | `max(2, 1+3) = 4` | `1 == 2` → False | `1` | `2` |
| `2` | `1` | `max(4, 2+1) = 4` | `2 == 2` → **True** | `2` | `4` |
| `3` | `1` | `max(4, 3+1) = 4` | `3 == 4` → False | `2` | `4` |

Loop ends (`range(n-1)` stops at `i = 3`). **Return:** `2`

---

## 5. Complexity

* **Time:** `O(n)` — a single pass over `n - 1` indices.
* **Space:** `O(1)` — three scalar variables.

---

## 6. Recall (30 seconds)

* **BFS by levels, without a graph:** `current_end` marks the current level's boundary, `max_reach` is the next level's candidate boundary, built up as the scan crosses the current level.
* **Jump trigger:** `i == current_end` → the whole current level has been scanned, so take the jump now.
* **Skip the last index:** `range(n - 1)` — no need to consider jumping *from* the destination.
