# 986. Interval List Intersections

**LC 986** · **Source:** [+] Claude · **Difficulty:** Medium · **Priority:** Core · **Pattern:** Two pointers across two sorted interval lists

---

## 1. Intuition

Two intervals overlap exactly where their ranges agree: the later of their two starts through the earlier
of their two ends. Since both lists are already sorted and each is internally non-overlapping, a single pass
with two pointers is enough — no interval needs to be revisited once its list has moved past it.

* `start = max(firstList[i][0], secondList[j][0])` and `end = min(firstList[i][1], secondList[j][1])` compute the intersection's boundaries directly — this works whether the two intervals overlap or not.
* `if start <= end` is the only check needed to know whether an actual intersection exists; if the ranges don't overlap, `start` ends up past `end`.
* `if firstList[i][1] < secondList[j][1]: i += 1 else: j += 1` — whichever interval ends earlier can never intersect anything further along in the *other* list (since that list is sorted and disjoint), so it's safe to move past it.

**Recall:** compute `[max(starts), min(ends)]`; keep it if `start <= end`; advance whichever interval ends earlier.

---

## 2. Approach

* **Idea:** because both lists are sorted and internally disjoint, the interval that ends earliest at any given moment has nothing left to gain from staying — advancing past it can never skip a valid intersection.
* **Data structure / pointers:** `i`, `j` index into `firstList` and `secondList`; `res` collects every valid intersection found.
* **Invariant:** at every step, no intersection between `firstList[:i]`/`secondList[:j]` and anything still ahead has been missed — any interval already passed over ended before the other list's current pointer even started.
* **Edge cases:**
  * Either list empty → the `while` condition fails immediately, returning `[]`.
  * Intervals touching at a single point (`[0, 2]` and `[2, 4]`) → `start = end = 2`, which passes `start <= end`, correctly appending `[2, 2]`.
  * Equal end times (`firstList[i][1] == secondList[j][1]`) → the `else` branch advances `j`; both intervals are effectively finished, since neither can intersect anything further given the other just ended too.
  * No intersections anywhere → `res` stays `[]`, even though both pointers still advance to the end of their lists.

---

## 3. Code

```python
class Solution:

    def intervalIntersection(
        self, firstList: list[list[int]], secondList: list[list[int]]
    ) -> list[list[int]]:
        i, j = 0, 0
        res = []

        while i < len(firstList) and j < len(secondList):
            # 1. Compute overlapping start and end
            start = max(firstList[i][0], secondList[j][0])
            end = min(firstList[i][1], secondList[j][1])

            # 2. Add valid intersection
            if start <= end:
                res.append([start, end])

            # 3. Advance pointer of interval ending earlier
            if firstList[i][1] < secondList[j][1]:
                i += 1
            else:
                j += 1

        return res


if __name__ == "__main__":
    solution = Solution()
    assert solution.intervalIntersection([[0, 2], [5, 10]], [[1, 5], [8, 12]]) == [
        [1, 2],
        [5, 5],
        [8, 10],
    ]
    assert solution.intervalIntersection([[0, 2]], [[2, 4]]) == [[2, 2]]
    assert solution.intervalIntersection([], [[1, 2]]) == []
    assert solution.intervalIntersection([[1, 3]], [[4, 6]]) == []
    print("All tests passed")
```

---

## 4. Dry Run

`firstList = [[0, 2], [5, 10]]`, `secondList = [[1, 5], [8, 12]]`

| Step | `firstList[i]` | `secondList[j]` | `[start, end]` | Valid? | Advance | `res` after |
| --- | --- | --- | --- | --- | --- | --- |
| **1** | `[0, 2]` | `[1, 5]` | `[1, 2]` | True | `i` (`2 < 5`) | `[[1, 2]]` |
| **2** | `[5, 10]` | `[1, 5]` | `[5, 5]` | True | `j` (`10 >= 5`) | `[[1, 2], [5, 5]]` |
| **3** | `[5, 10]` | `[8, 12]` | `[8, 10]` | True | `i` (`10 < 12`) | `[[1, 2], [5, 5], [8, 10]]` |

`i == 2 == len(firstList)`, loop ends. **Return:** `[[1, 2], [5, 5], [8, 10]]`

---

## 5. Complexity

* **Time:** `O(m + n)` — `m = len(firstList)`, `n = len(secondList)`; each step advances at least one pointer, so together they take at most `m + n` steps.
* **Space:** `O(1)` extra — `res` is the required output, not counted against extra space.

---

## 6. Recall (30 seconds)

* **Intersection formula:** `[max(starts), min(ends)]`, valid when `start <= end`.
* **Advance rule:** move past whichever interval ends earlier — it can't intersect anything further in the other, sorted, disjoint list.
* **Touching endpoints count:** a single shared point (`start == end`) is still a valid intersection.
