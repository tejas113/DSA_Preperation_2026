# 55. Jump Game

**LC 55** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Greedy, track the farthest reachable index

---

## 1. Intuition

You don't need to know *which* jumps get you to the end — only whether the end is reachable at all. So
instead of exploring every jump combination, track a single running fact: the farthest index reachable from
anything seen so far. If you ever reach a position that's beyond that farthest reach, you're stuck; if the
farthest reach ever covers the last index, you're done.

* `max_reach` is the farthest index reachable using only jumps from positions `0` through the current one.
* `if i > max_reach: return False` — the current position `i` is itself unreachable, since nothing earlier could jump this far; no jump from here can help, since you can never even arrive here.
* `max_reach = max(max_reach, i + nums[i])` — from position `i`, the farthest you could jump to is `i + nums[i]`; only keep it if it beats what was already known reachable.
* `if max_reach >= target: return True` — the last index is already provably reachable, so there's no need to keep scanning.

**Recall:** track `max_reach`; if `i` ever exceeds it, you're stuck (`False`); if `max_reach` ever reaches the last index, you're done (`True`).

---

## 2. Approach

* **Idea:** reachability only depends on the single number "farthest index reachable so far" — there's no need to track *how* you'd get there, since any position within that reach can be assumed reachable and its own jump range considered.
* **Data structure / pointers:** `max_reach` (farthest reachable index found so far), `i` (current position being considered), `target` (the last index).
* **Invariant:** at the start of each iteration, every index from `0` to `max_reach` is known to be reachable, and every index checked so far that's `<= max_reach` has already had its own jump range folded into `max_reach`.
* **Edge cases:**
  * Single element (`[0]`) → `target = 0`; at `i = 0`, `max_reach = 0 >= 0` triggers immediately, returning `True` (you're already at the last index).
  * Starts with `0` and more than one element (`[0, 2, 3]`) → at `i = 1`, `1 > max_reach (0)` triggers, correctly returning `False` — a leading `0` traps you unless it's the only element.
  * A `0` in the middle is only fatal if `max_reach` hasn't already jumped past it by the time it's reached — in `[3, 2, 1, 0, 4]`, `max_reach` stalls at `3` right at the `0`, so it never gets a chance to reach the trailing `4`.
  * Large jump values that overshoot the end → harmless, since `max_reach >= target` triggers the early return regardless of by how much.

---

## 3. Code

```python
class Solution:

    def canJump(self, nums: list[int]) -> bool:
        max_reach = 0
        target = len(nums) - 1

        for i in range(len(nums)):
            # If current index exceeds maximum reachable distance, trapped
            if i > max_reach:
                return False

            # Update maximum reachable index
            max_reach = max(max_reach, i + nums[i])

            # Early return if target index is reachable
            if max_reach >= target:
                return True

        return True


if __name__ == "__main__":
    solution = Solution()
    assert solution.canJump([2, 3, 1, 1, 4]) is True
    assert solution.canJump([3, 2, 1, 0, 4]) is False
    assert solution.canJump([0]) is True
    assert solution.canJump([0, 2, 3]) is False
    print("All tests passed")
```

---

## 4. Dry Run

**Case 1 — reachable (`nums = [2, 3, 1, 1, 4]`, `target = 4`):**

| `i` | `i > max_reach`? | `max_reach` after | `max_reach >= target`? |
| --- | --- | --- | --- |
| `0` | `0 > 0` → False | `max(0, 0+2) = 2` | `2 >= 4` → False |
| `1` | `1 > 2` → False | `max(2, 1+3) = 4` | `4 >= 4` → **True → return `True`** |

**Case 2 — trapped by a zero (`nums = [3, 2, 1, 0, 4]`, `target = 4`):**

| `i` | `i > max_reach`? | `max_reach` after | `max_reach >= target`? |
| --- | --- | --- | --- |
| `0` | `0 > 0` → False | `max(0, 0+3) = 3` | `3 >= 4` → False |
| `1` | `1 > 3` → False | `max(3, 1+2) = 3` | `3 >= 4` → False |
| `2` | `2 > 3` → False | `max(3, 2+1) = 3` | `3 >= 4` → False |
| `3` | `3 > 3` → False | `max(3, 3+0) = 3` | `3 >= 4` → False |
| `4` | `4 > 3` → **True → return `False`** | — | — |

---

## 5. Complexity

* **Time:** `O(n)` — one pass, possibly ending early via the `max_reach >= target` check.
* **Space:** `O(1)` — only `max_reach`, `target`, and the loop index.

---

## 6. Recall (30 seconds)

* **Track the farthest reach, not the path:** `max_reach = max(max_reach, i + nums[i])`.
* **Stuck check comes first:** `if i > max_reach: return False`, checked *before* updating `max_reach` at the current index.
* **Extension — Jump Game II (LC 45):** asks for the *minimum* number of jumps instead of just reachability, solved with a similar greedy "level by level" range expansion.
