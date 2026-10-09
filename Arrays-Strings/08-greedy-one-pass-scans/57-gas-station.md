# 134. Gas Station

**LC 134** · **Source:** LC150 + NC150 · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Greedy, reset the start whenever the running tank goes negative

---

## 1. Intuition

Two separate facts make this solvable in one pass. First: a valid starting station exists at all only if the
total gas available is at least the total cost (`sum(gas) >= sum(cost)`) — otherwise there simply isn't
enough fuel anywhere. Second, and less obvious: if starting at station `A` causes the tank to go negative by
the time you reach station `B`, then *no station between `A` and `B`* can be a valid start either — each of
them would arrive at that same failure point with an equal or smaller head start, since every station in
between only added to the deficit that eventually broke the tank. So the moment the running total goes
negative, the *very next* station is the only candidate worth trying next — everything before it (up to and
including the failing station) is provably eliminated.

* `if sum(gas) < sum(cost): return -1` — the global feasibility check, done once up front.
* `total` is the running fuel surplus/deficit starting from the current candidate `res`.
* `if total < 0: total = 0; res = i + 1` — the candidate start failed; reset the tank and try the very next station, discarding every station from the old start through `i` as impossible.
* Because the problem guarantees `sum(gas) >= sum(cost)` implies a solution exists, whatever `res` ends up being after the full scan is guaranteed to be that unique valid start — no need to verify it separately.

**Recall:** if total gas < total cost, no solution (`-1`); otherwise, reset the candidate start to `i + 1` every time the running tank goes negative, and the final candidate is guaranteed correct.

---

## 2. Approach

* **Idea:** a single greedy pass finds the valid start by treating a negative running total as proof that every station tried so far (up to and including the current one) is unusable — so jump straight past all of them.
* **Data structure / pointers:** `total` (running surplus since the current candidate start), `res` (current candidate starting index).
* **Invariant:** at every point, no station strictly before `res` can be the answer — either the global sum check already ruled out the whole problem, or an earlier negative-total reset already eliminated it.
* **Edge cases:**
  * Total gas less than total cost → `-1` immediately, before the main loop even runs.
  * A single station → the loop runs once; if `gas[0] >= cost[0]` (guaranteed by the global check when `n=1`), `total` stays `>= 0` and `res` stays `0`.
  * The tank never goes negative anywhere → `res` stays `0`, meaning station `0` itself is the valid start.
  * Net-zero at every station (`gas == cost` everywhere) → `total` never dips below `0`, so `res = 0` — a full loop with zero surplus is still valid, since you always have exactly enough to continue.

---

## 3. Code

```python
class Solution:

    def canCompleteCircuit(self, gas: list[int], cost: list[int]) -> int:
        # Step 1: Global check — if total gas < total cost, circuit is impossible
        if sum(gas) < sum(cost):
            return -1

        total = 0
        res = 0

        # Step 2: Find the unique valid starting station
        for i in range(len(gas)):
            total += gas[i] - cost[i]

            # If current tank goes negative, reset start to next station
            if total < 0:
                total = 0
                res = i + 1

        return res


if __name__ == "__main__":
    solution = Solution()
    assert solution.canCompleteCircuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
    assert solution.canCompleteCircuit([2, 3, 4], [3, 4, 3]) == -1
    assert solution.canCompleteCircuit([5], [4]) == 0
    assert solution.canCompleteCircuit([2, 2, 2], [2, 2, 2]) == 0
    print("All tests passed")
```

### Alternative: fold the global sum check into the single pass

Avoids a separate `sum(gas)`/`sum(cost)` computation by accumulating the total surplus alongside the
per-candidate running tank in the same loop.

```python
class SolutionOnePass:

    def canCompleteCircuit(self, gas: list[int], cost: list[int]) -> int:
        total_surplus = 0
        current_tank = 0
        start_idx = 0

        for i in range(len(gas)):
            diff = gas[i] - cost[i]
            total_surplus += diff
            current_tank += diff

            if current_tank < 0:
                start_idx = i + 1
                current_tank = 0

        return start_idx if total_surplus >= 0 else -1


if __name__ == "__main__":
    solution = SolutionOnePass()
    assert solution.canCompleteCircuit([1, 2, 3, 4, 5], [3, 4, 5, 1, 2]) == 3
    assert solution.canCompleteCircuit([2, 3, 4], [3, 4, 3]) == -1
    print("All tests passed")
```

---

## 4. Dry Run

`gas = [1, 2, 3, 4, 5]`, `cost = [3, 4, 5, 1, 2]` → `sum(gas) = 15 >= sum(cost) = 15`, feasible.

| `i` | `gas[i] - cost[i]` | `total` after | `total < 0`? | Action | `res` after |
| --- | --- | --- | --- | --- | --- |
| `0` | `-2` | `-2` | **True** | reset `total = 0` | `1` |
| `1` | `-2` | `-2` | **True** | reset `total = 0` | `2` |
| `2` | `-2` | `-2` | **True** | reset `total = 0` | `3` |
| `3` | `+3` | `3` | False | — | `3` |
| `4` | `+3` | `6` | False | — | `3` |

**Return:** `3`

---

## 5. Complexity

* **Time:** `O(n)` — the global sum check is `O(n)`, and the main loop is another `O(n)`.
* **Space:** `O(1)` — a few scalar variables.

**One-pass alternative:** same `O(n)` time, but as a single pass instead of two separate scans.

---

## 6. Recall (30 seconds)

* **Global check first:** `sum(gas) < sum(cost)` → `-1`, no valid start exists anywhere.
* **Reset rule:** the moment `total < 0`, every station from the old candidate through the current one is eliminated — jump the candidate to `i + 1`.
* **No verification needed:** given the global check passes, whatever `res` ends up as after the scan is guaranteed to be the unique valid answer.
